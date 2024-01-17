from datetime import datetime
from django.utils import timezone
import logging

from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings

from rttcore.permissions import IsSuperUserOrStaff
from rttnews.filters import NewsFilter
from rttnews.serializers import serializers
from rttnews.models.models import News, NewsCategory, Source, NewsRelevanceLog, SourceType, NewsAssessmentWorkflow, \
    NewsAnswer, NewsQuestion, NewsUpdateLogForAssessmentWorkflowRemove, NewsRelevance
from rttnews.services.news_api_service import NewsApiService
from rttnews.services.news_service import NewsService
from rttorganization.models.models import Organization
from rttorganization.serializers.serializers import RelevantOrganizationsSerializer
from rttproduct.models.models import ProductCategory, MaterialCategory
from rttnews.tasks import task_process_news
from rttnews.paginations import NewsPagination
from rttcore.services.email_service import send_mail_via_mailjet_template
from rttorganization.services.organization_services import OrganizationService

logger = logging.getLogger(__name__)


class NewsCategoryViewSet(viewsets.ModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = serializers.NewsCategorySerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().prefetch_related('documents', 'selected_by', 'discharged_by', 'source').distinct().order_by('-pub_date')
    serializer_classes = {
        'list': serializers.NewsListSerializer,
        'retrieve': serializers.NewsDetailSerializer,
        'save_document': serializers.NewsDocumentSaveSerializer,
        'update': serializers.NewsPatchSerializer,
        'partial_update': serializers.NewsPatchSerializer,
    }
    default_serializer_class = serializers.NewsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    pagination_class = NewsPagination

    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = NewsFilter
    search_fields = ['title', 'body']
    filterset_fields = ['regions', 'source', 'news_categories', 'product_categories', 'status', 'active',
                        'review_green', 'review_yellow']

    def get_queryset(self):
        queryset = self.queryset
        news_status = self.request.GET.get('status', '')
        is_activated = self.request.GET.get('active', False)
        if news_status == 'd':
            queryset = queryset.order_by('-discharged_on')
        elif news_status == 's' and is_activated:
            queryset = queryset.order_by('-selected_on')

        return queryset

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        news_status = request.data.get('status', '')

        if news_status == 's' and instance.status in ['n', 'd']:
            request.data['selected_by'] = request.user.id
            request.data['selected_on'] = timezone.now()

        elif news_status == 'd' and instance.status in ['n', 's']:
            request.data['discharged_by'] = request.user.id
            request.data['discharged_on'] = timezone.now()
        news_status_selected_to_discharged = False
        if news_status == 'd' and instance.status in ['s']:
            news_status_selected_to_discharged = True

        instance_review_yellow = instance.review_yellow
        instance_review_comment = instance.review_comment
        review_yellow = request.data.get('review_yellow', False)
        review_comment = request.data.get('review_comment', None)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # save_news_update_log_for_assessment_workflow_remove
        self.save_news_update_log_for_assessment_workflow_remove(instance.id)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if not instance_review_yellow and review_yellow and not instance_review_comment and review_comment:
            self.send_review_news_email_notification(instance, request, news_status_selected_to_discharged)

        if news_status_selected_to_discharged:
            self.delete_assessments_for_discharged_news(instance.id)
        return Response(serializer.data)

    @staticmethod
    def send_review_news_email_notification(instance, request, news_status_selected_to_discharged):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1197
        """

        email_to = None
        news_status = None
        # if news status is 's' and active 'true' then that news is online
        if instance.status == 's' and instance.active:
            news_status = 'Selected'
            email_to = instance.selected_by.email
        # if news status is 'd' then that news is discharged
        elif instance.status == 'd':
            news_status = 'Discharged'
            if news_status_selected_to_discharged:
                email_to = instance.selected_by.email
            else:
                email_to = instance.discharged_by.email

        if email_to:
            base_url = settings.SITE_BASE_URL
            subject = f'Review news: {instance.title}'
            news_categories_name = ''
            for news_category in instance.news_categories.all():
                news_categories_name += ", " + news_category.name if len(
                    news_categories_name) > 0 else news_category.name
            user_name = ''
            if request.user.first_name:
                user_name = request.user.first_name
                if request.user.last_name:
                    if request.user.first_name:
                        user_name += ' ' + request.user.last_name
                    else:
                        user_name = request.user.last_name
            if not user_name:
                user_name = request.user.username

            template_id = settings.MAILJET_REVIEW_NEWS_NOTIFICATION_TEMPLATE_ID
            variables_dict = {
                "alert_name": 'Review News',
                'title': instance.title,
                'status': news_status,
                'pub_date': str(instance.pub_date)[:11],
                'source': instance.source.name if instance.source else '',
                'news_categories': news_categories_name,
                'review_comment': request.data.get('review_comment'),
                'commented_by': user_name,
                'news_url': f"{base_url}backend/news-info/news/{instance.id}/edit"
            }
            mail_status = send_mail_via_mailjet_template(email_to, template_id, subject, variables_dict)

    @staticmethod
    def save_news_update_log_for_assessment_workflow_remove(news_id):
        try:
            NewsUpdateLogForAssessmentWorkflowRemove.objects.create(news_id=news_id)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)

    @staticmethod
    def delete_assessments_for_discharged_news(news_id):
        try:
            news_assessment_list = NewsRelevance.objects.filter(news_id=news_id)
            organization_ids = []
            for news_assessment in news_assessment_list:
                organization_ids.append(news_assessment.organization_id)

            NewsAssessmentWorkflow.objects.filter(Q(news_id=news_id) &
                                                  ~Q(organization_id__in=organization_ids)).delete()
        except Exception as ex:
            logger.error(str(ex), exc_info=True)

    # def list(self, request, **kwargs):
    #     queryset = self.get_queryset()
    #     news_status = self.request.GET.get('status', None)
    #     active = self.request.GET.get('active', None)
    #     if news_status is not None:
    #         queryset = queryset.filter(status=news_status)
    #     if active is not None:
    #         queryset = queryset.filter(active=True)
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_paginated_response(serializers.NewsDetailSerializer(page, many=True).data)
    #     else:
    #         serializer = serializers.NewsDetailSerializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def body_documents(self, request, id=None):
        obj = get_object_or_404(News, pk=id)
        news_service = NewsService()
        response = news_service.get_news_body_documents(obj.body)
        return Response(response)

    @action(detail=True, methods=['get'])
    def get_relevant_organizations(self, request, id=None):
        try:
            '''
            docs: https://chemycal.atlassian.net/browse/RTT-477
            '''
            news_id = int(id)
            organization_document_queryset = NewsService().get_relevant_organization_queryset_by_news(news_id)
            if organization_document_queryset is None:
                return Response({'message': 'Invalid News ID'}, status=status.HTTP_404_NOT_FOUND)
            response_data = []
            for organization_document in organization_document_queryset:
                organization_data = {
                    'id': organization_document.id,
                    'name': organization_document.name,
                }
                response_data.append(organization_data)
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
        return Response({'message': 'An Error Occurred'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def save_document(self, request, id):
        news_obj = get_object_or_404(News, pk=id)
        document_data = request.data
        serializer = serializers.NewsDocumentSaveSerializer(data=document_data)

        if serializer.is_valid():
            document = serializer.save(serializer.data.get('link'))
            news_obj.documents.add(document)
            return Response(document.attachment.url, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_news_from_api(self, request):
        news_api_service = NewsApiService()
        from_date = request.GET.get('from_date', None)
        try:
            token_response = news_api_service.get_token()
        except Exception as ex:
            print(ex)
            return Response({'message': 'Chemycal API is not responding!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = task_process_news.delay(from_date)
        return Response({'message': 'Chemycal news fetch process has been successfully run in celery.'},
                        status=status.HTTP_200_OK)


class NewsSourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all().prefetch_related('news_source').select_related('type')
    serializer_classes = {
        'list': serializers.NewsSourceDetailsSerializer,
        'retrieve': serializers.NewsSourceDetailsSerializer
    }
    default_serializer_class = serializers.NewsSourceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(serializers.NewsSourceDetailsSerializer(page, many=True).data)
        else:
            serializer = serializers.NewsSourceDetailsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewsRelevanceViewSet(viewsets.ModelViewSet):
    queryset = NewsRelevanceLog.objects.all()
    serializer_class = serializers.NewsRelevanceLogSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        news_id = self.request.GET.get('news_id', None)
        if news_id is not None:
            queryset = queryset.filter(news_id=news_id)
        serializer = serializers.NewsRelevanceLogSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.data.get('news', None):
            news_id = request.data['news']
            news_relevance_log_qs = NewsRelevanceLog.objects\
                .filter(news_id=news_id, organization_id=request.data.get('organization')).order_by('-created').first()
            if news_relevance_log_qs:
                if request.data.get('relevancy', None) and request.data['relevancy'] == news_relevance_log_qs.relevancy:
                    return Response({"message": "previous and current relevancy is same"},
                                    status=status.HTTP_400_BAD_REQUEST)
                data['prev_relevancy'] = news_relevance_log_qs.relevancy
                data['parent'] = news_relevance_log_qs.id
            else:
                data['prev_relevancy'] = None
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SourceTypeViewSet(viewsets.ModelViewSet):
    queryset = SourceType.objects.all()
    serializer_class = serializers.SourceTypeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'


class NewsAssessmentWorkflowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsAssessmentWorkflow.objects.all()
    serializer_class = serializers.NewsAssessmentWorkflowSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        queryset = self.queryset
        sort_order = self.request.GET.get('sort_order', "desc")
        if sort_order == "asc":
            queryset = queryset.order_by('news__pub_date')
        else:
            queryset = queryset.order_by('-news__pub_date')

        return queryset


class NewsAnswerViewSet(viewsets.ModelViewSet):
    queryset = NewsAnswer.objects.all()
    serializer_classes = {
        'retrieve': serializers.NewsAnswerSerializer,
        'update': serializers.NewsAnswerUpdateSerializer,
        'partial_update': serializers.NewsAnswerUpdateSerializer,
    }
    default_serializer_class = serializers.NewsAnswerSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['answered_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = request.user.id
        '''
        Before setting new pin_by, have to remove old pin_by for that question. 
        Cause only one pined answer may have in question. 
        https://chemycal.atlassian.net/browse/RTT-883
        '''
        if request.data.get('pin_by', None):
            serializer = serializers.NewsAnswerPinSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                try:
                    NewsAnswer.objects.filter(question_id=instance.question, news_id=instance.news).update(pin_by=None)
                except Exception as ex:
                    logger.error(str(ex), exc_info=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if user_id != instance.answered_by.id:
            return Response({"message": "Only answer owner has the permission to edit"},
                            status=status.HTTP_403_FORBIDDEN)
        else:
            if request.data.get('edited', None):
                request.data['edited'] = instance.edited if instance.edited else None
            if request.data.get('answer_text', None):
                if instance.answer_text != request.data.get('answer_text'):
                    request.data['edited'] = timezone.now()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.answered_by.id != request.user.id:
                return Response({'message': 'you do not have permission to delete!'}, status=status.HTTP_403_FORBIDDEN)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewsQuestionViewSet(viewsets.ModelViewSet):
    queryset = NewsQuestion.objects.all()
    serializer_class = serializers.NewsQuestionSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['organization', ]

    def list(self, request, *args, **kwargs):
        """
        doc: doc: https://chemycal.atlassian.net/browse/RTT-904
        """
        if not request.GET.get('organization', None):
            return Response({'message': 'organization is required!'}, status=status.HTTP_400_BAD_REQUEST)
        return super().list(request,args,kwargs)

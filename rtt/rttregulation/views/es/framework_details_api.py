from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.services.system_filter_service import SystemFilterService
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.documents import QuestionDocument
from rttregulation.models.models import RegulationMute
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.id_search_service import IdSearchService

from django.db.models import Q

from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttcore.permissions import has_substance_module_permission


class RegulatoryFrameworkDetailApiView(APIView):
    permission_classes = (IsAuthenticated,)
    rating_service = RatingSearchService()

    def get(self, request, framework_id):
        organization_id = request.user.organization_id
        framework_queryset = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            organization_id, apply_mute_filter=False).filter('match', id=framework_id).to_queryset().first()

        if not framework_queryset or not organization_id:
            return Response(status=status.HTTP_204_NO_CONTENT)

        framework_details = self.__get_framework_object(request, framework_queryset, distinct_item=False)
        framework_regions = []

        for url in framework_queryset.urls.all():
            framework_details['links'].append({'id': url.id, 'text': url.text, 'description': url.description})

        for topic in framework_queryset.topics.all():
            framework_details['topics'].append({'id': topic.id, 'name': topic.name})

        for region in framework_queryset.regions.all():
            framework_regions.append({'id': region.id, 'name': region.name})
        framework_details['regions'] = framework_regions

        for document in framework_queryset.documents.all():
            framework_details['documents'].append({
                'id': document.id,
                'title': document.title,
                'link': document.attachment.url if document.attachment else None,
            })

        framework_details['regulations'] = self.__get_framework_related_regulations(framework_queryset,
                                                                                    framework_regions, organization_id)

        framework_details['news'] = self.__get_framework_related_news_list(framework_queryset, organization_id)

        substance_module_permission = has_substance_module_permission(organization_id)
        substance_count = RelevantSubstanceService().get_organization_relevant_substance_data(
            organization_id, data_name='framework', data_id=framework_id, only_my_org=False).count()
        framework_details['substance_count'] = substance_count if substance_module_permission else 0

        framework_details['is_muted'] = RegulationMute.objects.filter(
            organization_id=organization_id, regulatory_framework_id=framework_queryset.id, is_muted=True).exists()
        return Response(framework_details, status=status.HTTP_200_OK)

    def __get_framework_object(self, request, framework_queryset, distinct_item=True):

        organization_id = request.user.organization_id
        return {
            'id': framework_queryset.id,
            'name': framework_queryset.name,
            'description': framework_queryset.description,
            'status': framework_queryset.status.name,
            'language': framework_queryset.language.name,
            'issuing_body': framework_queryset.issuing_body.name,
            'created': framework_queryset.created,
            'impact_rating': self.rating_service.get_framework_rating_obj(organization_id, framework_queryset.id),
            'links': [],
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id,
                framework_queryset.product_categories.all(), serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id,
                framework_queryset.material_categories.all(), serialize=True, distinct_item=distinct_item),
            'topics': [],
            'regions': [],
            'documents': [],
            'regulations': [],
            'news': [],
        }

    def __get_framework_related_regulations(self, framework_queryset, framework_regions, organization_id):
        regulation_list = []
        rel_reg_ids = RelevantRegulationService().get_relevant_regulation_id_organization(organization_id)
        regulations = framework_queryset.regulation_regulatory_framework.all().order_by('-created')
        for regulation in regulations:
            if regulation.review_status != 'd' and IdSearchService().does_id_exit_in_sorted_list(
                    rel_reg_ids, regulation.id):
                regulation_obj = {
                    'id': regulation.id,
                    'name': regulation.name,
                    'status': regulation.status.name,
                    'description': regulation.description,
                    'impact_rating': self.rating_service.get_regulation_rating_obj(organization_id, regulation.id),
                    'regions': framework_regions,
                    'milestones': [],
                    'topics': [],
                }

                for milestone in regulation.regulation_milestone.all():
                    regulation_obj['milestones'].append({
                        'id': milestone.id,
                        'name': milestone.name,
                        'description': milestone.description,
                        'date': milestone.to_date
                    })

                for topic in regulation.topics.all():
                    regulation_obj['topics'].append({'id': topic.id, 'name': topic.name})

                regulation_list.append(regulation_obj)

        return regulation_list

    def __get_framework_related_news_list(self, framework_queryset, organization_id):
        news_list = []
        relevant_regulation_ids_organization = RelevantRegulationService().\
            get_relevant_regulation_id_organization(organization_id)

        news_regulatory_frameworks_queryset = framework_queryset.news_regulatory_frameworks.\
            filter(Q(active=True) & Q(status='s')).order_by('-pub_date').\
            prefetch_related('regions', 'product_categories', 'material_categories', 'regulations')
        for news in news_regulatory_frameworks_queryset:
            news_obj = {
                'id': news.id,
                'date': news.pub_date,
                'status': news.status,
                'source': {'id': news.source.id, 'name': news.source.name},
                'title': news.title,
                'impact_rating': self.rating_service.get_news_rating_obj(organization_id, news.id),
                'regions': [],
                'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                    organization_id,
                    news.product_categories.all(), serialize=True),
                'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                    organization_id,
                    news.material_categories.all(), serialize=True),
                'regulations': [],
            }

            for region in news.regions.all():
                news_obj['regions'].append({'id': region.id, 'name': region.name})
            relevant_regulation = news.regulations.filter(id__in=relevant_regulation_ids_organization)
            for regulation in relevant_regulation:
                if regulation.review_status != 'd':
                    regulation_obj = {
                        'id': regulation.id,
                        'name': regulation.name,
                        'description': regulation.name,
                        'status': regulation.status.name,
                        'regions': [],
                        'topics': [],
                        'impact_rating': self.rating_service.get_regulation_rating_obj(organization_id,
                                                                                       regulation.id)
                    }

                    for region in regulation.regulatory_framework.regions.all():
                        regulation_obj['regions'].append({'id': region.id, 'name': region.name})

                    for topic in regulation.topics.all():
                        regulation_obj['topics'].append({'id': topic.id, 'name': topic.name})

                    news_obj['regulations'].append(regulation_obj)

            news_list.append(news_obj)

        return news_list

    @staticmethod
    def __get_organization_questions(request):
        organization_questions = []
        if request.user.organization_id:
            questions = QuestionDocument.search().filter('match', organization__id=request.user.organization_id) \
                .to_queryset()
            if questions:
                for question in questions:
                    organization_questions.append({
                        'id': question.id,
                        'name': question.name,
                        'description': question.description
                    })
        return organization_questions

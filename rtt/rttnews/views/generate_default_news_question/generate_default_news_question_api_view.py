import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rttcore.permissions import IsSuperUserOrStaff
from rttorganization.models.models import Organization
from rttnews.models.models import NewsAnswer, NewsQuestion, NewsRelevanceLog

logger = logging.getLogger(__name__)
User = get_user_model()


class GenerateDefaultNewsQuestionAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)

    @staticmethod
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'default_question_name': openapi.Schema(type=openapi.TYPE_STRING,
                                                    description='news question name that will be set for comment.',
                                                    default='Comment'),
            'default_question_description': openapi.Schema(type=openapi.TYPE_STRING,
                                                           description='news question description that '
                                                                       'will be set for comment.',
                                                           default='user comments'),
        }
    ))
    def post(request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-898
        """
        try:
            default_question_name = request.data.get('default_question_name', 'Comment')
            default_question_description = request.data.get('default_question_description', 'user comments')
            response = []
            organization_qs = Organization.objects.all()
            for organization in organization_qs:
                news_question_qs, created = NewsQuestion.objects.get_or_create(name__icontains=default_question_name,
                                                                               organization_id=organization.id,
                                                                               defaults={
                                                                                   'name': default_question_name,
                                                                                   'description': default_question_description})
                res_data = {
                    'organization_id': organization.id,
                    'organization_name': organization.name,
                    'default_question_create': created,
                    'default_question_id': news_question_qs.id,
                    'total_answer_created': 0
                }
                if created:
                    news_relevance_log_qs = NewsRelevanceLog.objects.filter(organization_id=organization.id,
                                                                            comment__isnull=False)
                    news_answer_obj_list = []
                    for news_rel_log in news_relevance_log_qs:
                        news_answer_obj_list.append(
                            NewsAnswer(answer_text=news_rel_log.comment, question=news_question_qs,
                                       news=news_rel_log.news, answered_by=news_rel_log.user,
                                       created=news_rel_log.created,
                                       modified=news_rel_log.modified))
                    NewsAnswer.objects.bulk_create(news_answer_obj_list)
                    res_data['total_answer_created'] = news_relevance_log_qs.count()
                response.append(res_data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

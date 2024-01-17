import logging
import math

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from rttcore.services.util_service import UtilsService
from rttnews.models.models import NewsAnswer, NewsQuestion
from rttcore.services.impact_assessment_answer_service import ImpactAssessmentAnswerService

logger = logging.getLogger(__name__)


class NewsImpactAssessmentQuestionListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    """
    doc: https://chemycal.atlassian.net/browse/RTT-825
    """

    @staticmethod
    def get(request):
        try:
            user_id = request.user.id
            organization_id = request.user.organization_id
            if request.GET.get('news_id', None):
                news_id = int(request.GET.get('news_id'))
            else:
                return Response({"message": "news_id must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            response = []
            news_question_qs = NewsQuestion.objects.filter(organization_id=organization_id)
            for news_question in news_question_qs:
                news_answer_qs = NewsAnswer.objects.filter(question_id=news_question.id, news_id=news_id).order_by(
                    'pin_by', '-created')
                if news_answer_qs:
                    news_answer = news_answer_qs.first()
                    response.append({
                        'id': news_question.id,
                        'name': news_question.name,
                        'answers': [ImpactAssessmentAnswerService().get_answer_object(news_answer, user_id)],
                        'has_more': UtilsService().has_more(news_answer_qs.count()-1, 3, 0)
                    })
                else:
                    response.append({
                        'id': news_question.id,
                        'name': news_question.name,
                        'answers': [],
                        'has_more': False
                    })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewsImpactAssessmentAnswerListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    """
    doc: https://chemycal.atlassian.net/browse/RTT-825
    """

    @staticmethod
    def get(request):
        try:
            user_id = request.user.id
            if request.GET.get('question_id', None):
                question_id = int(request.GET.get('question_id'))
            else:
                return Response({"message": "question_id must be sent"}, status=status.HTTP_400_BAD_REQUEST)

            if request.GET.get('news_id', None):
                news_id = int(request.GET.get('news_id'))
            else:
                return Response({"message": "news_id must be sent"}, status=status.HTTP_400_BAD_REQUEST)

            news_answer_qs = NewsAnswer.objects.filter(
                Q(question_id=question_id) & Q(news_id=news_id)).order_by('pin_by', '-created')
            if news_answer_qs.count() < 1:
                return Response({"message": "No answer found!"}, status=status.HTTP_404_NOT_FOUND)
            answer_list = []
            page_size = int(request.GET.get('pageSize', 1))
            if page_size == 0:
                has_more = UtilsService().has_more(news_answer_qs.count(), 1, 1)
                news_answer_qs = news_answer_qs[0:1]
            else:
                start_idx = (page_size * 3) - 2
                end_idx = start_idx + 3
                has_more = UtilsService().has_more(news_answer_qs.count() - 1, 3, page_size)
                news_answer_qs = news_answer_qs[start_idx:end_idx]
            for news_answer in news_answer_qs:
                answer_list.append(ImpactAssessmentAnswerService().get_answer_object(news_answer, user_id))
            response = {
                'answers': answer_list,
                'has_more': has_more
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

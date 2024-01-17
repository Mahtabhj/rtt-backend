import logging
import math

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from rttcore.services.util_service import UtilsService
from rttregulation.models.models import Question, Answer
from rttcore.services.impact_assessment_answer_service import ImpactAssessmentAnswerService

logger = logging.getLogger(__name__)


class RegulationImpactAssessmentQuestionListAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    """
    doc: https://chemycal.atlassian.net/browse/RTT-825
    """
    @staticmethod
    def get(request):
        try:
            user_id = request.user.id
            organization_id = request.user.organization_id
            regulation_id = request.GET.get('regulation_id', None)
            framework_id = request.GET.get('framework_id', None)
            if regulation_id and framework_id:
                return Response({"message": "Only regulation_id OR framework_id have to send"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif not regulation_id and not framework_id:
                return Response({"message": "Both regulation_id and framework_id can not be empty"},
                                status=status.HTTP_400_BAD_REQUEST)
            response = []
            reg_question_qs = Question.objects.filter(organization_id=organization_id)
            for reg_question in reg_question_qs:
                if regulation_id:
                    reg_answer_qs = Answer.objects.filter(regulation_id=regulation_id,
                                                          question_id=reg_question.id).order_by('pin_by', '-created')
                else:
                    reg_answer_qs = Answer.objects.filter(regulatory_framework_id=framework_id,
                                                          question_id=reg_question.id).order_by('pin_by', '-created')
                if reg_answer_qs:
                    reg_answer = reg_answer_qs.first()
                    response.append({
                        'id': reg_question.id,
                        'name': reg_question.name,
                        'answers': [ImpactAssessmentAnswerService().get_answer_object(reg_answer, user_id)],
                        'has_more': UtilsService().has_more(reg_answer_qs.count()-1, 3, 0)
                    })
                else:
                    response.append({
                        'id': reg_question.id,
                        'name': reg_question.name,
                        'answers': [],
                        'has_more': False
                    })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegulationImpactAssessmentAnswerListAPIView(APIView):
    permission_classes = (IsAuthenticated, )
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

            regulation_id = request.GET.get('regulation_id', None)
            framework_id = request.GET.get('framework_id', None)
            if regulation_id and framework_id:
                return Response({"message": "Only regulation_id OR framework_id have to send"},
                                status=status.HTTP_400_BAD_REQUEST)
            if not regulation_id and not framework_id:
                return Response({"message": "Both regulation_id and framework_id can not be empty"},
                                status=status.HTTP_400_BAD_REQUEST)
            answer_list = []
            reg_answer_qs = Answer.objects.filter(question_id=question_id).order_by('pin_by', '-created')

            if regulation_id:
                regulation_id = int(regulation_id)
                reg_answer_qs = reg_answer_qs.filter(regulation_id=regulation_id)
            else:
                framework_id = int(framework_id)
                reg_answer_qs = reg_answer_qs.filter(regulatory_framework_id=framework_id)
            if reg_answer_qs.count() < 1:
                return Response({"message": "No answer found!"}, status=status.HTTP_404_NOT_FOUND)

            page_size = int(request.GET.get('pageSize', 1))
            if page_size == 0:
                has_more = UtilsService().has_more(reg_answer_qs.count(), 1, 1)
                reg_answer_qs = reg_answer_qs[0:1]
            else:
                start_idx = (page_size * 3) - 2
                end_idx = start_idx + 3
                has_more = UtilsService().has_more(reg_answer_qs.count() - 1, 3, page_size)
                reg_answer_qs = reg_answer_qs[start_idx:end_idx]
            for reg_answer in reg_answer_qs:
                answer_list.append(ImpactAssessmentAnswerService().get_answer_object(reg_answer, user_id))
            response = {
                'answers': answer_list,
                'has_more': has_more
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

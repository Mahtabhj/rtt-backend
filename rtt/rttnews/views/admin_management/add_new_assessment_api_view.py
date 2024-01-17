import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsSuperUserOrStaff
from rttnews.models.models import NewsAnswer

logger = logging.getLogger(__name__)


class NewAssessmentBulkAddAdminAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)

    @staticmethod
    def post(request, news_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-904
        """
        try:
            user_id = request.user.id
            assessment_answers = request.data.get('assessments', None)
            if not assessment_answers:
                return Response({"message": "assessments must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            succeed_ans_add_count = 0
            for assessment_ans in assessment_answers:
                try:
                    answer_text = assessment_ans['answer_text']
                    question_id = assessment_ans['question_id']
                    NewsAnswer.objects.create(answer_text=answer_text, question_id=question_id, news_id=news_id,
                                              answered_by_id=user_id)
                    succeed_ans_add_count += 1
                except Exception as exc:
                    logger.error(str(exc), exc_info=True)
            response = {
                "message": f"{succeed_ans_add_count} news-assessment-answer(s) has been added"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

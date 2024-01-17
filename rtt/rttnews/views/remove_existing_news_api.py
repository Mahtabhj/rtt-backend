import logging
from django.db.models import Q

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rttcore.permissions import IsSuperUserOrStaff

from rttnews.services.news_service import NewsService
from rttnews.models.models import NewsAssessmentWorkflow

logger = logging.getLogger(__name__)


class RemoveExistingNewsIrrelevantToOrganization(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            news_assessment_workflow_qs = NewsAssessmentWorkflow.objects.filter(status__exact='to_be_assessed')
            visited_news = {}
            for news_assessment_workflow in news_assessment_workflow_qs:
                news_id = news_assessment_workflow.news_id
                if str(news_id) not in visited_news:
                    visited_news[str(news_id)] = True
                    organization_doc_qs = NewsService().get_relevant_organization_queryset_by_news(news_id)
                    organization_doc_qs = organization_doc_qs[0:organization_doc_qs.count()]
                    relevant_org_id_list = []
                    for org in organization_doc_qs:
                        relevant_org_id_list.append(org.id)
                    NewsAssessmentWorkflow.objects.filter(Q(news_id=news_id) & Q(status__exact='to_be_assessed') &
                                                          ~Q(organization_id__in=relevant_org_id_list)).delete()
            return Response({'message': 'succeed'}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

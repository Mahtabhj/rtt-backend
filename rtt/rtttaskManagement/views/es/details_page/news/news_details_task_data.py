import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveTaskManagementModule
from rtttaskManagement.services.task_core_service import TaskCoreService
from rtttaskManagement.services.task_list_display_service import TaskListDisplayService

logger = logging.getLogger(__name__)


class TaskListInNewsDetails(APIView):
    permission_classes = (IsAuthenticated, IsActiveTaskManagementModule, )

    @staticmethod
    def get(request, news_id):
        try:
            filters = {
                'news': [news_id]
            }
            organization_id = request.user.organization_id
            task_doc_queryset = TaskCoreService().get_filtered_task_queryset(organization_id, filters).sort('-due_date')
            task_doc_queryset = task_doc_queryset[0:task_doc_queryset.count()]
            response = TaskListDisplayService().get_task_list(task_doc_queryset)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

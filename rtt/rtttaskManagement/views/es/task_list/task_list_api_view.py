from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveTaskManagementModule
from rtttaskManagement.services.task_core_service import TaskCoreService
from rtttaskManagement.services.task_list_display_service import TaskListDisplayService

logger = logging.getLogger(__name__)


class TaskListAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveTaskManagementModule, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='filter by status: done/open, default is open'),
            'assignee': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of assignee ID',
                                       items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product ID',
                                       items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulations ID',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'substances': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of substances ID',
                                         items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last mentioned from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last mentioned to data(yyyy-mm-dd)'),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Any keyword, will be searched in task name, task description, '
                                                 'assignee name, product name, substance name')
        }
    ))
    def post(self, request):
        try:
            filters = {
                'status': request.data.get('status', None),
                'assignee': request.data.get('assignee', None),
                'products': request.data.get('products', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'regulations': request.data.get('regulations', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'substances': request.data.get('substances', None)
            }
            task_status = request.data.get('status', None)
            if task_status and task_status == 'archived':
                filters['is_archive'] = True
                filters['status'] = None
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id
            task_doc_queryset = TaskCoreService().get_filtered_task_queryset(
                organization_id, filters, search_keyword).sort('-due_date')
            task_doc_queryset = task_doc_queryset[0:task_doc_queryset.count()]
            response = TaskListDisplayService().get_task_list(task_doc_queryset)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

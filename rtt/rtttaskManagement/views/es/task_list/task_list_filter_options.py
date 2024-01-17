from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveTaskManagementModule
from rtttaskManagement.services.task_core_service import TaskCoreService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.id_search_service import IdSearchService

logger = logging.getLogger(__name__)
rel_regulation_service = RelevantRegulationService()


class TaskListFilterOptionAPIView(APIView):
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
            organization_id = request.user.organization_id
            search_keyword = request.data.get('search', None)
            task_doc_queryset = TaskCoreService().get_filtered_task_queryset(
                organization_id, filters, search_keyword)
            task_doc_queryset = task_doc_queryset[0:task_doc_queryset.count()]
            assignee_list = []
            visited_assignee = {}
            product_list = []
            visited_product = {}
            regulation_list = []
            visited_regulation = {}
            framework_list = []
            visited_framework = {}
            rel_fw_ids = rel_regulation_service.get_relevant_regulatory_framework_id_organization(organization_id)
            rel_reg_ids = rel_regulation_service.get_relevant_regulation_id_organization(organization_id)
            substance_list = []
            visited_substance = {}
            for task in task_doc_queryset:
                if task.assignee and str(task.assignee.id) not in visited_assignee:
                    assignee_list.append({
                        'id': task.assignee.id,
                        'first_name': task.assignee.first_name,
                        'last_name': task.assignee.last_name
                    })
                    visited_assignee[str(task.assignee.id)] = True
                for product in task.products:
                    if str(product.id) not in visited_product:
                        product_list.append({
                            'id': product.id,
                            'name': product.name
                        })
                        visited_product[str(product.id)] = True
                for regulation in task.regulations:
                    if IdSearchService().does_id_exit_in_sorted_list(rel_reg_ids, regulation.id) and \
                            str(regulation.id) not in visited_regulation:
                        regulation_list.append({
                            'id': regulation.id,
                            'name': regulation.name
                        })
                        visited_regulation[str(regulation.id)] = True
                for framework in task.regulatory_frameworks:
                    if IdSearchService().does_id_exit_in_sorted_list(rel_fw_ids, framework.id) and \
                            str(framework.id) not in visited_framework:
                        framework_list.append({
                            'id': framework.id,
                            'name': framework.name
                        })
                        visited_framework[str(framework.id)] = True
                for substance in task.substances:
                    if str(substance.id) not in visited_substance:
                        substance_list.append({
                            'id': substance.id,
                            'name': substance.name
                        })
                        visited_substance[str(substance.id)] = True
            response = {
                'assignee': assignee_list,
                'products': product_list,
                'regulations': regulation_list,
                'regulatory_frameworks': framework_list,
                'substances': substance_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

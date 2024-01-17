import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rttcore.permissions import IsActiveTaskManagementModule
from django.contrib.auth import get_user_model
from rttcore.services.system_filter_service import SystemFilterService
from rttproduct.documents import ProductDocument

from elasticsearch_dsl import Q

User = get_user_model()
logger = logging.getLogger(__name__)


class TaskCreateEditFilterOption(APIView):
    permission_classes = (IsAuthenticated, IsActiveTaskManagementModule, )

    def get(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-605
        """
        try:
            organization_id = request.user.organization_id
            response = {
                'assignee': self.get_assignee_drop_down_options(organization_id, current_user_id=request.user.id),
                'products': self.get_product_drop_down_options(organization_id),
                'regulatory_frameworks': self.get_regulatory_framework_drop_down_options(organization_id),
                'regulations': self.get_regulations_drop_down_options(organization_id)
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_assignee_drop_down_options(organization_id, current_user_id):
        result = []
        user_queryset = User.objects.filter(organization_id=organization_id)
        for user in user_queryset:
            user_obj = {
                'id': user.id,
                'avatar': user.avatar.url if user.avatar else None,
                'first_name': user.first_name if user.first_name else None,
                'last_name': user.last_name if user.last_name else None,
                'username': user.username
            }
            if user.id == current_user_id and len(result) != 0:
                temp_user_obj = result[0]
                result[0] = user_obj
                result.append(temp_user_obj)
            else:
                result.append(user_obj)
        return result

    @staticmethod
    def get_product_drop_down_options(organization_id):
        result = []
        product_doc_qs: ProductDocument = ProductDocument().search().filter(
            Q('match', organization__id=organization_id)
        ).source(['id', 'name'])
        product_doc_qs = product_doc_qs[0:product_doc_qs.count()]
        for product in product_doc_qs:
            result.append({
                'id': product.id,
                'name': product.name
            })
        return result

    @staticmethod
    def get_regulatory_framework_drop_down_options(organization_id):
        result = []
        regulatory_framework_doc_qs = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            organization_id).source(['id', 'name'])
        regulatory_framework_doc_qs = regulatory_framework_doc_qs[0:regulatory_framework_doc_qs.count()]
        for framework in regulatory_framework_doc_qs:
            result.append({
                'id': framework.id,
                'name': framework.name
            })
        return result

    @staticmethod
    def get_regulations_drop_down_options(organization_id):
        result = []
        regulation_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(
            organization_id).source(['id', 'name'])
        regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
        for regulation in regulation_doc_qs:
            result.append({
                'id': regulation.id,
                'name': regulation.name
            })
        return result

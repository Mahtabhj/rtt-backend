import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveDocumentManagementModule
from rttcore.services.system_filter_service import SystemFilterService
from rttproduct.documents import ProductDocument

logger = logging.getLogger(__name__)


class DocManagementCreateEditDropdownOptionsAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveDocumentManagementModule)

    def get(self, request):
        try:
            response = []
            organization_id = request.user.organization_id
            # relevant_regulations
            relevant_regulations = self.get_relevant_regulations_organization(organization_id)
            # relevant_frameworks
            relevant_frameworks = self.get_relevant_frameworks_organization(organization_id)
            # relevant_products
            relevant_products = self.get_relevant_products_organization(organization_id)
            # relevant_news
            relevant_news = self.get_relevant_news_organization(organization_id)

            response.append({
                'regulations': relevant_regulations,
                'regulatory_frameworks': relevant_frameworks,
                'products': relevant_products,
                'news': relevant_news,
            })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_relevant_regulations_organization(organization_id):
        relevant_regulations = []
        organization_regulation_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(
            organization_id).source(['id', 'name']).sort('name.raw')
        organization_regulation_qs = organization_regulation_qs[0:organization_regulation_qs.count()]
        for organization_regulation in organization_regulation_qs:
            relevant_regulations.append({
                'id': organization_regulation.id,
                'name': organization_regulation.name,
            })
        return relevant_regulations

    @staticmethod
    def get_relevant_frameworks_organization(organization_id):
        relevant_frameworks = []
        organization_framework_qs = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            organization_id).source(['id', 'name']).sort('name.raw')
        organization_framework_qs = organization_framework_qs[0:organization_framework_qs.count()]
        for organization_framework in organization_framework_qs:
            relevant_frameworks.append({
                'id': organization_framework.id,
                'name': organization_framework.name,
            })
        return relevant_frameworks

    @staticmethod
    def get_relevant_news_organization(organization_id):
        relevant_news = []
        organization_news_qs = SystemFilterService().get_system_filtered_news_document_queryset(
            organization_id).source(['id', 'title'])
        organization_news_qs = organization_news_qs[0:organization_news_qs.count()]
        for organization_news in organization_news_qs:
            relevant_news.append({
                'id': organization_news.id,
                'title': organization_news.title,
            })
        return relevant_news

    @staticmethod
    def get_relevant_products_organization(organization_id):
        relevant_products = []
        product_queryset = ProductDocument.search().filter('match', organization__id=organization_id).source(
            ['id', 'name', 'image'])
        product_queryset = product_queryset[0:product_queryset.count()]
        for product in product_queryset:
            relevant_products.append({
                'id': product.id,
                'name': product.name,
                'image': product.image,
            })
        return relevant_products

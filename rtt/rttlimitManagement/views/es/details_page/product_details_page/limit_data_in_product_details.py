from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status

from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttproduct.documents import ProductDocument
from rttproduct.services.product_services import ProductServices
from rttlimitManagement.services.product_detail_limit_tab_service import LimitInProductDetailsService

logger = logging.getLogger(__name__)


class LimitInProductDetails(APIView):
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in regulation_name, framework_name, substance_name, '
                                                 'substance_ec, substance_cas, scope'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Last position for pagination'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER, description='First position for pagination'),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regions IDs',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        }
    ))
    def post(self, request, product_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1230
        """
        try:
            search_keyword = request.data.get('search', None)
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            organization_id = request.user.organization_id
            regions = request.data.get('regions', None)

            # get product related substance id_list
            product_related_substance_id_list = LimitInProductDetailsService().get_product_related_substance_id_list(
                organization_id, product_id, regions, product_detail_page=True)

            # get product category and material category id_list and will be used for filtering related fw & reg
            product_categories_ids = []
            material_categories_ids = []
            product_search_qs = ProductDocument.search().filter('match', id=product_id)
            for product_search in product_search_qs:
                for product_category in product_search.product_categories:
                    product_categories_ids.extend(
                        ProductServices().get_all_parent_product_category_ids(product_category))
                for material_category in product_search.material_categories:
                    material_categories_ids.append(material_category.id)
            # get unique product categories
            product_categories_ids = list(set(product_categories_ids))
            # get product related framework id_list
            product_related_framework_id_list = LimitInProductDetailsService().get_product_related_framework_id_list(
                organization_id, product_categories_ids, material_categories_ids, regions)
            # get product related regulation id_list
            product_related_regulation_id_list = LimitInProductDetailsService().get_product_related_regulation_id_list(
                organization_id, product_categories_ids, material_categories_ids, regions)

            # if a product has no related substance or (no related framework and no regulation)
            if len(product_related_substance_id_list) < 1 or (len(product_related_framework_id_list) < 1 and
                                                              len(product_related_regulation_id_list) < 1):
                response = {
                    'count': 0,
                    'results': []
                }
                return Response(response, status=status.HTTP_200_OK)

            # create filter for limit and filter by substance_ids
            filters = {
                'substances': product_related_substance_id_list,
                'regulatory_frameworks': product_related_framework_id_list,
                'regulations': product_related_regulation_id_list,
            }
            regulation_substance_limit_qs = LimitCoreService().get_regulation_substance_limit_queryset(
                organization_id, filters)
            '''keyword search in substances name, CAS, EC, framework name, regulation name'''
            if search_keyword:
                regulation_substance_limit_qs = LimitInProductDetailsService().get_filtered_limit_queryset(
                    regulation_substance_limit_qs, search_keyword)
            count = regulation_substance_limit_qs.count()
            regulation_substance_limit_qs = regulation_substance_limit_qs[skip:skip + limit]
            limit_data = []
            for limit in regulation_substance_limit_qs:
                if limit.regulatory_framework:
                    limit_obj = LimitInProductDetailsService().get_regulation_limit_object(
                        limit, limit.regulatory_framework, is_regulation=False)
                    limit_data.append(limit_obj)
                else:
                    limit_obj = LimitInProductDetailsService().get_regulation_limit_object(
                        limit, limit.regulation, is_regulation=True)
                    limit_data.append(limit_obj)
            response = {
                'count': count,
                'results': limit_data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

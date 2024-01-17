from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status

from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttregulation.services.regulation_tagged_region_service import RegulationTaggedRegionService
from rttproduct.documents import ProductDocument
from rttproduct.services.product_services import ProductServices
from rttlimitManagement.services.product_detail_limit_tab_service import LimitInProductDetailsService

logger = logging.getLogger(__name__)


class LimitDataFilterOption(APIView):
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in regulation_name, framework_name, substance_name, '
                                                 'substance_ec, substance_cas, scope'),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regions IDs',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        }
    ))
    def post(self, request, product_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1287
        """
        try:
            search_keyword = request.data.get('search', None)
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
                response = []
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
            regulation_substance_limit_qs = regulation_substance_limit_qs[0:regulation_substance_limit_qs.count()]
            region_list = []
            visited_region = {}
            for limit in regulation_substance_limit_qs:
                if limit.regulatory_framework:
                    for region in limit.regulatory_framework.regions:
                        if str(region.id) not in visited_region:
                            region_list.append({'id': region.id, 'name': region.name})
                            visited_region[str(region.id)] = True
                else:
                    if limit.regulation.regulatory_framework:
                        regulation_region_list = RegulationTaggedRegionService().get_region_data(
                            framework_id=limit.regulation.regulatory_framework.id)
                        for region in regulation_region_list:
                            if str(region['id']) not in visited_region:
                                region_list.append({'id': region['id'], 'name': region['name']})
                                visited_region[str(region['id'])] = True

            response = {
                'regions': region_list,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

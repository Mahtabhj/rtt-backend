from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.region_page_services import RegionPageServices
from rttlimitManagement.services.additional_attributes_data_service import AdditionalAttributesDataService
from rttregulation.services.regulation_tagged_region_service import RegulationTaggedRegionService
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttcore.services.id_search_service import IdSearchService

logger = logging.getLogger(__name__)


class LimitTablListData(APIView):
    permission_classes = (IsAuthenticated,)
    region_page_service = RegionPageServices()

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'related_products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product ID',
                                               items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'product_categories': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product categories ID',
                                                 items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'material_categories': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of material categories ID',
                                                  items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'related_regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulation ID',
                                                  items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'related_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                                 items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'news': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news ID',
                                   items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='filter by rating.'),
            'status': openapi.Schema(type=openapi.TYPE_ARRAY, description='filter by status.',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topic ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Value of limit'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER, description='Value of skip'),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Any keyword, will be searched in substance name, EC, CAS, '
                                                 'framework name, regulation name, scope'),
        }
    ))
    def post(self, request, region_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1193
        """
        try:
            region_id = int(region_id)
            organization_id = request.user.organization_id
            filters = {
                'related_products': request.data.get('related_products', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'related_regulations': request.data.get('related_regulations', None),
                'related_frameworks': request.data.get('related_frameworks', None),
                'news': request.data.get('news', None),
                'rating': request.data.get('rating', None),
                'status': request.data.get('status', None),
                'topics': request.data.get('topics', None)
            }
            limit = request.data.get('limit', 20)
            skip = request.data.get('skip', 0)
            search_keyword = request.data.get('search', None)
            queryset_limit = self.region_page_service.get_filtered_limit_queryset(organization_id, region_id, filters,
                                                                                  search_keyword)
            count = queryset_limit.count()
            queryset_limit = queryset_limit[skip:skip + limit]
            relevant_substance_ids = RelevantSubstanceService().get_organization_relevant_substance_ids(organization_id)

            limit_data_list = []
            for limit in queryset_limit:
                regulation_obj = None
                additional_attributes = None
                region_list = []

                # related regulatory_framework
                if limit.regulatory_framework:
                    regulation_obj = {
                        'id': limit.regulatory_framework.id,
                        'name': limit.regulatory_framework.name,
                        'is_regulation': False,
                    }
                    additional_attributes = AdditionalAttributesDataService.get_additional_attributes_data(
                        limit.id, limit.regulatory_framework.id, is_regulation=False)
                    # regions which are tagged with framework
                    region_list = self.get_framework_tagged_region_list(limit.regulatory_framework.regions)

                # related regulation
                if limit.regulation:
                    regulation_obj = {
                        'id': limit.regulation.id,
                        'name': limit.regulation.name,
                        'is_regulation': True,
                    }
                    additional_attributes = AdditionalAttributesDataService.get_additional_attributes_data(
                        limit.id, limit.regulation.id, is_regulation=True)
                    # regions which are tagged with regulations framework
                    region_list = RegulationTaggedRegionService().get_region_data(
                        framework_id=limit.regulation.regulatory_framework.id)

                limit_data_list.append({
                    'id': limit.id,
                    'regulation': regulation_obj,
                    'substance': {
                        'id': limit.substance.id,
                        'name': limit.substance.name,
                        'cas_no': limit.substance.cas_no,
                        'ec_no': limit.substance.ec_no,
                        'is_relevant': IdSearchService().does_id_exit_in_sorted_list(relevant_substance_ids,
                                                                                     limit.substance.id)
                    },
                    'regions': region_list,
                    'scope': limit.scope,
                    'limit_value': limit.limit_value,
                    'measurement_limit_unit': limit.measurement_limit_unit,
                    'limit_additional_attributes': additional_attributes,
                })
            response = {
                "count": count,
                "results": limit_data_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_framework_tagged_region_list(region_queryset):
        region_list = []
        for region in region_queryset:
            region_list.append({
                "id": region.id,
                "name": region.name,
            })
        return region_list

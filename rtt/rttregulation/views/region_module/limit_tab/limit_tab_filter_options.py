from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.region_page_services import RegionPageServices
from rttregulation.services.relevant_regulation_service import RelevantRegulationService

logger = logging.getLogger(__name__)


class LimitTabFilterOption(APIView):
    permission_classes = (IsAuthenticated,)
    rel_regulation_service = RelevantRegulationService()

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
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Any keyword, will be searched in task name, framework, '
                                                 'regulation name, product name')
        }
    ))
    def post(self, request, region_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1259
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
            search_keyword = request.data.get('search', None)
            limit_doc_qs = RegionPageServices().get_filtered_limit_queryset(organization_id, region_id, filters,
                                                                            search_keyword)
            limit_doc_qs = limit_doc_qs[0:limit_doc_qs.count()]

            """
            limit data
            """
            framework_list = []
            visited_framework = {}
            regulations_list = []
            visited_regulation = {}

            for limit in limit_doc_qs:
                if limit.regulatory_framework:
                    if str(limit.regulatory_framework.id) not in visited_framework:
                        framework_list.append({
                            'id': limit.regulatory_framework.id,
                            'name': limit.regulatory_framework.name
                        })
                        visited_framework[str(limit.regulatory_framework.id)] = True
                if limit.regulation:
                    if str(limit.regulation.id) not in visited_regulation:
                        regulations_list.append({
                            'id': limit.regulation.id,
                            'name': limit.regulation.name
                        })
                        visited_regulation[str(limit.regulation.id)] = True
            response = {
                'frameworks': framework_list,
                'regulations': regulations_list,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

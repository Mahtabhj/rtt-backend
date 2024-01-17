from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttcore.services.id_search_service import IdSearchService
from rttnews.services.relevant_news_service import RelevantNewsService
from rttsubstance.services.substance_core_service import SubstanceCoreService

logger = logging.getLogger(__name__)


class SubstanceNewsPrioritizedFilterOptions(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'uses_and_applications': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                    description='List of uses_and_applications ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Product ID',
                                       items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='search by name, ec_no and cas_no'),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region id',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'news_source_types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news source type id',
                                                items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last mentioned from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last mentioned to data(yyyy-mm-dd)'),
            'prioritization_strategies': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                        description='List of prioritization_strategies ID',
                                                        items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(self, request):
        try:
            filters = {
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'products': request.data.get('products', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'regions': request.data.get('regions', None),
                'news_source_types': request.data.get('news_source_types', None),
                'news_from_date': request.data.get('from_date', None),
                'news_to_date': request.data.get('to_date', None),
                'prioritization_strategies': request.data.get('prioritization_strategies', None)
            }
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id
            news_prioritized_substance_list = SubstanceCoreService().get_filtered_substance_queryset(organization_id,
                                                                                                     news_prioritized=True,
                                                                                                     filters=filters,
                                                                                                     search_keyword=search_keyword)
            news_prioritized_substance_list = news_prioritized_substance_list[0:news_prioritized_substance_list.count()]
            relevant_news_ids = RelevantNewsService().get_organization_relevant_news_ids(organization_id)
            regions_list = []
            source_types_list = []
            visited_news_ids = []
            relevant_property_datapoint_ids = set()
            for substance in news_prioritized_substance_list:
                for substance_property_data_point in substance.substance_property_data_point_relation:
                    if substance_property_data_point.property_data_point:
                        relevant_property_datapoint_ids.add(substance_property_data_point.property_data_point.id)
                for news in substance.substances_news:
                    if news.id not in visited_news_ids and IdSearchService().does_id_exit_in_sorted_list(
                            relevant_news_ids, news.id):
                        visited_news_ids.append(news.id)
                        for region in news.regions:
                            region_obj = {
                                'id': region.id,
                                'name': region.name
                            }
                            if region_obj not in regions_list:
                                regions_list.append(region_obj)
                        if news.source.type:
                            source_type_obj = {
                                'id': news.source.type.id,
                                'name': news.source.type.name
                            }
                            if source_type_obj not in source_types_list:
                                source_types_list.append(source_type_obj)
            prioritization_strategies_list = SubstanceCoreService().get_prioritization_strategies_queryset(
                organization_id, list(relevant_property_datapoint_ids), serializer=True)
            response = {
                "regions": regions_list,
                "source_types": source_types_list,
                "prioritization_strategies": prioritization_strategies_list,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

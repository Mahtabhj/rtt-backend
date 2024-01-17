from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.region_page_services import RegionPageServices
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.id_search_service import IdSearchService

logger = logging.getLogger(__name__)


class NewsTabFilterOption(APIView):
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
        doc: https://chemycal.atlassian.net/browse/RTT-1039
        """
        try:
            region_id = int(region_id)
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
            organization_id = request.user.organization_id
            """
            news data
            """
            rel_reg_ids = self.rel_regulation_service.get_relevant_regulation_id_organization(organization_id)
            rel_fw_ids = self.rel_regulation_service.get_relevant_regulatory_framework_id_organization(organization_id)
            framework_list = []
            visited_framework = {}
            regulations_list = []
            visited_regulation = {}
            topics_list = []
            visited_topics = {}

            news_doc_qs = RegionPageServices().get_filtered_news_queryset(organization_id, region_id, filters,
                                                                          search_keyword)
            news_doc_qs = news_doc_qs[0:news_doc_qs.count()]
            for news in news_doc_qs:
                for framework in news.regulatory_frameworks:
                    if IdSearchService().does_id_exit_in_sorted_list(rel_fw_ids, framework.id) and str(framework.id) \
                            not in visited_framework:
                        framework_list.append({
                            'id': framework.id,
                            'name': framework.name
                        })
                        visited_framework[str(framework.id)] = True
                for regulation in news.regulations:
                    if IdSearchService().does_id_exit_in_sorted_list(rel_reg_ids, regulation.id) and \
                            str(regulation.id) not in visited_regulation:
                        regulations_list.append({
                            'id': regulation.id,
                            'name': regulation.name
                        })
                        visited_regulation[str(regulation.id)] = True
                for news_category in news.news_categories:
                    if news_category.topic and str(news_category.topic.id) not in visited_topics:
                        topics_list.append({
                            'id': news_category.topic.id,
                            'name': news_category.topic.name
                        })
                        visited_topics[str(news_category.topic.id)] = True
            response = {
                'frameworks': framework_list,
                'regulations': regulations_list,
                'topics': topics_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

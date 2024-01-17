from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from collections import defaultdict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.id_search_service import IdSearchService

from elasticsearch_dsl import Q

from rttregulation.services.region_page_services import RegionPageServices

logger = logging.getLogger(__name__)


class RegionTimeLine(APIView):
    permission_classes = (IsAuthenticated, )

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
            'status': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of status ID',
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
        doc: https://chemycal.atlassian.net/browse/RTT-1037
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
            related_milestones_ids = RelevantRegulationService().get_relevant_milestone_id_organization(organization_id)
            response = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: []))))
            """
            news data
            """
            queryset_news = RegionPageServices().get_filtered_news_queryset(organization_id, region_id, filters,
                                                                            search_keyword)
            queryset_news = queryset_news[0:queryset_news.count()]
            for news in queryset_news:
                date = news.pub_date
                self.assign_data(date, response, data_name='news', data_id=news.id)

            """
            framework data
            """
            queryset_framework = RegionPageServices().get_filtered_framework_queryset(organization_id, region_id,
                                                                                      filters, search_keyword)
            queryset_framework = queryset_framework.filter(
                # making sure every framework has milestone(s)
                Q('nested',
                  path='regulatory_framework_milestone',
                  query=Q('exists', field="regulatory_framework_milestone.id"))
            )
            queryset_framework = queryset_framework[0:queryset_framework.count()]
            for framework in queryset_framework:
                for milestone in framework.regulatory_framework_milestone:
                    if IdSearchService().does_id_exit_in_sorted_list(related_milestones_ids, milestone.id):
                        if not milestone.from_date:
                            continue
                        date = milestone.from_date
                        self.assign_data(date, response, data_name='milestones', data_id=milestone.id)

            """
            regulation data
            """
            queryset_regulation = RegionPageServices().get_filtered_regulation_queryset(organization_id, region_id,
                                                                                        filters, search_keyword)
            queryset_regulation = queryset_regulation.filter(
                # making sure every regulation has milestone(s)
                Q('nested',
                  path='regulation_milestone',
                  query=Q('exists', field="regulation_milestone.id"))
            )
            queryset_regulation = queryset_regulation[0:queryset_regulation.count()]
            for regulation in queryset_regulation:
                for milestone in regulation.regulation_milestone:
                    if IdSearchService().does_id_exit_in_sorted_list(related_milestones_ids, milestone.id):
                        if not milestone.from_date:
                            continue
                        date = milestone.from_date
                        self.assign_data(date, response, data_name='milestones', data_id=milestone.id)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def assign_data(date, response, data_name, data_id):
        response[str(date.year)][str(date.month)][str(date.day)][data_name].append(data_id)

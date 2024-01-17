from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.rating_search_service import RatingSearchService
from rttnews.services.news_report_page_services import NewsReportPageServices
from rttcore.permissions import IsActiveReportsModule

logger = logging.getLogger(__name__)


class NewsReportFilterOptionsApiView(APIView):
    permission_classes = (IsAuthenticated, IsActiveReportsModule)
    rating_service = RatingSearchService()

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='filter by rating.'),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last modified from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last modified to data(yyyy-mm-dd)'),
            'sort_order': openapi.Schema(type=openapi.TYPE_STRING, description='Sorting: asc/desc, default is desc.')
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1277
        """
        try:
            organization_id = request.user.organization_id
            """store regions"""
            # create filter for getting multiselect regions
            regions_filters = {
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'ratings': request.data.get('ratings', None)
            }
            # apply filter
            regions_tagged_news_doc_qs = NewsReportPageServices().get_filtered_news_queryset(regions_filters,
                                                                                             organization_id)
            # take all queryset
            regions_tagged_news_doc_qs = regions_tagged_news_doc_qs[0:regions_tagged_news_doc_qs.count()]

            regions_list = []
            visited_regions = {}
            for news in regions_tagged_news_doc_qs:
                # get regions which are tagged with news
                self.get_regions_filter_options(news.regions, regions_list, visited_regions)

            """store rating"""
            # create filter for getting multiselect rating
            ratings_filters = {
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'regions': request.data.get('regions', None),
            }
            # apply main filter
            ratings_tagged_news_doc_qs = NewsReportPageServices().get_filtered_news_queryset(ratings_filters,
                                                                                             organization_id)
            # take all queryset
            ratings_tagged_news_doc_qs = ratings_tagged_news_doc_qs[0:ratings_tagged_news_doc_qs.count()]

            rating_list = []
            for news in ratings_tagged_news_doc_qs:
                # get rating which are tagged with news
                self.get_rating_filter_options(news.news_relevance, rating_list, organization_id)
                # making sure, if null is tagged then include 0 rating
                rating_list = set(rating_list)
                if len(rating_list) < ratings_tagged_news_doc_qs.count():
                    rating_list.add(0)
                rating_list = list(rating_list)

            response = {
                'regions': regions_list,
                'rating': rating_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_regions_filter_options(regions_qs, regions_list, visited_regions):
        for region in regions_qs:
            if str(region.id) not in visited_regions:
                region_obj = {
                    'id': region.id,
                    'name': region.name
                }
                regions_list.append(region_obj)
                visited_regions[str(region.id)] = True

    @staticmethod
    def get_rating_filter_options(rating_qs, rating_list, organization_id):
        for rating in rating_qs:
            if rating.organization.id == organization_id:
                rating_list.append(rating.relevancy)

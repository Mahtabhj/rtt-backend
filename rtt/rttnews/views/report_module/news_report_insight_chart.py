from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttnews.services.news_report_page_services import NewsReportPageServices
from rttcore.permissions import IsActiveReportsModule

logger = logging.getLogger(__name__)


class NewsReportInsightChart(APIView):
    permission_classes = (IsAuthenticated, IsActiveReportsModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'ratings': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of rating, 0 if Not rated',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last modified from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last modified to data(yyyy-mm-dd)'),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1279
        """
        try:
            filters = {
                'regions': request.data.get('regions', None),
                'ratings': request.data.get('ratings', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None)
            }
            organization_id = request.user.organization_id
            """
            news data
            """
            news_doc_qs = NewsReportPageServices().get_filtered_news_queryset(filters, organization_id)
            rated_news_filters = {
                'ratings': [1, 2, 3, 4, 5]
            }
            # get the count only for rated news
            rated_news_count = NewsReportPageServices().rating_filtered_news_doc_qs(
                news_doc_qs, rated_news_filters, organization_id).count()

            agg_dict = NewsReportPageServices().get_rating_group_by_dict(organization_id)
            news_doc_queryset = news_doc_qs.update_from_dict(agg_dict).execute()
            group_by_doc_queryset = None
            for news_doc in news_doc_queryset.aggregations:
                group_by_doc_queryset = news_doc
            group_by_rating = {
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
            }
            for group_by_doc_qs in group_by_doc_queryset.news_relevance.results.buckets:
                rating_key_value = {str(group_by_doc_qs.key): group_by_doc_qs.doc_count}
                group_by_rating.update(rating_key_value)
            response = {
                'chart_one': {
                    'rated': rated_news_count,
                    'not_rated': news_doc_qs.count() - rated_news_count
                },
                'chart_two': group_by_rating
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

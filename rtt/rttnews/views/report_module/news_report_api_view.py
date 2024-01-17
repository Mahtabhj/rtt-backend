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


class NewsReportAPIView(APIView):
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
            'sort_order': openapi.Schema(type=openapi.TYPE_STRING, description='Sorting: asc/desc, default is desc.'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='For pagination.Default is 10.'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1275
        """
        try:
            filters = {
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'ratings': request.data.get('ratings', None),
                'regions': request.data.get('regions', None),
            }
            sort_order = request.data.get('sort_order', 'desc')
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            organization_id = request.user.organization_id
            """
            news data
            """
            news_list = []
            # apply filter
            news_doc_qs = NewsReportPageServices().get_filtered_news_queryset(filters, organization_id)
            # sort news queryset
            news_doc_qs = NewsReportPageServices().get_sorted_news_doc_qs(news_doc_qs, sort_order, organization_id)
            news_doc_qs_count = news_doc_qs.count()
            # apply pagination
            news_doc_qs = news_doc_qs[skip:skip + limit]

            for news in news_doc_qs:
                news_obj = NewsReportPageServices().get_news_object(news, organization_id)
                news_list.append(news_obj)
            response = {
                'count': news_doc_qs_count,
                'results': news_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

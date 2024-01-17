import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import pytz
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttnews.services.news_report_page_services import NewsReportPageServices


utc = pytz.UTC
logger = logging.getLogger(__name__)


class SubstanceLatestUpdatesNewsAPIView(APIView):
    """
    doc: https://chemycal.atlassian.net/browse/RTT-1454
    """
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'uses_and_applications': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                    description='List of uses_and_applications ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product ID',
                                       items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topic ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last mentioned from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last mentioned to data(yyyy-mm-dd)'),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='search for news, framework and regulation'),
        }
    ))
    def post(self, request, *args, **kwargs):
        try:
            substance_filters = {
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'products': request.data.get('products', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None)
            }
            filters = {
                'regions': request.data.get('regions', None),
                'topics': request.data.get('topics', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'search': request.data.get('search', None)
            }
            sort_order = request.data.get('sort_order', 'desc')
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            organization_id = request.user.organization_id
            substance_queryset = SubstanceCoreService().get_filtered_substance_queryset(
                organization_id, filters=substance_filters).source(['id'])
            substance_queryset = substance_queryset[0:substance_queryset.count()]
            substance_ids = []
            for substance in substance_queryset:
                substance_ids.append(substance.id)
            news_doc_qs_count, news_list = self.get_news_data(filters, organization_id, substance_ids, skip, limit, sort_order)
            response = {
                'count': news_doc_qs_count,
                'results': news_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_news_data(filters, organization_id, substance_ids, skip, limit, sort_order):
        news_list = []
        # apply filter
        news_doc_qs = NewsReportPageServices().get_filtered_news_queryset(filters, organization_id)
        news_doc_qs = news_doc_qs.filter(
            Q('nested',
              path='substances',
              query=Q('terms', substances__id=substance_ids))
        )
        # sort news queryset
        news_doc_qs = NewsReportPageServices().get_sorted_news_doc_qs(news_doc_qs, sort_order, organization_id)
        news_doc_qs_count = news_doc_qs.count()
        # apply pagination
        news_doc_qs = news_doc_qs[skip:skip + limit]

        for news in news_doc_qs:
            news_obj = NewsReportPageServices().get_news_object(news, organization_id)
            news_list.append(news_obj)
        return news_doc_qs_count, news_list

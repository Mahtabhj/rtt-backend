from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from elasticsearch_dsl import Q
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttcore.services.dashboard_services import DashboardService

logger = logging.getLogger(__name__)


class NewsPrioritizedSubstanceData(APIView):
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
            'sort_field': openapi.Schema(type=openapi.TYPE_STRING, enum=['name', 'mentioned', 'prioritization'],
                                         description='sort by filed name'),
            'sort_order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'],
                                         description='sort data in asc or desc order'),
            'prioritization_strategies': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                        description='List of prioritization_strategies ID',
                                                        items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(self, request):
        """
        https://chemycal.atlassian.net/browse/RTT-636
        """
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
            sort_field = request.data.get('sort_field', 'mentioned').lower()
            sort_order = request.data.get('sort_order', 'desc').lower()
            organization_id = request.user.organization_id
            name_sort_order = 'asc'
            if sort_field == 'name':
                name_sort_order = sort_order
            news_prioritized_substance_list = SubstanceCoreService().get_filtered_substance_queryset(organization_id,
                                                                                                     news_prioritized=True,
                                                                                                     filters=filters,
                                                                                                     search_keyword=search_keyword,
                                                                                                     sort_field='name',
                                                                                                     sort_order=name_sort_order)
            news_prioritized_substance_list = news_prioritized_substance_list[0:news_prioritized_substance_list.count()]
            news_filters = {
                'regions': request.data.get('regions', None),
                'news_source_types': request.data.get('news_source_types', None)
            }
            relevant_news_ids = self.get_relevant_filtered_news_ids_organization(organization_id, filters=news_filters)
            results = []
            for substance in news_prioritized_substance_list:
                mentioned = 0
                for news in substance.substances_news:
                    if str(news.id) in relevant_news_ids:
                        mentioned = mentioned + 1
                data = {
                    "id": substance.id,
                    "name": substance.name,
                    "mentioned": mentioned,
                    "prioritization": mentioned
                }
                results.append(data)
            if sort_field == 'mentioned':
                results = sorted(results, key=lambda i: i['mentioned'], reverse=True if sort_order == 'desc' else False)
            elif sort_field == 'prioritization':
                results = sorted(results, key=lambda i: i['prioritization'],
                                 reverse=True if sort_order == 'desc' else False)
            response = {
                "count": news_prioritized_substance_list.count(),
                "results": results
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
            return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_relevant_filtered_news_ids_organization(organization_id, filters):
        organization_relevant_news_ids = {}
        organization_news_qs = DashboardService().get_filtered_news_queryset(filters, organization_id)
        if filters.get('news_source_types', None):
            organization_news_qs = organization_news_qs.filter(
                Q('terms', source__type__id=filters['news_source_types'])
            )
        organization_news_qs = organization_news_qs[0:organization_news_qs.count()]
        for news in organization_news_qs:
            organization_relevant_news_ids[str(news.id)] = True

        return organization_relevant_news_ids

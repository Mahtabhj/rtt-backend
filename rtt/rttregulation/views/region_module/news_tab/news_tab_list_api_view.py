from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.rating_search_service import RatingSearchService
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.services.region_page_services import RegionPageServices

logger = logging.getLogger(__name__)


class NewsTabListData(APIView):
    permission_classes = (IsAuthenticated,)
    rating_service = RatingSearchService()

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
                                                 'regulation name, product name'),
            'sort_order': openapi.Schema(type=openapi.TYPE_STRING, description='Sorting: asc/desc, default is desc.'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='For pagination.Default is 10.'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER),
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
            sort_order = request.data.get('sort_order', 'desc')
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id
            """
            news data
            """
            news_list = []
            news_doc_qs = RegionPageServices().get_filtered_news_queryset(
                organization_id, region_id, filters, search_keyword).source(['id', 'title', 'pub_date',
                                                                             'product_categories',
                                                                             'material_categories'])
            news_doc_qs = news_doc_qs.sort({
                    "news_relevance.relevancy": {
                        "order": sort_order,
                        "nested_path": "news_relevance",
                        "nested_filter": {
                            "term": {
                                "news_relevance.organization.id": organization_id
                            }
                        }
                    }
                }, {"pub_date": {"order": "desc"}})
            count = news_doc_qs.count()
            news_doc_qs = news_doc_qs[skip:skip + limit]
            for news in news_doc_qs:
                news_obj = {
                    'id': news.id,
                    'name': news.title,
                    'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                        organization_id, news.product_categories, serialize=True),
                    'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                        organization_id, news.material_categories, serialize=True),
                    'pub_date': news.pub_date,
                    'impact_rating': self.rating_service.get_news_rating_obj(organization_id, news.id)
                }
                news_list.append(news_obj)
            response = {
                'count': count,
                'results': news_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

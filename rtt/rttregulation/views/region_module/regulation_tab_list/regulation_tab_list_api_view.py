import functools

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
import copy
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.rating_search_service import RatingSearchService
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.services.region_page_services import RegionPageServices

logger = logging.getLogger(__name__)


class RegulationTabListData(APIView):
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
            'sort_field': openapi.Schema(type=openapi.TYPE_STRING, description='sort_field: name/rating'),
        }
    ))
    def post(self, request, region_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1038
        """
        try:
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
            region_id = int(region_id)
            organization_id = request.user.organization_id
            search_keyword = request.data.get('search', None)
            sort_field = request.data.get('sort_field', 'name')
            sort_order = request.data.get('sort_order', 'asc')
            self.sort_order = request.data.get('sort_order', 'asc')
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            regulation_data = []

            """
            framework data
            """
            queryset_framework = RegionPageServices().get_filtered_framework_queryset(
                organization_id, region_id, filters, search_keyword).source(['id', 'name', 'status', 'topics',
                                                                             'product_categories',
                                                                             'material_categories',
                                                                             'regulation_regulatory_framework'])

            if sort_field == 'name':
                if sort_order == 'asc':
                    queryset_framework = queryset_framework.sort('name.raw')
                else:
                    queryset_framework = queryset_framework.sort('-name.raw')
            else:
                queryset_framework = queryset_framework.sort({
                    "regulatory_framework_rating.rating": {
                        "order": sort_order,
                        "nested_path": "regulatory_framework_rating",
                        "nested_filter": {
                            "term": {
                                "regulatory_framework_rating.organization.id": organization_id
                            }
                        }
                    }
                })
            count = queryset_framework.count()
            queryset_framework = queryset_framework[skip: skip + limit]
            for framework in queryset_framework:
                """
                regulations data
                """
                regulations = []
                regulation_filters = copy.deepcopy(filters)
                if not filters.get('related_frameworks', None):
                    regulation_filters['related_frameworks'] = []
                regulation_filters['related_frameworks'].append(framework.id)
                regulation_doc_qs = RegionPageServices().get_filtered_regulation_queryset(
                    organization_id, region_id, regulation_filters, search_keyword).source(['id', 'name', 'status',
                                                                                            'topics',
                                                                                            'material_categories',
                                                                                            'product_categories',
                                                                                            'regulation_rating'])
                if sort_field == 'name':
                    if sort_order == 'asc':
                        regulation_doc_qs = regulation_doc_qs.sort('name.raw')
                    else:
                        regulation_doc_qs = regulation_doc_qs.sort('-name.raw')
                else:
                    regulation_doc_qs = regulation_doc_qs.sort({
                        "regulation_rating.rating": {
                            "order": sort_order,
                            "nested_path": "regulation_rating",
                            "nested_filter": {
                                "term": {
                                    "regulation_rating.organization.id": organization_id
                                }
                            }
                        }
                    })
                regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
                for regulation in regulation_doc_qs:
                    topic_list = []
                    for topic in regulation.topics:
                        topic_list.append({'id': topic.id, 'name': topic.name})
                    regulation_obj = {
                        'id': regulation.id,
                        'name': regulation.name,
                        'status': {'id': regulation.status.id, 'name': regulation.status.name},
                        'topics': topic_list,
                        'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                            organization_id, regulation.product_categories, serialize=True),
                        'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                            organization_id, regulation.material_categories, serialize=True),
                        'impact_rating': self.rating_service.get_regulation_rating_obj(organization_id, regulation.id)
                    }
                    regulations.append(regulation_obj)

                framework_topics = []
                for topic in framework.topics:
                    framework_topics.append({'id': topic.id, 'name': topic.name})
                framework_data = {
                    'id': framework.id,
                    'name': framework.name,
                    'status': {'id': framework.status.id, 'name': framework.status.name},
                    'topics': framework_topics,
                    'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                        organization_id, framework.product_categories, serialize=True),
                    'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                        organization_id, framework.material_categories, serialize=True),
                    'impact_rating': self.rating_service.get_framework_rating_obj(organization_id, framework.id),
                    'regulations': regulations
                }
                regulation_data.append(framework_data)
            response = {
                "count": count,
                "results": regulation_data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

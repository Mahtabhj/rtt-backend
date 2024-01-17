from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
import copy
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.region_page_services import RegionPageServices

logger = logging.getLogger(__name__)


class RegulationTabFilterOption(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
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
    def post(request, region_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1038
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

            topic_list = []
            visited_topics = {}
            status_list = []
            visited_status = {}
            framework_ids = []

            framework_doc_qs = RegionPageServices().get_filtered_framework_queryset(organization_id, region_id, filters,
                                                                                    search_keyword)
            framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
            """filter options from framework"""
            for framework in framework_doc_qs:
                framework_ids.append(framework.id)
                if str(framework.status.id) not in visited_status:
                    status_list.append({'id': framework.status.id, 'name': framework.status.name})
                    visited_status[str(framework.status.id)] = True

                for topic in framework.topics:
                    if str(topic.id) not in visited_topics:
                        topic_list.append({'id': topic.id, 'name': topic.name})
                        visited_topics[str(topic.id)] = True

            """filter options from regulations"""
            regulation_filters = copy.deepcopy(filters)
            if not filters.get('related_frameworks', None):
                regulation_filters['related_frameworks'] = []
            regulation_filters['related_frameworks'].extend(framework_ids)
            regulation_doc_qs = RegionPageServices().get_filtered_regulation_queryset(organization_id, region_id,
                                                                                      regulation_filters,
                                                                                      search_keyword)
            regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]

            for regulation in regulation_doc_qs:
                if str(regulation.status.id) not in visited_status:
                    status_list.append({'id': regulation.status.id, 'name': regulation.status.name})
                    visited_status[str(regulation.status.id)] = True

                for topic in regulation.topics:
                    if topic and str(topic.id) not in visited_topics:
                        topic_list.append({'id': topic.id, 'name': topic.name})
                        visited_topics[str(topic.id)] = True

            response = {
                'status': status_list,
                'topics': topic_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

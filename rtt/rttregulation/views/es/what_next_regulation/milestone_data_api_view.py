from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rttregulation.services.what_next_milestone_service import WhatNextMilestoneService
from rttregulation.services.regulation_tagged_region_service import RegulationTaggedRegionService

logger = logging.getLogger(__name__)


class WhatNextMilestoneAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'period': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='will filter milestones based on years'),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulation ID',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'milestone_types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of milestone_type ID',
                                              items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'product_categories': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product_category ID',
                                                 items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'material_categories': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of material_category ID',
                                                  items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in milestone name and description'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='limit for pagination'),

            'skip': openapi.Schema(type=openapi.TYPE_INTEGER, description='start position for pagination'),
            'related_products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of related_products ID',
                                               items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'status': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of status ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topics ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-707
        """
        try:
            period = str(request.data.get('period', ''))
            filters = {
                'period_start': period + '-01-01' if period else None,
                'period_end': period + '-12-31' if period else None,
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'regulations': request.data.get('regulations', None),
                'milestone_types': request.data.get('milestone_types', None),
                'regions': request.data.get('regions', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'related_products': request.data.get('related_products', None),
                'status': request.data.get('status', None),
                'topics': request.data.get('topics', None)
            }
            organization_id = request.user.organization_id
            search_keyword = request.data.get('search', None)
            limit = int(request.data.get('limit', 10))
            skip = int(request.data.get('skip', 0))
            milestone_doc_queryset = WhatNextMilestoneService().get_what_next_filtered_milestone_document_queryset(
                organization_id, filters, search_keyword)
            milestone_doc_queryset = milestone_doc_queryset[skip:skip + limit]
            results = []
            for milestone in milestone_doc_queryset:
                milestone_type = None
                if milestone.type:
                    milestone_type = {
                        'id': milestone.type.id,
                        'name': milestone.type.name
                    }
                regions = []
                regulation_obj = None
                if milestone.regulation:
                    regulation_obj = {
                        'id': milestone.regulation.id,
                        'name': milestone.regulation.name
                    }
                    if milestone.regulation.regulatory_framework:
                        regions = RegulationTaggedRegionService().get_region_data(
                            milestone.regulation.regulatory_framework.id)
                framework_obj = None
                if milestone.regulatory_framework:
                    framework_obj = {
                        'id': milestone.regulatory_framework.id,
                        'name': milestone.regulatory_framework.name
                    }
                    for region in milestone.regulatory_framework.regions:
                        regions.append({
                            'id': region.id,
                            'name': region.name
                        })
                results.append({
                    'id': milestone.id,
                    'name': milestone.name,
                    'description': milestone.description if milestone.description else '',
                    'regions': regions,
                    'milestone_type': milestone_type,
                    'date': milestone.from_date if milestone.from_date else None,
                    'regulation': regulation_obj,
                    'regulatory_framework': framework_obj,
                    'documents': [{'id': document.id, 'title': document.title} for document in milestone.documents]
                })
            response_data = {
                'count': milestone_doc_queryset.count(),
                'results': results
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

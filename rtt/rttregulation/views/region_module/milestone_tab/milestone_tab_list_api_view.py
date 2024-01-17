from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from rttregulation.services.region_page_services import RegionPageServices

logger = logging.getLogger(__name__)


class MilestoneTablListData(APIView):
    permission_classes = (IsAuthenticated,)
    region_page_service = RegionPageServices()

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
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(self, request, region_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1040
        """
        try:
            region_id = int(region_id)
            organization_id = request.user.organization_id
            upcoming_milestones_list = []
            past_milestones_list = []
            future = timezone.now() + timedelta(days=1)
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
            queryset_milestone = self.region_page_service.get_filtered_milestone_queryset(organization_id, region_id,
                                                                                          filters)
            queryset_milestone = queryset_milestone[0:queryset_milestone.count()]

            for milestone in queryset_milestone:
                regulatory_framework_obj = None
                if milestone.regulatory_framework:
                    regulatory_framework_obj = {
                        'id': milestone.regulatory_framework.id,
                        'name': milestone.regulatory_framework.name
                    }
                regulation_obj = None
                if milestone.regulation:
                    regulation_obj = {
                        'id': milestone.regulation.id,
                        'name': milestone.regulation.name
                    }
                milestone_data = {
                    'id': milestone.id,
                    'name': milestone.name,
                    'date': milestone.from_date,
                    'type': {
                        'id': milestone.type.id,
                        'name': milestone.type.name
                    },
                    'regulatory_framework': regulatory_framework_obj,
                    'regulation': regulation_obj
                }
                if milestone.from_date and milestone.from_date < future:
                    past_milestones_list.append(milestone_data)
                else:
                    upcoming_milestones_list.append(milestone_data)
            response = {
                'upcoming_milestones': sorted(upcoming_milestones_list, key=lambda data: data['date'], reverse=True),
                'past_milestones': sorted(past_milestones_list, key=lambda data: data['date'], reverse=True)
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

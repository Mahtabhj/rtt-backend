import logging
from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.services.system_filter_service import SystemFilterService
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.serializers.serializers import TopicIdNameSerializer, RegionIdNameSerializer
from rttregulation.services.rating_search_service import RatingSearchService
from rttcore.permissions import has_substance_module_permission
from rttregulation.services.regulatory_framework_content_service import RegulatoryFrameworkContentService
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService

logger = logging.getLogger(__name__)


class RegulatoryFrameworkContentGroupByData(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        topics = request.data.get('topics', None)
        regions = request.data.get('regions', None)
        products = request.data.get('product_categories', None)
        materials = request.data.get('material_categories', None)
        group_by_field = request.data.get('group_by_field', None)
        group_by_field_id = request.data.get('group_by_field_id', None)
        limit = request.data.get('limit', 10)
        skip = request.data.get('skip', 0)
        is_muted = request.data.get('is_muted', False)
        frameworks = request.data.get('regulatory_frameworks', None)
        self.organization_id = request.user.organization_id
        substance_module_permission = has_substance_module_permission(self.organization_id)
        if not (group_by_field == 'regions' or group_by_field == 'topics' or group_by_field == 'impact') or \
                not group_by_field_id >= 0:
            return Response({"message": "group_by_field AND group_by_field_id must be sent"},
                            status=status.HTTP_400_BAD_REQUEST)
        framework_list = []

        framework_queryset = RegulatoryFrameworkContentService(
            self.organization_id).get_filtered_regulatory_framework_queryset(topics, products, materials, regions,
                                                                             is_muted, frameworks,
                                                                             apply_regulation_mute=True)
        if group_by_field == 'regions':
            framework_queryset = framework_queryset.filter(
                Q('nested',
                  path='regions',
                  query=Q('match', regions__id=group_by_field_id))
            )
        elif group_by_field == 'topics':
            framework_queryset = framework_queryset.filter(
                Q('nested',
                  path='topics',
                  query=Q('match', topics__id=group_by_field_id))
            )
        else:
            if group_by_field_id == 0:
                framework_queryset = framework_queryset.filter(
                    Q('nested',
                      path='regulatory_framework_rating',
                      query=Q('match', regulatory_framework_rating__organization__id=self.organization_id) &
                            Q('match', regulatory_framework_rating__rating=0)) |
                    ~Q('nested',
                       path='regulatory_framework_rating',
                       query=Q('match', regulatory_framework_rating__organization__id=self.organization_id))
                )
            else:
                framework_queryset = framework_queryset.filter(
                    Q('nested',
                      path='regulatory_framework_rating',
                      query=Q('match', regulatory_framework_rating__organization__id=self.organization_id) &
                            Q('match', regulatory_framework_rating__rating=group_by_field_id))
                )
        framework_queryset = framework_queryset[skip:skip + limit]
        system_filtered_regulation_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(
            self.organization_id, is_muted=is_muted).source(['id']).sort('id')
        system_filtered_regulation_qs = system_filtered_regulation_qs[0:system_filtered_regulation_qs.count()]
        rel_reg_ids = []
        for regulation in system_filtered_regulation_qs:
            rel_reg_ids.append(regulation.id)
        for framework in framework_queryset:
            framework_obj = RegulatoryFrameworkContentService(self.organization_id).get_serialized_framework_object(
                framework, substance_module_permission, rel_reg_ids, is_muted)
            if framework_obj not in framework_list:
                framework_list.append(framework_obj)

        response = {
            'count': framework_queryset.count(),
            'results': framework_list
        }

        return Response(response, status=status.HTTP_200_OK)

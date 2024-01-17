from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status
from elasticsearch_dsl import Q

from rttcore.services.id_search_service import IdSearchService
from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttregulation.services.region_filtered_regulation_queryset_service import RegionFilteredRegulationQuerysetService
from rttlimitManagement.services.additional_attributes_data_service import AdditionalAttributesDataService
from rttlimitManagement.services.exemption_existence_check import ExemptionExistenceCheck
from rttregulation.documents import RegulatoryFrameworkDocument
from rttregulation.services.regulation_tagged_region_service import RegulationTaggedRegionService
from rttsubstance.models import Substance, SubstanceFamily
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService

logger = logging.getLogger(__name__)


class LimitInSubstanceDetails(APIView):
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regions IDs',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Framework IDs',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Regulations IDs',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in substance name, and region name'),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last update from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last update to data(yyyy-mm-dd)'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Last position for pagination'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER, description='First position for pagination')
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-677
        """
        try:
            if not substance_id:
                return Response([], status=status.HTTP_404_NOT_FOUND)
            substance_ids = self.get_family_substance_id(substance_id)
            substance_ids.append(substance_id)
            filters = {
                'substances': substance_ids,
                'regions': request.data.get('regions', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'regulations': request.data.get('regulations', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None)
            }
            organization_id = request.user.organization_id
            search_keyword = request.data.get('search', None)
            limit = int(request.data.get('limit', 10))
            skip = int(request.data.get('skip', 0))
            regulation_substance_limit_qs = LimitCoreService().get_regulation_substance_limit_queryset(
                organization_id, filters)
            if filters.get('regions', None):
                region_tagged_regulation_ids = RegionFilteredRegulationQuerysetService(). \
                    get_region_filtered_regulation_ids(organization_id, region_ids=filters['regions'])
                regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                    # filter by region(framework)
                    Q('nested',
                      path='regulatory_framework.regions',
                      query=Q('terms', regulatory_framework__regions__id=filters['regions'])) |
                    # filter by region_id (using regulation_ids)
                    Q('terms', regulation__id=region_tagged_regulation_ids)
                )
            if search_keyword:
                region_tagged_regulation_ids = RegionFilteredRegulationQuerysetService(). \
                    get_region_filtered_regulation_ids(organization_id, search_keyword=search_keyword)
                regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                    # any keyword. which will be searched in region name(framework)
                    Q('nested',
                      path='regulatory_framework.regions',
                      query=Q('match', regulatory_framework__regions__name=search_keyword)) |
                    # any keyword. which will be searched in region name(regulation) using regulation_ids
                    Q('terms', regulation__id=region_tagged_regulation_ids) |
                    # any keyword. which will be searched in framework name
                    Q('match', regulatory_framework__name=search_keyword) |
                    # any keyword. which will be searched in regulation name
                    Q('match', regulation__name=search_keyword) |
                    # any keyword. which will be searched in scope
                    Q('match', scope=search_keyword)
                )
            regulation_substance_limit_qs = regulation_substance_limit_qs[skip:skip + limit]
            relevant_substance_ids = RelevantSubstanceService().get_organization_relevant_substance_ids(organization_id)
            regulation_limit_list = []
            for limit in regulation_substance_limit_qs:
                if limit.regulatory_framework:
                    limit_obj = self.get_regulation_limit_object(limit, limit.regulatory_framework, is_regulation=False,
                                                                 relevant_substance_ids=relevant_substance_ids)
                    regulation_limit_list.append(limit_obj)
                elif limit.regulation:
                    limit_obj = self.get_regulation_limit_object(limit, limit.regulation, is_regulation=True,
                                                                 relevant_substance_ids=relevant_substance_ids)
                    regulation_limit_list.append(limit_obj)
            response = {
                "count": regulation_substance_limit_qs.count(),
                "results": regulation_limit_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_regulation_limit_object(self, regulation_substance_limit, regulation, is_regulation,
                                    relevant_substance_ids):
        region_list = []
        if not is_regulation:
            for region in regulation.regions:
                region_list.append({
                    'id': region.id,
                    'name': region.name
                })
        if is_regulation and regulation.regulatory_framework:
            region_list = RegulationTaggedRegionService().get_region_data(
                framework_id=regulation.regulatory_framework.id)
        has_exemption = ExemptionExistenceCheck().has_exemption_data(
            regulation.id, is_regulation, substance_id=regulation_substance_limit.substance.id)
        result = {
            'id': regulation.id,
            'name': regulation.name,
            'is_regulation': is_regulation,
            'has_exemption': has_exemption,
            'substance': {
                'id': regulation_substance_limit.substance.id,
                'name': regulation_substance_limit.substance.name,
                'cas_no': regulation_substance_limit.substance.cas_no,
                'ec_no': regulation_substance_limit.substance.ec_no,
                'is_relevant': IdSearchService().does_id_exit_in_sorted_list(
                    relevant_substance_ids, regulation_substance_limit.substance.id)
            },
            'regions': region_list,
            'scope': regulation_substance_limit.scope,
            'limit': regulation_substance_limit.limit_value,
            'limit_unit': regulation_substance_limit.measurement_limit_unit,
            'limit_note': regulation_substance_limit.limit_note,
            'additional_attributes': AdditionalAttributesDataService().get_additional_attributes_data(
                regulation_substance_limit.id, regulation.id, is_regulation)
        }
        return result

    @staticmethod
    def get_family_substance_id(substance_id):
        family_substance_ids = []
        substance_family_qs = SubstanceFamily.objects.filter(substance_id=substance_id)
        for substance_family in substance_family_qs:
            family_substance_ids.append(substance_family.family_id)
        return family_substance_ids

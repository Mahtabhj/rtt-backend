from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status

from rttlimitManagement.services.limit_filter_option_service import LimitFilterOptionService
from rttsubstance.models import SubstanceFamily

logger = logging.getLogger(__name__)


class LimitInSubstanceDetailsFilterOption(APIView):
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regions IDs',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Framework IDs',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulations IDs',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in substance name, scope and region name'),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last update from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last update to data(yyyy-mm-dd)')
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-678
        """
        try:
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
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id

            regulatory_frameworks = []
            visited_regulatory_frameworks = {}
            regulations = []
            visited_regulations = {}
            regions = []
            visited_regions = {}

            regulation_substance_limit_qs = LimitFilterOptionService().get_regulation_region_filter_option(
                organization_id, filters, search_keyword, substance_details_prioritized=True)
            regulation_substance_limit_qs = regulation_substance_limit_qs[0:regulation_substance_limit_qs.count()]
            for limit in regulation_substance_limit_qs:
                if limit.regulatory_framework and str(
                        limit.regulatory_framework.id) not in visited_regulatory_frameworks:
                    regulatory_frameworks.append({
                        'id': limit.regulatory_framework.id,
                        'name': limit.regulatory_framework.name
                    })
                    visited_regulatory_frameworks[str(limit.regulatory_framework.id)] = True
                    for region in limit.regulatory_framework.regions:
                        if str(region.id) not in visited_regions:
                            regions.append({
                                'id': region.id,
                                'name': region.name
                            })
                            visited_regions[str(region.id)] = True
                if limit.regulation and str(limit.regulation.id) not in visited_regulations:
                    regulations.append({
                        'id': limit.regulation.id,
                        'name': limit.regulation.name
                    })
                    visited_regulations[str(limit.regulation.id)] = True
                    if limit.regulation.regulatory_framework:
                        regions_list = LimitFilterOptionService().get_region_data(
                            limit.regulation.regulatory_framework.id, visited_regions)
                        regions.extend(regions_list)
            response = {
                'regions': regions,
                'regulatory_frameworks': regulatory_frameworks,
                'regulations': regulations
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_family_substance_id(substance_id):
        family_substance_ids = []
        substance_family_qs = SubstanceFamily.objects.filter(substance_id=substance_id)
        for substance_family in substance_family_qs:
            family_substance_ids.append(substance_family.family_id)
        return family_substance_ids

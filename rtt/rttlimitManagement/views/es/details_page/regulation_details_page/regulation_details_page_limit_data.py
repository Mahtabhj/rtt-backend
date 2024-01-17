from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status

from rttcore.services.id_search_service import IdSearchService
from rttlimitManagement.services.additional_attributes_data_service import AdditionalAttributesDataService
from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttlimitManagement.services.exemption_existence_check import ExemptionExistenceCheck
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService

logger = logging.getLogger(__name__)


class LimitInRegulationDetails(APIView):
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in substance name, EC_no and CAS_no'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='limit for pagination'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER, description='start position for pagination')
        }
    ))
    def post(self, request, regulation_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-676
        """
        try:
            if not regulation_id:
                return Response([], status=status.HTTP_404_NOT_FOUND)
            filters = {
                'regulations': [regulation_id]
            }
            search_keyword = request.data.get('search', None)
            limit = int(request.data.get('limit', 10))
            skip = int(request.data.get('skip', 0))
            organization_id = request.user.organization_id
            relevant_substance_ids = RelevantSubstanceService().get_organization_relevant_substance_ids(organization_id)

            limit_list = []
            regulation_substance_limit_qs = LimitCoreService().get_regulation_substance_limit_queryset(
                organization_id, filters, search_keyword)
            regulation_substance_limit_qs = regulation_substance_limit_qs[skip:limit+skip]
            for limit in regulation_substance_limit_qs:
                limit_list.append({
                    'has_exemption': ExemptionExistenceCheck().has_exemption_data(regulation_id, is_regulation=True,
                                                                                  substance_id=limit.substance.id),
                    'substance': {
                        'id': limit.substance.id,
                        'name': limit.substance.name,
                        'cas_no': limit.substance.cas_no,
                        'ec_no': limit.substance.ec_no,
                        'is_relevant': IdSearchService().does_id_exit_in_sorted_list(relevant_substance_ids,
                                                                                     limit.substance.id)
                    },
                    'scope': limit.scope,
                    'limit': limit.limit_value,
                    'limit_unit': limit.measurement_limit_unit,
                    'limit_note': limit.limit_note,
                    'additional_attributes': AdditionalAttributesDataService().get_additional_attributes_data(
                        limit.id, regulation_id, is_regulation=True)
                })
            response_data = {
                "count": regulation_substance_limit_qs.count(),
                "results": limit_list
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

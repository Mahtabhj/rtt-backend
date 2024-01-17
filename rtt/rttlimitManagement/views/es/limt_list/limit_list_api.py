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
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttlimitManagement.services.additional_attributes_data_service import AdditionalAttributesDataService
from rttlimitManagement.services.exemption_existence_check import ExemptionExistenceCheck
from rttregulation.documents import RegulationDocument

logger = logging.getLogger(__name__)


class LimitListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'substances': openapi.Schema(type=openapi.TYPE_ARRAY,
                                         description='List of substances IDs',
                                         items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'uses_and_applications': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                    description='List of UseAndApplications IDs',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'framework_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Framework ID'),
            'regulation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Regulations ID'),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in substance name, scope and region name'),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last modified from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last modified to data(yyyy-mm-dd)'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER,
                                    description='Last position for pagination'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER,
                                   description='First position for pagination'),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-634
        """
        try:
            filters = {
                'substances': request.data.get('substances', None),
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None)
            }
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id
            limit = int(request.data.get('limit', 10))
            skip = int(request.data.get('skip', 0))
            framework_id = request.data.get('framework_id', None)
            regulation_id = request.data.get('regulation_id', None)
            if not framework_id and not regulation_id:
                response_msg = {
                    'message': 'Either Regulation_ID or Framework_ID must be sent.'
                }
                return Response(response_msg, status=status.HTTP_400_BAD_REQUEST)
            if framework_id and regulation_id:
                response_msg = {
                    'message': 'Regulation_ID and Framework_ID both can not be sent.'
                }
                return Response(response_msg, status=status.HTTP_400_BAD_REQUEST)
            if framework_id:
                is_regulation = False
                regulation_or_framework_id = framework_id
                filters['regulatory_frameworks'] = [framework_id]
            else:
                is_regulation = True
                regulation_or_framework_id = regulation_id
                filters['regulations'] = [regulation_id]

            '''
            Include family substances limits data also along with filtered substances
            https://chemycal.atlassian.net/browse/RTT-820
            '''
            if filters.get('uses_and_applications', None):
                substances_id = LimitCoreService().get_substances_ids(filters.get('uses_and_applications', None))
                if not filters.get('substances', None):
                    filters['substances'] = []
                filters['substances'] = list(set(filters['substances'] + substances_id))

            if filters.get('substances', None):
                filters['substances'] = LimitCoreService().get_all_substance_family_ids(filters['substances'])

            relevant_substance_ids = RelevantSubstanceService().get_organization_relevant_substance_ids(organization_id)
            substance_limits_list = []
            regulation_substance_limit_qs = LimitCoreService().get_regulation_substance_limit_queryset(
                organization_id, filters)
            if search_keyword:
                search_keyword = search_keyword.lower()
                region_tagged_regulation_ids = self.get_region_regulation_ids(organization_id, search_keyword)
                regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                    # any keyword. which will be searched in substance name
                    Q('wildcard', substance__name='*{}*'.format(search_keyword)) |
                    # any keyword. which will be searched in scope
                    Q('wildcard', scope='*{}*'.format(search_keyword)) |
                    # any keyword. which will be searched in region name(framework)
                    Q('nested',
                      path='regulatory_framework.regions',
                      query=Q('match', regulatory_framework__regions__name=search_keyword)) |
                    # any keyword. which will be searched in region name(regulation) using regulation_ids
                    Q('terms', regulation__id=region_tagged_regulation_ids)
                )
            regulation_substance_limit_qs = regulation_substance_limit_qs[skip:limit + skip]
            for regulation_substance_limit in regulation_substance_limit_qs:
                substance_limits_list.append(self.get_regulation_substance_limit_data(
                    regulation_substance_limit, relevant_substance_ids, regulation_or_framework_id, is_regulation))
            response = {
                'count': regulation_substance_limit_qs.count(),
                'results': substance_limits_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_regulation_substance_limit_data(regulation_substance_limit, relevant_substance_ids, regulation_id,
                                            is_regulation):
        has_exemption = ExemptionExistenceCheck().has_exemption_data(
            regulation_id, is_regulation, substance_id=regulation_substance_limit.substance.id)
        is_relevant = IdSearchService().does_id_exit_in_sorted_list(relevant_substance_ids,
                                                                    regulation_substance_limit.substance.id)
        result = {
            'id': regulation_substance_limit.id,
            'has_exemption': has_exemption,
            'substance': {
                'id': regulation_substance_limit.substance.id,
                'name': regulation_substance_limit.substance.name,
                'cas_no': regulation_substance_limit.substance.cas_no,
                'ec_no': regulation_substance_limit.substance.ec_no,
                'is_relevant': is_relevant
            },
            'scope': regulation_substance_limit.scope,
            'limit': regulation_substance_limit.limit_value,
            'limit_unit': regulation_substance_limit.measurement_limit_unit,
            'limit_note': regulation_substance_limit.limit_note,
            'additional_attributes': AdditionalAttributesDataService().get_additional_attributes_data(
                regulation_substance_limit.id, regulation_id, is_regulation)
        }
        return result

    @staticmethod
    def get_region_regulation_ids(organization_id, search_keyword):
        regulation_ids = []
        regulation_doc: RegulationDocument = LimitCoreService().get_regulation_limit_queryset(organization_id).filter(
            Q('nested',
              path='regulatory_framework.regions',
              query=Q('match', regulatory_framework__regions__name=search_keyword))
        ).source(['id'])
        regulation_doc = regulation_doc[0:regulation_doc.count()]
        for regulation in regulation_doc:
            regulation_ids.append(regulation.id)
        return regulation_ids

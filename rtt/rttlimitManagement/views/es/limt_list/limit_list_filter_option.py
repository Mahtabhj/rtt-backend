from elasticsearch_dsl import Q

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status

from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttlimitManagement.services.limit_filter_option_service import LimitFilterOptionService
from rttsubstance.documents import SubstanceUsesAndApplicationDocument

logger = logging.getLogger(__name__)


class LimitListFilterOption(APIView):
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
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regions IDs',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Framework IDs',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulations IDs',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in substance name, scope and region name'),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last modified from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last modified to data(yyyy-mm-dd)'),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-670
        """
        try:
            filters = {
                'substances': request.data.get('substances', None),
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'regions': request.data.get('regions', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'regulations': request.data.get('regulations', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None)
            }
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id

            if filters.get('uses_and_applications', None):
                substances_id = LimitCoreService().get_substances_ids(filters.get('uses_and_applications', None))
                if not filters.get('substances', None):
                    filters['substances'] = []
                filters['substances'] = list(set(filters['substances'] + substances_id))

            '''
            Include family substances limits data also along with filtered substances
            https://chemycal.atlassian.net/browse/RTT-820
            '''
            if filters.get('substances', None):
                filters['substances'] = LimitCoreService().get_all_substance_family_ids(filters['substances'])

            framework_ids_list = []
            regulation_ids_list = []
            if filters.get('regulatory_frameworks', None) or (not filters.get('regulatory_frameworks', None) and
                                                              not filters.get('regulations', None)):
                framework_doc_qs = LimitCoreService().get_framework_limit_queryset(organization_id, filters,
                                                                                   search_keyword)
                framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
                for framework in framework_doc_qs:
                    if len(framework.regions) > 0:
                        framework_ids_list.append(framework.id)
            if filters.get('regulations', None) or (not filters.get('regulatory_frameworks', None) and
                                                    not filters.get('regulations', None)):
                regulation_doc_qs = LimitCoreService().get_regulation_limit_queryset(organization_id, filters,
                                                                                     search_keyword)
                regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
                for regulation in regulation_doc_qs:
                    if regulation.regulatory_framework and len(regulation.regulatory_framework.regions) > 0:
                        regulation_ids_list.append(regulation.id)

            reg_sub_limit_filters = {
                'substances': filters['substances'],
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None)
            }
            if framework_ids_list:
                reg_sub_limit_filters['regulatory_frameworks'] = framework_ids_list
            if regulation_ids_list:
                reg_sub_limit_filters['regulations'] = regulation_ids_list

            regulatory_frameworks = []
            visited_regulatory_frameworks = {}
            regulations = []
            visited_regulations = {}
            regions = []
            visited_regions = {}

            substances = []
            visited_substances = {}

            regulation_substance_limit_qs = LimitFilterOptionService().get_regulation_region_filter_option(
                organization_id, reg_sub_limit_filters, search_keyword)
            regulation_substance_limit_qs = regulation_substance_limit_qs[0:regulation_substance_limit_qs.count()]
            substance_ids = []
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

                if limit.substance and str(limit.substance.id) not in visited_substances:
                    substances.append({
                        'id': limit.substance.id,
                        'name': limit.substance.name
                    })
                    visited_substances[str(limit.substance.id)] = True
                    substance_ids.append(limit.substance['id'])
            """
            Get uses_and_applications using substance
            """
            uses_and_application_doc_qs = SubstanceUsesAndApplicationDocument().search().filter(
                Q('nested',
                  path='substances',
                  query=Q('terms', substances__id=substance_ids)) &
                Q('match', organization__id=organization_id)
            ).source(['id', 'name'])
            uses_and_application_doc_qs = uses_and_application_doc_qs[0:uses_and_application_doc_qs.count()]
            uses_and_applications = []
            for uses_and_application in uses_and_application_doc_qs:
                uses_and_applications.append({
                    'id': uses_and_application.id,
                    'name': uses_and_application.name,
                })

            response = {
                'regions': regions,
                'regulatory_frameworks': regulatory_frameworks,
                'regulations': regulations,
                'uses_and_applications': uses_and_applications
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

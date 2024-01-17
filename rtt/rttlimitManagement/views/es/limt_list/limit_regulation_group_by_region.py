from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status

from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttlimitManagement.models import LimitAttribute

logger = logging.getLogger(__name__)


class LimitRegulationGroupByRegion(APIView):
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
        doc: https://chemycal.atlassian.net/browse/RTT-634
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

            framework_doc_qs = None
            if filters.get('regulatory_frameworks', None) or (not filters.get('regulatory_frameworks', None) and
                                                              not filters.get('regulations', None)):
                framework_doc_qs = LimitCoreService().get_framework_limit_queryset(organization_id, filters,
                                                                                   search_keyword)
                framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
            regulation_doc_qs = None
            if filters.get('regulations', None) or (not filters.get('regulatory_frameworks', None) and
                                                    not filters.get('regulations', None)):
                regulation_doc_qs = LimitCoreService().get_regulation_limit_queryset(organization_id, filters,
                                                                                     search_keyword)
                regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
            response = []
            visited_region = {}

            '''Framework Data'''
            if framework_doc_qs:
                for framework in framework_doc_qs:
                    regulations_obj = {}
                    if len(framework.regions) > 0:
                        additional_attributes_header_list = self.get_additional_attributes_header_data(
                            framework.id, is_regulation=False)
                        regulations_obj = {
                            'id': framework.id,
                            'name': framework.name,
                            'description': framework.description,
                            'is_regulation': False,
                            'additional_attributes_header': additional_attributes_header_list
                        }
                    for region in framework.regions:
                        if str(region.id) not in visited_region:
                            region_obj = self.get_region_obj(region)
                            visited_region[str(region.id)] = len(response)
                            response.append(region_obj)
                        else:
                            index = visited_region[str(region.id)]
                            response[index]['count'] += 1
                        index = visited_region[str(region.id)]
                        response[index]['regulations'].append(regulations_obj)

            '''Regulation Data'''
            if regulation_doc_qs:
                for regulation in regulation_doc_qs:
                    regulations_obj = {}
                    if regulation.regulatory_framework and len(regulation.regulatory_framework.regions) > 0:
                        additional_attributes_header_list = self.get_additional_attributes_header_data(
                            regulation.id, is_regulation=True)
                        regulations_obj = {
                            'id': regulation.id,
                            'name': regulation.name,
                            'description': regulation.description,
                            'is_regulation': True,
                            'additional_attributes_header': additional_attributes_header_list
                        }
                    for region in regulation.regulatory_framework.regions:
                        if str(region.id) not in visited_region:
                            region_obj = self.get_region_obj(region)
                            visited_region[str(region.id)] = len(response)
                            response.append(region_obj)
                        else:
                            index = visited_region[str(region.id)]
                            response[index]['count'] += 1
                        index = visited_region[str(region.id)]
                        response[index]['regulations'].append(regulations_obj)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_region_obj(region_qs):
        region_obj = {
            'id': region_qs.id,
            'name': region_qs.name,
            'count': 1,
            'regulations': []
        }
        return region_obj

    @staticmethod
    def get_additional_attributes_header_data(regulation_id, is_regulation=False):
        additional_attributes_header_list = []
        if is_regulation:
            limit_attribute_qs = LimitAttribute.objects.filter(regulation_limit_attribute__regulation=regulation_id)
        else:
            limit_attribute_qs = LimitAttribute.objects.filter(
                regulation_limit_attribute__regulatory_framework=regulation_id)
        for limit_attribute in limit_attribute_qs:
            additional_attributes_header_list.append({
                'id': limit_attribute.id,
                'name': limit_attribute.name
            })
        return additional_attributes_header_list

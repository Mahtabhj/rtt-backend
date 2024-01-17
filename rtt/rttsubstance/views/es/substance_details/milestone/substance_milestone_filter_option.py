import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttregulation.documents import RegulatoryFrameworkDocument
from rttsubstance.views.es.substance_details.milestone.filtered_milestone_service import FilteredMilestoneService

logger = logging.getLogger(__name__)


class SubstanceMilestoneFilterOption(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'milestone_types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of milestone_types ID',
                                              items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulations ID',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of frameworks ID',
                                         items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING, description='search key_word in milestone name field'),
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-583
        """
        try:
            filters = {
                'regions': request.data.get('regions', None),
                'milestone_types': request.data.get('milestone_types', None),
                'regulations': request.data.get('regulations', None),
                'frameworks': request.data.get('frameworks', None),
                'search': request.data.get('search', None)
            }
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            milestone_queryset = FilteredMilestoneService().get_filtered_milestone_queryset(filters,
                                                                                            organization_id,
                                                                                            substance_id)
            milestone_queryset = milestone_queryset[0:milestone_queryset.count()]
            regions_list = []
            created_regions_dict = {}
            milestone_types_list = []
            created_milestone_types_dict = {}
            regulations_list = []
            created_regulations_dict = {}
            frameworks_list = []
            frameworks_ids_in_regulation = []
            created_frameworks_dict = {}
            for milestone in milestone_queryset:
                if milestone.regulatory_framework and str(milestone.regulatory_framework.id) \
                        not in created_frameworks_dict:
                    regulatory_framework_obj = {
                        'id': milestone.regulatory_framework.id,
                        'name': milestone.regulatory_framework.name
                    }
                    frameworks_list.append(regulatory_framework_obj)
                    created_frameworks_dict[str(milestone.regulatory_framework.id)] = True

                    for region in milestone.regulatory_framework.regions:
                        if str(region.id) not in created_regions_dict:
                            region_obj = {
                                'id': region.id,
                                'name': region.name
                            }
                            regions_list.append(region_obj)
                            created_regions_dict[str(region.id)] = True

                if milestone.regulation and str(milestone.regulation.id) not in created_regulations_dict:
                    regulation_obj = {
                        'id': milestone.regulation.id,
                        'name': milestone.regulation.name
                    }
                    regulations_list.append(regulation_obj)
                    created_regulations_dict[str(milestone.regulation.id)] = True

                    if milestone.regulation.regulatory_framework and str(milestone.regulation.regulatory_framework.id) \
                            not in created_frameworks_dict:
                        frameworks_ids_in_regulation.append(milestone.regulation.regulatory_framework.id)
                        created_frameworks_dict[str(milestone.regulation.regulatory_framework.id)] = True

                if milestone.type and str(milestone.type.id) not in created_milestone_types_dict:
                    milestone_type_obj = {
                        'id': milestone.type.id,
                        'name': milestone.type.name
                    }
                    milestone_types_list.append(milestone_type_obj)
                    created_milestone_types_dict[str(milestone.type.id)] = True
            framework_doc_queryset = RegulatoryFrameworkDocument.search().filter(
                Q('terms', id=frameworks_ids_in_regulation)
            ).source(['regions'])
            framework_doc_queryset = framework_doc_queryset[0:framework_doc_queryset.count()]
            for framework in framework_doc_queryset:
                for region in framework.regions:
                    if str(region.id) not in created_regions_dict:
                        region_obj = {
                            'id': region.id,
                            'name': region.name
                        }
                        regions_list.append(region_obj)
                        created_regions_dict[str(region.id)] = True
            response = {
                'regions': regions_list,
                'milestone_types': milestone_types_list,
                'regulations': regulations_list,
                'frameworks': frameworks_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

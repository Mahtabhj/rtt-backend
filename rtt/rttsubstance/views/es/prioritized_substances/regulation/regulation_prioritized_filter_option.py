from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttregulation.models.models import Region


class RegulationPrioritizedFilterOptions(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product ID',
                                       items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'uses_and_applications': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                    description='List of uses_and_applications ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topic ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Keyword, which will be searched in name, ec_no and cas_no'),
            'prioritization_strategies': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                        description='List of prioritization_strategies ID',
                                                        items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(self, request):
        try:
            filters = {
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'products': request.data.get('products', None),
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'regions': request.data.get('regions', None),
                'topics': request.data.get('topics', None),
                'prioritization_strategies': request.data.get('prioritization_strategies', None)
            }
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id
            return_data = self.get_filter_options(organization_id, filters, search_keyword)
            return Response(return_data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_filter_options(organization_id, filters, search_keyword):
        substance_queryset = SubstanceCoreService().get_filtered_substance_queryset(organization_id, filters,
                                                                                    search_keyword,
                                                                                    regulation_prioritized=True)
        substance_queryset = substance_queryset[0:substance_queryset.count()]
        related_frameworks_ids = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(
            organization_id)
        related_regulations_ids = RelevantRegulationService().get_relevant_regulation_id_organization(
            organization_id)
        regions_list = []
        topics_list = []
        visited_framework_ids = []
        visited_regulation_ids = []
        framework_ids_in_regulation = set()
        relevant_property_datapoint_ids = set()
        for substance in substance_queryset:
            for substance_property_data_point in substance.substance_property_data_point_relation:
                if substance_property_data_point.property_data_point:
                    relevant_property_datapoint_ids.add(substance_property_data_point.property_data_point.id)
            for framework in substance.substances_regulatory_framework:
                if framework.id not in visited_framework_ids:
                    visited_regulation_ids.append(framework.id)
                    if RelevantRegulationService().is_id_relevant(related_frameworks_ids, framework.id):
                        for region in framework.regions:
                            region_obj = {
                                'id': region.id,
                                'name': region.name
                            }
                            if region_obj not in regions_list:
                                regions_list.append(region_obj)
                        for topic in framework.topics:
                            topic_obj = {
                                'id': topic.id,
                                'name': topic.name
                            }
                            if topic_obj not in topics_list:
                                topics_list.append(topic_obj)
            for regulation in substance.substances_regulation:
                if regulation.id not in visited_regulation_ids:
                    visited_regulation_ids.append(regulation.id)
                    if RelevantRegulationService().is_id_relevant(related_regulations_ids, regulation.id):
                        if regulation.regulatory_framework:
                            framework_ids_in_regulation.add(regulation.regulatory_framework.id)
                        for topic in regulation.topics:
                            topic_obj = {
                                'id': topic.id,
                                'name': topic.name
                            }
                            if topic_obj not in topics_list:
                                topics_list.append(topic_obj)
        framework_ids_in_regulation = list(framework_ids_in_regulation)
        region_queryset = Region.objects.filter(regulatory_framework_region__in=framework_ids_in_regulation). \
            prefetch_related('regulatory_framework_region')
        for region in region_queryset:
            region_obj = {
                'id': region.id,
                'name': region.name
            }
            if region_obj not in regions_list:
                regions_list.append(region_obj)
        prioritization_strategies_list = SubstanceCoreService().get_prioritization_strategies_queryset(
            organization_id, list(relevant_property_datapoint_ids), serializer=True)
        result = {
            "regions": regions_list,
            "topics": topics_list,
            "prioritization_strategies": prioritization_strategies_list,
        }
        return result

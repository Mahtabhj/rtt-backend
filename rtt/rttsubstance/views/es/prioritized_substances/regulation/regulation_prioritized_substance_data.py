from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.dashboard_services import DashboardService


class RegulationPrioritizedAPIView(APIView):
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
            'sort_field': openapi.Schema(type=openapi.TYPE_STRING, enum=['name', 'mentioned', 'prioritization'],
                                         description="Apply sort on 'name', 'mentioned' or 'prioritization' field"),
            'sort_order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'],
                                         description="'asc' to apply Ascending or 'desc' to apply Descending order"),
            'prioritization_strategies': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                        description='List of prioritization_strategies ID',
                                                        items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-635
        """
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
            sort_field = request.data.get('sort_field', 'mentioned').lower()
            sort_order = request.data.get('sort_order', 'desc').lower()
            organization_id = request.user.organization_id
            total_substance_search = SubstanceCoreService().get_filtered_substance_queryset(organization_id,
                                                                                            regulation_prioritized=True,
                                                                                            filters=filters,
                                                                                            search_keyword=search_keyword)
            return_data = {
                "count": total_substance_search.count(),
                "results": self.get_regulation_prioritized_obj(organization_id, filters, search_keyword,  sort_field,
                                                               sort_order)
            }
            return Response(return_data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_regulation_prioritized_obj(self, organization_id, filters, search_keyword, sort_field, sort_order):
        result = []
        related_frameworks_ids = self.get_relevant_filtered_regulatory_framework_ids(organization_id, filters)
        related_regulations_ids = self.get_relevant_filtered_regulation_ids(organization_id, filters)
        name_sort_order = 'asc'
        if sort_field == 'name':
            name_sort_order = sort_order
        substance_queryset = SubstanceCoreService().get_filtered_substance_queryset(organization_id, filters,
                                                                                    search_keyword, sort_field='name',
                                                                                    sort_order=name_sort_order,
                                                                                    regulation_prioritized=True)
        substance_queryset = substance_queryset[0:substance_queryset.count()]
        for substance in substance_queryset:
            mentioned_count = 0
            for framework in substance.substances_regulatory_framework:
                if RelevantRegulationService().is_id_relevant(related_frameworks_ids, framework.id):
                    mentioned_count = mentioned_count + 1
            for regulation in substance.substances_regulation:
                if RelevantRegulationService().is_id_relevant(related_regulations_ids, regulation.id):
                    mentioned_count = mentioned_count + 1
            for milestone in substance.substances_regulation_milestone:
                milestone_framework_id = milestone.regulatory_framework.id
                milestone_regulation_id = milestone.regulation.id
                if milestone_framework_id and RelevantRegulationService().is_id_relevant(related_frameworks_ids,
                                                                                         milestone_framework_id):
                    mentioned_count = mentioned_count + 1
                if milestone_regulation_id and RelevantRegulationService().is_id_relevant(related_regulations_ids,
                                                                                          milestone_regulation_id):
                    mentioned_count = mentioned_count + 1
            substance_obj = {
                'id': substance.id,
                'name': substance.name,
                'mentioned': mentioned_count,
                'prioritization': mentioned_count
            }
            result.append(substance_obj)
        if sort_field in ['mentioned', 'prioritization']:
            result = sorted(result, key=lambda i: i[sort_field], reverse=True if sort_order == 'desc' else False)
        return result

    @staticmethod
    def get_relevant_filtered_regulatory_framework_ids(organization_id, filters):
        relevant_framework_ids_org = []
        organization_framework_qs = DashboardService().get_filtered_regulatory_framework_queryset(
            filters, organization_id).source(['id']).sort('id')
        organization_framework_qs = organization_framework_qs[0:organization_framework_qs.count()]
        for framework in organization_framework_qs:
            relevant_framework_ids_org.append(framework.id)

        return relevant_framework_ids_org

    @staticmethod
    def get_relevant_filtered_regulation_ids(organization_id, filters):
        relevant_regulation_ids_org = []
        organization_regulation_qs = DashboardService().get_filtered_regulation_queryset(
            filters, organization_id).source(['id']).sort('id')
        organization_regulation_qs = organization_regulation_qs[0:organization_regulation_qs.count()]
        for regulation in organization_regulation_qs:
            relevant_regulation_ids_org.append(regulation.id)

        return relevant_regulation_ids_org

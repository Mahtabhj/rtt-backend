from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttcore.services.dashboard_services import DashboardService
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttsubstance.models import Property


class SubstanceRelatedDataAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topic ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-625
        """
        try:
            filters = {
                'regions': request.data.get('regions', None),
                'topics': request.data.get('topics', None)
            }
            organization_id = request.user.organization_id
            substance_doc_qs = SubstanceCoreService().get_filtered_substance_queryset(organization_id,
                                                                                      filters={'id': substance_id})
            if substance_doc_qs.count() is 0:
                return Response({"message": "Invalid Substance ID"}, status=status.HTTP_404_NOT_FOUND)
            substance = None
            for substance_queryset in substance_doc_qs:
                substance = substance_queryset
            return_data = self.get_substance_related_data(organization_id, substance_id, substance, filters)
            return Response(return_data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "An Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)

    def get_substance_related_data(self, organization_id, substance_id, substance, filters):
        related_frameworks_ids = self.get_relevant_filtered_regulatory_framework_ids(organization_id, filters)
        related_regulations_ids = self.get_relevant_filtered_regulation_ids(organization_id, filters)
        result = {
            'ec_no': substance.ec_no,
            'cas_no': substance.cas_no,
            'uses_and_apps': [],
            'related_frameworks': [],
            'related_regulations': [],
            'related_milestones': [],
            'related_products': [],
            'properties': []
        }
        for uses_and_apps in substance.uses_and_application_substances:
            if uses_and_apps.organization.id == organization_id:
                uses_and_apps_obj = {
                    'id': uses_and_apps.id,
                    'name': uses_and_apps.name
                }
                result['uses_and_apps'].append(uses_and_apps_obj)
        for framework in substance.substances_regulatory_framework:
            if RelevantRegulationService().is_id_relevant(related_frameworks_ids, framework.id):
                result['related_frameworks'].append({
                    'id': framework.id,
                    'name': framework.name,
                    'status': framework.status.name
                })
        for regulation in substance.substances_regulation:
            if RelevantRegulationService().is_id_relevant(related_regulations_ids, regulation.id):
                result['related_regulations'].append({
                    'id': regulation.id,
                    'name': regulation.name,
                    'status': regulation.status.name
                })
        for milestone in substance.substances_regulation_milestone:
            if milestone.regulation and RelevantRegulationService().is_id_relevant(
                    related_regulations_ids, milestone.regulation.id):
                result['related_milestones'].append({
                    'id': milestone.regulation.id,
                    'name': milestone.name,
                    'date': milestone.from_date,
                    'is_regulation': True

                })
            elif milestone.regulatory_framework and RelevantRegulationService().is_id_relevant(
                    related_frameworks_ids, milestone.regulatory_framework.id):
                result['related_milestones'].append({
                    'id': milestone.regulatory_framework.id,
                    'name': milestone.name,
                    'date': milestone.from_date,
                    'is_regulation': False

                })
        for product in substance.substances_product:
            if product.organization.id is organization_id:
                result['related_products'].append({
                    'id': product.id,
                    'name': product.name
                })
        property_queryset = Property.objects.filter(
            prioritization_strategy_properties__organization_id=organization_id,
            property_data_property__substance_property_data_point_property_data_point__substance_id=substance_id
        ).distinct().order_by('id')
        for property_qs in property_queryset:
            properties_obj = {
                'id': property_qs.id,
                'name': property_qs.name
            }
            result['properties'].append(properties_obj)

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

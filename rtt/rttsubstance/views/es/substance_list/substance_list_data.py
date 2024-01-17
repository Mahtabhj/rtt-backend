from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService


class SubstanceListApiView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'uses_and_applications': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                    description='List of uses_and_applications ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Product ID',
                                       items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Keyword, which will be searched in name, ec_no and cas_no'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER,
                                    description='The number of rows in a page'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER,
                                   description='Omit a number rows from previous'),
            'sort_field': openapi.Schema(type=openapi.TYPE_STRING, enum=['name'],
                                         description="Apply sort on 'name' field"),
            'sort_order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'],
                                         description="'asc' to apply Ascending or 'desc' to apply Descending order")
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-540
        """
        try:
            filters = {
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'products': request.data.get('products', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None)
            }
            search_keyword = request.data.get('search', None)
            sort_field = request.data.get('sort_field', 'name').lower()
            sort_order = request.data.get('sort_order', 'asc').lower()
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            organization_id = request.user.organization_id
            total_substance_search = SubstanceCoreService().get_filtered_substance_queryset(organization_id, filters,
                                                                                            search_keyword, sort_field,
                                                                                            sort_order)
            return_data = {
                "count": total_substance_search.count(),
                "results": self.get_filtered_substance(organization_id, total_substance_search[skip:limit+skip])
            }
            return Response(return_data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "An Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_filtered_substance(organization_id, substance_doc_qs):
        related_frameworks_ids = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(
            organization_id)
        related_regulations_ids = RelevantRegulationService().get_relevant_regulation_id_organization(organization_id)
        related_milestones_ids = RelevantRegulationService().get_relevant_milestone_id_organization(organization_id)
        results = []
        for substance in substance_doc_qs:
            substance_obj = {
                'id': substance.id,
                'name': substance.name,
                'ec_no': substance.ec_no,
                'cas_no': substance.cas_no,
                'uses_and_apps': [],
                'related_frameworks': [],
                'related_regulations': [],
                'related_milestones': []
            }
            for uses_and_apps in substance.uses_and_application_substances:
                if uses_and_apps.organization.id == organization_id:
                    uses_and_apps_obj = {
                        'id': uses_and_apps.id,
                        'name': uses_and_apps.name
                    }
                    substance_obj['uses_and_apps'].append(uses_and_apps_obj)
            for framework in substance.substances_regulatory_framework:
                if RelevantRegulationService().is_id_relevant(related_frameworks_ids, framework.id):
                    substance_obj['related_frameworks'].append({
                        'id': framework.id,
                        'name': framework.name,
                        'status': framework.status.name
                    })
            for regulation in substance.substances_regulation:
                if RelevantRegulationService().is_id_relevant(related_regulations_ids, regulation.id):
                    substance_obj['related_regulations'].append({
                        'id': regulation.id,
                        'name': regulation.name,
                        'status': regulation.status.name
                    })
            for milestone in substance.substances_regulation_milestone:
                if RelevantRegulationService().is_id_relevant(related_milestones_ids, milestone.id):
                    substance_obj['related_milestones'].append({
                        'id': milestone.regulation.id if milestone.regulation else milestone.regulatory_framework.id,
                        'name': milestone.name,
                        'date': milestone.from_date,
                        'is_regulation': True if milestone.regulation else False

                    })
            results.append(substance_obj)
        return results

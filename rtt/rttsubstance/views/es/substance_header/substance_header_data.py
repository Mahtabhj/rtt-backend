from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.substance_core_service import SubstanceCoreService


class SubstanceHeaderData(APIView):
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
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER,
                                    description='Last substance_uses_and_application position for pagination'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER,
                                   description='First substance_uses_and_application position for pagination'),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-537
        """
        try:
            filters = {
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'products': request.data.get('products', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None)
            }
            organization_id = request.user.organization_id
            total_substance_search = SubstanceCoreService().get_filtered_substance_queryset(organization_id)
            filtered_total_substance_search = SubstanceCoreService().get_filtered_substance_queryset(organization_id,
                                                                                                     filters)
            substance_uses_and_application_qs = SubstanceCoreService().\
                get_filtered_substance_uses_and_application_queryset(organization_id)
            limit = request.data.get('limit', substance_uses_and_application_qs.count())
            skip = request.data.get('skip', 0)
            return_data = {
                "total_substance": total_substance_search.count(),
                "filtered_total_substance": filtered_total_substance_search.count(),
                "total_uses_and_app": substance_uses_and_application_qs.count(),
                "uses_and_apps": []
            }
            substance_uses_and_application_qs = substance_uses_and_application_qs[skip:limit]
            uses_and_apps_list = []
            for substance_uses_and_application in substance_uses_and_application_qs:
                substance_uses_and_application_obj = {
                    "id": substance_uses_and_application.id,
                    "name": substance_uses_and_application.name,
                    "substance_count": len(substance_uses_and_application.substances),
                    "filtered_substance_count": self.get_filtered_substance_count(substance_uses_and_application.id,
                                                                                  request)
                }
                uses_and_apps_list.append(substance_uses_and_application_obj)
            return_data['uses_and_apps'] = uses_and_apps_list
            return Response(return_data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "An Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_filtered_substance_count(uses_and_application_id, request):
        filters = {
            'uses_and_applications': [uses_and_application_id],
            'products': request.data.get('products', None),
            'regulatory_frameworks': request.data.get('regulatory_frameworks', None)
        }
        organization_id = request.user.organization_id
        substance_doc_queryset = SubstanceCoreService().get_filtered_substance_queryset(organization_id, filters)
        return substance_doc_queryset.count()

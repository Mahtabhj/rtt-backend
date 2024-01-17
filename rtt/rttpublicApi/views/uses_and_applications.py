from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rttpublicApi.permissions import IsPublicApiAuthorized
from rttsubstance.services.substance_core_service import SubstanceCoreService


class UsesAndApplicationsApi(APIView):
    permission_classes = [IsPublicApiAuthorized]

    def post(self, request):
        organization_id = request.public_api.get('organization_id', None)
        limit = int(request.data.get('limit', 10))
        skip = int(request.data.get('skip', 0))
        results = []
        uses_app_search = SubstanceCoreService().get_filtered_substance_uses_and_application_queryset(
            organization_id)
        count = uses_app_search.count()
        uses_app_search = uses_app_search[skip:limit + skip]

        for use_app in uses_app_search:
            results.append({
                'id': use_app.id,
                'name': use_app.name
            })
        response_data = {
            'count': count,
            'results': results
        }
        return Response(response_data, status=status.HTTP_200_OK)

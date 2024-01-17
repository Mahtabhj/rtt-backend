from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rttpublicApi.permissions import IsPublicApiAuthorized
from rttsubstance.models import Substance, SubstanceUsesAndApplication


class AddSubstanceApi(APIView):
    permission_classes = [IsPublicApiAuthorized]

    def post(self, request):
        organization_id = request.public_api.get('organization_id', None)
        cas = request.data.get('cas', None)
        ec = request.data.get('ec', None)
        use_and_application = request.data.get('use_and_application', None)

        substance_list = Substance.objects.filter(Q(ec_no=ec) | Q(cas_no=cas)) \
            .filter(ec_no__isnull=False, cas_no__isnull=False)
        uses_app_list = SubstanceUsesAndApplication.objects.filter(id__in=use_and_application,
                                                                   organization_id=organization_id)
        for use_and_application in uses_app_list:
            use_and_application.substances.add(*substance_list)

        results = []
        for substance in substance_list:
            results.append({
                'id': substance.id,
                'name': substance.name
            })
        response_data = {
            'message': '{} substance(s) found by CAS or EC number'.format(substance_list.count()),
            'results': results
        }
        return Response(response_data, status=status.HTTP_200_OK)

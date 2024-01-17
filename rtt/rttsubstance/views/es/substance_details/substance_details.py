from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.models import SubstanceExternalLink
from rttsubstance.services.substance_core_service import SubstanceCoreService


class SubstanceDetailsAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    def get(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-577
        """
        try:
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            substance_queryset = SubstanceCoreService().get_filtered_substance_queryset(organization_id,
                                                                                        filters={"id": substance_id})
            if substance_queryset.count() is 0:
                return Response({"message": "Invalid Substance ID"}, status=status.HTTP_404_NOT_FOUND)
            substance_queryset = substance_queryset[0: substance_queryset.count()]
            substance_qs = None
            for substance in substance_queryset:
                substance_qs = substance
            response = self.get_response_obj(substance_qs, substance_id, organization_id)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_response_obj(queryset, substance_id, organization_id):
        substance_external_link_qs = SubstanceExternalLink.objects.filter(
            substance=substance_id).select_related('external_link')
        external_links_list = []
        for substance_external_link in substance_external_link_qs:
            external_link_obj = {
                'name': substance_external_link.external_link.name,
                'value': substance_external_link.value
            }
            external_links_list.append(external_link_obj)
        result = {
            'name': queryset.name,
            'ec_no': queryset.ec_no,
            'cas_no': queryset.cas_no,
            'image': queryset.image,
            'molecular_formula': queryset.molecular_formula,
            'external_links': external_links_list,
            'uses_and_apps': [{'id': uses_and_app.id, 'name': uses_and_app.name} for uses_and_app in
                              queryset.uses_and_application_substances if
                              uses_and_app.organization.id == organization_id],
            'related_products': [{'id': related_product.id, 'name': related_product.name} for related_product in
                                 queryset.substances_product if related_product.organization.id == organization_id]
        }
        return result

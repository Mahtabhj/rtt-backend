import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.models import SubstanceUsesAndApplication, Substance

logger = logging.getLogger(__name__)


class AddSubstanceManuallyAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule, )

    @staticmethod
    def post(request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-835
        """
        try:
            uses_and_applications = request.data.get('uses_and_applications', None)
            substances = request.data.get('substances', None)
            if not uses_and_applications or not substances:
                return Response({"message": "Both uses_and_applications AND substances have to send"},
                                status=status.HTTP_400_BAD_REQUEST)
            valid_substance_ids = list(Substance.objects.filter(id__in=substances).values_list('id', flat=True))
            organization_id = request.user.organization_id
            use_and_app_count = 0
            for use_and_app in uses_and_applications:
                try:
                    substance_uses_and_application = SubstanceUsesAndApplication.objects.get(
                        id=use_and_app, organization_id=organization_id)
                    substance_uses_and_application.substances.add(*valid_substance_ids)
                    use_and_app_count += 1
                except Exception as exe:
                    logger.error(str(exe), exc_info=True)
            response = {
                'message': f"{len(valid_substance_ids)} substance(s) added in {use_and_app_count} uses and applications"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

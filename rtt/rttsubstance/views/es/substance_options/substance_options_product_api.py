import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttcore.permissions import has_substance_module_permission, IsActiveSubstanceModule

logger = logging.getLogger(__name__)


class SubstanceOptionsProductAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='keyword search in substances name, ec_no and cas_no'),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-618?focusedCommentId=11257
        """
        try:
            organization_id = request.user.organization_id
            substance_module_permission = has_substance_module_permission(organization_id)
            if not substance_module_permission:
                return Response([], status=status.HTTP_200_OK)
            search_keyword = request.data.get('search', None)
            response = []
            # keyword search in substances name, ec_no and cas_no
            if search_keyword:
                organization_substances_qs = SubstanceCoreService().get_filtered_substance_queryset(
                    organization_id, search_keyword=search_keyword)
                for substance in organization_substances_qs:
                    organization_substances_obj = {
                        'id': substance.id,
                        'name': substance.name,
                        'ec_no': substance.ec_no,
                        'cas_no': substance.cas_no
                    }
                    response.append(organization_substances_obj)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

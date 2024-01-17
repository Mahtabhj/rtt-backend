from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsSuperUserOrStaff
from rttlimitManagement.models import RegulationLimitAttribute

logger = logging.getLogger(__name__)


class RegulationLimitAttributeOptionAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)

    @staticmethod
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regulation_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                            description='send regulation or framework id in regulation_id parameter'),
            'is_regulation': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                            description='send true if regulation and false for framework'),
        }
    ))
    def post(request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-933
        """
        try:
            regulation_id = request.data.get('regulation_id', None)
            is_regulation = request.data.get('is_regulation', False)
            if not regulation_id:
                return Response({"message": "regulation_id must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            if is_regulation:
                regulation_limit_attribute_qs = RegulationLimitAttribute.objects.filter(
                    regulation_id=regulation_id).select_related('limit_attribute')
            else:
                regulation_limit_attribute_qs = RegulationLimitAttribute.objects.filter(
                    regulatory_framework=regulation_id).select_related('limit_attribute')
            response = []
            for reg_limit_att in regulation_limit_attribute_qs:
                response.append({
                    'id': reg_limit_att.id,
                    'name': reg_limit_att.limit_attribute.name,
                    'field_type': reg_limit_att.limit_attribute.field_type,
                    'list_values': reg_limit_att.limit_attribute.list_values
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

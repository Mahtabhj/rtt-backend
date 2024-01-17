from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveLimitsManagementModule, IsSuperUserOrStaff
from rttlimitManagement.models import RegulationSubstanceLimit

logger = logging.getLogger(__name__)


class LimitDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff, IsActiveLimitsManagementModule,)

    @staticmethod
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'limits': openapi.Schema(type=openapi.TYPE_ARRAY,
                                     description='List of limit ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'date': openapi.Schema(type=openapi.TYPE_STRING,
                                   description='date to be saved in the selected records'),
        }
    ))
    def post(request):
        try:
            limits = request.data.get('limits', None)
            date = request.data.get('date', None)
            if not limits:
                return Response({"message": "limits must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            if not date:
                return Response({"message": "date must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            successful_operation_count = 0
            for limit_id in limits:
                try:
                    limit_qs = RegulationSubstanceLimit.objects.get(id=limit_id)
                    limit_qs.status = 'deleted'
                    limit_qs.date_into_force = date
                    limit_qs.save()
                    successful_operation_count += 1
                except Exception as exc:
                    logger.error(str(exc), exc_info=True)
            response = {
                'message': f"{successful_operation_count} has been deleted"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.models.models import MilestoneMute

logger = logging.getLogger(__name__)


class MilestoneMuteUnmuteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'is_muted': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                       description='true to make R/FW mute and false to make unmute'),
            'milestone_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='enter milestone id')
        }
    ))
    def post(request, *args, **kwargs):
        try:
            milestone_id = request.data.get('milestone_id', None)
            is_muted = request.data.get('is_muted', False)
            user_id = request.user.id
            organization_id = request.user.organization_id
            if not milestone_id:
                return Response({"message": "milestone_id must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            MilestoneMute.objects.update_or_create(
                organization_id=organization_id, milestone_id=milestone_id,
                defaults={'is_muted': is_muted, 'user_id': user_id}
            )
            action = "muted" if is_muted else "unmuted"
            response = {
                "message": f"Milestone has been {action} successfully"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import logging
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsSuperUserOrStaff
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


class UserPermissionAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff, )

    @staticmethod
    def get(request):
        try:
            content_type_qs = ContentType.objects.filter(Q(permission__user__id=request.user.id) |
                                                         Q(permission__group__user__id=request.user.id)).distinct()
            permission_list = []
            for content_type in content_type_qs:
                permission_list.append(content_type.model)
            return Response(permission_list, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

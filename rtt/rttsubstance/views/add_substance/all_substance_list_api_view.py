import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttsubstance.services.all_substance_list_service import AllSubstanceListService
from rttcore.permissions import IsActiveSubstanceModule, IsSuperUserOrStaff

logger = logging.getLogger(__name__)


class AllSubstanceList(APIView):
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
        doc: https://chemycal.atlassian.net/browse/RTT-835?focusedCommentId=12041
        """
        try:
            search_keyword = request.data.get('search', None)
            if not search_keyword or len(search_keyword) < 4:
                return Response([], status=status.HTTP_200_OK)
            response = AllSubstanceListService.get_all_substance_list(search_keyword)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminAllSubstanceList(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='keyword search in substances name, ec_no and cas_no'),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-996
        """
        try:
            search_keyword = request.data.get('search', None)
            limit = request.data.get('limit', 100)
            skip = request.data.get('skip', 0)
            if not search_keyword or len(search_keyword) < 4:
                return Response([], status=status.HTTP_200_OK)
            response = AllSubstanceListService.get_all_substance_list(search_keyword, limit, skip)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

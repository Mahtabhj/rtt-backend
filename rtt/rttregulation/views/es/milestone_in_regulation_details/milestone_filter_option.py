from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from rttcore.services.system_filter_service import SystemFilterService
from rttregulation.documents import MilestoneDocument
from rttregulation.models.models import RegulationMilestone

logger = logging.getLogger(__name__)


class MilestoneInRegulationDetailsFilterOption(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regulation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Regulation ID or Framework ID', ),
            'types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of milestone_type IDs',
                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'is_regulation': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true if regulation_id and false '
                                                                                   'otherwise', ),
            'search': openapi.Schema(type=openapi.TYPE_STRING, description='search by milestone name', ),
            'is_muted': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true if muted and false otherwise', ),
        }
    ))
    def post(self, request):
        try:
            organization_id = request.user.organization_id
            regulation_id = request.data.get('regulation_id', None)
            types = request.data.get('types', None)
            search_keyword = request.data.get('search', None)
            is_muted = request.data.get('is_muted', False)
            if not regulation_id:
                return Response({"message": "regulation_id can not be set empty"}, status=status.HTTP_400_BAD_REQUEST)
            milestone_doc_qs = SystemFilterService().get_system_filtered_milestone_document_queryset(
                organization_id, is_muted)
            if request.data.get('is_regulation', False):
                # filter by regulation
                milestone_doc_qs = milestone_doc_qs.filter('match', regulation__id=regulation_id)
            else:
                # filter by regulatory_framework
                milestone_doc_qs = milestone_doc_qs.filter('match', regulatory_framework__id=regulation_id)
            if types:
                milestone_doc_qs = milestone_doc_qs.filter('terms', type__id=types)
            # search by milestone name, description
            if search_keyword:
                """doc: https://chemycal.atlassian.net/browse/RTT-1090 """
                milestone_id_list = list(RegulationMilestone.objects.filter(
                    Q(name__icontains=search_keyword) | Q(description__icontains=search_keyword)).values_list(
                    'id', flat=True))
                milestone_doc_qs = milestone_doc_qs.query('terms', id=milestone_id_list)
            milestone_doc_qs = milestone_doc_qs[0:milestone_doc_qs.count()]
            visited_type_id = {}
            response = []
            for milestone in milestone_doc_qs:
                if str(milestone.type.id) not in visited_type_id:
                    response.append({
                        'id': milestone.type.id,
                        'name': milestone.type.name
                    })
                    visited_type_id[str(milestone.type.id)] = True
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

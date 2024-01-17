from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from rttcore.permissions import has_substance_module_permission
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttcore.services.system_filter_service import SystemFilterService

from rttregulation.models.models import RegulationMilestone

logger = logging.getLogger(__name__)


class MilestoneInRegulationDetails(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regulation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Regulation ID or Framework ID', ),
            'types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of milestone_type IDs',
                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'is_regulation': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true if regulation_id and false '
                                                                                   'otherwise', ),
            'search': openapi.Schema(type=openapi.TYPE_STRING, description='search by milestone name',),
            'is_muted': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true if muted and false otherwise', ),
        }
    ))
    def post(self, request):
        try:
            regulation_id = request.data.get('regulation_id', None)
            types = request.data.get('types', None)
            search_keyword = request.data.get('search', None)
            is_muted = request.data.get('is_muted', False)
            if not regulation_id:
                return Response({"message": "regulation_id can not be set empty"}, status=status.HTTP_400_BAD_REQUEST)

            organization_id = request.user.organization_id
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
            upcoming_milestones_list = []
            past_milestones_list = []
            substance_module_permission = has_substance_module_permission(organization_id)
            future = timezone.now() + timedelta(days=1)

            for milestone in milestone_doc_qs:
                documents_list = []
                for document in milestone.documents:
                    documents_list.append({
                        'id': document.id,
                        'title': document.title,
                        'description': document.description,
                        'attachment': document.attachment
                    })
                milestone_obj = {
                    'id': milestone.id,
                    'name': milestone.name,
                    'date': milestone.from_date,
                    'type': {
                        'id': milestone.type.id,
                        'name': milestone.type.name
                    },
                    'description': milestone.description,
                    'documents': documents_list,
                    'urls': [{'id': url.id, 'text': url.text, 'description': url.description}
                             for url in milestone.urls],
                    'substance_count': RelevantSubstanceService().get_organization_relevant_substance_data(
                        organization_id, data_name='milestone', data_id=milestone.id, only_my_org=False).count()
                    if substance_module_permission else 0,
                    'is_muted': is_muted,
                }
                if milestone.from_date and milestone.from_date < future:
                    past_milestones_list.append(milestone_obj)
                else:
                    upcoming_milestones_list.append(milestone_obj)
            response = {
                'upcoming_milestones': sorted(upcoming_milestones_list, key=lambda data: data['date'], reverse=True),
                'past_milestones': sorted(past_milestones_list, key=lambda data: data['date'], reverse=True)
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

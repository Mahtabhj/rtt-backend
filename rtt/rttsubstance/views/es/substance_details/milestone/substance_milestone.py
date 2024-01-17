from django.utils import timezone
import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttregulation.documents import RegulatoryFrameworkDocument
from rttregulation.serializers.serializers import RegionIdNameSerializer
from rttsubstance.views.es.substance_details.milestone.filtered_milestone_service import FilteredMilestoneService

logger = logging.getLogger(__name__)


class SubstanceMilestoneAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'milestone_types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of milestone_types ID',
                                              items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulations ID',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of frameworks ID',
                                         items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING, description='search key_word in milestone name field'),
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-583
        """
        try:
            filters = {
                'regions': request.data.get('regions', None),
                'milestone_types': request.data.get('milestone_types', None),
                'regulations': request.data.get('regulations', None),
                'frameworks': request.data.get('frameworks', None),
                'search': request.data.get('search', None)
            }
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            milestone_queryset = FilteredMilestoneService().get_filtered_milestone_queryset(filters,
                                                                                            organization_id,
                                                                                            substance_id)
            milestone_queryset = milestone_queryset[0:milestone_queryset.count()]
            upcoming_milestones_list = []
            past_milestones_list = []
            for milestone in milestone_queryset:
                milestone_data = self.get_milestone_date(milestone)
                from_date = milestone_data['date'] if milestone_data['date'] else None
                if from_date and milestone_data['date'] > timezone.now():
                    upcoming_milestones_list.append(milestone_data)
                else:
                    past_milestones_list.append(milestone_data)
            response = {
                'upcoming_milestones': upcoming_milestones_list,
                'past_milestones': past_milestones_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_milestone_date(self, milestone):
        result = {
            'id': milestone.id,
            'name': milestone.name,
            'description': milestone.description,
            'date': milestone.from_date,
            'type': {
                'id': milestone.type.id,
                'name': milestone.type.name
            },
            'documents': [{'title': document.title, 'link': document.attachment}
                          for document in milestone.documents],
            'urls': [{'id': url.id, 'title': url.description, 'link': url.text} for url in milestone.urls],
            'regions': RegionIdNameSerializer(milestone.regulatory_framework.regions, many=True).data
            if milestone.regulatory_framework else self.get_regions_obj(milestone.regulation.regulatory_framework.id),
            'frameworks': [],
            'regulations': []
        }
        frameworks_list = []
        regulations_list = []
        if milestone.regulatory_framework:
            frameworks_list.append({'id': milestone.regulatory_framework.id,
                                    'name': milestone.regulatory_framework.name})
        if milestone.regulation:
            regulations_list.append({'id': milestone.regulation.id, 'name': milestone.regulation.name})
            if milestone.regulation.regulatory_framework:
                frameworks_list.append({'id': milestone.regulation.regulatory_framework.id,
                                        'name': milestone.regulation.regulatory_framework.name})
        result['frameworks'] = frameworks_list
        result['regulations'] = regulations_list
        return result

    @staticmethod
    def get_regions_obj(framework_id):
        regions_list = []
        framework_doc_queryset = RegulatoryFrameworkDocument.search().filter(
            Q('match', id=framework_id)
        ).source(['regions'])
        framework_doc_queryset = framework_doc_queryset[0:framework_doc_queryset.count()]
        for framework in framework_doc_queryset:
            for region in framework.regions:
                region_obj = {
                    'id': region.id,
                    'name': region.name
                }
                regions_list.append(region_obj)
        return regions_list

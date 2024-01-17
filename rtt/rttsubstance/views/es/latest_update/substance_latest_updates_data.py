from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.utils import timezone
from datetime import timedelta
import pytz
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttcore.services.system_filter_service import SystemFilterService
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttcore.services.dashboard_services import DashboardService


utc = pytz.UTC


class SubstanceLatestUpdatesMilestoneAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'uses_and_applications': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                    description='List of uses_and_applications ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product ID',
                                       items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topic ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last mentioned from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last mentioned to data(yyyy-mm-dd)'),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='search for news, framework and regulation'),
        }
    ))
    def post(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1454
        """
        try:
            substance_filters = {
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'products': request.data.get('products', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None)
            }
            filters = {
                'regions': request.data.get('regions', None),
                'topics': request.data.get('topics', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'search': request.data.get('search', None)
            }
            organization_id = request.user.organization_id
            substance_queryset = SubstanceCoreService().get_filtered_substance_queryset(
                organization_id, filters=substance_filters).source(['id'])
            substance_queryset = substance_queryset[0:substance_queryset.count()]
            substance_ids = []
            for substance in substance_queryset:
                substance_ids.append(substance.id)

            upcoming_milestones_list = []
            past_milestones_list = []
            future = timezone.now() + timedelta(days=1)
            milestone_doc_qs = self.get_milestone_doc_qs(filters, organization_id, substance_ids)
            milestone_doc_qs = milestone_doc_qs[0: milestone_doc_qs.count()]
            for milestone in milestone_doc_qs:
                regulatory_framework_obj = None
                if milestone.regulatory_framework:
                    regulatory_framework_obj = {
                        'id': milestone.regulatory_framework.id,
                        'name': milestone.regulatory_framework.name
                    }
                regulation_obj = None
                if milestone.regulation:
                    regulation_obj = {
                        'id': milestone.regulation.id,
                        'name': milestone.regulation.name
                    }
                milestone_data = {
                    'id': milestone.id,
                    'name': milestone.name,
                    'date': milestone.from_date,
                    'type': {
                        'id': milestone.type.id,
                        'name': milestone.type.name
                    },
                    'regulatory_framework': regulatory_framework_obj,
                    'regulation': regulation_obj
                }
                if milestone.from_date and milestone.from_date < future:
                    past_milestones_list.append(milestone_data)
                else:
                    upcoming_milestones_list.append(milestone_data)
            response = {
                'upcoming_milestones': sorted(upcoming_milestones_list, key=lambda data: data['date'], reverse=True),
                'past_milestones': sorted(past_milestones_list, key=lambda data: data['date'], reverse=True)
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_milestone_doc_qs(self, filters, organization_id, substance_ids):
        milestone_doc_qs = SystemFilterService().get_system_filtered_milestone_document_queryset(organization_id)
        framework_ids = self.get_framework_id_list(filters, organization_id, substance_ids)
        regulation_ids = self.get_regulation_id_list(filters, organization_id, substance_ids)
        # filter by regulation/framework
        milestone_doc_qs = milestone_doc_qs.filter(
            # related framework for system filter
            Q('terms', regulatory_framework__id=framework_ids) |
            # related regulation for system filter
            Q('terms', regulation__id=regulation_ids)
        )
        return milestone_doc_qs

    @staticmethod
    def get_framework_id_list(filters, organization_id, substance_ids):
        result = []
        queryset_regulatory = DashboardService().get_filtered_regulatory_framework_queryset(
            filters, organization_id).filter(
            Q('nested',
              path='substances',
              query=Q('terms', substances__id=substance_ids)) &
            Q('nested',
              path='regulatory_framework_milestone',
              query=Q('exists', field="regulatory_framework_milestone.id"))).source(['id'])
        queryset_regulatory = queryset_regulatory[0:queryset_regulatory.count()]
        for regulatory in queryset_regulatory:
            result.append(regulatory.id)
        return result

    @staticmethod
    def get_regulation_id_list(filters, organization_id, substance_ids):
        result = []
        queryset_regulation = DashboardService().get_filtered_regulation_queryset(filters, organization_id).filter(
            Q('nested',
              path='substances',
              query=Q('terms', substances__id=substance_ids)) |
            Q('nested',
              path='regulatory_framework.substances',
              query=Q('terms', regulatory_framework__substances__id=substance_ids))
        )
        queryset_regulation = queryset_regulation.filter(Q('nested', path='regulation_milestone',
                                                           query=Q('exists', field="regulation_milestone.id")))
        queryset_regulation = queryset_regulation[0:queryset_regulation.count()]
        for regulation in queryset_regulation:
            result.append(regulation.id)
        return result

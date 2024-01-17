from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import copy
import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.substance_details_filter_service import SubstanceDetailsFilterService
from rttregulation.services.relevant_topic_service import RelevantTopicService
from rttcore.services.id_search_service import IdSearchService


class SubstanceDetailsRegulationsFilterOptions(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news topic type ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'status': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of status ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='search for framework and regulation'),
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-581
        """
        try:
            filters = {
                'regions': request.data.get('regions', None),
                'topics': request.data.get('topics', None),
                'status': request.data.get('status', None)
            }
            search_keyword = request.data.get('search', None)
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            regions_list = []
            created_regions_dict = {}
            topics_list = []
            created_topics_dict = {}
            statuses_list = []
            created_statuses_dict = {}
            framework_id_list = []
            relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)
            """
            framework data
            """
            framework_doc_qs = SubstanceDetailsFilterService().get_filtered_framework_doc_queryset(
                organization_id, substance_id, filters, search_keyword)
            framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
            for framework in framework_doc_qs:
                framework_id_list.append(framework.id)
                for region in framework.regions:
                    self.assign_data(created_data_dict=created_regions_dict, data_list=regions_list, queryset=region)
                for topic in framework.topics:
                    if IdSearchService().does_id_exit_in_sorted_list(relevant_topics_ids, topic.id):
                        self.assign_data(created_data_dict=created_topics_dict, data_list=topics_list, queryset=topic)
                if framework.status:
                    self.assign_data(created_data_dict=created_statuses_dict, data_list=statuses_list,
                                     queryset=framework.status)

            if len(framework_id_list) > 0:
                """
                regulation data
                """
                regulation_filters = copy.deepcopy(filters)
                regulation_filters['related_frameworks'] = framework_id_list
                regulation_doc_qs = SubstanceDetailsFilterService().get_filtered_regulation_doc_queryset(
                    organization_id, substance_id, regulation_filters, search_keyword)
                regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
                for regulation in regulation_doc_qs:
                    if regulation.regulatory_framework:
                        for region in regulation.regulatory_framework.regions:
                            self.assign_data(created_data_dict=created_regions_dict, data_list=regions_list,
                                             queryset=region)
                    for topic in regulation.topics:
                        if IdSearchService().does_id_exit_in_sorted_list(relevant_topics_ids, topic.id):
                            self.assign_data(created_data_dict=created_topics_dict, data_list=topics_list,
                                             queryset=topic)
                    if regulation.status:
                        self.assign_data(created_data_dict=created_statuses_dict, data_list=statuses_list,
                                         queryset=regulation.status)
            response = {
                'regions': regions_list,
                'topics': topics_list,
                'statuses': statuses_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logging.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def assign_data(self, created_data_dict, data_list, queryset):
        if str(queryset.id) not in created_data_dict:
            region_obj = self.get_data_obj(queryset)
            data_list.append(region_obj)
            created_data_dict[str(queryset.id)] = True

    @staticmethod
    def get_data_obj(queryset):
        data_obj = {
            'id': queryset.id,
            'name': queryset.name
        }
        return data_obj

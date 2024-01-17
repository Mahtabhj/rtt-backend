from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttcore.services.system_filter_service import SystemFilterService
from rttregulation.services.relevant_topic_service import RelevantTopicService


class SubstanceRegionTopicChart(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    def get(self, request, substance_id):
        try:
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            regions_list = []
            topics_list = []
            created_regions_ids = {}
            created_topics_ids = {}
            relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)
            """
            news data
            """
            queryset_news = SystemFilterService().get_system_filtered_news_document_queryset(organization_id).filter(
                # news tagged to substance
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id)))
            queryset_news = queryset_news[0:queryset_news.count()]
            for news in queryset_news:
                for region in news.regions:
                    self.assign_data(data_id=region.id, data_name=region.name, created_data_ids=created_regions_ids,
                                     data_list=regions_list, field_name='news', field_id=news.id)
                for news_category in news.news_categories:
                    if news_category.topic and news_category.topic.id in relevant_topics_ids:
                        topic = news_category.topic
                        self.assign_data(data_id=topic.id, data_name=topic.name, created_data_ids=created_topics_ids,
                                         data_list=topics_list, field_name='news',
                                         field_id=news.id)
            """
            regulation data
            """
            queryset_regulation = SystemFilterService().get_system_filtered_regulation_document_queryset(
                organization_id).filter(
                # milestones of regulation to which the substance is tagged
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id)) |
                # milestones to which the substance is tagged
                Q('nested',
                  path='regulation_milestone.substances',
                  query=Q('match', regulation_milestone__substances__id=substance_id)))
            queryset_regulation = queryset_regulation[0:queryset_regulation.count()]
            for regulation in queryset_regulation:
                for region in regulation.regulatory_framework.regions:
                    self.assign_data(data_id=region.id, data_name=region.name, created_data_ids=created_regions_ids,
                                     data_list=regions_list, field_name='regulations',
                                     field_id=regulation.id)

                for topic in regulation.topics:
                    if topic.id in relevant_topics_ids:
                        self.assign_data(data_id=topic.id, data_name=topic.name, created_data_ids=created_topics_ids,
                                         data_list=topics_list, field_name='regulations',
                                         field_id=regulation.id)
            """
            framework data
            """
            queryset_framework = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
                organization_id).filter(
                # milestones of regulatory frameworks to which the milestone is tagged
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id)) |
                # milestones to which the substance is tagged
                Q('nested',
                  path='regulatory_framework_milestone.substances',
                  query=Q('match', regulatory_framework_milestone__substances__id=substance_id)))
            queryset_framework = queryset_framework[0:queryset_framework.count()]
            for framework in queryset_framework:
                for region in framework.regions:
                    self.assign_data(data_id=region.id, data_name=region.name, created_data_ids=created_regions_ids,
                                     data_list=regions_list, field_name='frameworks',
                                     field_id=framework.id)
                for topic in framework.topics:
                    if topic.id in relevant_topics_ids:
                        self.assign_data(data_id=topic.id, data_name=topic.name, created_data_ids=created_topics_ids,
                                         data_list=topics_list, field_name='frameworks',
                                         field_id=framework.id)
            response = {
                'regions': regions_list,
                'topics': topics_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def assign_data(self, data_id, data_name, created_data_ids, data_list, field_name, field_id):
        """
        [01]. At first we check data is created or not.
        [02]. If data is not found then we create data_structure, and assign the data into the data_list. Then create
         created_data_ids dictionary where key is the data_id and value is the data's index in the data_list.
        [03]. Then using the created_data_ids dictionary we find the index and update information in that index.
        """
        if str(data_id) not in created_data_ids:
            data_structure = self.create_data_structure(data_id, data_name)
            data_list.append(data_structure)
            created_data_ids[str(data_id)] = len(data_list) - 1
        data_idx = created_data_ids[str(data_id)]
        data_list[data_idx][field_name]['selected_ids'].append(field_id)

    @staticmethod
    def create_data_structure(data_id, data_name):
        data_structure = {
            'id': data_id,
            'title': data_name,
            'news': {
                'selected_ids': []
            },
            'regulations': {
                'selected_ids': []
            },
            'frameworks': {
                'selected_ids': []
            }
        }
        return data_structure

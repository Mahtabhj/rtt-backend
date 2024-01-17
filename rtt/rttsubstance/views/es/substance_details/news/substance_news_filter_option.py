from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttcore.services.dashboard_services import DashboardService
from rttregulation.services.relevant_topic_service import RelevantTopicService


class SubstanceNewsFilterOptions(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news topic type ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'source_types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news source type ID',
                                           items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING, description='search key_word in news_title'),
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-582
        """
        try:
            filters = {
                'regions': request.data.get('regions', None),
                'topics': request.data.get('topics', None),
                'source_types': request.data.get('source_types', None),
                'search': request.data.get('search', None)
            }
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)
            regions_list = []
            visited_regions_dict = {}
            topics_list = []
            visited_topics_dict = {}
            news_source_types_list = []
            visited_news_source_types_dict = {}
            queryset_news = DashboardService().get_filtered_news_queryset(filters, organization_id).filter(
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id))
            ).sort('-pub_date')
            if filters.get('source_types', None):
                queryset_news = queryset_news.filter(
                    Q('terms', source__type__id=filters['source_types'])
                )
            queryset_news = queryset_news[0:queryset_news.count()]
            for news in queryset_news:
                for region in news.regions:
                    if str(region.id) not in visited_regions_dict:
                        region_obj = {
                            'id': region.id,
                            'name': region.name
                        }
                        regions_list.append(region_obj)
                        visited_regions_dict[str(region.id)] = True
                for news_category in news.news_categories:
                    if news_category.topic and news_category.topic.id in relevant_topics_ids:
                        if str(news_category.topic.id) not in visited_topics_dict:
                            topic_obj = {
                                'id': news_category.topic.id,
                                'name': news_category.topic.name
                            }
                            topics_list.append(topic_obj)
                            visited_topics_dict[str(news_category.topic.id)] = True
                if news.source.type:
                    if str(news.source.type.id) not in visited_news_source_types_dict:
                        source_type_obj = {
                            'id': news.source.type.id,
                            'name': news.source.type.name
                        }
                        news_source_types_list.append(source_type_obj)
                        visited_news_source_types_dict[str(news.source.type.id)] = True
            response = {
                'regions': regions_list,
                'topics': topics_list,
                'source_types': news_source_types_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

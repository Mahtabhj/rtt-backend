from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import pytz
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttcore.services.dashboard_services import DashboardService
from rttregulation.services.relevant_topic_service import RelevantTopicService

utc = pytz.UTC


class SubstanceLatestUpdatesFilterOptions(APIView):
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
    def post(self, request, tab_name, *args, **kwargs):
        try:
            """
            doc: https://chemycal.atlassian.net/browse/RTT-650
            """
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
            regions_list = []
            topics_list = []
            relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)
            if tab_name == "news":
                """
                news data
                """
                queryset_news = DashboardService().get_filtered_news_queryset(filters, organization_id).filter(
                    Q('nested',
                      path='substances',
                      query=Q('terms', substances__id=substance_ids)))
                queryset_news = queryset_news[0:queryset_news.count()]
                for news in queryset_news:
                    for region in news.regions:
                        region_obj = {
                            'id': region.id,
                            'name': region.name
                        }
                        if region_obj not in regions_list:
                            regions_list.append(region_obj)
                    for news_category in news.news_categories:
                        if news_category.topic and news_category.topic.id in relevant_topics_ids:
                            topic_obj = {
                                'id': news_category.topic.id,
                                'name': news_category.topic.name
                            }
                            if topic_obj not in topics_list:
                                topics_list.append(topic_obj)
            else:
                """
                regulatory framework data
                """
                queryset_regulatory = DashboardService().get_filtered_regulatory_framework_queryset(filters,
                                                                                                    organization_id).filter(
                    Q('nested',
                      path='substances',
                      query=Q('terms', substances__id=substance_ids)) &
                    Q('nested',
                      path='regulatory_framework_milestone',
                      query=Q('exists', field="regulatory_framework_milestone.id"))).sort(
                    '-regulatory_framework_milestone.from_date')
                queryset_regulatory = queryset_regulatory[0:queryset_regulatory.count()]
                for framework in queryset_regulatory:
                    for region in framework.regions:
                        region_obj = {
                            'id': region.id,
                            'name': region.name
                        }
                        if region_obj not in regions_list:
                            regions_list.append(region_obj)
                    for topic in framework.topics:
                        if topic.id in relevant_topics_ids:
                            topic_obj = {
                                'id': topic.id,
                                'name': topic.name
                            }
                            if topic_obj not in topics_list:
                                topics_list.append(topic_obj)
                """
                regulation data
                """
                queryset_regulation = DashboardService().get_filtered_regulation_queryset(filters, organization_id).filter(
                    Q('nested',
                      path='substances',
                      query=Q('terms', substances__id=substance_ids)) |
                    Q('nested',
                      path='regulatory_framework.substances',
                      query=Q('terms', regulatory_framework__substances__id=substance_ids))
                ).sort('-regulation_milestone.from_date')
                queryset_regulation = queryset_regulation.filter(Q('nested',
                                                                   path='regulation_milestone',
                                                                   query=Q('exists', field="regulation_milestone.id")))
                queryset_regulation = queryset_regulation[0:queryset_regulation.count()]
                for regulation in queryset_regulation:
                    if regulation.regulatory_framework:
                        for region in regulation.regulatory_framework.regions:
                            region_obj = {
                                'id': region.id,
                                'name': region.name
                            }
                            if region_obj not in regions_list:
                                regions_list.append(region_obj)
                    for topic in regulation.topics:
                        if topic.id in relevant_topics_ids:
                            topic_obj = {
                                'id': topic.id,
                                'name': topic.name
                            }
                            if topic_obj not in topics_list:
                                topics_list.append(topic_obj)
            response = {
                'regions': regions_list,
                'topics': topics_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

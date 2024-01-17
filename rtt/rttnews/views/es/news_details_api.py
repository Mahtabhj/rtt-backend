from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.services.system_filter_service import SystemFilterService
from rttnews.documents import NewsDocument
from rttnews.models.models import News
from rttnews.services.news_search_service import NewsSearchService
from rttcore.permissions import has_substance_module_permission
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService


class NewsDetailsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    news_search_service = NewsSearchService()

    def get(self, request, news_id):
        organization_id = request.user.organization_id
        news_queryset = SystemFilterService().get_system_filtered_news_document_queryset(
            organization_id).filter('match', id=news_id)

        news_details = {}
        for news in news_queryset:
            news_details = self.news_search_service.get_news_object_by_qs(news, organization_id, distinct_item=False)
            news_id = news.id

        if not news_details:
            return Response(status=status.HTTP_204_NO_CONTENT)

        substance_module_permission = has_substance_module_permission(organization_id)
        substance_count = RelevantSubstanceService().get_organization_relevant_substance_data(
            organization_id, data_name='news', data_id=news_id, serializer=False, only_my_org=False).count()
        news_details['substance_count'] = substance_count if substance_module_permission else []
        return Response(news_details, status=status.HTTP_200_OK)


class RelatedNewsListApiView(APIView):
    permission_classes = (IsAuthenticated,)
    news_search_service = NewsSearchService()

    def get(self, request, news_id):
        organization_id = request.user.organization_id
        news_queryset = SystemFilterService().get_system_filtered_news_document_queryset(
            organization_id).filter('match', id=news_id)
        if not news_queryset:
            return Response(status=status.HTTP_204_NO_CONTENT)
        news_category_list = []
        for news in news_queryset:
            for news_categories in news.news_categories:
                news_category_list.append(news_categories.id)
        related_news = SystemFilterService().get_system_filtered_news_document_queryset(
            organization_id).filter(~Q('match', id=news_id)).filter(
            'nested',
            path='news_categories',
            query=Q('terms', news_categories__id=news_category_list)
        ).sort('-pub_date')
        result = []
        for news in related_news:
            result.append(self.news_search_service.get_news_object_by_qs(news, organization_id))
        return Response(result, status=status.HTTP_200_OK)

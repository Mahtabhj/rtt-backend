from django.conf import settings
from django.core.cache import cache as django_cache

from rttcore.services.system_filter_service import SystemFilterService


class RelevantNewsService:

    def __init__(self):
        # cache timeout in seconds
        self.django_cache_timeout = settings.DJANGO_CACHE_TIMEOUT

    def get_organization_relevant_news_ids(self, organization_id):
        """
            params:
            organization_id : int

            Return a list of relevant_news_ids of an organization in ascending order
        """

        '''
        check in django_cache
        '''
        cache_data = django_cache.get('organization_relevant_news_ids_{}'.format(organization_id))
        if cache_data:
            return cache_data

        organization_relevant_news_ids = []
        organization_news_qs = SystemFilterService() \
            .get_system_filtered_news_document_queryset(organization_id) \
            .sort('id')
        organization_news_qs = organization_news_qs[0:organization_news_qs.count()]
        for news in organization_news_qs:
            organization_relevant_news_ids.append(news.id)

        '''
        set data into django cache
        '''
        django_cache.set('organization_relevant_news_ids_{}'.format(organization_id),
                         organization_relevant_news_ids,
                         self.django_cache_timeout)

        return organization_relevant_news_ids

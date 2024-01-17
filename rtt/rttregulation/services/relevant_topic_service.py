from django.conf import settings
from django.core.cache import cache as django_cache

from rttregulation.models.core_models import Topic


class RelevantTopicService:

    def __init__(self):
        # cache timeout in seconds
        self.django_cache_timeout = settings.DJANGO_CACHE_TIMEOUT

    def get_relevant_topic_id_organization(self, organization_id):
        """
            params:
            organization_id : user organization_id (int)

            Return a list of relevant_topic_ids of an organization in ascending order
        """
        '''
        check in django_cache
        '''
        cache_data = django_cache.get('relevant_topic_id_organization_{}'.format(organization_id))
        # print('relevant_topic_ids_org_cache: ', cache_data)
        if cache_data:
            return cache_data

        relevant_topic_id_organization = []
        topic_queryset = Topic.objects.filter(
            industry_topics__organization_industries__id=organization_id).order_by('id')
        for topic in topic_queryset:
            relevant_topic_id_organization.append(topic.id)
        '''
        set data into django cache
        '''
        django_cache.set('relevant_topic_id_organization_{}'.format(organization_id),
                         relevant_topic_id_organization,
                         self.django_cache_timeout)

        return relevant_topic_id_organization

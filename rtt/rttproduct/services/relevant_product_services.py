from django.conf import settings
from django.core.cache import cache as django_cache

from rttproduct.documents import ProductDocument


class RelevantProductService:

    def __init__(self):
        # cache timeout in seconds
        self.django_cache_timeout = settings.DJANGO_CACHE_TIMEOUT

    def get_organization_relevant_product_ids(self, organization_id):
        """
            params:
            organization_id : int

            Return a list of relevant_product_ids of an organization in ascending order
        """

        '''
        check in django_cache
        '''
        cache_data = django_cache.get('organization_relevant_product_ids_{}'.format(organization_id))
        if cache_data:
            return cache_data

        organization_relevant_product_ids = []
        product_queryset = ProductDocument.search().filter('match', organization__id=organization_id).sort('id')
        product_queryset = product_queryset[0:product_queryset.count()]
        for product in product_queryset:
            organization_relevant_product_ids.append(product.id)

        '''
        set data into django cache
        '''
        django_cache.set('organization_relevant_product_ids_{}'.format(organization_id),
                         organization_relevant_product_ids,
                         self.django_cache_timeout)

        return organization_relevant_product_ids

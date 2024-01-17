from rttcore.services.system_filter_service import SystemFilterService
from django.conf import settings
from django.core.cache import cache as django_cache


class RelevantRegulationService:

    def __init__(self):
        # cache timeout in seconds
        self.django_cache_timeout = settings.DJANGO_CACHE_TIMEOUT

    def get_relevant_regulation_id_organization(self, organization_id):
        """
            params:
            organization_id : user organization_id (int)

            Return a list of relevant_regulation_ids of an organization sorted in ascending order
        """

        '''
        check in django_cache
        '''
        cache_data = django_cache.get('relevant_regulation_id_organization_{}'.format(organization_id))
        # print('relevant_regulation_id_org_cache: ', cache_data)
        if cache_data:
            return cache_data

        relevant_regulation_id_organization = []
        organization_regulation_qs = SystemFilterService().\
            get_system_filtered_regulation_document_queryset(organization_id).source(['id']).sort('id')
        organization_regulation_qs = organization_regulation_qs[0:organization_regulation_qs.count()]
        for organization_regulation in organization_regulation_qs:
            relevant_regulation_id_organization.append(organization_regulation.id)

        '''
        set data into django cache
        '''
        django_cache.set('relevant_regulation_id_organization_{}'.format(organization_id),
                         relevant_regulation_id_organization,
                         self.django_cache_timeout)

        return relevant_regulation_id_organization

    def get_relevant_regulatory_framework_id_organization(self, organization_id):
        """
            params:
            organization_id : user organization_id (int)

            Return a list of regulatory_framework_ids of an organization sorted in ascending order
        """

        '''
        check in django_cache
        '''
        cache_data = django_cache.get('relevant_regulatory_framework_id_organization{}'.format(organization_id))
        # print('relevant_regulatory_framework_id_org_cache: ', cache_data)
        if cache_data:
            return cache_data

        relevant_regulatory_framework_id_organization = []
        organization_regulatory_framework_qs = SystemFilterService().\
            get_system_filtered_regulatory_framework_queryset(organization_id).source(['id']).sort('id')
        organization_regulatory_framework_qs = \
            organization_regulatory_framework_qs[0:organization_regulatory_framework_qs.count()]
        for organization_regulatory_framework in organization_regulatory_framework_qs:
            relevant_regulatory_framework_id_organization.append(organization_regulatory_framework.id)

        '''
        set data into django cache
        '''
        django_cache.set('relevant_regulatory_framework_id_organization{}'.format(organization_id),
                         relevant_regulatory_framework_id_organization,
                         self.django_cache_timeout)

        return relevant_regulatory_framework_id_organization

    @staticmethod
    def is_id_relevant(relevant_ids_list, key_id):
        """
        This function will receive a list as 1st parameter(sorted in ascending order) and an integer value as
        2nd parameter. This function will check whether the integer is present in the list or not. If the value is in
        the list then the function will return true and false otherwise.

        This function is based on 'binary search' algorithm, where:
            [01]. The list must be sorted in ascending order.
            [02]. Time complexity is: O(log n)

        How Binary search algo works:
            Binary search is an efficient algorithm for finding an item from a sorted list of items.
        It works by repeatedly dividing in half the portion of the list that could contain the item,
        until you've narrowed down the possible locations to just one.
        For more info: https://www.khanacademy.org/computing/computer-science/algorithms/binary-search/a/binary-search
        """
        low = 0
        high = len(relevant_ids_list) - 1
        while low <= high:
            mid = (high + low) // 2
            # If key_id is greater, ignore left half
            if relevant_ids_list[mid] < key_id:
                low = mid + 1
            # If key_id is smaller, ignore right half
            elif relevant_ids_list[mid] > key_id:
                high = mid - 1
            # means key_id is present
            else:
                return True

        # If we reach here, then the element was not present
        return False

    def get_relevant_milestone_id_organization(self, organization_id):
        """
            params:
            organization_id : user organization_id (int)

            Return a list of milestone_ids of an organization sorted in ascending order
        """

        '''
        check in django_cache
        '''
        cache_data = django_cache.get('relevant_milestone_id_organization{}'.format(organization_id))
        # print('relevant_milestone_id_org_cache: ', cache_data)
        if cache_data:
            return cache_data

        relevant_milestone_id_organization = []
        organization_milestone_qs = SystemFilterService().\
            get_system_filtered_milestone_document_queryset(organization_id).source(['id']).sort('id')
        organization_milestone_qs = organization_milestone_qs[0:organization_milestone_qs.count()]
        for organization_milestone in organization_milestone_qs:
            relevant_milestone_id_organization.append(organization_milestone.id)

        '''
        set data into django cache
        '''
        django_cache.set('relevant_milestone_id_organization{}'.format(organization_id),
                         relevant_milestone_id_organization,
                         self.django_cache_timeout)

        return relevant_milestone_id_organization

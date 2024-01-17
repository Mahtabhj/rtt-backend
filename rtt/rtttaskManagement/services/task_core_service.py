from elasticsearch_dsl import Q

from rtttaskManagement.documents import TaskDocument


class TaskCoreService:
    """
    This service is for prepare task list according to organization and apply filter.
    """

    @staticmethod
    def get_filtered_task_queryset(organization_id, filters=None, search_keyword=None):
        """
        :param int organization_id: Required. user organization_id(int).
        :param str search_keyword: optional. any keyword. which will be searched in name, ec_no and cas_no
        :param dict filters: optional. Additional filter options. Sample filters dict:
                        filters = {
                           'id': int or None,
                           'status': string or None,
                           'assignee': list object or None,
                           'products': list object or None,
                           'regulatory_frameworks': list object or None,
                           'regulations': list object or None,
                           'news': list object or None,
                           'from_date': date string (yyyy-mm-dd),
                           'to_date': date string (yyyy-mm-dd),
                           'is_archive': send is_archive data if True and False otherwise,
                        }
        """
        '''
        filter task which is relevant for organization
        '''
        task_search: TaskDocument = TaskDocument.search().filter(
            'match', created_by__organization__id=organization_id
        )

        '''filter by search_keyword'''
        if search_keyword:
            task_search = task_search.filter(
                # any keyword. which will be searched in task_name
                Q('match', name=search_keyword) |
                # any keyword. which will be searched in task description
                Q('match', description=search_keyword) |
                # any keyword. which will be searched in first_name of the assignee
                Q('match', assignee__first_name=search_keyword) |
                # any keyword. which will be searched in last_name of the assignee
                Q('match', assignee__last_name=search_keyword) |
                # any keyword. which will be searched in product_name
                Q('nested',
                  path='products',
                  query=Q('match', products__name=search_keyword)) |
                Q('nested',
                  path='substances',
                  query=Q('match', substances__name=search_keyword))
            )

        if filters is None:
            return task_search

        '''
        filters
        https://chemycal.atlassian.net/browse/RTT-606
        https://chemycal.atlassian.net/browse/RTT-604
        '''

        if filters.get('id', None):
            task_search = task_search.filter('match', id=filters['id'])

        if filters.get('status', None):
            task_search = task_search.filter('match', status=filters['status'])

        if filters.get('is_archive', None):
            task_search = task_search.filter('match', is_archive=filters['is_archive'])
        else:
            task_search = task_search.filter('match', is_archive=False)

        if filters.get('assignee', None):
            task_search = task_search.filter(
                'terms', assignee__id=filters['assignee']
            )

        if filters.get('products', None):
            task_search = task_search.filter(
                Q('nested',
                  path='products',
                  query=Q('terms', products__id=filters['products']))
            )

        if filters.get('regulatory_frameworks', None):
            task_search = task_search.filter(
                Q('nested',
                  path='regulatory_frameworks',
                  query=Q('terms', regulatory_frameworks__id=filters['regulatory_frameworks']))
            )

        if filters.get('regulations', None):
            task_search = task_search.filter(
                Q('nested',
                  path='regulations',
                  query=Q('terms', regulations__id=filters['regulations']))
            )

        if filters.get('news', None):
            task_search = task_search.filter(
                Q('nested',
                  path='news',
                  query=Q('terms', news__id=filters['news']))
            )

        if filters.get('from_date', None) and filters.get('to_date', None):
            from_date = filters['from_date']
            to_date = filters['to_date']
            task_search = task_search.filter(
                'range', due_date={'gte': from_date, 'lte': to_date}
            )

        if filters.get('substances', None):
            task_search = task_search.filter(
                Q('nested',
                  path='substances',
                  query=Q('terms', substances__id=filters['substances']))
            )

        return task_search

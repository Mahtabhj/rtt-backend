from elasticsearch_dsl import Q

from rttcore.services.system_filter_service import SystemFilterService


class SubstanceDetailsFilterService:

    def get_filtered_framework_doc_queryset(self, organization_id, substance_id, filters=None, search_keyword=None):
        """
        apply system filters
        """
        regulation_doc_qs = self.get_filtered_regulation_doc_queryset(organization_id, substance_id, filters,
                                                                      search_keyword)
        regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
        relevant_reg_id_list = []
        for regulation in regulation_doc_qs:
            relevant_reg_id_list.append(regulation.id)

        framework_doc_qs = SystemFilterService().get_system_filtered_regulatory_framework_queryset(organization_id)
        framework_doc_qs = framework_doc_qs.filter(
            # Frameworks relevant to the organization which are tagged to the substance
            Q('nested',
              path='substances',
              query=Q('match', substances__id=substance_id)) |
            # regulation relevant to the organization which are tagged to the substance
            Q('nested',
              path='regulation_regulatory_framework',
              query=Q('terms', regulation_regulatory_framework__id=relevant_reg_id_list))
        )
        '''
        user custom filters
        '''
        # search keyword in framework and regulation name
        if search_keyword:
            framework_doc_qs = framework_doc_qs.filter(
                # search on framework_name
                Q('match', name=search_keyword) |
                # search on regulation_name
                Q('nested',
                  path='regulation_regulatory_framework',
                  query=Q('terms', regulation_regulatory_framework__id=relevant_reg_id_list))
            )

        # filter by topics
        if filters.get('topics', None):
            framework_doc_qs = framework_doc_qs.filter(
                # topic filter on framework
                Q('nested',
                  path='topics',
                  query=Q('terms', topics__id=filters['topics'])) |
                # topic filter on regulation
                Q('nested',
                  path='regulation_regulatory_framework',
                  query=Q('terms', regulation_regulatory_framework__id=relevant_reg_id_list))
            )

        # filter by region
        if filters.get('regions', None):
            framework_doc_qs = framework_doc_qs.filter(
                Q('nested',
                  path='regions',
                  query=Q('terms', regions__id=filters['regions']))
            )

        # filter by status
        if filters.get('status', None):
            framework_doc_qs = framework_doc_qs.filter(
                # status filter on framework
                Q('terms', status__id=filters['status']) |
                # status filter on regulation
                Q('nested',
                  path='regulation_regulatory_framework',
                  query=Q('terms', regulation_regulatory_framework__id=relevant_reg_id_list))
            )

        return framework_doc_qs

    @staticmethod
    def get_filtered_regulation_doc_queryset(organization_id, substance_id, filters=None, search_keyword=None):
        """
        apply system filters
        """
        regulation_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(organization_id)

        regulation_doc_qs = regulation_doc_qs.filter(
            # Regulations relevant to the organization which are tagged to the substance
            Q('nested',
              path='substances',
              query=Q('match', substances__id=substance_id))
        )

        '''
        user custom filters
        '''
        # search keyword in regulation name
        if search_keyword:
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('match', name=search_keyword)
            )

        # filter by related regulatory_framework
        if filters.get('related_frameworks', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                'terms', regulatory_framework__id=filters['related_frameworks']
            )

        # filter by topic
        if filters.get('topics', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='topics',
                  query=Q('terms', topics__id=filters['topics']))
            )

        # filter by region
        if filters.get('regions', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('terms', regulatory_framework__regions__id=filters['regions']))
            )

        # filter by status
        if filters.get('status', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('terms', status__id=filters['status'])
            )

        return regulation_doc_qs

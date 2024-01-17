from datetime import datetime
from elasticsearch_dsl import Q
from rttcore.services.system_filter_service import SystemFilterService
from rttlimitManagement.documents import RegulationSubstanceLimitDocument
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttsubstance.models import SubstanceFamily, Substance


class LimitCoreService:
    """
    This service is for prepare Limit list according to an organization and apply filter.
        filters = {
          'substances': list object or None,
          'regions'': list object or None,
          'regulatory_frameworks': list object or None,
          'regulations': list object or None,
          'from_date': date string (yyyy-mm-dd),
          'to_date': date string (yyyy-mm-dd)
        }
    """

    @staticmethod
    def get_regulation_limit_queryset(organization_id, filters=None, search_keyword=None):
        """
        This function will return regulation_queryset that has at least one RegulationSubstanceLimit
        :param int organization_id: Required. user organization_id(int)
        :param dict filters: optional. Additional filter options, Sample filters' dict is given above
        :param str search_keyword: optional. any keyword. which will be searched in substance name,
        scope and region name
        """

        '''Fetch regulation_queryset where at least one RegulationSubstanceLimit is exist'''
        regulation_queryset = SystemFilterService().get_system_filtered_regulation_document_queryset(
            organization_id).filter(
            Q('nested',
              path='regulation_regulation_substance_limit',
              query=Q('exists', field='regulation_regulation_substance_limit'))
        ).filter('match', publish_limit_data=True).filter(
            Q('nested',
              path='regulation_regulation_substance_limit',
              query=Q('match', regulation_regulation_substance_limit__status='active'))
        )

        '''keyword search in substances name'''
        if search_keyword:
            search_keyword = search_keyword.lower()
            regulation_queryset = regulation_queryset.filter(
                # any keyword. which will be searched in substance name and limit with active status
                Q('nested',
                  path='regulation_regulation_substance_limit',
                  query=Q('wildcard',
                          regulation_regulation_substance_limit__substance__name='*{}*'.format(search_keyword)) & Q(
                      'match', regulation_regulation_substance_limit__status='active')) |
                # any keyword. which will be searched in scope and limit with active status
                Q('nested',
                  path='regulation_regulation_substance_limit',
                  query=Q('wildcard', regulation_regulation_substance_limit__scope='*{}*'.format(search_keyword)) & Q(
                      'match', regulation_regulation_substance_limit__status='active')) |
                # any keyword. which will be searched in region name
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('match', regulatory_framework__regions__name=search_keyword))
            )

        '''If filter dict is empty, queryset will be returned here'''
        if filters is None:
            return regulation_queryset

        '''Filter by regulations'''
        if filters.get('regulations', None):
            regulation_queryset = regulation_queryset.filter(
                Q('terms', id=filters['regulations'])
            )

        '''Filter by regions'''
        if filters.get('regions', None):
            regulation_queryset = regulation_queryset.filter(
                'nested',
                path='regulatory_framework.regions',
                query=Q('terms', regulatory_framework__regions__id=filters['regions'])
            )

        '''Filter by substance'''
        if filters.get('substances', None):
            regulation_queryset = regulation_queryset.filter(
                'nested',
                path='regulation_regulation_substance_limit',
                query=Q('terms', regulation_regulation_substance_limit__substance__id=filters['substances'])
            )

        '''Filter by from_date & to_date in between a RegulationSubstanceLimit was modified'''
        if filters.get('from_date', None) and not filters.get('to_date', None):
            filters['to_date'] = datetime.now().date()
        if filters.get('from_date', None) and filters.get('to_date', None):
            regulation_queryset = regulation_queryset.filter(
                Q('nested',
                  path='regulation_regulation_substance_limit',
                  query=Q('range',
                          regulation_regulation_substance_limit__modified={'gte': filters['from_date'],
                                                                           'lte': filters['to_date']}))
            )

        return regulation_queryset

    @staticmethod
    def get_framework_limit_queryset(organization_id, filters=None, search_keyword=None):
        """
        This function will return framework_queryset that has at least one RegulationSubstanceLimit
        :param int organization_id: Required. user organization_id(int)
        :param dict filters: optional. Additional filter options, Sample filters' dict is given above
        :param str search_keyword: optional. any keyword. which will be searched in substance name,
        scope and region name
        """

        '''Fetch framework_queryset where at least one RegulationSubstanceLimit is exist'''
        framework_queryset = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            organization_id).filter(
            Q('nested',
              path='regulatory_framework_regulation_substance_limit',
              query=Q('exists', field='regulatory_framework_regulation_substance_limit'))
        ).filter('match', publish_limit_data=True).filter(
            Q('nested',
              path='regulatory_framework_regulation_substance_limit',
              query=Q('match', regulatory_framework_regulation_substance_limit__status='active'))
        )

        '''keyword search in substances name'''
        if search_keyword:
            search_keyword = search_keyword.lower()
            framework_queryset = framework_queryset.filter(
                # any keyword. which will be searched in substance name and limit with active status
                Q('nested',
                  path='regulatory_framework_regulation_substance_limit',
                  query=Q('wildcard', regulatory_framework_regulation_substance_limit__substance__name='*{}*'.format(
                      search_keyword)) & Q('match', regulatory_framework_regulation_substance_limit__status='active')
                  ) |
                # any keyword. which will be searched in scope and limit with active status
                Q('nested',
                  path='regulatory_framework_regulation_substance_limit',
                  query=Q('wildcard',
                          regulatory_framework_regulation_substance_limit__scope='*{}*'.format(search_keyword)) & Q(
                      'match', regulatory_framework_regulation_substance_limit__status='active')
                  ) |
                # any keyword. which will be searched in region name
                Q('nested',
                  path='regions',
                  query=Q('match', regions__name=search_keyword))
            )

        '''If filter dict is empty, queryset will be returned here'''
        if filters is None:
            return framework_queryset

        '''Filter by regulatory_frameworks'''
        if filters.get('regulatory_frameworks', None):
            framework_queryset = framework_queryset.filter(
                Q('terms', id=filters['regulatory_frameworks'])
            )

        '''Filter by regions'''
        if filters.get('regions', None):
            framework_queryset = framework_queryset.filter(
                'nested',
                path='regions',
                query=Q('terms', regions__id=filters['regions'])
            )

        '''Filter by substance'''
        if filters.get('substances', None):
            framework_queryset = framework_queryset.filter(
                'nested',
                path='regulatory_framework_regulation_substance_limit',
                query=Q('terms', regulatory_framework_regulation_substance_limit__substance__id=filters['substances'])
            )

        '''Filter by from_date & to_date in between a RegulationSubstanceLimit was modified'''
        if filters.get('from_date', None) and not filters.get('to_date', None):
            filters['to_date'] = datetime.now().date()
        if filters.get('from_date', None) and filters.get('to_date', None):
            framework_queryset = framework_queryset.filter(
                Q('nested',
                  path='regulatory_framework_regulation_substance_limit',
                  query=Q('range',
                          regulatory_framework_regulation_substance_limit__modified={'gte': filters['from_date'],
                                                                                     'lte': filters['to_date']}))
            )

        return framework_queryset

    @staticmethod
    def get_regulation_substance_limit_queryset(organization_id, filters=None, search_keyword=None,
                                                exclude_deleted: bool = True):
        """
        :param int organization_id: Required. user organization_id(int)
        :param dict filters: optional. Additional filter options, Sample filters'
                filters = {
                    'regulatory_frameworks': list object or None,
                    'regulations': list object or None,
                    'substances': list object or None,
                    'material_categories': list object or None,
                    'product_categories': list object or None,
                    'from_date': date string (yyyy-mm-dd),
                    'to_date': date string (yyyy-mm-dd)
                }
        :param str search_keyword: optional. any keyword. which will be searched in substance name, CAS, EC
        :param str exclude_deleted: bool optional. if True deleted status limit will be included.
        """
        regulation_substance_limit_qs: RegulationSubstanceLimitDocument = RegulationSubstanceLimitDocument().search()

        '''Filter by relevant frameworks and regulations'''
        relevant_framework_ids = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(
            organization_id)
        relevant_regulation_ids = RelevantRegulationService().get_relevant_regulation_id_organization(organization_id)
        regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
            # relevant frameworks
            Q('terms', regulatory_framework__id=relevant_framework_ids) |
            # relevant regulations
            Q('terms', regulation__id=relevant_regulation_ids)
        ).filter(
            Q('match', regulatory_framework__publish_limit_data=True) |
            Q('match', regulation__publish_limit_data=True)
        )
        if exclude_deleted:
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter('match', status='active')

        '''keyword search in substances name, CAS, EC'''
        if search_keyword:
            search_keyword = search_keyword.lower()
            regulation_substance_limit_qs = regulation_substance_limit_qs.query(
                # any keyword. which will be searched in substance name
                Q('wildcard', substance__name='*{}*'.format(search_keyword)) |
                # any keyword. which will be searched in substance CAS
                Q('match', substance__cas_no=search_keyword) |
                # any keyword. which will be searched in substance ES
                Q('match', substance__ec_no=search_keyword)
            ).sort("_score")

        '''If filter dict is empty, queryset will be returned here'''
        if filters is None:
            return regulation_substance_limit_qs

        '''Filter by substances'''
        if filters.get('substances', None):
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                Q('terms', substance__id=filters['substances'])
            )

        '''Filter by material_categories'''
        if filters.get('material_categories', None):
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                Q('nested',
                  path='regulatory_framework.material_categories',
                  query=Q('terms', regulatory_framework__material_categories__id=filters['material_categories'])) |
                Q('nested',
                  path='regulation.material_categories',
                  query=Q('terms', regulation__material_categories__id=filters['material_categories']))
            )

        '''Filter by product_categories'''
        if filters.get('product_categories', None):
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                Q('nested',
                  path='regulatory_framework.product_categories',
                  query=Q('terms', regulatory_framework__product_categories__id=filters['product_categories'])) |
                Q('nested',
                  path='regulation.product_categories',
                  query=Q('terms', regulation__product_categories__id=filters['product_categories']))
            )

        '''Filter by regulatory_frameworks and regulations'''
        if filters.get('regulatory_frameworks', None) and filters.get('regulations', None):
            # If regulatory_frameworks and regulations both filter are given then applying OR condition
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                Q('terms', regulatory_framework__id=filters['regulatory_frameworks']) |
                Q('terms', regulation__id=filters['regulations'])
            )
        if filters.get('regulatory_frameworks', None) and not filters.get('regulations', None):
            # If only regulatory_frameworks filter is given then applying regulatory_frameworks filter
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                Q('terms', regulatory_framework__id=filters['regulatory_frameworks'])
            )
        if not filters.get('regulatory_frameworks', None) and filters.get('regulations', None):
            # If only regulations filter is given then applying regulations filter
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                Q('terms', regulation__id=filters['regulations'])
            )

        '''Filter by from_date & to_date in between a RegulationSubstanceLimit was modified'''
        if filters.get('from_date', None) and not filters.get('to_date', None):
            filters['to_date'] = datetime.now().date()
        if filters.get('from_date', None):
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                Q('range', modified={'gte': filters['from_date'], 'lte': filters['to_date']})
            )

        return regulation_substance_limit_qs

    @staticmethod
    def get_all_substance_family_ids(substance_id_list):
        substance_family_qs = SubstanceFamily.objects.filter(substance_id__in=substance_id_list)
        for substance_family in substance_family_qs:
            substance_id_list.append(substance_family.family_id)
        return substance_id_list

    @staticmethod
    def get_substances_ids(uses_and_application_id_list):
        substance_id_list = list(Substance.objects.filter(
            uses_and_application_substances__id__in=uses_and_application_id_list).values_list('id', flat=True))
        return substance_id_list

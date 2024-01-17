from elasticsearch_dsl import Q

from rttnews.services.relevant_news_service import RelevantNewsService
from rttregulation.documents import MilestoneDocument, RegulationDocument
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttsubstance.documents import SubstanceDocument, SubstanceUsesAndApplicationDocument
from rttsubstance.models import PropertyDataPoint, SubstancePropertyDataPoint, PrioritizationStrategy, \
    SubstanceUsesAndApplication


class SubstanceCoreService:
    """
       This service is for prepare substance list according to an organization and apply filter.
       Or send all substances and apply filter when only_my_org is False
       """

    @staticmethod
    def get_filtered_substance_queryset(organization_id, filters=None, search_keyword=None,
                                        sort_field='name', sort_order='asc',
                                        regulation_prioritized=False, news_prioritized=False,
                                        property_prioritized=False, only_my_org=True,
                                        product_detail_page=False):
        """
        :param int organization_id: Required. user organization_id(int).
        :param str search_keyword: optional. any keyword. which will be searched in name, ec_no and cas_no
        :param str sort_field: optional. default sort field 'name'
        :param str sort_order: optional. two options ('asc', 'desc'). default sort order 'asc'
        :param bool regulation_prioritized: optional. if True only related regulation(regulations, framework, milestones)
                                    tagged substance will be returned
        :param bool news_prioritized: optional. if True only related news tagged substance will be returned
        :param bool property_prioritized: optional. if True only related property data point tagged substance will be returned
        :param bool only_my_org: optional. bool, default is True
        :param bool product_detail_page: optional. bool, default is False
        :param dict filters: optional. Additional filter options. Sample filters dict:
                        filters = {
                           'id': int or None,
                           'uses_and_applications': list object or None,
                           'regulatory_frameworks': list object or None,
                           'products': list object or None,
                           'regions': list object or None,
                           'topics': list object or None,
                           'news_source_types': list object or None,
                           'news_from_date': date string (yyyy-mm-dd),
                           'news_to_date': date string (yyyy-mm-dd),
                           'prioritization_strategies': list of object or None,
                        }
        """

        '''
        filter substances which is relevant for organization
        '''
        if sort_field.lower() in ['name', 'ec_no', 'cas_no']:
            sort_field = sort_field.lower() + '.raw'

        if only_my_org:
            substance_search: SubstanceDocument = SubstanceDocument.search().filter(
                'nested',
                path='uses_and_application_substances',
                query=Q('match', uses_and_application_substances__organization__id=organization_id)
            ).sort({sort_field: {"order": sort_order}})
        else:
            substance_search: SubstanceDocument = SubstanceDocument.search().sort(
                {
                    "uses_and_application_substances.id": {
                        "order": 'desc',
                        "nested_path": "uses_and_application_substances",
                        "nested_filter": {
                            "term": {
                                "uses_and_application_substances.organization.id": organization_id
                            }
                        }
                    }
                })

        '''
        keyword search in substances name, ec_no and cas_no
        '''
        if search_keyword:
            substance_search = substance_search.query(
                Q('match', name=search_keyword) |
                Q('match_phrase', ec_no=search_keyword) | Q('match_phrase', cas_no=search_keyword) |
                Q('match', ec_no=search_keyword) | Q('match', cas_no=search_keyword)) \
                .sort("_score")

        '''
        Regulation Prioritized substance
        https://chemycal.atlassian.net/browse/RTT-635
        '''
        if regulation_prioritized:
            relevant_regulatory_framework_ids = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(
                organization_id)
            relevant_regulation__ids = RelevantRegulationService().get_relevant_regulation_id_organization(
                organization_id)
            substance_search = substance_search.filter(
                # tagged to any relevant frameworks
                Q('nested',
                  path='substances_regulatory_framework',
                  query=Q('terms', substances_regulatory_framework__id=relevant_regulatory_framework_ids)) |
                # tagged to any relevant regulations
                Q('nested',
                  path='substances_regulation',
                  query=Q('terms', substances_regulation__id=relevant_regulation__ids)) |
                # tagged to any milestone of any relevant frameworks
                Q('nested',
                  path='substances_regulation_milestone',
                  query=Q('terms',
                          substances_regulation_milestone__regulatory_framework__id=relevant_regulatory_framework_ids)) |
                # tagged to any milestone of any relevant regulations
                Q('nested',
                  path='substances_regulation_milestone',
                  query=Q('terms', substances_regulation_milestone__regulation__id=relevant_regulation__ids))
            )

        '''
        News Prioritized substance
        https://chemycal.atlassian.net/browse/RTT-636
        '''
        if news_prioritized:
            relevant_news_ids = RelevantNewsService().get_organization_relevant_news_ids(organization_id)
            substance_search = substance_search.filter(
                # tagged to any relevant news
                Q('nested',
                  path='substances_news',
                  query=Q('terms', substances_news__id=relevant_news_ids))
            )

        '''
        property Prioritized substance
        https://chemycal.atlassian.net/browse/RTT-637
        '''
        if property_prioritized:
            if filters.get('prioritization_strategies', None):
                relevant_property_datapoint_ids = list(PropertyDataPoint.objects.filter(
                    property__prioritization_strategy_properties__organization_id=organization_id,
                    substance_property_data_point_property_data_point__status='active',
                    property__prioritization_strategy_properties__id__in=filters[
                        'prioritization_strategies']).values_list(
                    'id', flat=True))
            else:
                default_org_strategy = PrioritizationStrategy.objects.filter(
                    organization_id=organization_id, default_org_strategy=True).first()
                default_org_strategy_id = default_org_strategy.id
                relevant_property_datapoint_ids = list(PropertyDataPoint.objects.filter(
                    property__prioritization_strategy_properties__organization_id=organization_id,
                    substance_property_data_point_property_data_point__status='active',
                    property__prioritization_strategy_properties__id=default_org_strategy_id).values_list(
                    'id', flat=True))
            substance_search = substance_search.filter(
                Q('nested',
                  path='substance_property_data_point_relation',
                  query=Q('terms',
                          substance_property_data_point_relation__property_data_point__id=relevant_property_datapoint_ids) &
                        Q('match', substance_property_data_point_relation__status='active')
                  )
            )

        """
        apply custom filters
        """

        if filters is None:
            return substance_search

        if filters.get('id', None):
            substance_search = substance_search.filter('match', id=filters['id'])

        if filters.get('uses_and_applications', None):
            substance_search = substance_search.filter(
                'nested',
                path='uses_and_application_substances',
                query=Q('terms', uses_and_application_substances__id=filters['uses_and_applications'])
            )
        '''
        https://chemycal.atlassian.net/browse/RTT-536
        '''
        if filters.get('products', None):
            if product_detail_page:
                product_tagged_use_and_app_list = list(SubstanceUsesAndApplication.objects.filter(
                    product_substance_use_and_apps__in=filters['products']).values_list('id', flat=True))
                substance_search = substance_search.filter(
                    Q('nested',
                      path='substances_product',
                      query=Q('terms', substances_product__id=filters['products']) &
                            Q('match', substances_product__organization__id=organization_id)) |
                    Q('nested',
                      path='uses_and_application_substances',
                      query=(Q('terms', uses_and_application_substances__id=product_tagged_use_and_app_list) &
                            Q('match', uses_and_application_substances__organization__id=organization_id)))
                )
            else:
                substance_search = substance_search.filter(
                    Q('nested',
                      path='substances_product',
                      query=Q('terms', substances_product__id=filters['products']) &
                            Q('match', substances_product__organization__id=organization_id))
                )
        '''
        https://chemycal.atlassian.net/browse/RTT-536
        '''
        if filters.get('regulatory_frameworks', None):
            milestone_regulation_regulatory_framework = MilestoneDocument.search() \
                .filter('terms', regulation__regulatory_framework__id=filters['regulatory_frameworks']).source(['id'])
            milestone_regulation_regulatory_framework_ids = []
            for milestone in milestone_regulation_regulatory_framework:
                milestone_regulation_regulatory_framework_ids.append(milestone.id)
            substance_search = substance_search.filter(
                Q('nested',
                  path='substances_regulatory_framework',
                  query=Q('terms', substances_regulatory_framework__id=filters['regulatory_frameworks'])) |
                Q('nested',
                  path='substances_regulation_milestone',
                  query=Q('terms',
                          substances_regulation_milestone__regulatory_framework__id=filters['regulatory_frameworks'])) |
                Q('nested',
                  path='substances_regulation',
                  query=Q('terms',
                          substances_regulation__regulatory_framework__id=filters['regulatory_frameworks'])) |
                Q('nested',
                  path='substances_regulation_milestone',
                  query=Q('terms',
                          substances_regulation_milestone__id=milestone_regulation_regulatory_framework_ids))
            )

        '''
        filter by topics in 
        (regulation_prioritized) regulatory_frameworks or regulations 
        (news_prioritized) news
        https://chemycal.atlassian.net/browse/RTT-565
        '''
        if filters.get('regions', None):
            if regulation_prioritized:
                regulation_regions_ids = []
                regulation_regions_doc_qs = RegulationDocument.search().filter(
                    Q('nested',
                      path='regulatory_framework.regions',
                      query=Q('terms', regulatory_framework__regions__id=filters['regions']))
                ).source(['id'])
                regulation_regions_doc_qs = regulation_regions_doc_qs[0:regulation_regions_doc_qs.count()]
                for regulation_region in regulation_regions_doc_qs:
                    regulation_regions_ids.append(regulation_region.id)
                substance_search = substance_search.filter(
                    # regions in the framework
                    Q('nested',
                      path='substances_regulatory_framework.regions',
                      query=Q('terms', substances_regulatory_framework__regions__id=filters['regions'])) |
                    # regions in the regulation via framework
                    Q('nested',
                      path='substances_regulation',
                      query=Q('terms', substances_regulation__id=regulation_regions_ids))
                )
            if news_prioritized:
                substance_search = substance_search.filter(
                    # regions in the news
                    Q('nested',
                      path='substances_news.regions',
                      query=Q('terms', substances_news__regions__id=filters['regions']))
                )
        '''
        filter by topics in regulatory_frameworks or regulations
        https://chemycal.atlassian.net/browse/RTT-565
        '''
        if filters.get('topics', None):
            if regulation_prioritized:
                substance_search = substance_search.filter(
                    # topics in the framework
                    Q('nested',
                      path='substances_regulatory_framework.topics',
                      query=Q('terms', substances_regulatory_framework__topics__id=filters['topics'])) |
                    # topics in the regulation
                    Q('nested',
                      path='substances_regulation.topics',
                      query=Q('terms', substances_regulation__topics__id=filters['topics']))
                )

        '''
        filter by news_source_types in news (news_prioritized)
        https://chemycal.atlassian.net/browse/RTT-565
        '''
        if filters.get('news_source_types', None):
            if news_prioritized:
                substance_search = substance_search.filter(
                    Q('nested',
                      path='substances_news',
                      query=Q('terms', substances_news__source__type__id=filters['news_source_types']))
                )
        '''
        filter by substance last_mentioned in news (news_prioritized)
        https://chemycal.atlassian.net/browse/RTT-565
        '''
        if filters.get('news_from_date', None) and filters.get('news_to_date', None):
            if news_prioritized:
                from_date = filters['news_from_date']
                to_date = filters['news_to_date']
                substance_search = substance_search.filter(
                    Q('nested',
                      path='substance_news_relation',
                      query=Q('range', substance_news_relation__modified={'gte': from_date, 'lte': to_date}))
                )

        '''
        filter by prioritization_strategies
        https://chemycal.atlassian.net/browse/RTT-1315
        '''
        if filters.get('prioritization_strategies', None):
            relevant_property_datapoint_ids = list(PropertyDataPoint.objects.filter(
                property__prioritization_strategy_properties__organization_id=organization_id,
                substance_property_data_point_property_data_point__status='active',
                property__prioritization_strategy_properties__id__in=filters['prioritization_strategies']).values_list(
                'id', flat=True))
            substance_search = substance_search.filter(
                Q('nested',
                  path='substance_property_data_point_relation',
                  query=Q('terms',
                          substance_property_data_point_relation__property_data_point__id=relevant_property_datapoint_ids) &
                        Q('match', substance_property_data_point_relation__status='active')
                  )
            )

        return substance_search

    @staticmethod
    def get_filtered_substance_uses_and_application_queryset(organization_id, filters=None):
        substance_uses_and_application_search: SubstanceUsesAndApplicationDocument = SubstanceUsesAndApplicationDocument \
            .search().filter('match', organization__id=organization_id).sort('name.raw')
        return substance_uses_and_application_search

    @staticmethod
    def get_prioritization_strategies_queryset(organization_id, relevant_property_datapoint_id_list, serializer=False):
        prioritization_strategy_qs = PrioritizationStrategy.objects.filter(
            organization_id=organization_id,
            properties__property_data_property__id__in=relevant_property_datapoint_id_list).distinct()
        if not serializer:
            return prioritization_strategy_qs
        prioritization_strategies_list = []
        for prioritization_strategy in prioritization_strategy_qs:
            prioritization_strategies_list.append({
                "id": prioritization_strategy.id,
                "name": prioritization_strategy.name,
            })
        return prioritization_strategies_list

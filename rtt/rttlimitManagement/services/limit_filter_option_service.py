from elasticsearch_dsl import Q

from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttregulation.services.region_filtered_regulation_queryset_service import RegionFilteredRegulationQuerysetService
from rttregulation.documents import RegulatoryFrameworkDocument


class LimitFilterOptionService:

    def get_regulation_region_filter_option(self, organization_id, filters, search_keyword=None,
                                            substance_details_prioritized=False):
        """
        This function will return dict of framework list, regulation list and region list
        :param int organization_id: Required. user organization_id(int)
        :param dict filters: Required. sample filter:
                filters = {
                            'regulatory_frameworks': list object or None,
                            'regulations': list object or None,
                            'substances': list object or None,
                            'from_date': date string (yyyy-mm-dd),
                            'to_date': date string (yyyy-mm-dd)
                        }
        :param str search_keyword: optional. any keyword. which will be searched in substance name, Scope
        :param bool substance_details_prioritized: optional. Applicable for substance_details_page filter
        """
        regulation_substance_limit_qs = LimitCoreService().get_regulation_substance_limit_queryset(organization_id,
                                                                                                   filters)
        if search_keyword and not substance_details_prioritized:
            regulation_ids = RegionFilteredRegulationQuerysetService(). \
                get_region_filtered_regulation_ids(organization_id, search_keyword=search_keyword)
            regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                # any keyword. which will be searched in substance name
                Q('match', substance__name=search_keyword) |
                # any keyword. which will be searched in scope
                Q('match', scope=search_keyword) |
                # any keyword. which will be searched in region name(framework)
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('match', regulatory_framework__regions__name=search_keyword)) |
                # any keyword. which will be searched in region name(regulation) using regulation_ids
                Q('terms', regulation__id=regulation_ids)
            )
        if substance_details_prioritized:
            if filters.get('regions', None):
                region_tagged_regulation_ids = RegionFilteredRegulationQuerysetService(). \
                    get_region_filtered_regulation_ids(organization_id, region_ids=filters['regions'])
                regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                    # filter by region(framework)
                    Q('nested',
                      path='regulatory_framework.regions',
                      query=Q('terms', regulatory_framework__regions__id=filters['regions'])) |
                    # filter by region_id (using regulation_ids)
                    Q('terms', regulation__id=region_tagged_regulation_ids)
                )
            if search_keyword:
                region_tagged_regulation_ids = RegionFilteredRegulationQuerysetService(). \
                    get_region_filtered_regulation_ids(organization_id, search_keyword=search_keyword)
                regulation_substance_limit_qs = regulation_substance_limit_qs.filter(
                    # any keyword. which will be searched in region name(framework)
                    Q('nested',
                      path='regulatory_framework.regions',
                      query=Q('match', regulatory_framework__regions__name=search_keyword)) |
                    # any keyword. which will be searched in region name(regulation) using regulation_ids
                    Q('terms', regulation__id=region_tagged_regulation_ids) |
                    # any keyword. which will be searched in framework name
                    Q('match', regulatory_framework__name=search_keyword) |
                    # any keyword. which will be searched in regulation name
                    Q('match', regulation__name=search_keyword) |
                    # any keyword. which will be searched in scope
                    Q('match', scope=search_keyword)
                )

        return regulation_substance_limit_qs

    @staticmethod
    def get_region_data(framework_id, visited_regions):
        result = []
        regulatory_framework_doc_qs: RegulatoryFrameworkDocument = RegulatoryFrameworkDocument().search().filter(
            'match', id=framework_id
        ).source(['regions'])
        regulatory_framework_doc_qs = regulatory_framework_doc_qs[0:regulatory_framework_doc_qs.count()]
        for regulatory_framework in regulatory_framework_doc_qs:
            for region in regulatory_framework.regions:
                if str(region.id) not in visited_regions:
                    result.append({
                        'id': region.id,
                        'name': region.name
                    })
                    visited_regions[str(region.id)] = True

        return result

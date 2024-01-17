from elasticsearch_dsl import Q
from rttlimitManagement.services.limit_core_service import LimitCoreService


class RegionFilteredRegulationQuerysetService:
    @staticmethod
    def get_region_filtered_regulation_ids(organization_id, region_ids=None, search_keyword=None):
        """
        This function will return regulation_ids list filter by region_ids and region name
        :param int organization_id: Required. user organization_id(int)
        :param list region_ids: optional. list of region_ids
        :param string search_keyword: optional. any keyword. which will be searched in region name
        """
        regulation_ids = []
        regulation_doc = LimitCoreService().get_regulation_limit_queryset(organization_id).source(['id'])
        if region_ids:
            regulation_doc = regulation_doc.filter(
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('terms', regulatory_framework__regions__id=region_ids))
            )
        if search_keyword:
            regulation_doc = regulation_doc.filter(
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('match', regulatory_framework__regions__name=search_keyword))
            )

        regulation_doc = regulation_doc[0:regulation_doc.count()]
        for regulation in regulation_doc:
            regulation_ids.append(regulation.id)
        return regulation_ids

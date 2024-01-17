from elasticsearch_dsl import Q

from rttcore.services.system_filter_service import SystemFilterService
from rttcore.services.dashboard_services import DashboardService


class FilteredMilestoneService:
    """
    filters = {
        'regions': List of region ID
        'milestone_types': List of milestone_type ID
        'regulations': List of regulation ID
        'frameworks': List of framework ID
        'search': Key word will be searched in milestone name field
    }
    """

    @staticmethod
    def get_filtered_milestone_queryset(filters, organization_id, substance_id):
        """
        apply system filters
        """
        milestone_search = SystemFilterService().get_system_filtered_milestone_document_queryset(
            organization_id).filter(
            # milestones to which the substance is tagged
            Q('nested',
              path='substances',
              query=Q('match', substances__id=substance_id))
        )
        if filters.get('search', None):
            milestone_search = milestone_search.filter(
                Q('match', name=filters['search'])
            )
        region_filtered_regulation_ids = []
        if filters.get('regions', None):
            regulation_region_filter = {
                'regions': filters.get('regions', None)
            }
            region_filtered_regulation_qs = DashboardService().get_filtered_regulation_queryset(
                filters=regulation_region_filter, organization_id=organization_id).source(['id'])
            region_filtered_regulation_qs = region_filtered_regulation_qs[0:region_filtered_regulation_qs.count()]
            for regulation in region_filtered_regulation_qs:
                region_filtered_regulation_ids.append(regulation.id)

        if filters.get('regions', None):
            milestone_search = milestone_search.filter(
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('terms', regulatory_framework__regions__id=filters['regions'])) |
                Q('terms', regulation__id=region_filtered_regulation_ids)
            )
        if filters.get('milestone_types', None):
            milestone_search = milestone_search.filter(
                Q('terms', type__id=filters['milestone_types'])
            )
        if filters.get('regulations', None):
            milestone_search = milestone_search.filter('terms', regulation__id=filters['regulations'])
        if filters.get('frameworks', None):
            milestone_search = milestone_search.filter('terms', regulatory_framework__id=filters['frameworks'])

        return milestone_search

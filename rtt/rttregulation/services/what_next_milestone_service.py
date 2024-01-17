from django.utils import timezone
from elasticsearch_dsl import Q

from rttcore.services.system_filter_service import SystemFilterService
from rttcore.services.dashboard_services import DashboardService


class WhatNextMilestoneService:

    def get_what_next_filtered_milestone_document_queryset(self, organization_id, filters=None, search_keyword=None):
        """
        The responsibility of this service is to make sure milestone_from date is future and apply filters and
        search_keyword to the system_filtered_milestone_document_queryset
        :param int organization_id: Required. user organization_id(int)
        :param str search_keyword: optional. any keyword
        :param dict filters: optional. Additional filter options. Sample filters_dict
                        filters = {
                           'period_start': year_start_date string,
                           'period_end': year_end_date string,
                           'regulatory_frameworks': list object or None,
                           'regulations': list object or None,
                           'milestone_types': list object or None,
                           'regions': list object or None,
                           'product_categories': list object or None,
                           'material_categories': list object or None,
                        }
        """
        # apply system filters
        milestone_doc_queryset = SystemFilterService().get_system_filtered_milestone_document_queryset(
            organization_id).sort('from_date')

        # making sure all the milestones are from future
        today = timezone.now()
        milestone_doc_queryset = milestone_doc_queryset.filter(
            Q('range', from_date={'gt': today})
        )

        if search_keyword:
            # filter by search_keyword
            milestone_doc_queryset = milestone_doc_queryset.filter(
                Q('match', name=search_keyword) |
                Q('match', description=search_keyword)
            )

        # if no filter is apply return milestone_doc_queryset
        if not filters:
            return milestone_doc_queryset

        '''
        https://chemycal.atlassian.net/browse/RTT-702
        '''
        # filter by period
        if filters.get('period_start', None) and filters.get('period_end', None):
            milestone_doc_queryset = milestone_doc_queryset.filter(
                Q('range', from_date={'gte': filters['period_start'], 'lte': filters['period_end']})
            )

        # filter by regulatory_frameworks or regulations
        if filters.get('regulatory_frameworks', None) or filters.get('regulations', None):
            milestone_doc_queryset = milestone_doc_queryset.filter(
                Q('terms', regulatory_framework__id=filters['regulatory_frameworks']) |
                Q('terms', regulation__id=filters['regulations'])
            )

        # filter by milestone_types
        if filters.get('milestone_types', None):
            milestone_doc_queryset = milestone_doc_queryset.filter(
                Q('terms', type__id=filters['milestone_types'])
            )

        # filter by regions
        if filters.get('regions', None):
            region_filtered_regulation_ids = self.get_region_filtered_regulation_ids(organization_id,
                                                                                     region_ids=filters['regions'])
            milestone_doc_queryset = milestone_doc_queryset.filter(
                # regulatory_framework regions
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('terms', regulatory_framework__regions__id=filters['regions'])) |
                # regulation regions using regulation_id
                Q('terms', regulation__id=region_filtered_regulation_ids)
            )

        # filter by product_categories
        if filters.get('product_categories', None):
            milestone_doc_queryset = milestone_doc_queryset.filter(
                # regulation product_categories
                Q('nested',
                  path='regulation.product_categories',
                  query=Q('terms', regulation__product_categories__id=filters['product_categories'])) |
                # regulatory_framework product_categories
                Q('nested',
                  path='regulatory_framework.product_categories',
                  query=Q('terms', regulatory_framework__product_categories__id=filters['product_categories']))
            )

        # filter by material_categories
        if filters.get('material_categories', None):
            milestone_doc_queryset = milestone_doc_queryset.filter(
                # regulation material_categories
                Q('nested',
                  path='regulation.material_categories',
                  query=Q('terms', regulation__material_categories__id=filters['material_categories'])) |
                # regulatory_framework material_categories
                Q('nested',
                  path='regulatory_framework.material_categories',
                  query=Q('terms', regulatory_framework__material_categories__id=filters['material_categories']))
            )
        # filter by related_product
        if filters.get('related_products', None):
            product_categories_id, material_categories_id = DashboardService().\
                get_related_products_product_category_material_category_ids(filters['related_products'])
            # filter by product_categories/material_categories
            milestone_doc_queryset = milestone_doc_queryset.filter(
                # regulation product_categories
                Q('nested',
                  path='regulation.product_categories',
                  query=Q('terms', regulation__product_categories__id=product_categories_id)) |
                # regulatory_framework product_categories
                Q('nested',
                  path='regulatory_framework.product_categories',
                  query=Q('terms', regulatory_framework__product_categories__id=product_categories_id)) |
                # regulation material_categories
                Q('nested',
                  path='regulation.material_categories',
                  query=Q('terms', regulation__material_categories__id=material_categories_id)) |
                # regulatory_framework material_categories
                Q('nested',
                  path='regulatory_framework.material_categories',
                  query=Q('terms', regulatory_framework__material_categories__id=material_categories_id))
            )

        # filter by topics
        if filters.get('topics', None):
            milestone_doc_queryset = milestone_doc_queryset.filter(
                # regulation topic
                Q('nested',
                  path='regulation.topics',
                  query=Q('terms', regulation__topics__id=filters['topics'])) |
                # regulatory_framework topic
                Q('nested',
                  path='regulatory_framework.topics',
                  query=Q('terms', regulatory_framework__topics__id=filters['topics']))
            )

        # filter by status
        if filters.get('status', None):
            milestone_doc_queryset = milestone_doc_queryset.filter(
                # regulation status
                Q('terms', regulation__status__id=filters['status']) |
                # regulatory_framework status
                Q('terms', regulatory_framework__status__id=filters['status'])
            )
        return milestone_doc_queryset

    @staticmethod
    def get_region_filtered_regulation_ids(organization_id, region_ids):
        regulation_ids = []
        regulation_doc = SystemFilterService().get_system_filtered_regulation_document_queryset(
            organization_id).source(['id'])
        regulation_doc = regulation_doc.filter(
            Q('nested',
              path='regulatory_framework.regions',
              query=Q('terms', regulatory_framework__regions__id=region_ids))
        )
        regulation_doc = regulation_doc[0:regulation_doc.count()]
        for regulation in regulation_doc:
            regulation_ids.append(regulation.id)
        return regulation_ids

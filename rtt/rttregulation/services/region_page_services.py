import copy
from elasticsearch_dsl import Q

from rttcore.services.system_filter_service import SystemFilterService
from rttproduct.documents import ProductCategoryDocument, MaterialCategoryDocument
from rttlimitManagement.services.limit_core_service import LimitCoreService


class RegionPageServices:
    """
    This service is for region_page all endpoints.
    To make region_page data synchronize, all region_page endpoint get queryset from this service.
    Sample filters dict:
    filters = {
            'related_products': list object or None,
            'product_categories': list object or None,
            'material_categories': list object or None,
            'related_regulations': list object or None,
            'related_frameworks': list object or None,
            'news': list object or None,
            'rating': int or None,
            'status': list object or None,
            'topics': list object or None,
        }
    """

    def get_filtered_news_queryset(self, organization_id, region_id, filters=None, search_keyword=None):
        # apply system filters
        news_doc_qs = SystemFilterService().get_system_filtered_news_document_queryset(organization_id)
        # news tagged to regions
        news_doc_qs = news_doc_qs.filter(
            Q('nested',
              path='regions',
              query=Q('match', regions__id=region_id))
        )
        '''
        user custom filters
        '''
        # search keyword in news
        if search_keyword:
            news_doc_qs = news_doc_qs.filter(
                # search on news_title
                Q('match', title=search_keyword)
            )

        if not filters:
            return news_doc_qs
        # filter by topics
        if filters.get('topics', None):
            news_doc_qs = news_doc_qs.filter(
                Q('nested',
                  path='news_categories',
                  query=Q('terms', news_categories__topic__id=filters['topics']))
            )

        # filter by product_categories
        if filters.get('product_categories', None):
            news_doc_qs = news_doc_qs.filter(
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=filters['product_categories']))
            )

        # filter by material_categories
        if filters.get('material_categories', None):
            news_doc_qs = news_doc_qs.filter(
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=filters['material_categories']))
            )

        # filter by related_products
        if filters.get('related_products', None):
            product_categories_id = self.get_related_product_category_ids(filters['related_products'])
            material_categories_id = self.get_related_material_category_ids(filters['related_products'])
            news_doc_qs = news_doc_qs.filter(
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=product_categories_id)) |
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=material_categories_id))
            )

        # filter by related_regulations
        if filters.get('related_regulations', None):
            news_doc_qs = news_doc_qs.filter(
                'nested',
                path='regulations',
                query=Q('terms', regulations__id=filters['related_regulations'])
            )

        # filter by related_frameworks
        if filters.get('related_frameworks', None):
            news_doc_qs = news_doc_qs.filter(
                'nested',
                path='regulatory_frameworks',
                query=Q('terms', regulatory_frameworks__id=filters['related_frameworks'])
            )

        # filter by rating
        if filters.get('rating', None):
            news_doc_qs = news_doc_qs.filter(
                Q('nested',
                  path='news_relevance',
                  query=Q('match', news_relevance__relevancy=filters['rating']) &
                    Q('match', news_relevance__organization__id=organization_id))
            )

        # filter by news
        if filters.get('news', None):
            news_doc_qs = news_doc_qs.filter(
                'terms', id=filters['news']
            )

        return news_doc_qs

    def get_filtered_framework_queryset(self, organization_id, region_id, filters=None, search_keyword=None):
        # apply system filter
        framework_doc_qs = SystemFilterService().get_system_filtered_regulatory_framework_queryset(organization_id)

        # regulatory_framework tagged to region
        framework_doc_qs = framework_doc_qs.filter(
            Q('nested',
              path='regions',
              query=Q('match', regions__id=region_id))
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
                  query=Q('match', regulation_regulatory_framework__name=search_keyword))
            )

        if not filters:
            return framework_doc_qs
        # filter by status
        if filters.get('status', None):
            framework_doc_qs = framework_doc_qs.filter(
                # status filter on framework
                Q('terms', status__id=filters['status']) |
                # status filter on regulation
                Q('nested',
                  path='regulation_regulatory_framework',
                  query=Q('terms', regulation_regulatory_framework__status__id=filters['status']))
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
                  path='regulation_regulatory_framework.topics',
                  query=Q('terms', regulation_regulatory_framework__topics__id=filters['topics']))
            )

        # filter by product_categories
        if filters.get('product_categories', None):
            framework_doc_qs = framework_doc_qs.filter(
                # product_categories filter on framework
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=filters['product_categories'])) |
                # product_categories filter on regulation
                Q('nested',
                  path='regulation_regulatory_framework.product_categories',
                  query=Q('terms',
                          regulation_regulatory_framework__product_categories__id=filters['product_categories']))
            )

        # filter by material_categories
        if filters.get('material_categories', None):
            framework_doc_qs = framework_doc_qs.filter(
                # material_categories filter on framework
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=filters['material_categories'])) |
                # material_categories filter on regulation
                Q('nested',
                  path='regulation_regulatory_framework.material_categories',
                  query=Q('terms',
                          regulation_regulatory_framework__material_categories__id=filters['material_categories']))
            )

        # filter by related_products
        if filters.get('related_products', None):
            product_categories_id = self.get_related_product_category_ids(filters['related_products'])
            material_categories_id = self.get_related_material_category_ids(filters['related_products'])
            framework_doc_qs = framework_doc_qs.filter(
                # related_products filter on framework using product_categories
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=product_categories_id)) |
                # related_products filter on framework using material_categories
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=material_categories_id)) |
                # related_products filter on regulation using product_categories
                Q('nested',
                  path='regulation_regulatory_framework.product_categories',
                  query=Q('terms', regulation_regulatory_framework__product_categories__id=product_categories_id)) |
                # related_products filter on regulation using material_categories
                Q('nested',
                  path='regulation_regulatory_framework.material_categories',
                  query=Q('terms', regulation_regulatory_framework__material_categories__id=material_categories_id))
            )

        # filter by related_regulations
        if filters.get('related_regulations', None):
            framework_doc_qs = framework_doc_qs.filter(
                Q('nested',
                  path='regulation_regulatory_framework',
                  query=Q('terms', regulation_regulatory_framework__id=filters['related_regulations']))
            )

        # filter by related_frameworks
        if filters.get('related_frameworks', None):
            framework_doc_qs = framework_doc_qs.filter(
                Q('terms', id=filters['related_frameworks'])
            )

        # filter by rating
        if filters.get('rating', None):
            rating_filtered_regulation_ids = self.get_rating_filtered_regulation_ids(filters['rating'], organization_id)
            framework_doc_qs = framework_doc_qs.filter(
                # rating filter in framework
                Q('nested',
                  path='regulatory_framework_rating',
                  query=Q('match', regulatory_framework_rating__rating=filters['rating']) &
                    Q('match', regulatory_framework_rating__organization__id=organization_id)) |
                # rating filter in regulation
                Q('nested',
                  path='regulation_regulatory_framework',
                  query=Q('terms', regulation_regulatory_framework__id=rating_filtered_regulation_ids))
            )

        # filter by news
        if filters.get('news', None):
            framework_doc_qs = framework_doc_qs.filter(
                Q('nested',
                  path='news_regulatory_frameworks',
                  query=Q('terms', news_regulatory_frameworks__id=filters['news']))
            )

        return framework_doc_qs

    def get_filtered_regulation_queryset(self, organization_id, region_id, filters=None, search_keyword=None):
        # apply system filter
        regulation_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(organization_id)

        # regulation tagged to region
        regulation_doc_qs = regulation_doc_qs.filter(
            Q('nested',
              path='regulatory_framework.regions',
              query=Q('match', regulatory_framework__regions__id=region_id))
        )

        '''
        user custom filters
        '''
        # search keyword in regulation and framework name
        if search_keyword:
            regulation_doc_qs = regulation_doc_qs.filter(
                # search on regulation_name
                Q('match', name=search_keyword) |
                # search on framework_name
                Q('match', regulatory_framework__name=search_keyword)
            )

        if not filters:
            return regulation_doc_qs
        # filter by status
        if filters.get('status', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                # status filter on regulation
                Q('terms', status__id=filters['status'])
            )

        # filter by topics
        if filters.get('topics', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                # topic filter on framework
                Q('nested',
                  path='topics',
                  query=Q('terms', topics__id=filters['topics']))
            )

        # filter by product_categories
        if filters.get('product_categories', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                # product_categories filter on regulation
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=filters['product_categories']))
            )

        # filter by material_categories
        if filters.get('material_categories', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                # material_categories filter on regulation
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=filters['material_categories']))
            )

        # filter by related_products
        if filters.get('related_products', None):
            product_categories_id = self.get_related_product_category_ids(filters['related_products'])
            material_categories_id = self.get_related_material_category_ids(filters['related_products'])
            regulation_doc_qs = regulation_doc_qs.filter(
                # related_products filter on regulation using product_categories
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=product_categories_id)) |
                # related_products filter on regulation using material_categories
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=material_categories_id))
            )

        # filter by related_regulations
        if filters.get('related_regulations', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('terms', id=filters['related_regulations'])
            )

        # filter by related_frameworks
        if filters.get('related_frameworks', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('terms', regulatory_framework__id=filters['related_frameworks'])
            )

        # filter by rating
        if filters.get('rating', None):
            rating_filtered_framework_ids = self.get_rating_filtered_framework_ids(filters['rating'], organization_id)
            regulation_doc_qs = regulation_doc_qs.filter(
                # rating filter in regulation
                Q('nested',
                  path='regulation_rating',
                  query=Q('match', regulation_rating__rating=filters['rating']) &
                    Q('match', regulation_rating__organization__id=organization_id))
            )

        # filter by news
        if filters.get('news', None):
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='regulation_news',
                  query=Q('terms', regulation_news__id=filters['news']))
            )

        return regulation_doc_qs

    def get_filtered_milestone_queryset(self, organization_id, region_id, filters=None):
        # apply system filter
        milestone_doc_qs = SystemFilterService().get_system_filtered_milestone_document_queryset(organization_id)
        framework_filters = copy.deepcopy(filters)
        framework_filters['related_regulations'] = None
        framework_doc_qs = self.get_filtered_framework_queryset(organization_id, region_id,
                                                                framework_filters).source(['id'])
        framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]

        regulation_filters = copy.deepcopy(filters)
        regulation_filters['related_frameworks'] = None
        regulation_doc_qs = self.get_filtered_regulation_queryset(organization_id, region_id,
                                                                  regulation_filters).source(['id'])
        regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
        framework_ids = []
        regulation_ids = []
        for framework in framework_doc_qs:
            framework_ids.append(framework.id)
        for regulation in regulation_doc_qs:
            regulation_ids.append(regulation.id)

        # filter by regulation/framework
        milestone_doc_qs = milestone_doc_qs.filter(
            # related framework for system filter
            Q('terms', regulatory_framework__id=framework_ids) |
            # related regulation for system filter
            Q('terms', regulation__id=regulation_ids)
        )

        '''
        user custom filters
        '''

        if not filters:
            return milestone_doc_qs
        # related framework for custom filter
        if filters.get('related_frameworks', None):
            milestone_doc_qs = milestone_doc_qs.filter(
                Q('terms', regulatory_framework__id=filters['related_frameworks'])
            )

        # related regulation for custom filter
        if filters.get('related_regulations', None):
            milestone_doc_qs = milestone_doc_qs.filter(
                Q('terms', regulation__id=filters['related_regulations'])
            )

        return milestone_doc_qs

    @staticmethod
    def get_related_product_category_ids(product_id_list):
        product_categories_id = []
        product_category_doc_qs: ProductCategoryDocument = ProductCategoryDocument.search().filter(
            'nested',
            path='product_product_categories',
            query=Q('terms', product_product_categories__id=product_id_list)
        ).source(['id'])
        product_category_doc_qs = product_category_doc_qs[0:product_category_doc_qs.count()]
        for product_category in product_category_doc_qs:
            product_categories_id.append(product_category.id)

        return product_categories_id

    @staticmethod
    def get_related_material_category_ids(product_id_list):
        material_categories_id = []
        material_category_doc_qs: MaterialCategoryDocument = MaterialCategoryDocument.search().filter(
            'nested',
            path='product_material_categories',
            query=Q('terms', product_material_categories__id=product_id_list)
        ).source(['id'])
        material_category_doc_qs = material_category_doc_qs[0:material_category_doc_qs.count()]
        for material_category in material_category_doc_qs:
            material_categories_id.append(material_category.id)

        return material_categories_id

    @staticmethod
    def get_rating_filtered_regulation_ids(rating_value, organization_id):
        regulation_ids = []
        regulation_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(
            organization_id).filter(
            Q('nested',
              path='regulation_rating',
              query=Q('match', regulation_rating__rating=rating_value) &
                Q('match', regulation_rating__organization__id=organization_id))
        ).source(['id'])
        regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
        for regulation in regulation_doc_qs:
            regulation_ids.append(regulation.id)

        return regulation_ids

    @staticmethod
    def get_rating_filtered_framework_ids(rating_value, organization_id):
        framework_ids = []
        framework_doc_qs = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            organization_id).filter(
            Q('nested',
              path='regulatory_framework_rating',
              query=Q('match', regulatory_framework_rating__rating=rating_value) &
                Q('match', regulatory_framework_rating__organization__id=organization_id))
        ).source(['id'])
        framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
        for framework in framework_doc_qs:
            framework_ids.append(framework.id)

        return framework_ids

    def get_filtered_limit_queryset(self, organization_id, region_id, filters=None, search_keyword=None):

        limit_doc_qs = LimitCoreService().get_regulation_substance_limit_queryset(organization_id)

        # apply system filter
        framework_filters = copy.deepcopy(filters)
        framework_filters['related_regulations'] = None
        framework_doc_qs = self.get_filtered_framework_queryset(organization_id, region_id,
                                                                framework_filters).source(['id'])
        framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]

        regulation_filters = copy.deepcopy(filters)
        regulation_filters['related_frameworks'] = None
        regulation_doc_qs = self.get_filtered_regulation_queryset(organization_id, region_id,
                                                                  regulation_filters).source(['id'])
        regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
        framework_ids = []
        regulation_ids = []
        for framework in framework_doc_qs:
            framework_ids.append(framework.id)
        for regulation in regulation_doc_qs:
            regulation_ids.append(regulation.id)

        # filter by regulation/framework
        limit_doc_qs = limit_doc_qs.filter(
            # related framework for system filter
            Q('terms', regulatory_framework__id=framework_ids) |
            # related regulation for system filter
            Q('terms', regulation__id=regulation_ids)
        )

        # search keyword in limit data
        if search_keyword:
            limit_doc_qs = limit_doc_qs.query(
                Q('match', substance__name=search_keyword) | Q('match', substance__ec_no=search_keyword) |
                Q('match', substance__cas_no=search_keyword) | Q('match', regulatory_framework__name=search_keyword) |
                Q('match', regulation__name=search_keyword) | Q('match', scope=search_keyword)
            ).sort('_score')
        '''
        user custom filters
        '''
        if not filters:
            return limit_doc_qs
        # related framework for custom filter
        if filters.get('related_frameworks', None):
            limit_doc_qs = limit_doc_qs.filter(
                Q('terms', regulatory_framework__id=filters['related_frameworks'])
            )
        # related regulation for custom filter
        if filters.get('related_regulations', None):
            limit_doc_qs = limit_doc_qs.filter(
                Q('terms', regulation__id=filters['related_regulations'])
            )
        return limit_doc_qs

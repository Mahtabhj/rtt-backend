import subprocess

from elasticsearch_dsl import Q

from rttcore.services.system_filter_service import SystemFilterService
from rttnews.documents import NewsDocument
from rttproduct.documents import ProductDocument, ProductCategoryDocument, MaterialCategoryDocument
from rttregulation.documents import RegulatoryFrameworkDocument, RegulationDocument


class DashboardService:
    """
    This service is for Dashboard all endpoints.
    To make dashboard data synchronize, all dashboard endpoint get queryset from this service.

    Sample filters dict:
    filters = {
            'topics': list object or None,
            'regions': list object or None,
            'product_categories': list object or None,
            'material_categories': list object or None,
            'from_date': list object or None,
            'to_date': list object or None,
            'news': list object or None,
            'regulations': list object or None,
            'frameworks': list object or None,
            'related_products': list object or None,
            'related_regulations': list object or None,
            'related_frameworks': list object or None,
            'search': optional. any keyword. which will be searched
        }
    """

    def get_filtered_news_queryset(self, filters, organization_id):
        """
        apply system filters
        """
        news_search = SystemFilterService().get_system_filtered_news_document_queryset(organization_id)

        '''
        user custom filters
        '''
        if filters.get('search', None):
            news_search = news_search.filter(
                Q('match', title=filters['search'])
            )
        if filters.get('topics', None):
            news_search = news_search.filter(
                Q('nested',
                  path='news_categories',
                  query=Q('terms', news_categories__topic__id=filters['topics']))
            )
        if filters.get('regions', None):
            news_search = news_search.filter(
                'nested',
                path='regions',
                query=Q('terms', regions__id=filters['regions'])
            )
        if filters.get('product_categories', None):
            news_search = news_search.filter(
                'nested',
                path='product_categories',
                query=Q('terms', product_categories__id=filters['product_categories'])
            )
        if filters.get('material_categories', None):
            news_search = news_search.filter(
                'nested',
                path='material_categories',
                query=Q('terms', material_categories__id=filters['material_categories'])
            )
        if filters.get('from_date', None) and filters.get('to_date', None):
            news_search = news_search.filter(
                'range',
                pub_date={'from': filters['from_date'], 'to': filters['to_date']}
            )
        if filters.get('news', None):
            news_search = news_search.filter('terms', id=filters['news'])
        if filters.get('related_products', None):
            product_categories_id, material_categories_id = \
                self.get_related_products_product_category_material_category_ids(filters['related_products'])
            news_search = news_search.filter(
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=product_categories_id)) |
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=material_categories_id))
            )
        if filters.get('related_regulations', None):
            news_search = news_search.filter(
                'nested',
                path='regulations',
                query=Q('terms', regulations__id=filters['related_regulations'])
            )
        if filters.get('related_frameworks', None):
            news_search = news_search.filter(
                'nested',
                path='regulatory_frameworks',
                query=Q('terms', regulatory_frameworks__id=filters['related_frameworks'])
            )
        if filters.get('regulations', None) and filters.get('from_date', None) and filters.get('to_date', None):
            news_search = news_search.filter(Q(
                'nested',
                path='regulations',
                query=Q('terms', regulations__id=filters['regulations'])
            ) & Q('nested',
                  path='regulations.regulation_milestone',
                  query=Q('range', regulations__regulation_milestone__from_date={'gte': filters['from_date']}) &
                        Q('range', regulations__regulation_milestone__from_date={'lte': filters['to_date']})))

        if filters.get('frameworks', None) and filters.get('from_date', None) and filters.get('to_date', None):
            news_search = news_search.filter(Q(
                'nested',
                path='regulatory_frameworks',
                query=Q('terms', regulatory_frameworks__id=filters['frameworks'])
            ) & Q('nested',
                  path='regulatory_frameworks.regulatory_framework_milestone',
                  query=Q('range', regulatory_frameworks__regulatory_framework_milestone__from_date={
                      'gte': filters['from_date']}) &
                        Q('range',
                          regulatory_frameworks__regulatory_framework_milestone__from_date={
                              'lte': filters['to_date']})))

        return news_search

    def get_filtered_regulation_queryset(self, filters, organization_id):
        """
        apply system filters
        """
        regulation_search = SystemFilterService().get_system_filtered_regulation_document_queryset(organization_id)

        '''
        user custom filters
        '''
        if filters.get('search', None):
            regulation_search = regulation_search.filter(
                Q('match', name=filters['search'])
            )
        if filters.get('topics', None):
            regulation_search = regulation_search.filter(
                'nested',
                path='topics',
                query=Q('terms', topics__id=filters['topics'])
            )
        if filters.get('regions', None):
            regulation_search = regulation_search.filter(
                'nested',
                path='regulatory_framework.regions',
                query=Q('terms', regulatory_framework__regions__id=filters['regions'])
            )
        if filters.get('product_categories', None):
            regulation_search = regulation_search.filter(
                'nested',
                path='product_categories',
                query=Q('terms', product_categories__id=filters['product_categories'])
            )
        if filters.get('material_categories', None):
            regulation_search = regulation_search.filter(
                'nested',
                path='material_categories',
                query=Q('terms', material_categories__id=filters['material_categories'])
            )
        if filters.get('from_date', None) and filters.get('to_date', None):
            regulation_search = regulation_search.filter(
                'nested',
                path='regulation_milestone',
                query=Q('range', regulation_milestone__from_date={'gte': filters['from_date']}) &
                      Q('range', regulation_milestone__from_date={'lte': filters['to_date']})
            )
        if filters.get('regulations', None):
            regulation_search = regulation_search.filter('terms', id=filters['regulations'])
        if filters.get('regulations', None) and filters.get('from_date', None) and filters.get('to_date', None):
            regulation_search = regulation_search.filter(Q('terms', id=filters['regulations']) & Q(
                'nested',
                path='regulation_milestone',
                query=Q('range', regulation_milestone__from_date={'gte': filters['from_date']}) &
                      Q('range', regulation_milestone__from_date={'lte': filters['to_date']})
            ))

        if filters.get('related_products', None):
            product_categories_id, material_categories_id = \
                self.get_related_products_product_category_material_category_ids(filters['related_products'])
            regulation_search = regulation_search.filter(
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=product_categories_id)) |
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=material_categories_id))
            )
        if filters.get('related_regulations', None):
            regulation_search = regulation_search.filter('terms', id=filters['related_regulations'])
        if filters.get('related_frameworks', None):
            regulation_search = regulation_search.filter(
                'terms', regulatory_framework__id=filters['related_frameworks']
            )
        if filters.get('status', None):
            regulation_search = regulation_search.filter('terms', status__id=filters['status'])

        return regulation_search

    def get_filtered_regulatory_framework_queryset(self, filters, organization_id):

        """
        apply system filters
        """
        regulatory_search = SystemFilterService().get_system_filtered_regulatory_framework_queryset(organization_id)

        '''
        user custom filters
        '''
        if filters.get('search', None):
            regulatory_search = regulatory_search.filter(
                Q('match', name=filters['search'])
            )
        if filters.get('topics', None):
            regulatory_search = regulatory_search.filter(
                'nested',
                path='topics',
                query=Q('terms', topics__id=filters['topics'])
            )
        if filters.get('regions', None):
            regulatory_search = regulatory_search.filter(
                'nested',
                path='regions',
                query=Q('terms', regions__id=filters['regions'])
            )
        if filters.get('product_categories', None):
            regulatory_search = regulatory_search.filter(
                'nested',
                path='product_categories',
                query=Q('terms', product_categories__id=filters['product_categories'])
            )
        if filters.get('material_categories', None):
            regulatory_search = regulatory_search.filter(
                'nested',
                path='material_categories',
                query=Q('terms', material_categories__id=filters['material_categories'])
            )
        if filters.get('from_date', None) and filters.get('to_date', None):
            regulatory_search = regulatory_search.filter(
                'nested',
                path='regulatory_framework_milestone',
                query=Q('range', regulatory_framework_milestone__from_date={'gte': filters['from_date']}) &
                      Q('range', regulatory_framework_milestone__from_date={'lte': filters['to_date']})
            )
        if filters.get('related_products', None):
            product_categories_id, material_categories_id = \
                self.get_related_products_product_category_material_category_ids(filters['related_products'])
            regulatory_search = regulatory_search.filter(
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=product_categories_id)) |
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=material_categories_id))
            )
        if filters.get('related_regulations', None):
            regulatory_search = regulatory_search.filter(
                'nested',
                path='regulation_regulatory_framework',
                query=Q('terms', regulation_regulatory_framework__id=filters['related_regulations'])
            )
        if filters.get('related_frameworks', None):
            regulatory_search = regulatory_search.filter('terms', id=filters['related_frameworks'])

        if filters.get('frameworks', None) and filters.get('from_date', None) and filters.get('to_date', None):
            regulatory_search = regulatory_search.filter(Q('terms', id=filters['frameworks']) & Q(
                'nested',
                path='regulatory_framework_milestone',
                query=Q('range', regulatory_framework_milestone__from_date={'gte': filters['from_date']}) &
                      Q('range', regulatory_framework_milestone__from_date={'lte': filters['to_date']})
            ))

        if filters.get('status', None):
            regulatory_search = regulatory_search.filter('terms', status__id=filters['status'])

        return regulatory_search

    @staticmethod
    def get_filtered_product_queryset(filters, product_queryset=ProductDocument.search()):
        if filters.get('related_products', None):
            product_queryset = product_queryset.filter(
                'terms', id=filters['related_products']
            )
        if filters.get('product_categories', None):
            product_queryset = product_queryset.filter(
                'nested',
                path='product_categories',
                query=Q('terms', product_categories__id=filters['product_categories'])
            )
        if filters.get('material_categories', None):
            product_queryset = product_queryset.filter(
                'nested',
                path='material_categories',
                query=Q('terms', material_categories__id=filters['material_categories'])
            )
        if filters.get('regions', None):
            product_queryset = product_queryset.filter(
                'nested',
                path='product_categories.product_cat_reg_framework.regions',
                query=Q('terms', product_categories__product_cat_reg_framework__regions__id=filters['regions'])
            ).filter(
                'nested',
                path='material_categories.material_cat_reg_framework.regions',
                query=Q('terms', material_categories__material_cat_reg_framework__regions__id=filters['regions'])
            )
        if filters.get('topics', None):
            product_queryset = product_queryset.filter(
                Q('nested',
                  path='product_categories.product_cat_reg_framework.topics',
                  query=Q('terms', product_categories__product_cat_reg_framework__topics__id=filters['topics'])) |
                Q('nested',
                  path='product_categories.product_category_news.news_categories',
                  query=Q('terms',
                          product_categories__product_category_news__news_categories__topic__id=filters['topics']))

            )

        return product_queryset

    @staticmethod
    def is_return_data(filters, content_type=None):
        if not filters['news'] and not filters['regulations'] and not filters['frameworks']:
            return True
        elif content_type == 'news' and filters['news']:
            return True
        elif content_type == 'regulations' and filters['regulations']:
            return True
        elif content_type == 'frameworks' and filters['frameworks']:
            return True
        else:
            return False

    @staticmethod
    def check_es_exception(exception):
        print(exception)
        if exception.error and exception.error == 'index_not_found_exception':
            try:
                # turned off due to it takes too long time.
                # p = subprocess.call(['sh', './rebuild.sh'])
                return True
            except:
                return False
        else:
            return False

    @staticmethod
    def get_related_products_product_category_material_category_ids(product_id_list):
        """
        This function take list of product IDs and return their products_category_id & material_category_id list
        :param list product_id_list: Required. list of product IDs(list).
        """
        product_categories_id = []
        product_category_doc_qs: ProductCategoryDocument = ProductCategoryDocument.search().filter(
            'nested',
            path='product_product_categories',
            query=Q('terms', product_product_categories__id=product_id_list)
        ).source(['id'])
        product_category_doc_qs = product_category_doc_qs[0:product_category_doc_qs.count()]
        for product_category in product_category_doc_qs:
            product_categories_id.append(product_category.id)

        material_categories_id = []
        material_category_doc_qs: MaterialCategoryDocument = MaterialCategoryDocument.search().filter(
            'nested',
            path='product_material_categories',
            query=Q('terms', product_material_categories__id=product_id_list)
        ).source(['id'])
        material_category_doc_qs = material_category_doc_qs[0:material_category_doc_qs.count()]
        for material_category in material_category_doc_qs:
            material_categories_id.append(material_category.id)

        return product_categories_id, material_categories_id

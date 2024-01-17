from elasticsearch_dsl import Q

from django.core.cache import cache as django_cache
from django.conf import settings

from rttproduct.documents import ProductCategoryDocument, MaterialCategoryDocument
from rttproduct.services.product_services import ProductServices
from rttorganization.documents import OrganizationDocument


class OrganizationService:
    @staticmethod
    def get_organization_product_category_ids(organization_id):
        """
        params:
        organization_id : user organization_id (int)

        Return a list of product_category_ids which product_category or their children have at least one product
        """

        cache_data = django_cache.get('organization_product_categories_{}'.format(organization_id))
        # print('product_categories', cache_data)
        if cache_data:
            return cache_data

        organization_product_categories = ProductCategoryDocument.search().filter(
            'nested',
            path='product_product_categories',
            query=Q('match', product_product_categories__organization__id=organization_id)
        ).source(['id', 'parent'])
        organization_product_categories = organization_product_categories[0: organization_product_categories.count()]
        organization_product_category_ids = set()
        for product_category in organization_product_categories:
            all_parent_list = ProductServices().get_all_parent_product_category_ids(product_category)
            organization_product_category_ids.update(all_parent_list)

        organization_product_category_ids = list(organization_product_category_ids)

        '''
        set data into django cache
        '''
        django_cache.set('organization_product_categories_{}'.format(organization_id),
                         organization_product_category_ids, settings.DJANGO_CACHE_TIMEOUT)

        return organization_product_category_ids

    @staticmethod
    def get_organization_material_category_ids(organization_id):
        """
        params:
        organization_id : user organization_id (int)

        Return a list of material_categories_ids which material_category have at least one product
        """

        cache_data = django_cache.get('organization_material_categories_{}'.format(organization_id))
        # print('material_categories', cache_data)
        if cache_data:
            return cache_data

        organization_material_categories = MaterialCategoryDocument.search().filter(
            'nested',
            path='product_material_categories',
            query=Q('match', product_material_categories__organization__id=organization_id)
        ).source(['id'])
        organization_material_categories = organization_material_categories[0: organization_material_categories.count()]
        organization_material_categories_ids = list({v['id']: v for v in organization_material_categories})

        '''
        set data into django cache
        '''
        django_cache.set('organization_material_categories_{}'.format(organization_id),
                         organization_material_categories_ids, settings.DJANGO_CACHE_TIMEOUT)

        return organization_material_categories_ids

    @staticmethod
    def get_relevant_organizations(filters):

        regulations_ids = []
        frameworks_ids = []
        topic_ids = []

        if filters.get('regulations', None):
            regulations_ids = filters['regulations']
        if filters.get('frameworks', None):
            frameworks_ids = filters['frameworks']
        if filters.get('topics', None):
            topic_ids = filters['topics']

        product_categories_queryset = ProductCategoryDocument.search().filter(
            Q('nested',
              path='regulation_product_categories',
              query=Q('terms', regulation_product_categories__id=regulations_ids)) |
            Q('nested',
              path='product_cat_reg_framework',
              query=Q('terms', product_cat_reg_framework__id=frameworks_ids))
        ).source(['id'])
        product_categories_queryset = product_categories_queryset[0: product_categories_queryset.count()]
        product_category_ids = set()
        product_category_ids.update(filters['product_categories'])
        for product_category in product_categories_queryset:
            product_category_ids.add(product_category['id'])
        get_all_child_list = ProductServices().get_all_tree_child_product_category_ids(
            list(product_category_ids))
        product_category_ids = set()
        product_category_ids.update(get_all_child_list)
        product_category_ids = list(product_category_ids)

        material_categories_queryset = MaterialCategoryDocument.search().filter(
            Q('nested',
              path='regulation_material_categories',
              query=Q('terms', regulation_material_categories__id=regulations_ids)) |
            Q('nested',
              path='material_cat_reg_framework',
              query=Q('terms', material_cat_reg_framework__id=frameworks_ids))
        ).source(['id'])
        material_categories_queryset = material_categories_queryset[0: material_categories_queryset.count()]
        material_categories_ids = set()
        material_categories_ids.update(filters['material_categories'])
        material_categories_ids.update({v['id']: v for v in material_categories_queryset})
        material_categories_ids = list(material_categories_ids)

        if product_category_ids or material_categories_ids or regulations_ids or frameworks_ids:
            topic_ids = []

        organization_document_queryset = OrganizationDocument.search().filter(
            Q('nested',
              path='product_organization.product_categories',
              query=Q('terms', product_organization__product_categories__id=product_category_ids)) |
            Q('nested',
              path='product_organization.material_categories',
              query=Q('terms', product_organization__material_categories__id=material_categories_ids)) |
            Q('nested',
              path='industries.topics',
              query=Q('terms', industries__topics__id=topic_ids))
        )

        return organization_document_queryset

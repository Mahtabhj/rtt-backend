from elasticsearch_dsl import Q

from rttproduct.models.models import ProductCategory
from rttregulation.documents import RegulatoryFrameworkDocument, RegulationDocument


class ProductServices:

    def get_all_parent_product_category_ids(self, product_category, product_category_ids=None):
        """
        params:
        product_category : django product category object

        Return all parent product category id list (including params product_category id)
        """
        if product_category_ids is None:
            product_category_ids = []
        product_category_ids.append(product_category.id)
        if product_category.parent:
            if isinstance(product_category.parent, ProductCategory):
                self.get_all_parent_product_category_ids(product_category.parent, product_category_ids)
            else:
                parent_product_category = ProductCategory.objects.get(id=product_category.parent.id)
                self.get_all_parent_product_category_ids(parent_product_category, product_category_ids)
        return product_category_ids

    def get_all_parent_product_category_list(self, product_category, product_category_list=None):
        """
        params:
        product_category : django product category object

        Return all parent product category object list (including params product_category object)
        """
        if product_category_list is None:
            product_category_list = []
        if not isinstance(product_category, ProductCategory):
            product_category = ProductCategory.objects.get(id=product_category.id)

        product_category_list.append(product_category)

        if product_category.parent:
            if isinstance(product_category.parent, ProductCategory):
                self.get_all_parent_product_category_list(product_category.parent, product_category_list)
            else:
                parent_product_category = ProductCategory.objects.get(id=product_category.parent.id)
                self.get_all_parent_product_category_list(parent_product_category, product_category_list)
        return product_category_list

    def get_all_tree_child_product_category_ids(self, parent_id_or_list, product_category_ids=None):
        """
        params:
        parent_id_or_list : a single product category id or a list of product category ids

        Return all child product category id list (including params parent_id_or_list)
        """
        if parent_id_or_list and isinstance(parent_id_or_list, int):
            parent_id_or_list = [parent_id_or_list]
        if product_category_ids is None:
            product_category_ids = []
        product_category_ids.extend(parent_id_or_list)
        child_qs = ProductCategory.objects.filter(parent_id__in=parent_id_or_list).values_list('id', flat=True)
        if child_qs:
            new_parents = list(child_qs)
            self.get_all_tree_child_product_category_ids(new_parents, product_category_ids)
        return list(set(product_category_ids))

    @staticmethod
    def get_all_frameworks(organization_id, product_category_ids=None, material_category_ids=None):
        """
        params:
        product_category_ids : list of ids
        material_category_ids : list of ids

        Return elasticsearch_dsl search queryset of RegulatoryFrameworkDocument
        """
        if material_category_ids is None:
            material_category_ids = []
        if product_category_ids is None:
            product_category_ids = []

        framework_qs = RegulatoryFrameworkDocument.search().filter(Q('match', review_status='o'))
        # apply mute-unmute filter
        framework_qs = framework_qs.filter(
            Q('nested',
              path='regulation_mute_framework',
              query=(Q('match', regulation_mute_framework__organization__id=organization_id) &
                     Q('match', regulation_mute_framework__is_muted=False))) |
            ~Q('nested',
               path='regulation_mute_framework',
               query=(Q('match', regulation_mute_framework__organization__id=organization_id) &
                      Q('exists', field='regulation_mute_framework')))
        )
        framework_qs = framework_qs.filter(
            Q('nested',
              path='product_categories',
              query=Q('terms', product_categories__id=product_category_ids)) |
            Q('nested',
              path='material_categories',
              query=Q('terms', material_categories__id=material_category_ids)
              ) |
            # related regulations material_categories
            Q(Q('nested',
                path='regulation_regulatory_framework',
                query=Q('match', regulation_regulatory_framework__review_status='o')) &
              Q('nested',
                path='regulation_regulatory_framework.material_categories',
                query=Q('terms',
                        regulation_regulatory_framework__material_categories__id=material_category_ids))
              ) |
            # related regulations product_categories
            Q(Q('nested',
                path='regulation_regulatory_framework',
                query=Q('match', regulation_regulatory_framework__review_status='o')) &
              Q('nested',
                path='regulation_regulatory_framework.product_categories',
                query=Q('terms',
                        regulation_regulatory_framework__product_categories__id=product_category_ids))
              )
        )
        return framework_qs

    @staticmethod
    def get_all_regulations(organization_id, product_category_ids=None, material_category_ids=None):
        """
        params:
        product_category_ids : list of ids
        material_category_ids : list of ids

        Return elasticsearch_dsl search queryset of RegulationDocument
        """

        if material_category_ids is None:
            material_category_ids = []
        if product_category_ids is None:
            product_category_ids = []

        regulation_qs = RegulationDocument.search().filter(Q('match', review_status='o'))
        regulation_qs = regulation_qs.filter(
            Q('nested',
              path='regulation_mute_regulation',
              query=(Q('match', regulation_mute_regulation__organization__id=organization_id) &
                     Q('match', regulation_mute_regulation__is_muted=False))) |
            ~Q('nested',
               path='regulation_mute_regulation',
               query=(Q('match', regulation_mute_regulation__organization__id=organization_id) &
                      Q('exists', field='regulation_mute_regulation')))
        )
        regulation_qs = regulation_qs.filter(
            Q('nested',
              path='product_categories',
              query=Q('terms', product_categories__id=product_category_ids)) |
            Q('nested',
              path='material_categories',
              query=Q('terms', material_categories__id=material_category_ids)
              )
        )
        return regulation_qs

    @staticmethod
    def get_related_product_filtered_queryset(filters, product_queryset):
        if filters.get('related_products', None):
            product_queryset = product_queryset.filter(
                'terms', id=filters['related_products']
            )
        product_queryset = product_queryset.filter(
            Q('nested',
              path='product_categories',
              query=Q('terms', product_categories__id=filters['product_categories'])) |
            Q('nested',
              path='material_categories',
              query=Q('terms', material_categories__id=filters['material_categories']))
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
    def get_filtered_news_queryset(search_keyword, filters, news_queryset):
        if search_keyword:
            news_queryset = news_queryset.filter(
                # search on news_title
                Q('match', title=search_keyword)
            )
        if filters.get('topics', None):
            news_queryset = news_queryset.filter(
                Q('nested',
                  path='news_categories',
                  query=Q('terms', news_categories__topic__id=filters['topics']))
            )
        # filter by regulations
        if filters.get('regulations', None):
            news_queryset = news_queryset.filter(
                'nested',
                path='regulations',
                query=Q('terms', regulations__id=filters['regulations'])
            )

        # filter by frameworks
        if filters.get('frameworks', None):
            news_queryset = news_queryset.filter(
                'nested',
                path='regulatory_frameworks',
                query=Q('terms', regulatory_frameworks__id=filters['frameworks'])
            )

        return news_queryset

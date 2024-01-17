import logging

from elasticsearch_dsl import Q as Q

from rttnews.documents import NewsDocument
from rttproduct.documents import ProductCategoryDocument, MaterialCategoryDocument
from rttorganization.documents import OrganizationDocument
from rttregulation.models.core_models import Topic
from rttproduct.services.product_services import ProductServices
from bs4 import BeautifulSoup


class NewsService:

    @staticmethod
    def get_news_body_documents(news_body):
        file_list = []
        extensions_to_check = ('.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx')
        soup = BeautifulSoup(news_body, 'html.parser')
        for a in soup.find_all('a'):
            try:
                href_split = a['href'].split('/')
                if href_split[-1].lower().endswith(extensions_to_check):
                    file_list.append({
                        'title': a.text,
                        'link': a['href']
                    })
            except Exception as ex:
                logging.error(str(ex), exc_info=True)
        return file_list

    @staticmethod
    def get_relevant_organization_queryset_by_news(news_id):
        """
        Takes a single news_id(date_type --> integer) of a news.
        Returns a queryset of organization(organization_document_queryset) where news_id is belong to that.
        """
        news_document: NewsDocument = NewsDocument.search().filter('match', id=news_id)
        if news_document.count() == 0:
            return None
        news_regulations_ids = []
        news_frameworks_ids = []
        for new_doc in news_document:
            for regulations_dict in new_doc.regulations:
                news_regulations_ids.append(regulations_dict['id'])
            for regulatory_frameworks_dict in new_doc.regulatory_frameworks:
                news_frameworks_ids.append(regulatory_frameworks_dict['id'])

        news_product_categories = ProductCategoryDocument.search().filter(
            Q('nested',
              path='product_category_news',
              query=Q('match', product_category_news__id=news_id)) |
            Q('nested',
              path='regulation_product_categories',
              query=Q('terms', regulation_product_categories__id=news_regulations_ids)) |
            Q('nested',
              path='product_cat_reg_framework',
              query=Q('terms', product_cat_reg_framework__id=news_frameworks_ids))
        ).source(['id'])

        news_product_categories = news_product_categories[0: news_product_categories.count()]
        news_product_category_ids = set()
        for product_category in news_product_categories:
            news_product_category_ids.add(product_category['id'])
        get_all_child_list = ProductServices().get_all_tree_child_product_category_ids(
            list(news_product_category_ids))
        news_product_category_ids = set()
        news_product_category_ids.update(get_all_child_list)
        news_product_category_ids = list(news_product_category_ids)

        news_material_categories = MaterialCategoryDocument.search().filter(
            Q('nested',
              path='material_category_news',
              query=Q('match', material_category_news__id=news_id)) |
            Q('nested',
              path='regulation_material_categories',
              query=Q('terms', regulation_material_categories__id=news_regulations_ids)) |
            Q('nested',
              path='material_cat_reg_framework',
              query=Q('terms', material_cat_reg_framework__id=news_frameworks_ids))
        ).source(['id'])
        news_material_categories = news_material_categories[0: news_material_categories.count()]
        news_material_categories_ids = list({v['id']: v for v in news_material_categories})

        new_topic_ides = []
        if not news_regulations_ids and not news_frameworks_ids and not news_product_category_ids \
                and not news_material_categories_ids:
            news_topic_queryset = Topic.objects.filter(news_category_topic__news_categories=news_id).distinct()
            news_topic_queryset = news_topic_queryset[0:news_topic_queryset.count()]
            for news_topic in news_topic_queryset:
                new_topic_ides.append(news_topic.id)

        organization_document_queryset = OrganizationDocument.search().filter(
            Q('nested',
              path='product_organization.product_categories',
              query=Q('terms', product_organization__product_categories__id=news_product_category_ids)) |
            Q('nested',
              path='product_organization.material_categories',
              query=Q('terms', product_organization__material_categories__id=news_material_categories_ids)) |
            Q('nested',
              path='industries.topics',
              query=Q('terms', industries__topics__id=new_topic_ides))
        )
        return organization_document_queryset

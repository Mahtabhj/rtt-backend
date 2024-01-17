import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttproduct.documents import ProductDocument
from rttnews.documents import NewsDocument
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.serializers.serializers import TopicIdNameSerializer
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttproduct.services.product_services import ProductServices
from rttcore.services.id_search_service import IdSearchService

from elasticsearch_dsl import Q

logger = logging.getLogger(__name__)


class ProductRelatedNewsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    rating_search_service = RatingSearchService()

    def get(self, request, product_id):
        news_list = []
        organization = request.user.organization
        product_queryset = ProductDocument.search().filter('match', id=product_id)
        if not product_queryset:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        search_keyword = request.GET.get('search', None)
        skip = int(request.GET.get('skip', 0))
        limit = int(request.GET.get('limit', 10))
        sort_order = request.GET.get('sort_order', 'desc')

        regulations = request.GET.get('regulations', None)
        regulations = [int(item) for item in regulations.split(',')] if regulations else None

        frameworks = request.GET.get('frameworks', None)
        frameworks = [int(item) for item in frameworks.split(',')] if frameworks else None

        topics = request.GET.get('topics', None)
        topics = [int(item) for item in topics.split(',')] if topics else None

        filters = {
            'regulations': regulations,
            'frameworks': frameworks,
            'topics': topics
        }

        product_categories_ids = set()
        material_categories_ids = []
        for product_qs in product_queryset:
            for product_categories in product_qs.product_categories:
                all_parent_list = ProductServices().get_all_parent_product_category_ids(product_categories)
                product_categories_ids.update(all_parent_list)
            for material_categories in product_qs.material_categories:
                material_categories_ids.append(material_categories.id)
        product_categories_ids = list(product_categories_ids)
        news_queryset = NewsDocument.search().filter(
            Q('bool',
              must=[Q('match', active=True), Q('match', status='s')],
              should=[Q('nested',
                        path='product_categories',
                        query=Q('terms', product_categories__id=product_categories_ids)),
                      Q('nested',
                        path='material_categories',
                        query=Q('terms', material_categories__id=material_categories_ids))
                      ],
              minimum_should_match=1
              )
        )
        news_queryset = ProductServices().get_filtered_news_queryset(search_keyword, filters, news_queryset)
        count = news_queryset.count()
        news_queryset = news_queryset[skip:skip+limit]
        news_queryset = news_queryset.sort({
            "news_relevance.relevancy": {
                "order": sort_order,
                "nested_path": "news_relevance",
                "nested_filter": {
                    "term": {
                        "news_relevance.organization.id": organization.id
                    }
                }
            }
        }, {"pub_date": {"order": "desc"}})

        for news in news_queryset:
            data = self.get_news_object(news, organization.id)
            data['impact_rating'] = self.rating_search_service.get_news_rating_obj(organization.id, news.id)
            news_list.append(data)

        response = {
            'count': count,
            'results': news_list
        }
        return Response(response, status=status.HTTP_200_OK)

    @staticmethod
    def get_news_object(news, organization_id):
        relevant_regulation_ids_organization = RelevantRegulationService(). \
            get_relevant_regulation_id_organization(organization_id)
        relevant_regulatory_framework_ids_organization = RelevantRegulationService(). \
            get_relevant_regulatory_framework_id_organization(organization_id)

        relative_news_regulations = []
        relative_news_regulatory_framework = []
        relevant_regulation = list(filter(lambda rel_regulation:
                                          rel_regulation.id in relevant_regulation_ids_organization, news.regulations))
        for regulation in relevant_regulation:
            regulation_obj = {
                'id': regulation.id,
                'name': regulation.name,
                'status': regulation.status.name
            }
            relative_news_regulations.append(regulation_obj)

        relevant_regulatory_framework = list(filter(lambda reg_fw:
                                                    reg_fw.id in relevant_regulatory_framework_ids_organization,
                                                    news.regulatory_frameworks))
        for reg_framework in relevant_regulatory_framework:
            reg_framework_obj = {
                'id': reg_framework.id,
                'name': reg_framework.name
            }
            relative_news_regulatory_framework.append(reg_framework_obj)

        data = {
            'id': news.id,
            'title': news.title,
            'date': news.pub_date,
            'body': news.body,
            'source': {
                'id': news.source.id,
                'name': news.source.name,
                'image': news.source.image if news.source.image else None
            },
            'cover_image': news.cover_image if news.cover_image else None,
            'status': news.status,
            'active': news.active,
            'regions': [{'id': region.id, 'name': region.name} for region in news.regions],
            'topics': [],
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id,
                news.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id,
                news.material_categories, serialize=True),
            'regulations': relative_news_regulations,
            'frameworks': relative_news_regulatory_framework
        }
        for news_category in news.news_categories:
            if news_category.topic:
                topic_obj = {
                    'id': news_category.topic.id,
                    'name': news_category.topic.name
                }
                if topic_obj not in data['topics']:
                    data['topics'].append(topic_obj)
        return data


class ProductRelatedNewsFilterOptionsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, product_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1234
        """
        try:
            product_queryset = ProductDocument.search().filter('match', id=product_id)
            if not product_queryset:
                return Response({}, status=status.HTTP_204_NO_CONTENT)

            search_keyword = request.GET.get('search', None)

            regulations = request.GET.get('regulations', None)
            regulations = [int(item) for item in regulations.split(',')] if regulations else None

            frameworks = request.GET.get('frameworks', None)
            frameworks = [int(item) for item in frameworks.split(',')] if frameworks else None

            topics = request.GET.get('topics', None)
            topics = [int(item) for item in topics.split(',')] if topics else None

            filters = {
                'regulations': regulations,
                'frameworks': frameworks,
                'topics': topics
            }
            organization_id = request.user.organization_id
            """
            news data
            """
            rel_reg_ids = RelevantRegulationService().get_relevant_regulation_id_organization(organization_id)
            rel_fw_ids = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(organization_id)
            framework_list = []
            visited_framework = {}
            regulations_list = []
            visited_regulation = {}
            topics_list = []
            visited_topics = {}

            product_categories_ids = set()
            material_categories_ids = []
            for product_qs in product_queryset:
                for product_categories in product_qs.product_categories:
                    all_parent_list = ProductServices().get_all_parent_product_category_ids(product_categories)
                    product_categories_ids.update(all_parent_list)
                for material_categories in product_qs.material_categories:
                    material_categories_ids.append(material_categories.id)
            product_categories_ids = list(product_categories_ids)

            news_doc_qs = NewsDocument.search().filter(
                Q('bool',
                  must=[Q('match', active=True), Q('match', status='s')],
                  should=[Q('nested',
                            path='product_categories',
                            query=Q('terms', product_categories__id=product_categories_ids)),
                          Q('nested',
                            path='material_categories',
                            query=Q('terms', material_categories__id=material_categories_ids))
                          ],
                  minimum_should_match=1
                  )
            )
            news_doc_qs = ProductServices().get_filtered_news_queryset(search_keyword, filters, news_doc_qs)
            news_doc_qs = news_doc_qs[0:news_doc_qs.count()]

            for news in news_doc_qs:
                for framework in news.regulatory_frameworks:
                    if IdSearchService().does_id_exit_in_sorted_list(rel_fw_ids, framework.id) and str(framework.id) \
                            not in visited_framework:
                        framework_list.append({
                            'id': framework.id,
                            'name': framework.name
                        })
                        visited_framework[str(framework.id)] = True
                for regulation in news.regulations:
                    if IdSearchService().does_id_exit_in_sorted_list(rel_reg_ids, regulation.id) and \
                            str(regulation.id) not in visited_regulation:
                        regulations_list.append({
                            'id': regulation.id,
                            'name': regulation.name
                        })
                        visited_regulation[str(regulation.id)] = True
                for news_category in news.news_categories:
                    if news_category.topic and str(news_category.topic.id) not in visited_topics:
                        topics_list.append({
                            'id': news_category.topic.id,
                            'name': news_category.topic.name
                        })
                        visited_topics[str(news_category.topic.id)] = True
            response = {
                'frameworks': framework_list,
                'regulations': regulations_list,
                'topics': topics_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

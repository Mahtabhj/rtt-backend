from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttproduct.documents import ProductDocument
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttproduct.services.product_services import ProductServices
from rttregulation.documents import RegulatoryFrameworkDocument, RegulationDocument
from rttregulation.serializers.serializers import RegionIdNameSerializer
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_topic_service import RelevantTopicService
from rttcore.services.id_search_service import IdSearchService
from rttcore.services.system_filter_service import SystemFilterService


class ProductRelatedFrameworksApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, product_id):
        framework_list = []
        regions = request.data.get('regions', None)
        topics = request.data.get('topics', None)
        search_keyword = request.data.get('search', None)
        sort_order = request.data.get('sort_order', 'desc')
        limit = request.data.get('limit', 10)
        skip = request.data.get('skip', 0)

        product_search_qs = ProductDocument.search().filter('match', id=product_id)
        if not product_search_qs:
            return Response(status=status.HTTP_204_NO_CONTENT)

        organization_id = request.user.organization_id
        relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)
        product_categories_ids = []
        material_categories_ids = []
        for product_search in product_search_qs:
            for product_category in product_search.product_categories:
                product_categories_ids.extend(ProductServices().get_all_parent_product_category_ids(product_category))
            for material_category in product_search.material_categories:
                material_categories_ids.append(material_category.id)

        # get framework_id_list which are directly tagged with mat_cat or product_cat
        fw_level_tag_id_list = get_mat_cat_product_cat_tagged_framework_id_list(organization_id, product_categories_ids,
                                                                                material_categories_ids)
        framework_qs = get_related_framework_filter(regions, topics, product_categories_ids,
                                                    material_categories_ids, request.user.organization_id,
                                                    search_keyword)
        framework_qs = framework_qs.sort({
            "regulatory_framework_rating.rating": {
                "order": sort_order,
                "nested_path": "regulatory_framework_rating",
                "nested_filter": {
                    "term": {
                        "regulatory_framework_rating.organization.id": organization_id
                    }
                }
            }
        })
        count = framework_qs.count()
        framework_qs = framework_qs[skip:skip + limit]

        '''regulatory framework data'''
        for framework in framework_qs:
            framework_obj = self.__get_related_framework_object(framework, organization_id, relevant_topics_ids)
            '''regulation data'''
            regulations = []
            related_frameworks = [framework.id]
            fw_level_tag = IdSearchService().does_id_exit_in_sorted_list(fw_level_tag_id_list, framework.id)
            regulation_doc_qs = get_related_regulation_filter(regions, topics, product_categories_ids,
                                                              material_categories_ids, organization_id,
                                                              related_frameworks, search_keyword, fw_level_tag)
            regulation_doc_qs = regulation_doc_qs.sort({
                "regulation_rating.rating": {
                    "order": sort_order,
                    "nested_path": "regulation_rating",
                    "nested_filter": {
                        "term": {
                            "regulation_rating.organization.id": organization_id
                        }
                    }
                }
            })
            regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
            for regulation in regulation_doc_qs:
                topic_list = []
                for topic in regulation.topics:
                    if topic.id in relevant_topics_ids:
                        topic_list.append({'id': topic.id, 'name': topic.name})
                regulation_obj = {
                    'id': regulation.id,
                    'name': regulation.name,
                    'status': {'id': regulation.status.id, 'name': regulation.status.name},
                    'topics': topic_list,
                    'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                        organization_id, regulation.product_categories, serialize=True),
                    'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                        organization_id, regulation.material_categories, serialize=True),
                    'impact_rating': RatingSearchService().get_regulation_rating_obj(organization_id, regulation.id)
                }
                regulations.append(regulation_obj)
            framework_obj['regulations'] = regulations
            framework_list.append(framework_obj)

        response = {
            'count': count,
            'results': framework_list
        }
        return Response(response, status=status.HTTP_200_OK)

    @staticmethod
    def __get_related_framework_object(framework, organization_id, relevant_topics_ids):
        issuing_body = {}
        if framework.issuing_body:
            issuing_body = {'id': framework.issuing_body.id, 'name': framework.issuing_body.name}
        framework_topics = []
        for topic in framework.topics:
            if topic.id in relevant_topics_ids:
                framework_topics.append({'id': topic.id, 'name': topic.name})
        framework_obj = {
            'id': framework.id,
            'name': framework.name,
            'description': framework.description,
            'status': framework.status.name,
            'issuing_body': issuing_body,
            'regions': RegionIdNameSerializer(framework.regions, many=True).data,
            'topics': framework_topics,
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id,
                framework.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id,
                framework.material_categories, serialize=True),
            'impact_rating': RatingSearchService().get_framework_rating_obj(organization_id, framework.id,
                                                                            framework.regulatory_framework_rating),
        }
        return framework_obj


class ProductDetailFilterOptionsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, product_id):
        regions = request.data.get('regions', None)
        topics = request.data.get('topics', None)
        search_keyword = request.data.get('search', None)
        response = {'regions': [], 'topics': []}
        visited_topic_id = {}
        visited_region_id = {}

        product_search_qs = ProductDocument.search().filter('match', id=product_id)

        if not product_search_qs:
            return Response(status=status.HTTP_204_NO_CONTENT)

        product_categories_ids = []
        material_categories_ids = []
        for product_search in product_search_qs:
            for product_categories in product_search.product_categories:
                product_categories_ids.extend(ProductServices().get_all_parent_product_category_ids(product_categories))
            for material_categories in product_search.material_categories:
                material_categories_ids.append(material_categories.id)

        regulatory_framework_queryset = get_related_framework_filter(regions, topics, product_categories_ids,
                                                                     material_categories_ids,
                                                                     request.user.organization_id, search_keyword)
        regulatory_framework_queryset = regulatory_framework_queryset[0:regulatory_framework_queryset.count()]
        organization_id = request.user.organization_id
        # get framework_id_list which are directly tagged with mat_cat or product_cat
        fw_level_tag_id_list = get_mat_cat_product_cat_tagged_framework_id_list(organization_id,
                                                                                product_categories_ids,
                                                                                material_categories_ids)
        relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)
        for regulatory_framework in regulatory_framework_queryset:
            related_frameworks = [regulatory_framework.id]
            for region in regulatory_framework.regions:
                if str(region.id) not in visited_region_id:
                    visited_region_id[str(region.id)] = True
                    region_obj = {'id': region.id, 'name': region.name}
                    response['regions'].append(region_obj)
            for topic in regulatory_framework.topics:
                if IdSearchService().does_id_exit_in_sorted_list(relevant_topics_ids, topic.id):
                    if str(topic.id) not in visited_topic_id:
                        visited_topic_id[str(topic.id)] = True
                        topic_obj = {'id': topic.id, 'name': topic.name}
                        response['topics'].append(topic_obj)

            fw_level_tag = IdSearchService.does_id_exit_in_sorted_list(fw_level_tag_id_list, regulatory_framework.id)
            regulation_doc_qs = get_related_regulation_filter(regions, topics, product_categories_ids,
                                                              material_categories_ids, organization_id,
                                                              related_frameworks, search_keyword, fw_level_tag)
            regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]

            for regulation in regulation_doc_qs:
                for topic in regulation.topics:
                    if IdSearchService().does_id_exit_in_sorted_list(relevant_topics_ids, topic.id):
                        if str(topic.id) not in visited_topic_id:
                            topic_obj = {'id': topic.id, 'name': topic.name}
                            response['topics'].append(topic_obj)

        return Response(response, status=status.HTTP_200_OK)


def get_related_framework_filter(regions, topics, product_categories_ids, material_categories_ids, organization_id,
                                 search_keyword=None):
    framework_qs = ProductServices().get_all_frameworks(organization_id,
                                                        product_categories_ids, material_categories_ids)
    # search keyword in framework and regulation name
    if search_keyword:
        framework_qs = framework_qs.filter(
            # search on framework_name
            Q('match', name=search_keyword) |
            # search on regulation_name
            Q('nested',
              path='regulation_regulatory_framework',
              query=Q('match', regulation_regulatory_framework__name=search_keyword))
        )

    # filter by regions
    if regions:
        framework_qs = framework_qs.filter(
            'nested',
            path='regions',
            query=Q('terms', regions__id=regions)
        )

    # filter by topic
    if topics:
        framework_qs = framework_qs.filter(
            # topic filter on framework
            Q('nested',
              path='topics',
              query=Q('terms', topics__id=topics)) |
            # topic filter on regulation
            Q('nested',
              path='regulation_regulatory_framework.topics',
              query=Q('terms', regulation_regulatory_framework__topics__id=topics))
        )

    return framework_qs


def get_related_regulation_filter(regions, topics, product_categories_ids, material_categories_ids, organization_id,
                                  related_frameworks_list, search_keyword, fw_level_tag):
    regulation_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(organization_id)
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
    # filter by related_frameworks
    regulation_qs = regulation_qs.filter(
        Q('terms', regulatory_framework__id=related_frameworks_list)
    )
    if not fw_level_tag:
        regulation_qs = regulation_qs.filter(
            Q('nested',
              path='product_categories',
              query=Q('terms', product_categories__id=product_categories_ids)) |
            Q('nested',
              path='material_categories',
              query=Q('terms', material_categories__id=material_categories_ids))
        )

    # search keyword in regulation name
    if search_keyword:
        regulation_qs = regulation_qs.filter(
            Q('match', name=search_keyword)
        )

    # filter by regions
    if regions:
        regulation_qs = regulation_qs.filter(
            Q('nested',
              path='regulatory_framework.regions',
              query=Q('terms', regulatory_framework__regions__id=regions))
        )

    # filter by topics
    if topics:
        regulation_qs = regulation_qs.filter(
            Q('nested',
              path='topics',
              query=Q('terms', topics__id=topics))
        )

    return regulation_qs


def get_mat_cat_product_cat_tagged_framework_id_list(organization_id, product_category_ids, material_category_ids):
    results = []

    framework_qs = RegulatoryFrameworkDocument.search().filter(Q('match', review_status='o')).source(['id']).sort('id')

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

    # get framework which are directly tagged with mat_cat or product_cat
    framework_qs = framework_qs.filter(
        Q('nested',
          path='product_categories',
          query=Q('terms', product_categories__id=product_category_ids)) |
        Q('nested',
          path='material_categories',
          query=Q('terms', material_categories__id=material_category_ids))
    )
    framework_qs = framework_qs[0:framework_qs.count()]
    for framework in framework_qs:
        results.append(framework.id)

    return results

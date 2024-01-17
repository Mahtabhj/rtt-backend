from elasticsearch_dsl import Q

from rttcore.services.id_search_service import IdSearchService
from rttcore.services.system_filter_service import SystemFilterService
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.models.models import RegulationMute
from rttregulation.serializers.serializers import TopicIdNameSerializer, RegionIdNameSerializer
from rttregulation.services.rating_search_service import RatingSearchService
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService


class RegulatoryFrameworkContentService:
    def __init__(self, organization_id):
        self.organization_id = organization_id

    def get_filtered_regulatory_framework_queryset(self, topics, products, materials, regions, is_muted=False,
                                                   regulatory_frameworks=None, apply_mute_filter=True,
                                                   apply_regulation_mute=False, status=None):
        # apply system filter
        framework_queryset = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            self.organization_id, is_muted, apply_mute_filter, apply_regulation_mute)

        # apply system filter for getting reg doc to generate relevant reg_id
        regulation_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(
            self.organization_id, is_muted, apply_mute_filter).source(['id'])
        regulation_id_list = []
        for regulation in regulation_doc_qs:
            regulation_id_list.append(regulation.id)

        # filter by framework on framework_es_doc
        if regulatory_frameworks:
            framework_queryset = framework_queryset.filter(
                Q('terms', id=regulatory_frameworks)
            )
        # filter by related topic on framework_es_doc
        if topics:
            framework_queryset = framework_queryset.filter(
                # topic filter on framework
                Q('nested',
                  path='topics',
                  query=Q('terms', topics__id=topics)) |
                # topic filter on regulation
                Q(Q('nested',
                  path='regulation_regulatory_framework.topics',
                  query=Q('terms', regulation_regulatory_framework__topics__id=topics)) &
                  Q('nested',
                    path='regulation_regulatory_framework',
                    query=Q('terms', regulation_regulatory_framework__id=regulation_id_list)))
            )
        # filter by related product_category on framework_es_doc
        if products:
            framework_queryset = framework_queryset.filter(
                # product_categories filter on framework
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=products)) |
                # product_categories filter on regulation
                Q(Q('nested',
                  path='regulation_regulatory_framework.product_categories',
                  query=Q('terms', regulation_regulatory_framework__product_categories__id=products)) &
                  Q('nested',
                    path='regulation_regulatory_framework',
                    query=Q('terms', regulation_regulatory_framework__id=regulation_id_list)))
            )

        # filter by related material_cat on framework_es_doc
        if materials:
            framework_queryset = framework_queryset.filter(
                # material_categories filter on framework
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=materials)) |
                # material_categories filter on regulation
                Q(Q('nested',
                  path='regulation_regulatory_framework.material_categories',
                  query=Q('terms', regulation_regulatory_framework__material_categories__id=materials)) &
                  Q('nested',
                    path='regulation_regulatory_framework',
                    query=Q('terms', regulation_regulatory_framework__id=regulation_id_list)))
            )
        # filter by related region on framework_es_doc
        if regions:
            framework_queryset = framework_queryset.filter(
                'nested',
                path='regions',
                query=Q('terms', regions__id=regions)
            )

        # filter by status on framework_es_doc
        if status:
            framework_queryset = framework_queryset.filter(
                # status filter on framework
                Q('terms', status__id=status) |
                # status filter on regulation
                Q('nested',
                  path='regulation_regulatory_framework',
                  query=Q('terms', regulation_regulatory_framework__status__id=status) &
                        Q('terms', regulation_regulatory_framework__id=regulation_id_list))
            )

        return framework_queryset

    def get_filtered_regulation_queryset(self, topics, products, materials, regions, is_muted=False,
                                         regulatory_frameworks=None, apply_mute_filter=True, status=None):

        regulation_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(
            self.organization_id, is_muted, apply_mute_filter)

        # filter by related regulatory_framework on regulation_es_doc
        if regulatory_frameworks:
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('terms', regulatory_framework__id=regulatory_frameworks)
            )

        # filter by related topic on regulation_es_doc
        if topics:
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='topics',
                  query=Q('terms', topics__id=topics))
            )

        # filter by related product_categories on regulation_es_doc
        if products:
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='product_categories',
                  query=Q('terms', product_categories__id=products))
            )

        # filter by related material_categories on regulation_es_doc
        if materials:
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='material_categories',
                  query=Q('terms', material_categories__id=materials))
            )

        # filter by related region on regulation_es_doc
        if regions:
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('terms', regulatory_framework__regions__id=regions))
            )

        # filter by status on regulation_es_doc
        if status:
            regulation_doc_qs = regulation_doc_qs.filter(
                # status filter on regulation
                Q('terms', status__id=status)
            )

        return regulation_doc_qs

    def get_serialized_framework_object(self, framework_obj, substance_module_permission, relevant_regulation_ids,
                                        is_muted):
        tagged_substances_list = []
        related_milestones_ids = RelevantRegulationService().get_relevant_milestone_id_organization(
            self.organization_id)
        if substance_module_permission:
            tagged_substances_list = RelevantSubstanceService().get_organization_relevant_substance_data(
                self.organization_id, data_name='framework', data_id=framework_obj.id, serializer=True)
        data = {
            'id': framework_obj.id,
            'name': framework_obj.name,
            'is_muted': RegulationMute.objects.filter(
                organization_id=self.organization_id, regulatory_framework_id=framework_obj.id, is_muted=True).exists(),
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                self.organization_id,
                framework_obj.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                self.organization_id,
                framework_obj.material_categories, serialize=True),
            'topics': TopicIdNameSerializer(framework_obj.topics, many=True).data,
            'urls': [],
            'regions': RegionIdNameSerializer(framework_obj.regions, many=True).data,
            'language': {'id': framework_obj.language.id, 'name': framework_obj.language.name},
            'issuing_body': {'id': framework_obj.issuing_body.id, 'name': framework_obj.issuing_body.name},
            'status': framework_obj.status.name,
            'text': framework_obj.description,
            'regulations': [],
            'milestones': [],
            'substances': tagged_substances_list,
            'impact_rating': RatingSearchService().get_framework_rating_obj(self.organization_id, framework_obj.id,
                                                                            framework_obj.regulatory_framework_rating),
        }
        for urls in framework_obj.urls:
            data['urls'].append({'id': urls.id, 'text': urls.text})
        for regulation in framework_obj.regulation_regulatory_framework:
            if regulation.review_status == 'o' and IdSearchService().does_id_exit_in_sorted_list(
                    relevant_regulation_ids, regulation.id):
                data['regulations'].append({
                    'id': regulation.id,
                    'name': regulation.name,
                    'is_muted': is_muted,
                    'type': regulation.type.name,
                    'description': regulation.description,
                    'date': regulation.created,
                    'status': regulation.status.name,
                })
        for milestone in framework_obj.regulatory_framework_milestone:
            if IdSearchService().does_id_exit_in_sorted_list(related_milestones_ids, milestone.id):
                data['milestones'].append({
                    'id': milestone.id,
                    'name': milestone.name,
                    'type': milestone.type.name,
                    'description': milestone.description,
                    'date': milestone.from_date,
                })
        return data

    def get_tabular_format_framework_obj(self, framework, relevant_topics_ids):
        framework_object = {
            'id': framework.id,
            'name': framework.name,
            'status': {'id': framework.status.id, 'name': framework.status.name},
            'is_muted': RegulationMute.objects.filter(
                organization_id=self.organization_id, regulatory_framework_id=framework.id, is_muted=True).exists(),
            'topics': self.get_relevant_topic_list(relevant_topics_ids, framework.topics),
            'regions': [{'id': region.id, 'name': region.name} for region in framework.regions],
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                self.organization_id, framework.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                self.organization_id, framework.material_categories, serialize=True),
            'impact_rating': RatingSearchService().get_framework_rating_obj(self.organization_id, framework.id),
        }
        return framework_object

    def get_tabular_format_regulation_obj(self, regulation, relevant_topics_ids, is_muted):
        regulation_object = {
            'id': regulation.id,
            'name': regulation.name,
            'status': {'id': regulation.status.id, 'name': regulation.status.name},
            'is_muted': is_muted,
            'topics': self.get_relevant_topic_list(relevant_topics_ids, regulation.topics),
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                self.organization_id, regulation.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                self.organization_id, regulation.material_categories, serialize=True),
            'impact_rating': RatingSearchService().get_regulation_rating_obj(self.organization_id, regulation.id),
        }
        return regulation_object

    @staticmethod
    def get_relevant_topic_list(relevant_topics_ids, topics):
        results = []
        for topic in topics:
            if IdSearchService().does_id_exit_in_sorted_list(relevant_topics_ids, topic.id):
                results.append({
                    'id': topic.id,
                    'name': topic.name,
                })
        return results

    def get_rating_sorted_regulatory_framework_doc_qs(self, framework_doc_qs, sort_order):
        # return rating sorted framework doc
        framework_doc_qs = framework_doc_qs.sort({
            "regulatory_framework_rating.rating": {
                "order": sort_order,
                "nested_path": "regulatory_framework_rating",
                "nested_filter": {
                    "term": {
                        "regulatory_framework_rating.organization.id": self.organization_id
                    }
                }
            }
        })
        return framework_doc_qs

    def get_rating_sorted_regulation_doc_qs(self, regulation_doc_qs, sort_order):
        # return rating sorted regulation doc
        regulation_doc_qs = regulation_doc_qs.sort({
            "regulation_rating.rating": {
                "order": sort_order,
                "nested_path": "regulation_rating",
                "nested_filter": {
                    "term": {
                        "regulation_rating.organization.id": self.organization_id
                    }
                }
            }
        })
        return regulation_doc_qs

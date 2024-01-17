from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.id_search_service import IdSearchService
from rttregulation.services.regulation_tagged_region_service import RegulationTaggedRegionService


class NewsSearchService:
    rating_service = RatingSearchService()

    def get_news_object_by_qs(self, news_document_queryset, organization_id, distinct_item=True):
        relevant_regulation_id = RelevantRegulationService().get_relevant_regulation_id_organization(organization_id)
        relevant_framework_id = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(
            organization_id)
        news_details = {
            'id': news_document_queryset.id,
            'title': news_document_queryset.title,
            'body': news_document_queryset.body,
            'date': news_document_queryset.pub_date,
            'status': news_document_queryset.status,
            'cover_image': news_document_queryset.cover_image if news_document_queryset.cover_image else None,
            'source': {'id': news_document_queryset.source.id, 'name': news_document_queryset.source.name,
                       'image': news_document_queryset.source.image if news_document_queryset.source.image else None},
            'impact_rating': self.rating_service.get_news_rating_obj(organization_id, news_document_queryset.id),
            'regions': [],
            'documents': [],
            'topics': [],
            'regulatory_frameworks': self.get_related_regulation_list(organization_id, relevant_framework_id,
                                                                      news_document_queryset.regulatory_frameworks,
                                                                      is_regulation=False),
            'regulations': self.get_related_regulation_list(organization_id, relevant_regulation_id,
                                                            news_document_queryset.regulations, is_regulation=True),
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id,
                news_document_queryset.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id,
                news_document_queryset.material_categories, serialize=True, distinct_item=distinct_item),
        }

        for region in news_document_queryset.regions:
            news_details['regions'].append({'id': region.id, 'name': region.name})

        for news_category in news_document_queryset.news_categories:
            if news_category.topic:
                topic_obj = {
                    'id': news_category.topic.id,
                    'name': news_category.topic.name
                }
                if topic_obj not in news_details['topics']:
                    news_details['topics'].append(topic_obj)

        for document in news_document_queryset.documents:
            news_details['documents'].append({
                'id': document.id,
                'title': document.title,
                'link': document.attachment if document.attachment else None,
            })

        return news_details

    def get_related_regulation_list(self, organization_id, relevant_regulation_id, regulation_queryset,
                                    is_regulation=False):
        result = []
        for regulation in regulation_queryset:
            if IdSearchService().does_id_exit_in_sorted_list(relevant_regulation_id, regulation.id):
                status_obj = None
                if regulation.status:
                    status_obj = {'id': regulation.status.id, 'name': regulation.status.name}
                if is_regulation:
                    impact_rating_obj = self.rating_service.get_regulation_rating_obj(organization_id, regulation.id)
                    region_list = []
                    if regulation.regulatory_framework:
                        region_list = RegulationTaggedRegionService().get_region_data(
                            regulation.regulatory_framework.id)
                else:
                    impact_rating_obj = self.rating_service.get_framework_rating_obj(organization_id, regulation.id)
                    region_list = [{'id': region.id, 'name': region.name} for region in regulation.regions]
                result.append({
                    'id': regulation.id,
                    'name': regulation.name,
                    'status': status_obj,
                    'impact_rating': impact_rating_obj,
                    'regions': region_list
                })
        return result

from rttregulation.services.rating_search_service import RatingSearchService
from rttproduct.services.category_validator_services import CategoryValidatorServices


class SearchService:
    rating_service = RatingSearchService()

    def get_regulation_list_item(self, regulation_doc, organization_id):
        regulation_details = {
            'id': regulation_doc.id,
            'name': regulation_doc.name,
            'description': regulation_doc.name,
            'review_status': regulation_doc.review_status,
            'created': regulation_doc.created,
            'status': regulation_doc.status.name,
            'type': regulation_doc.type.name,
            'language': regulation_doc.language.name,
            'impact_rating': self.rating_service.get_regulation_rating_obj(organization_id, regulation_doc.id,
                                                                           regulation_doc.regulation_rating),
            'links': [],
            'product_categories': [],
            'material_categories': [],
            'topics': [],
            'documents': [],
            'milestones': [],
        }
        for url in regulation_doc.urls:
            regulation_details['links'].append({'id': url.id, 'text': url.text})
        # relevant_product_categories
        regulation_details['product_categories'] = CategoryValidatorServices().get_relevant_product_categories(
            organization_id, regulation_doc.product_categories, serialize=True)
        # relevant_material_categories
        regulation_details['material_categories'] = CategoryValidatorServices().get_relevant_material_categories(
            organization_id, regulation_doc.material_categories, serialize=True)
        for topic in regulation_doc.topics:
            regulation_details['topics'].append({'id': topic.id, 'name': topic.name})
        for document in regulation_doc.documents:
            regulation_details['documents'].append({
                'id': document.id,
                'title': document.title,
                'link': document.attachment,
            })
        for milestone in regulation_doc.regulation_milestone:
            regulation_details['milestones'].append({
                'id': milestone.id,
                'name': milestone.name,
                'date': milestone.to_date,
            })
        return regulation_details

    def get_framework_list_item(self, framework_doc, organization_id):
        # relevant_product_categories
        rel_product_categories = CategoryValidatorServices().get_relevant_product_categories(
            organization_id, framework_doc.product_categories, serialize=True)
        # relevant_material_categories
        rel_material_categories = CategoryValidatorServices().get_relevant_material_categories(
            organization_id, framework_doc.material_categories, serialize=True)
        framework_obj = {
            'id': framework_doc.id,
            'name': framework_doc.name,
            'language': {'id': framework_doc.language.id, 'name': framework_doc.language.name},
            'issuing_body': {'id': framework_doc.issuing_body.id, 'name': framework_doc.issuing_body.name},
            'status': framework_doc.status.name,
            'description': framework_doc.description,
            'impact_rating': self.rating_service.get_framework_rating_obj(organization_id, framework_doc.id,
                                                                          framework_doc.regulatory_framework_rating),
            'product_categories': rel_product_categories,
            'material_categories': rel_material_categories,
            'urls': [],
        }
        for urls in framework_doc.urls:
            framework_obj['urls'].append({'id': urls.id, 'text': urls.text})
        return framework_obj

    def get_news_list_item(self, news_doc, organization_id):
        # relevant_product_categories
        rel_product_categories = CategoryValidatorServices().get_relevant_product_categories(
            organization_id, news_doc.product_categories, serialize=True)
        # relevant_material_categories
        rel_material_categories = CategoryValidatorServices().get_relevant_material_categories(
            organization_id, news_doc.material_categories, serialize=True)
        news_details = {
            'id': news_doc.id,
            'title': news_doc.title,
            'body': news_doc.body,
            'pub_date': news_doc.pub_date,
            'status': news_doc.status,
            'cover_image': news_doc.cover_image,
            'source': {'id': news_doc.source.id, 'name': news_doc.source.name},
            'impact_rating': self.rating_service.get_news_rating_obj(organization_id, news_doc.id,
                                                                     news_doc.news_relevance),
            'regions': [],
            'news_categories': [],
            'product_categories': rel_product_categories,
            'material_categories': rel_material_categories,
        }
        for region in news_doc.regions:
            news_details['regions'].append({'id': region.id, 'name': region.name})

        for news_category in news_doc.news_categories:
            news_details['news_categories'].append({'id': news_category.id, 'name': news_category.name})

        return news_details

    @staticmethod
    def get_product_list_item(product_doc, organization_id):
        # relevant_product_categories
        rel_product_categories = CategoryValidatorServices().get_relevant_product_categories(
            organization_id, product_doc.product_categories, serialize=True)
        # relevant_material_categories
        rel_material_categories = CategoryValidatorServices().get_relevant_material_categories(
            organization_id, product_doc.material_categories, serialize=True)
        product_details = {
            'id': product_doc.id,
            'name': product_doc.name,
            'description': product_doc.description,
            'image': product_doc.image,
            'product_categories': rel_product_categories,
            'material_categories': rel_material_categories
        }
        return product_details

    @staticmethod
    def get_document_list_item(document_doc):
        document_details = {
            'id': document_doc.id,
            'title': document_doc.title,
            'description': document_doc.description,
            'link': document_doc.attachment,
        }
        return document_details

    @staticmethod
    def get_milestone_list_item(organization_id, milestone_doc):
        milestone_details = [{
            'id': milestone_doc.id,
            'name': milestone_doc.name,
            'description': milestone_doc.description
        }]
        result = {}
        if milestone_doc.regulatory_framework:
            # relevant_product_categories
            rel_product_categories = CategoryValidatorServices().get_relevant_product_categories(
                organization_id, milestone_doc.regulatory_framework.product_categories, serialize=True)
            # relevant_material_categories
            rel_material_categories = CategoryValidatorServices().get_relevant_material_categories(
                organization_id, milestone_doc.regulatory_framework.material_categories, serialize=True)
            result = {
                'type': 'regulatory-framework',
                'id': milestone_doc.regulatory_framework.id,
                'name': milestone_doc.regulatory_framework.name,
                'milestones': milestone_details,
                'status': milestone_doc.regulatory_framework.status.name,
                'issuing_body': {'id': milestone_doc.regulatory_framework.issuing_body.id,
                                 'name': milestone_doc.regulatory_framework.issuing_body.name},
                'product_categories': rel_product_categories,
                'material_categories': rel_material_categories,
                'regulations': [], #should pass related regulation list if required. For now empty
                'regions': [],
                'impact_rating': RatingSearchService().get_framework_rating_obj(organization_id,
                                                                                milestone_doc.regulatory_framework.id),
                'topics': []
            }
            regulatory = milestone_doc.regulatory_framework
            for region in regulatory.regions:
                result['regions'].append({'id': region.id, 'name': region.name})
            for topic in regulatory.topics:
                result['topics'].append({'id': topic.id, 'name': topic.name})
        elif milestone_doc.regulation:
            regulation = milestone_doc.regulation
            # relevant_product_categories
            rel_product_categories = CategoryValidatorServices().get_relevant_product_categories(
                organization_id, regulation.product_categories, serialize=True)
            # relevant_material_categories
            rel_material_categories = CategoryValidatorServices().get_relevant_material_categories(
                organization_id, regulation.material_categories, serialize=True)
            result = {
                'type': 'regulation',
                'id': regulation.id,
                'name': regulation.name,
                'milestones': milestone_details,
                'status': regulation.status.name,
                'issuing_body': {
                    'id': regulation.regulatory_framework.issuing_body.id,
                    'name': regulation.regulatory_framework.issuing_body.name
                },
                'regulatory-framework': {},     #should pass framework object if required. For now empty
                'product_categories': rel_product_categories,
                'material_categories': rel_material_categories,
                'regions': [],
                'impact_rating': RatingSearchService().get_regulation_rating_obj(organization_id, regulation.id)
            }
            for region in regulation.regulatory_framework.regions:
                result['regions'].append({'id': region.id, 'name': region.name})
        return result

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.permissions import has_substance_module_permission
from rttcore.services.system_filter_service import SystemFilterService
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.documents import RegulationDocument
from rttregulation.models.models import RegulationMute
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService

from django.db.models import Q

from rttsubstance.services.relevant_substance_service import RelevantSubstanceService


class RegulationDetailApiView(APIView):
    permission_classes = (IsAuthenticated,)
    regulation_search_service = RatingSearchService()

    def get(self, request, regulation_id):
        organization_id = request.user.organization_id
        regulation_queryset = SystemFilterService().get_system_filtered_regulation_document_queryset(
            organization_id).filter('match', id=regulation_id).to_queryset().first()

        if not regulation_queryset or not organization_id:
            regulation_queryset = RegulationDocument.search().filter('match', review_status='o') \
                .filter('match', id=regulation_id).to_queryset().first()
            is_regulation_framework_relevant = None
            if regulation_queryset:
                is_regulation_framework_relevant = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
                    organization_id).filter('match', id=regulation_queryset.regulatory_framework_id)
            if not is_regulation_framework_relevant:
                return Response(status=status.HTTP_204_NO_CONTENT)

        regulation_details = self.__get_regulation_object(regulation_queryset, organization_id, distinct_item=False)

        for url in regulation_queryset.urls.all():
            regulation_details['links'].append({'id': url.id, 'text': url.text, 'description': url.description})

        for topic in regulation_queryset.topics.all():
            regulation_details['topics'].append({'id': topic.id, 'name': topic.name})

        for document in regulation_queryset.documents.all():
            regulation_details['documents'].append({
                'id': document.id,
                'title': document.title,
                'link': document.attachment.url,
            })

        regulation_details['frameworks'] = [self.__get_regulation_related_framework(regulation_queryset)]

        regulation_details['regions'] = regulation_details['frameworks'][0]['regions'] \
            if regulation_details['frameworks'].__len__() > 0 else []

        substance_module_permission = has_substance_module_permission(organization_id)
        substances_count = RelevantSubstanceService().get_organization_relevant_substance_data(
            organization_id, data_name='regulation', data_id=regulation_id, only_my_org=False).count()
        regulation_details['substance_count'] = substances_count if substance_module_permission else 0

        regulation_details['news'] = self.__get_regulation_related_news_list(regulation_queryset, organization_id)
        return Response(regulation_details, status=status.HTTP_200_OK)

    def __get_regulation_object(self, regulation_queryset, organization_id, distinct_item=False):
        rating_obj = self.regulation_search_service.get_regulation_rating_obj(organization_id, regulation_queryset.id)
        return {
            'id': regulation_queryset.id,
            'name': regulation_queryset.name,
            'is_muted': RegulationMute.objects.filter(organization_id=organization_id,
                                                      regulation_id=regulation_queryset.id, is_muted=True).exists(),
            'description': regulation_queryset.description,
            'review_status': regulation_queryset.review_status,
            'created': regulation_queryset.created,
            'status': regulation_queryset.status.name,
            'type': regulation_queryset.type.name,
            'language': regulation_queryset.language.name,
            'frameworks': [],
            'impact_rating': rating_obj,
            'links': [],
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id,
                regulation_queryset.product_categories.all(), serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id,
                regulation_queryset.material_categories.all(), serialize=True, distinct_item=distinct_item),
            'topics': [],
            'regions': [],
            'documents': [],
            'news': [],
        }

    @staticmethod
    def __get_regulation_related_framework(regulation_queryset):

        regulatory_framework = regulation_queryset.regulatory_framework

        regulation_obj = {
            'id': regulatory_framework.id,
            'name': regulatory_framework.name,
            'description': regulatory_framework.description,
            'created': regulatory_framework.created,
            'regions': [],
        }

        for region in regulatory_framework.regions.all():
            regulation_obj['regions'].append({'id': region.id, 'name': region.name})

        return regulation_obj

    def __get_regulation_related_news_list(self, regulation_queryset, organization_id):
        news_list = []
        relevant_regulatory_framework_ids_organization = RelevantRegulationService().\
            get_relevant_regulatory_framework_id_organization(organization_id)

        regulation_news_queryset = regulation_queryset.regulation_news.filter(Q(active=True) & Q(status='s')).order_by('-pub_date')
        for news in regulation_news_queryset:
            news_obj = {
                'id': news.id,
                'date': news.pub_date,
                'status': news.status,
                'title': news.title,
                'source': {'id': news.source.id, 'name': news.source.name},
                'impact_rating': self.regulation_search_service.get_news_rating_obj(organization_id, news.id),
                'regions': [],
                'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                    organization_id,
                    news.product_categories.all(), serialize=True),
                'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                    organization_id,
                    news.material_categories.all(), serialize=True),
                'regulatory_frameworks': [],
            }

            for region in news.regions.all():
                news_obj['regions'].append({'id': region.id, 'name': region.name})

            relevant_regulatory_framework = news.regulatory_frameworks.filter(
                id__in=relevant_regulatory_framework_ids_organization)
            for framework in relevant_regulatory_framework:
                news_obj['regulatory_frameworks'].append({'id': framework.id, 'name': framework.name})

            news_list.append(news_obj)

        return news_list

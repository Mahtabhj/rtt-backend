from elasticsearch_dsl import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rttcore.services.system_filter_service import SystemFilterService
from rttnews.documents import RegionDocument
from rttnotification.models import NotificationAlert
from rttnotification.serializers import NotificationAlertSerializer
from rttproduct.documents import ProductCategoryDocument, MaterialCategoryDocument
from rttregulation.documents import TopicDocument


class NotificationAlertViewSet(viewsets.ModelViewSet):
    queryset = NotificationAlert.objects.all()
    serializer_class = NotificationAlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def options(self, request, **kwargs):
        organization = request.user.organization
        contents = []
        frequencies = []
        product_categories = []
        material_categories = []
        regulatory_frameworks = []
        topics = []
        regions = []

        industry_ids = list(organization.industries.all().values_list('id', flat=True))

        '''
        notification contents
        '''
        for content in NotificationAlert.CONTENT_CHOICES:
            contents.append({
                'title': content[1],
                'value': content[0],
            })

        '''
        notification frequencies
        '''
        for frequency in NotificationAlert.FREQUENCY_CHOICES:
            frequencies.append({
                'title': frequency[1],
                'value': frequency[0],
            })

        '''
        product_categories
        '''
        product_category_queryset = ProductCategoryDocument.search().filter(
            'nested',
            path='industry',
            query=Q('terms', industry__id=industry_ids)
        ).source(['id', 'name'])
        product_category_queryset = product_category_queryset[0:product_category_queryset.count()]
        for product_category in product_category_queryset:
            product_categories.append({'id': product_category.id, 'name': product_category.name})

        '''
        material_categories
        '''
        material_category_queryset = MaterialCategoryDocument.search().filter('terms', industry__id=industry_ids) \
            .source(['id', 'name', 'industry'])
        material_category_queryset = material_category_queryset[0:material_category_queryset.count()]

        for material_category in material_category_queryset:
            material_categories.append({
                'id': material_category.id,
                'name': material_category.name,
                'industry': {
                    'id': material_category.industry.id,
                    'name': material_category.industry.name
                }
            })

        '''
        regulatory_frameworks
        '''
        regulatory_framework_queryset = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            organization.id).source(['id', 'name'])
        regulatory_framework_queryset = regulatory_framework_queryset[0: regulatory_framework_queryset.count()]

        for framework in regulatory_framework_queryset:
            regulatory_frameworks.append({'id': framework.id, 'name': framework.name})

        '''
        topics
        '''
        topic_queryset = TopicDocument.search().filter(
            'nested',
            path='industry_topics',
            query=Q('terms', industry_topics__id=industry_ids)
        ).source(['id', 'name'])
        for topic in topic_queryset:
            topics.append({'id': topic.id, 'name': topic.name})

        '''
        regions
        '''
        region_queryset = RegionDocument.search().source(['id', 'name'])
        for region in region_queryset:
            regions.append({'id': region.id, 'name': region.name})

        response = {
            'contents': contents,
            'frequencies': frequencies,
            'product_categories': product_categories,
            'material_categories': material_categories,
            'regulatory_frameworks': regulatory_frameworks,
            'topics': topics,
            'regions': regions,
        }
        return Response(response, status=status.HTTP_200_OK)

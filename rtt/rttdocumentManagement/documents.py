from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from rttcore.elasticsearch_analyzer import html_strip, search_analyzer, user_name_analyzer, substance_name_analyzer
from rttdocumentManagement.models import DocumentManagement
from rttnews.models.models import News
from rttregulation.models.models import RegulatoryFramework, Regulation
from rttproduct.models.models import Product
from rttsubstance.models import Substance

from django.contrib.auth import get_user_model

User = get_user_model()


@registry.register_document
class DocumentManagementDocument(Document):
    name = fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    description = fields.TextField(analyzer=html_strip)
    regulatory_frameworks = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    })
    regulations = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    })
    products = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()}),
        'image': fields.FileField()
    })
    substances = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=substance_name_analyzer, fields={'raw': fields.KeywordField()}),
        'ec_no': fields.TextField(fields={'raw': fields.KeywordField()}),
        'cas_no': fields.TextField(fields={'raw': fields.KeywordField()})
    })
    news = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    })
    attachment_document = fields.FileField()
    uploaded_by = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(analyzer=user_name_analyzer, fields={'raw': fields.KeywordField()}),
        'last_name': fields.TextField(analyzer=user_name_analyzer, fields={'raw': fields.KeywordField()}),
        'avatar': fields.FileField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        })
    })
    created = fields.DateField()
    modified = fields.DateField()

    class Index:
        name = 'document_management'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = DocumentManagement

        fields = [
            'id',
        ]
        related_models = [User, RegulatoryFramework, Regulation, Product, Substance, News]

    def get_queryset(self):
        return super(DocumentManagementDocument, self).get_queryset().prefetch_related(
            'regulatory_frameworks', 'regulations', 'products', 'substances', 'news',
        )

    @staticmethod
    def get_instances_from_related(related_instance):
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.doc_management_frameworks.all()
        if isinstance(related_instance, Regulation):
            return related_instance.doc_management_regulations.all()
        if isinstance(related_instance, Product):
            return related_instance.doc_management_products.all()
        if isinstance(related_instance, Substance):
            return related_instance.doc_management_substances.all()
        if isinstance(related_instance, News):
            return related_instance.doc_management_news.all()

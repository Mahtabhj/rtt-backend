from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from rttcore.elasticsearch_analyzer import search_analyzer, html_strip
from rttdocument.models.models import Document as DocumentModel
from rttnews.models.models import News
from rttproduct.models.models import ProductCategory, MaterialCategory
from rttregulation.models.models import Regulation, RegulatoryFramework


@registry.register_document
class DocumentModelDocument(Document):
    title = fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    description = fields.TextField(analyzer=html_strip)
    created = fields.DateField()
    attachment = fields.FileField()
    regulation_documents = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'review_status': fields.TextField(),
        'product_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
        }),
        'material_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
            'short_name': fields.TextField()
        })
    })
    framework_documents = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'review_status': fields.TextField(),
        'product_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
        }),
        'material_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
            'short_name': fields.TextField()
        }),
    })
    news_documents = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
        'status': fields.TextField(),
        'active': fields.BooleanField(),
        'product_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
        }),
        'material_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
            'short_name': fields.TextField()
        }),
    })

    class Index:
        name = 'document'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = DocumentModel

        fields = [
            'id',
        ]
        related_models = [Regulation, RegulatoryFramework, News]

    @staticmethod
    def get_instances_from_related(related_instance):
        if isinstance(related_instance, Regulation):
            if isinstance(related_instance, ProductCategory):
                return related_instance.regulation_product_categories.all()
            if isinstance(related_instance, MaterialCategory):
                return related_instance.regulation_material_categories.all()
            return related_instance.documents.all()
        if isinstance(related_instance, RegulatoryFramework):
            if isinstance(related_instance, ProductCategory):
                return related_instance.product_cat_reg_framework.all()
            if isinstance(related_instance, MaterialCategory):
                return related_instance.material_cat_reg_framework.all()
            return related_instance.documents.all()
        if isinstance(related_instance, News):
            if isinstance(related_instance, ProductCategory):
                return related_instance.product_category_news.all()
            if isinstance(related_instance, MaterialCategory):
                return related_instance.material_category_news.all()
            return related_instance.documents.all()

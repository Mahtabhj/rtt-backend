from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from django.contrib.auth import get_user_model

from rttcore.elasticsearch_analyzer import html_strip, search_analyzer, task_name_analyzer, user_name_analyzer
from rttnews.models.models import News
from rttregulation.models.models import RegulatoryFramework, Regulation
from rttproduct.models.models import Product
from rtttaskManagement.models import Task
from rttsubstance.models import Substance

User = get_user_model()


@registry.register_document
class TaskDocument(Document):
    name = fields.TextField(analyzer=task_name_analyzer, fields={'raw': fields.KeywordField()})
    description = fields.TextField(analyzer=html_strip)
    status = fields.TextField()
    assignee = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(analyzer=user_name_analyzer, fields={'raw': fields.KeywordField()}),
        'last_name': fields.TextField(analyzer=user_name_analyzer, fields={'raw': fields.KeywordField()}),
        'avatar': fields.FileField()
    })
    created_by = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(),
        'avatar': fields.FileField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        })
    })
    products = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()}),
        'image': fields.FileField()
    })
    regulatory_frameworks = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    regulations = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    news = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField()
    })
    substances = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()}),
        'ec_no': fields.TextField(),
        'cas_no': fields.TextField()
    })
    due_date = fields.DateField()
    is_archive = fields.BooleanField()

    class Index:
        name = 'task'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Task

        fields = [
            'id',
        ]
        related_models = [User, Product, RegulatoryFramework, Regulation, News, Substance]

    def get_queryset(self):
        return super(TaskDocument, self).get_queryset().prefetch_related(
            'products', 'regulatory_frameworks', 'regulations', 'news', 'substances'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Product):
            return related_instance.task_related_products.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.task_regulatory_frameworks.all()
        if isinstance(related_instance, Regulation):
            return related_instance.task_regulations.all()
        if isinstance(related_instance, News):
            return related_instance.task_news.all()
        if isinstance(related_instance, Substance):
            return related_instance.task_substances.all()

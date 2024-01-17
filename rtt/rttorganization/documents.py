from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from rttorganization.models.models import Organization
from rttproduct.models.core_models import Industry
from rttregulation.models.core_models import Topic
from rttproduct.models.models import Product, ProductCategory, MaterialCategory


@registry.register_document
class OrganizationDocument(Document):
    product_organization = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        })
    })
    industries = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
        })
    })

    class Index:
        name = 'organization'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 1}

    class Django:
        model = Organization

        fields = [
            'id',
            'name',
            'address',
            'description',
            'tax_code',
        ]
        related_models = [Product, Industry]

    def get_queryset(self):
        return super(OrganizationDocument, self).get_queryset().prefetch_related(
            'industries', 'product_organization'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Product):
            return related_instance.organization
        if isinstance(related_instance, Industry):
            return related_instance.organization_industries.all()

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from rttcore.elasticsearch_analyzer import substance_name_analyzer, region_analyzer, search_analyzer
from rttlimitManagement.models import Exemption, RegulationSubstanceLimit
from rttsubstance.models import Substance
from rttregulation.models.models import RegulatoryFramework, Regulation


@registry.register_document
class ExemptionDocument(Document):
    substance = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=substance_name_analyzer, fields={'raw': fields.KeywordField()}),
        'cas_no': fields.TextField(fields={'raw': fields.KeywordField()}),
        'ec_no': fields.TextField(fields={'raw': fields.KeywordField()}),
        'is_family': fields.BooleanField()
    })
    regulatory_framework = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    regulation = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    article = fields.TextField()
    reference = fields.TextField()
    application = fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    notes = fields.TextField()
    status = fields.TextField()
    expiration_date = fields.DateField()
    date_into_force = fields.DateField()

    class Index:
        name = 'exemption'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Exemption

        fields = [
            'id',
        ]
        related_models = [Substance, RegulatoryFramework, Regulation]

    def get_queryset(self):
        return super(ExemptionDocument, self).get_queryset().select_related(
            'substance', 'regulatory_framework', 'regulation',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Substance):
            return related_instance.substance_exemption.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.regulatory_framework_exemption.all()
        if isinstance(related_instance, Regulation):
            return related_instance.regulation_exemption.all()


@registry.register_document
class RegulationSubstanceLimitDocument(Document):
    substance = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=substance_name_analyzer, fields={'raw': fields.KeywordField()}),
        'cas_no': fields.TextField(fields={'raw': fields.KeywordField()}),
        'ec_no': fields.TextField(fields={'raw': fields.KeywordField()}),
        'is_family': fields.BooleanField()
    })
    regulatory_framework = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()}),
        'publish_limit_data': fields.BooleanField(),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(analyzer=region_analyzer, fields={'raw': fields.KeywordField()})
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'short_name': fields.TextField(),
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    regulation = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()}),
        'publish_limit_data': fields.BooleanField(),
        'regulatory_framework': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'review_status': fields.TextField(),
            'description': fields.TextField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'short_name': fields.TextField()
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    scope = fields.TextField(fields={'raw': fields.KeywordField()})
    limit_value = fields.FloatField()
    measurement_limit_unit = fields.TextField()
    limit_note = fields.TextField()
    status = fields.TextField()
    date_into_force = fields.DateField()
    modified = fields.DateField()
    created = fields.DateField()

    class Index:
        name = 'regulation_substance_limit'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = RegulationSubstanceLimit

        fields = [
            'id',
        ]
        related_models = [Substance, RegulatoryFramework, Regulation]

    def get_queryset(self):
        return super(RegulationSubstanceLimitDocument, self).get_queryset().select_related(
            'substance', 'regulatory_framework', 'regulation',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Substance):
            return related_instance.regulation_substance_limit.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.regulatory_framework_regulation_substance_limit.all()
        if isinstance(related_instance, Regulation):
            return related_instance.regulation_regulation_substance_limit.all()

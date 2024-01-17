from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from rttcore.elasticsearch_analyzer import substance_name_analyzer, substance_number_analyzer
from rttsubstance.models import Substance, SubstanceUsesAndApplication, SubstancePropertyDataPoint, SubstanceFamily
from rttproduct.models.models import Product
from rttnews.models.models import SubstanceNews, News
from rttregulation.models.models import (SubstanceRegulatoryFramework, SubstanceRegulation, SubstanceRegulationMilestone,
                                         RegulatoryFramework, Regulation, RegulationMilestone)
from rttlimitManagement.models import RegulationSubstanceLimit


@registry.register_document
class SubstanceDocument(Document):
    name = fields.TextField(analyzer=substance_name_analyzer, fields={'raw': fields.KeywordField()})
    ec_no = fields.TextField(fields={'raw': fields.KeywordField()})
    cas_no = fields.TextField(fields={'raw': fields.KeywordField()})
    image = fields.FileField()
    molecular_formula = fields.TextField()
    chemycal_id = fields.TextField(analyzer=substance_name_analyzer, fields={'raw': fields.KeywordField()})
    modified = fields.DateField()
    uses_and_application_substances = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
    })
    substances_product = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        })
    })
    substance_news_relation = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'news': fields.ObjectField(properties={
            'id': fields.IntegerField(),
        }),
        'modified': fields.DateField()
    })
    substances_news = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'body': fields.TextField(),
        'title': fields.TextField(),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'source': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'type': fields.ObjectField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField()
            })
        })
    })
    # substance_regulatory_framework_relation = fields.NestedField(properties={
    #     'id': fields.IntegerField(),
    #     'regulatory_framework': fields.ObjectField(properties={
    #         'id': fields.IntegerField(),
    #     }),
    #     'modified': fields.DateField()
    # })
    substances_regulatory_framework = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    # substance_regulation_relation = fields.NestedField(properties={
    #     'id': fields.IntegerField(),
    #     'regulation': fields.ObjectField(properties={
    #         'id': fields.IntegerField(),
    #     }),
    #     'modified': fields.DateField()
    # })
    substances_regulation = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'regulatory_framework': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    # substance_regulation_milestone_relation = fields.NestedField(properties={
    #     'id': fields.IntegerField(),
    #     'regulation_milestone': fields.ObjectField(properties={
    #         'id': fields.IntegerField(),
    #     }),
    #     'modified': fields.DateField()
    # })
    substances_regulation_milestone = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
        'from_date': fields.DateField(),
        'to_date': fields.DateField(),
        'regulatory_framework': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'regulation': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })

    substance_property_data_point_relation = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'property_data_point': fields.ObjectField(properties={
            'id': fields.IntegerField(),
        }),
        'value': fields.TextField(),
        'status': fields.TextField()
    })
    regulation_substance_limit = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'regulatory_framework': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'regulation': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })

    substance_family = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'family': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'family_source': fields.TextField(),
        'modified': fields.DateField(),
    })

    class Index:
        name = 'substance'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Substance

        fields = [
            'id',
            'is_family',
        ]
        related_models = [SubstanceUsesAndApplication, Product,
                          RegulatoryFramework, Regulation, RegulationMilestone, News,
                          SubstanceNews, SubstancePropertyDataPoint, RegulationSubstanceLimit, SubstanceFamily]

    def get_queryset(self):
        return super(SubstanceDocument, self).get_queryset().prefetch_related(
            'substances_product', 'substance_news_relation',
            'substance_regulatory_framework_relation', 'substance_regulation_relation',
            'substance_regulation_milestone_relation', 'substances_news', 'substances_regulatory_framework',
            'substances_regulation', 'substances_regulation_milestone', 'substance_property_data_point_relation',
            'regulation_substance_limit'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, SubstanceUsesAndApplication):
            return related_instance.substances.all()
        if isinstance(related_instance, Product):
            return related_instance.substances.all()
        if isinstance(related_instance, News):
            return related_instance.substances.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.substances.all()
        if isinstance(related_instance, Regulation):
            return related_instance.substances.all()
        if isinstance(related_instance, RegulationMilestone):
            return related_instance.substances.all()
        if isinstance(related_instance, SubstanceNews):
            return related_instance.substance
        if isinstance(related_instance, SubstanceRegulatoryFramework):
            return related_instance.substance
        if isinstance(related_instance, SubstanceRegulation):
            return related_instance.substance
        if isinstance(related_instance, SubstanceRegulationMilestone):
            return related_instance.substance
        if isinstance(related_instance, SubstancePropertyDataPoint):
            return related_instance.substance
        if isinstance(related_instance, RegulationSubstanceLimit):
            return related_instance.substance
        if isinstance(related_instance, SubstanceFamily):
            return related_instance.substance


@registry.register_document
class SubstanceUsesAndApplicationDocument(Document):
    name = fields.TextField(fields={'raw': fields.KeywordField()})
    organization = fields.ObjectField(properties={
        'id': fields.IntegerField(),
    })
    substances = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    class Index:
        name = 'substance_uses_and_application'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = SubstanceUsesAndApplication

        fields = [
            'id',
        ]
        related_models = [Substance]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Substance):
            return related_instance.uses_and_application_substances.all()


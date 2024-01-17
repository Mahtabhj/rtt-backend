from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from rttcore.elasticsearch_analyzer import html_strip, search_analyzer, substance_name_analyzer, region_analyzer, \
    limit_scope_analyzer
from rttlimitManagement.models import RegulationSubstanceLimit
from rttnews.models.models import News
from rttorganization.models.models import Organization
from rttproduct.models.core_models import Industry
from rttproduct.models.models import ProductCategory, MaterialCategory, Product
from rttregulation.models.core_models import Topic
from rttregulation.models.models import Region, Regulation, RegulatoryFramework, Status, IssuingBody, RegulationType, \
    RegulationMilestone, MilestoneType, Url, Language, Question, RegulationRating, RegulatoryFrameworkRating, \
    RegulationRatingLog, RegulatoryFrameworkRatingLog, RegulationMute, MilestoneMute
from rttsubstance.models import Substance
from rttdocument.models.models import Document as DocumentModel


@registry.register_document
class RegulationDocument(Document):
    name = fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    description = fields.TextField(analyzer=html_strip)
    regulation_mute_regulation = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'is_muted': fields.BooleanField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField()
        })
    })
    status = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    type = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    language = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'code': fields.TextField(),
    })
    regulatory_framework = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()}),
        'review_status': fields.TextField(),
        'description': fields.TextField(),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(analyzer=region_analyzer, fields={'raw': fields.KeywordField()}),
            'country_code': fields.TextField(),
            'latitude': fields.FloatField(),
            'longitude': fields.FloatField()
        }),
        'issuing_body': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'created': fields.DateField(),
        'regulatory_framework_milestone': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField(),
            'from_date': fields.DateField(),
            'to_date': fields.DateField()
        }),
        'substances': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
    })
    regulation_milestone = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
        'from_date': fields.DateField(),
        'to_date': fields.DateField(),
        'type': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'substances': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        })
    })
    material_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'short_name': fields.TextField(),
        'industry': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    product_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        # Related Products
        'product_product_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
    })
    topics = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    urls = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'text': fields.TextField()
    })
    documents = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
        'description': fields.TextField(),
        'attachment': fields.FileField()
    })
    # Related News
    regulation_news = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
        'pub_date': fields.DateField(),
        'status': fields.TextField(),
        'source': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'regulatory_frameworks': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'short_name': fields.TextField(),
        })
    })
    created = fields.DateField()
    regulation_rating = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'rating': fields.IntegerField(),
        'comment': fields.TextField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'created': fields.DateField()
    })
    substances = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    regulation_regulation_substance_limit = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'substance': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(fields={'raw': fields.KeywordField()}),
            'cas_no': fields.TextField(fields={'raw': fields.KeywordField()}),
            'ec_no': fields.TextField(fields={'raw': fields.KeywordField()}),
        }),
        'scope': fields.TextField(fields={'raw': fields.KeywordField()}),
        'limit_value': fields.FloatField(),
        'measurement_limit_unit': fields.TextField(),
        'date_into_force': fields.DateField(),
        'status': fields.TextField(),
        'modified': fields.DateField()
    })
    publish_limit_data = fields.BooleanField()

    class Index:
        name = 'regulations'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Regulation

        fields = [
            'id',
            'review_status'
        ]
        related_models = [Region, RegulatoryFramework, RegulationMilestone, MilestoneType, Status, Product,
                          ProductCategory, MaterialCategory, Topic, RegulationRating, Substance,
                          RegulationSubstanceLimit, RegulationMute]

    def get_queryset(self):
        return super(RegulationDocument, self).get_queryset().select_related(
            'type', 'language', 'status', 'regulatory_framework',
        ).prefetch_related(
            'documents', 'material_categories', 'product_categories', 'urls', 'topics', 'regulation_milestone',
            'regulation_news', 'regulation_rating', 'substances', 'regulation_mute_regulation',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, RegulatoryFramework):
            if isinstance(related_instance, Region):
                return related_instance.regulatory_framework_region.all()
            if isinstance(related_instance, IssuingBody):
                return related_instance.regulatory_framework_issuing_body.all()
            if isinstance(related_instance, Status):
                return related_instance.regulatory_framework_status.all()
            if isinstance(related_instance, RegulationMilestone):
                return related_instance.regulatory_framework
            return related_instance.regulation_regulatory_framework.all()
        if isinstance(related_instance, RegulationMilestone):
            if isinstance(related_instance, MilestoneType):
                return related_instance.regulation_milestone_type.all()
            return related_instance.regulation
        if isinstance(related_instance, Status):
            return related_instance.regulation_status.all()
        if isinstance(related_instance, Topic):
            return related_instance.regulation_topics.all()
        if isinstance(related_instance, ProductCategory):
            if isinstance(related_instance, Product):
                return related_instance.product_categories.all()
            return related_instance.regulation_product_categories.all()
        if isinstance(related_instance, RegulationRating):
            return related_instance.regulation
        if isinstance(related_instance, Substance):
            return related_instance.substances_regulation.all()
        if isinstance(related_instance, RegulationSubstanceLimit):
            return related_instance.regulation
        if isinstance(related_instance, RegulationMute):
            return related_instance.regulation


@registry.register_document
class RegulatoryFrameworkDocument(Document):
    name = fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    description = fields.TextField(analyzer=html_strip)
    regulation_mute_framework = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'is_muted': fields.BooleanField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField()
        })
    })
    regions = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=region_analyzer, fields={'raw': fields.KeywordField()}),
        'country_code': fields.TextField(),
        'latitude': fields.FloatField(),
        'longitude': fields.FloatField()
    })
    status = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    issuing_body = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    language = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    product_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        # Related Products
        'product_product_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()

        }),
    })
    material_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'short_name': fields.TextField(),
        'industry': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    topics = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField()
    })
    urls = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'text': fields.TextField()
    })
    documents = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
        'description': fields.TextField(),
        'attachment': fields.FileField()
    })
    # Related Milestones
    regulatory_framework_milestone = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
        'from_date': fields.DateField(),
        'to_date': fields.DateField(),
        'type': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'documents': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'title': fields.TextField(),
            'description': fields.TextField(),
            'attachment': fields.FileField()
        }),
        'urls': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'text': fields.TextField()
        }),
        'substances': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
    })
    # Related Regulations
    regulation_regulatory_framework = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()}),
        'description': fields.TextField(),
        'review_status': fields.TextField(),
        'created': fields.DateField(),
        'modified': fields.DateField(),
        'type': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'regulation_milestone': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField(),
            'to_date': fields.DateField(),
            'from_date': fields.DateField(),
            'type': fields.ObjectField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField(),
            })
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'substances': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        })
    })
    # Related News
    news_regulatory_frameworks = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
        'pub_date': fields.DateField(),
        'status': fields.TextField(),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'source': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'short_name': fields.TextField(),
        }),
        'regulations': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField(),
            'status': fields.ObjectField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField(),
            }),
            'regulatory_framework': fields.ObjectField(properties={
                'regions': fields.NestedField(properties={
                    'id': fields.IntegerField(),
                    'name': fields.TextField(),
                }),
            }),
            'topics': fields.NestedField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField(),
            }),
        })
    })
    substances = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    created = fields.DateField()
    modified = fields.DateField()
    regulatory_framework_rating = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'rating': fields.IntegerField(),
        'comment': fields.TextField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'created': fields.DateField()
    })
    regulatory_framework_regulation_substance_limit = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'substance': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(fields={'raw': fields.KeywordField()}),
            'cas_no': fields.TextField(fields={'raw': fields.KeywordField()}),
            'ec_no': fields.TextField(fields={'raw': fields.KeywordField()}),
        }),
        'scope': fields.TextField(fields={'raw': fields.KeywordField()}),
        'limit_value': fields.FloatField(),
        'measurement_limit_unit': fields.TextField(),
        'status': fields.TextField(),
        'date_into_force': fields.DateField(),
        'modified': fields.DateField()
    })
    publish_limit_data = fields.BooleanField()

    class Index:
        name = 'regulatory_framework'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = RegulatoryFramework

        fields = [
            'id',
            'review_status',
        ]
        related_models = [Region, Status, IssuingBody, ProductCategory, MaterialCategory, Regulation, RegulationType,
                          RegulationMilestone, MilestoneType, Topic, News, Product, RegulatoryFrameworkRating,
                          Substance, RegulationSubstanceLimit, RegulationMute]

    def get_queryset(self):
        return super(RegulatoryFrameworkDocument, self).get_queryset().select_related(
            'language', 'status', 'issuing_body'
        ).prefetch_related(
            'regions', 'documents', 'material_categories', 'product_categories', 'urls', 'topics',
            'regulatory_framework_milestone', 'regulation_regulatory_framework', 'news_regulatory_frameworks',
            'regulatory_framework_rating', 'substances', 'regulatory_framework_regulation_substance_limit',
            'regulation_mute_framework',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Region):
            return related_instance.regulatory_framework_region.all()
        if isinstance(related_instance, Status):
            return related_instance.regulatory_framework_status.all()
        if isinstance(related_instance, IssuingBody):
            return related_instance.regulatory_framework_issuing_body.all()
        if isinstance(related_instance, ProductCategory):
            if isinstance(related_instance, Product):
                return related_instance.product_categories.all()
            return related_instance.product_cat_reg_framework.all()
        if isinstance(related_instance, MaterialCategory):
            return related_instance.material_cat_reg_framework.all()
        if isinstance(related_instance, Language):
            return related_instance.language_reg_framework.all()
        if isinstance(related_instance, Url):
            return related_instance.url_reg_framework.all()
        if isinstance(related_instance, RegulationMilestone):
            if isinstance(related_instance, MilestoneType):
                return related_instance.regulation_milestone_type.all()
            # if isinstance(related_instance, Url):
            #     return related_instance
            return related_instance.regulatory_framework
        if isinstance(related_instance, Topic):
            return related_instance.regulatory_framework_topics.all()
        if isinstance(related_instance, Regulation):
            if isinstance(related_instance, RegulationType):
                return related_instance.regulation_regulation_type.all()
            if isinstance(related_instance, RegulationMilestone):
                if isinstance(related_instance, MilestoneType):
                    return related_instance.regulation_milestone_type.all()
                return related_instance.regulation
            return related_instance.regulatory_framework

        if isinstance(related_instance, News):
            if isinstance(related_instance, Regulation):
                return related_instance.regulation_news.all()
            if isinstance(related_instance, Region):
                return related_instance.region_news.all()
            return related_instance.regulatory_frameworks.all()
        if isinstance(related_instance, RegulatoryFrameworkRating):
            return related_instance.regulatory_framework
        if isinstance(related_instance, Substance):
            return related_instance.substances_regulatory_framework.all()
        if isinstance(related_instance, RegulationSubstanceLimit):
            return related_instance.regulatory_framework
        if isinstance(related_instance, RegulationMute):
            return related_instance.regulatory_framework


@registry.register_document
class QuestionDocument(Document):
    organization = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    class Index:
        name = 'question'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Question

        fields = [
            'id',
            'name',
            'description'
        ]

    def get_queryset(self):
        return super(QuestionDocument, self).get_queryset().select_related(
            'organization'
        )


@registry.register_document
class RegulationRatingLogDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    organization = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    regulation = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'review_status': fields.TextField(),
        'regulatory_framework': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'review_status': fields.TextField(),
            'regions': fields.NestedField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField(),
            }),
        }),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        })
    })
    created = fields.DateField()

    class Index:
        name = 'regulation_rating_log'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = RegulationRatingLog

        fields = [
            'id',
            'rating',
            'comment'
        ]
        related_models = [Regulation]

    def get_queryset(self):
        return super(RegulationRatingLogDocument, self).get_queryset().select_related(
            'organization', 'regulation', 'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Organization):
            return related_instance.regulationratinglog_set.all()
        if isinstance(related_instance, Regulation):
            return related_instance.regulation_rating_log.all()




@registry.register_document
class RegulatoryFrameworkRatingLogDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    organization = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    regulatory_framework = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'review_status': fields.TextField(),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
        }),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        })
    })
    created = fields.DateField()

    class Index:
        name = 'regulatory_framework_rating_log'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = RegulatoryFrameworkRatingLog

        fields = [
            'id',
            'rating',
            'comment'
        ]
        related_models = [RegulatoryFramework]

    def get_queryset(self):
        return super(RegulatoryFrameworkRatingLogDocument, self).get_queryset().select_related(
            'organization', 'regulatory_framework', 'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Organization):
            return related_instance.regulatoryframeworkratinglog_set.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.regulatory_framework_rating_log.all()


@registry.register_document
class TopicDocument(Document):
    created = fields.DateField()
    industry_topics = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
    })

    class Index:
        name = 'topic'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Topic

        fields = [
            'id',
            'name',
            'description'
        ]
        related_models = [Industry]

    def get_queryset(self):
        return super(TopicDocument, self).get_queryset().prefetch_related(
            'industry_topics',
        )

    @staticmethod
    def get_instances_from_related(related_instance):
        if isinstance(related_instance, Industry):
            return related_instance.topics.all()


@registry.register_document
class MilestoneDocument(Document):
    name = fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    description = fields.TextField(analyzer=html_strip)
    milestone_mute_milestone = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'is_muted': fields.BooleanField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField()
        })
    })
    from_date = fields.DateField()
    to_date = fields.DateField()
    created = fields.DateField()
    type = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    regulatory_framework = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'review_status': fields.TextField(),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'product_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
        }),
        'material_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
            'short_name': fields.TextField(),
            'industry': fields.ObjectField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField()
            })
        }),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(fielddata=True)
        }),
        'substances': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
        'issuing_body': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    regulation = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'review_status': fields.TextField(),
        'regulatory_framework': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'review_status': fields.TextField(),
            'description': fields.TextField(),
            'created': fields.DateField(),
            'regions': fields.NestedField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField(fielddata=True)
            }),
            'status': fields.ObjectField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField()
            }),
            'issuing_body': fields.ObjectField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField()
            }),
        }),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'product_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
        }),
        'material_categories': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
            'short_name': fields.TextField(),
            'industry': fields.ObjectField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField()
            })
        }),
        'topics': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'substances': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        }),
    })
    documents = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
        'description': fields.TextField(),
        'attachment': fields.FileField()
    })
    urls = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'text': fields.TextField(),
        'description': fields.TextField()
    })
    substances = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    class Index:
        name = 'milestone'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = RegulationMilestone

        fields = [
            'id',
        ]

        related_models = [MilestoneType, Regulation, RegulatoryFramework, Substance, DocumentModel, Url, MilestoneMute]

    def get_queryset(self):
        return super(MilestoneDocument, self).get_queryset().select_related(
            'type', 'regulation', 'regulatory_framework',
        ).prefetch_related('substances', 'documents', 'urls', 'milestone_mute_milestone')

    @staticmethod
    def get_instances_from_related(related_instance):
        if isinstance(related_instance, MilestoneType):
            return related_instance.regulation_milestone_type.all()
        if isinstance(related_instance, Regulation):
            return related_instance.regulation_milestone.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.regulatory_framework_milestone.all()
        if isinstance(related_instance, Substance):
            return related_instance.substances_regulation_milestone.all()
        if isinstance(related_instance, DocumentModel):
            return related_instance.documents_regulation_milestone.all()
        if isinstance(related_instance, Url):
            return related_instance.urls_regulation_milestone.all()
        if isinstance(related_instance, MilestoneMute):
            return related_instance.milestone

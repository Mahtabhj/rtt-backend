from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from rttcore.elasticsearch_analyzer import html_strip, search_analyzer
from rttdocument.models.models import Document as NewsDocumentModel
from rttnews.models.models import News, NewsRelevance, NewsCategory, Source, NewsRelevanceLog
from rttproduct.models.models import ProductCategory, MaterialCategory, Product
from rttregulation.models.models import (Region, Regulation, RegulationType,
                                         RegulatoryFramework, Status, Url, Language,
                                         IssuingBody, RegulationMilestone, MilestoneType)
from rttorganization.models.models import Organization
from rttsubstance.models import Substance
from rttregulation.models.core_models import Topic

User = get_user_model()


@registry.register_document
class RegionDocument(Document):
    name = fields.TextField(analyzer=html_strip, fields={'raw': fields.KeywordField()}, )
    description = fields.TextField(analyzer=html_strip)
    iso_name = fields.TextField()
    country_code = fields.TextField()
    parent = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    region_page = fields.BooleanField()
    country_flag = fields.FileField()
    industries = fields.NestedField(properties={
        'id': fields.IntegerField(),
    })

    class Index:
        name = 'region'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Region

        fields = [
            'id',
        ]


@registry.register_document
class NewsDocument(Document):
    title = fields.TextField(analyzer=search_analyzer, fields={'raw': fields.KeywordField()})
    body = fields.TextField(analyzer=html_strip)
    regions = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(fielddata=True),
        'country_code': fields.TextField(),
        'latitude': fields.FloatField(),
        'longitude': fields.FloatField()
    })
    regulations = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
        'review_status': fields.TextField(),
        'created': fields.DateField(),
        'type': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
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
            'name': fields.TextField(),
        }),
        'regulation_milestone': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField(),
            'from_date': fields.DateField(),
            'to_date': fields.DateField()
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        })
    })
    regulatory_frameworks = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
        'review_status': fields.TextField(),
        'created': fields.DateField(),
        'status': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'regulatory_framework_milestone': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField(),
            'from_date': fields.DateField(),
            'to_date': fields.DateField()
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
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
    material_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'short_name': fields.TextField(),
        'industry': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    news_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'topic': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
    })
    documents = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
        'description': fields.TextField(),
        'attachment': fields.FileField()
    })
    selected_by = fields.ObjectField(properties={
        'name': fields.TextField(),
        'avatar': fields.FileField(),
    })
    source = fields.ObjectField(properties={
        'id': fields.TextField(),
        'name': fields.TextField(),
        'image': fields.FileField(),
        'type': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    news_relevance = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'relevancy': fields.IntegerField(),
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
        'ec_no': fields.TextField(),
        'cas_no': fields.FileField()
    })
    cover_image = fields.FileField()

    class Index:
        name = 'news'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = News

        fields = [
            'id',
            'pub_date',
            'status',
            'selected_on',
            'active'
        ]
        related_models = [Region, Regulation, RegulatoryFramework, ProductCategory, MaterialCategory, NewsCategory,
                          Document, User, Source, NewsRelevance, Substance]

    def get_queryset(self):
        return super(NewsDocument, self).get_queryset().select_related(
            'source', 'selected_by'
        ).prefetch_related(
            'regions', 'news_categories', 'product_categories', 'material_categories', 'documents',
            'regulations', 'regulatory_frameworks', 'news_relevance', 'substances',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Region):
            return related_instance.region_news.all()
        if isinstance(related_instance, Regulation):
            return related_instance.regulation_news.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.news_regulatory_frameworks.all()
        if isinstance(related_instance, ProductCategory):
            return related_instance.product_category_news.all()
        if isinstance(related_instance, MaterialCategory):
            return related_instance.material_category_news.all()
        if isinstance(related_instance, NewsCategory):
            return related_instance.news_categories.all()
        if isinstance(related_instance, Document):
            return related_instance.news_documents.all()
        if isinstance(related_instance, User):
            return related_instance.selected_by.all()
        if isinstance(related_instance, Source):
            return related_instance.news_source.all()
        if isinstance(related_instance, NewsRelevance):
            return related_instance.news
        if isinstance(related_instance, Substance):
            return related_instance.substances_news.all()


@registry.register_document
class NewsRelevanceLogDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    organization = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    news = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
        'status': fields.TextField(),
        'active': fields.BooleanField(),
        'news_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'topic': fields.ObjectField(properties={
                'id': fields.IntegerField(),
            }),
        }),
        'regions': fields.NestedField(properties={
            'id': fields.IntegerField(),
        }),
        'product_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'material_categories': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
        'regulatory_frameworks': fields.NestedField(properties={
            'id': fields.IntegerField()
        }),
    })
    created = fields.DateField()

    class Index:
        name = 'news_relevance_log'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = NewsRelevanceLog

        fields = [
            'id',
            'relevancy',
            'comment'
        ]

        related_models = [Organization, News]

    def get_queryset(self):
        return super(NewsRelevanceLogDocument, self).get_queryset().select_related(
            'organization', 'news', 'user',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Organization):
            return related_instance.newsrelevancelog_set.all()
        if isinstance(related_instance, News):
            return related_instance.news_relevance_log.all()

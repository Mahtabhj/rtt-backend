from datetime import datetime

import pytz
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from rttcore.elasticsearch_analyzer import html_strip, search_analyzer, case_insensitive_sort_analyzer
from rttnews.models.models import News, NewsCategory
from rttorganization.models.models import Organization
from rttproduct.models.models import MaterialCategory, ProductCategory, Product
from rttproduct.models.core_models import Industry
from rttproduct.services.product_services import ProductServices
from rttregulation.models.core_models import Topic
from rttregulation.models.models import Region, Regulation, RegulatoryFramework, RegulationMilestone, Status
from rttsubstance.models import Substance

utc = pytz.UTC


@registry.register_document
class MaterialCategoryDocument(Document):
    material_category_news = fields.NestedField(properties={
        'body': fields.TextField(analyzer=html_strip),
        'title': fields.TextField(),
        'id': fields.IntegerField(),
        'modified': fields.DateField(),
        'pub_date': fields.DateField(),
        'created': fields.DateField(),
    })
    # Related Products
    product_material_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        })
    })
    regulation_material_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'modified': fields.DateField(),
    })
    material_cat_reg_framework = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    industry = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    class Index:
        name = 'material_category'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = MaterialCategory

        fields = [
            'id',
            'name'
        ]
        related_models = [News, Product, Regulation, RegulatoryFramework, Industry]

    def get_queryset(self):
        return super(MaterialCategoryDocument, self).get_queryset().select_related(
            'industry',
        ).prefetch_related(
            'material_category_news', 'product_material_categories', 'regulation_material_categories',
            'material_cat_reg_framework',
        )

    @staticmethod
    def get_instances_from_related(related_instance):
        if isinstance(related_instance, News):
            return related_instance.material_categories.all()
        if isinstance(related_instance, Product):
            return related_instance.material_categories.all()
        if isinstance(related_instance, Regulation):
            return related_instance.material_categories.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.material_categories.all()
        if isinstance(related_instance, Industry):
            return related_instance.material_category_industry.all()


@registry.register_document
class ProductCategoryDocument(Document):
    parent = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    product_category_news = fields.NestedField(properties={
        'body': fields.TextField(analyzer=html_strip),
        'title': fields.TextField(),
        'id': fields.IntegerField(),
    })
    # Related Products
    product_product_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        })
    })
    regulation_product_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'modified': fields.DateField(),
    })
    product_cat_reg_framework = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    industry = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    class Index:
        name = 'product_category'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = ProductCategory

        fields = [
            'id',
            'name'
        ]
        related_models = [News, Product, Regulation, RegulatoryFramework, Industry]

    def get_queryset(self):
        return super(ProductCategoryDocument, self).get_queryset().select_related(
            'parent',
        ).prefetch_related(
            'industry', 'product_category_news', 'product_product_categories', 'regulation_product_categories',
            'product_cat_reg_framework',
        )

    @staticmethod
    def get_instances_from_related(related_instance):
        if isinstance(related_instance, News):
            return related_instance.product_categories.all()
        if isinstance(related_instance, Product):
            return related_instance.product_categories.all()
        if isinstance(related_instance, Regulation):
            return related_instance.product_categories.all()
        if isinstance(related_instance, RegulatoryFramework):
            return related_instance.product_categories.all()
        if isinstance(related_instance, Industry):
            return related_instance.product_category_industries.all()


@registry.register_document
class ProductDocument(Document):
    name = fields.TextField(search_analyzer=search_analyzer, analyzer=case_insensitive_sort_analyzer, fielddata='true')
    description = fields.TextField(analyzer=html_strip)
    image = fields.FileField()
    created = fields.DateField()
    last_mentioned = fields.DateField()
    organization = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    product_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'parent': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
        }),
        'product_product_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField()
        }),
        'product_cat_reg_framework': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField(),
            'regions': fields.NestedField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField()
            }),
            'topics': fields.NestedField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField()
            }),
        }),
        'product_category_news': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'title': fields.TextField(),
            'pub_date': fields.DateField(),
            'body': fields.TextField(),
            'cover_image': fields.FileField(),
            'status': fields.TextField(),
            'active': fields.BooleanField(),
            'news_categories': fields.NestedField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField(),
                'topic': fields.ObjectField(properties={
                    'id': fields.IntegerField(),
                    'name': fields.TextField(),
                }),
            }),
        }),
    })
    material_categories = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'short_name': fields.TextField(),
        'product_material_categories': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'description': fields.TextField()
        }),
        'material_cat_reg_framework': fields.NestedField(properties={
            'name': fields.TextField(),
            'id': fields.IntegerField(),
            'regions': fields.NestedField(properties={
                'id': fields.IntegerField(),
                'name': fields.TextField()
            }),
        }),
        'material_category_news': fields.NestedField(properties={
            'id': fields.IntegerField(),
            'title': fields.TextField(),
        }),
        'industry': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })
    substances = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })
    substance_use_and_apps = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'organization': fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField()
        })
    })

    def prepare_last_mentioned(self, instance):
        news_date = datetime.strptime('09-19-1800 00:00:00', '%m-%d-%Y %H:%M:%S').replace(tzinfo=utc)
        product_category_list = []
        for product_category in instance.product_categories.all():
            product_category_list.extend(ProductServices().get_all_parent_product_category_list(product_category))

        for data in product_category_list:
            for item in data.regulation_product_categories.all():
                reg_milestone = item.regulation_milestone.all().order_by("-created").first()
                if reg_milestone is not None:
                    if reg_milestone.created > news_date:
                        news_date = reg_milestone.created
            for item in data.product_cat_reg_framework.all():
                frame_milestone = item.regulatory_framework_milestone.all().order_by("-created").first()
                if frame_milestone is not None:
                    if frame_milestone.created > news_date:
                        news_date = frame_milestone.created
            latest_news = data.product_category_news.all().order_by("-pub_date").first()
            if latest_news and latest_news.active:
                if latest_news.pub_date > news_date:
                    news_date = latest_news.pub_date
        for data in instance.material_categories.all():
            for item in data.regulation_material_categories.all():
                reg_milestone = item.regulation_milestone.all().order_by("-created").first()
                if reg_milestone is not None:
                    if reg_milestone.created > news_date:
                        news_date = reg_milestone.created
            for item in data.material_cat_reg_framework.all():
                frame_milestone = item.regulatory_framework_milestone.all().order_by("-created").first()
                if frame_milestone is not None:
                    if frame_milestone.created > news_date:
                        news_date = frame_milestone.created
            latest_news = data.material_category_news.all().order_by("-pub_date").first()
            if latest_news and latest_news.active:
                if latest_news.pub_date > news_date:
                    news_date = latest_news.pub_date
        return news_date

    class Index:
        name = 'product'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Product

        fields = [
            'id'
        ]
        related_models = [Organization, ProductCategory, MaterialCategory, Substance]

    def get_queryset(self):
        return super(ProductDocument, self).get_queryset().select_related(
            'organization',
        ).prefetch_related(
            'material_categories', 'product_categories', 'substances'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Organization):
            return related_instance.product_organization.all()
        if isinstance(related_instance, ProductCategory):
            return related_instance.product_product_categories.all()
        if isinstance(related_instance, MaterialCategory):
            return related_instance.product_material_categories.all()
        if isinstance(related_instance, Substance):
            return related_instance.substances_product.all()

from django.db.models import Q

from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework.validators import UniqueTogetherValidator

from rttproduct.models.core_models import Industry
from rttproduct.models.models import Product, ProductCategory, MaterialCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ProductUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'organization', 'material_categories', 'product_categories',
                  'substance_use_and_apps')
        validators = [
            UniqueTogetherValidator(
                queryset=Product.objects.all(),
                fields=['name', 'organization'],
                message='Product having same name and organization already exists'
            )
        ]


class ProductIdNameImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'image', )


class ProductIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class ProductCategoryIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'parent')


class MaterialCategoryIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = ('id', 'name')


class IndustrySerializer(serializers.ModelSerializer):
    product_categories = ProductCategoryIdNameSerializer(many=True, read_only=True,
                                                         source='product_category_industries')
    material_categories = MaterialCategoryIdNameSerializer(many=True, read_only=True,
                                                           source='material_category_industry')

    class Meta:
        model = Industry
        fields = ('id', 'name', 'description', 'product_categories', 'material_categories')


class ProductCategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), allow_null=True)
    industry = serializers.PrimaryKeyRelatedField(many=True, queryset=Industry.objects.all())

    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'description', 'online', 'parent', 'industry', 'image')

    def validate(self, data):
        prod_cat_name = data.get('name', None)
        if data.get('industry', None):
            print(data.get('industry'))

            for industry in data.get('industry'):
                already_exists = False
                if self.context['request'].method == 'POST':
                    already_exists = Industry.objects.filter(
                        Q(product_category_industries__name__exact=prod_cat_name) &
                        Q(id=industry.id)
                    ).exists()
                elif self.context['request'].method == 'PUT' or self.context['request'].method == 'PATCH':
                    prod_cat_id = int(self.context['view'].kwargs['pk'])
                    already_exists = Industry.objects.filter(
                        ~Q(product_category_industries__id=prod_cat_id) &
                        Q(product_category_industries__name__exact=prod_cat_name) &
                        Q(id=industry.id)
                    ).exists()

                if already_exists:
                    raise serializers.ValidationError("Product category name and Industry must be unique")
        return data


class MaterialCategoryIdNameShortNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = ('id', 'name', 'short_name')


class MaterialCategorySerializer(serializers.ModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all())

    class Meta:
        model = MaterialCategory
        fields = ('id', 'name', 'description', 'online', 'industry', 'image')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('name', 'industry'),
                message=_('Name and Industry should be unique!!')
            )
        ]


class MaterialCategoryDetailsSerializer(serializers.ModelSerializer):
    industry = IndustrySerializer(read_only=True)

    class Meta:
        model = MaterialCategory
        fields = ('id', 'name', 'description', 'online', 'industry', 'image')


class ProductSerializerDetails(serializers.ModelSerializer):
    product_categories = ProductCategorySerializer(many=True, read_only=True)
    material_categories = MaterialCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('material_categories', 'product_categories')

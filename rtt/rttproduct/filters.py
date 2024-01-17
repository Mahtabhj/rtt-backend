import django_filters

from rttdocument.filters import NumberInFilter
from rttproduct.models.models import ProductCategory


class ProductCategoryFilter(django_filters.FilterSet):
    industry = NumberInFilter(field_name='industry', lookup_expr='in')

    class Meta:
        model = ProductCategory
        fields = ['industry', ]

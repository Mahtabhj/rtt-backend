import django_filters

from rttdocument.filters import NumberInFilter
from rttregulation.models.models import Regulation, RegulatoryFramework


class RegulationFilter(django_filters.FilterSet):
    regulatory_framework = NumberInFilter(field_name='regulatory_framework', lookup_expr='in')
    type = NumberInFilter(field_name='type', lookup_expr='in')
    rf_id = NumberInFilter(field_name='regulatory_framework', lookup_expr='in')

    class Meta:
        model = Regulation
        fields = ('regulatory_framework', 'type', 'review_status', )


class RegulatoryFrameworkFilter(django_filters.FilterSet):
    issuing_body = NumberInFilter(field_name='issuing_body', lookup_expr='in')
    status = NumberInFilter(field_name='status', lookup_expr='in')
    regions = NumberInFilter(field_name='regions', lookup_expr='in')
    material_categories = NumberInFilter(field_name='material_categories', lookup_expr='in')
    product_categories = NumberInFilter(field_name='product_categories', lookup_expr='in')

    class Meta:
        model = RegulatoryFramework
        fields = ('issuing_body', 'status', 'regions', 'material_categories', 'product_categories', 'review_status')

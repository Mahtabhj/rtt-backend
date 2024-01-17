import django_filters

from rttsubstance.models import SubstancePropertyDataPoint, Substance


class SubstancePropertyDataPointFilter(django_filters.FilterSet):
    property_data_point = django_filters.CharFilter(field_name='property_data_point__name', lookup_expr='icontains')
    property = django_filters.CharFilter(field_name='property_data_point__property__name', lookup_expr='icontains')
    value = django_filters.CharFilter(field_name='value', lookup_expr='icontains')

    class Meta:
        model = SubstancePropertyDataPoint
        fields = ('property_data_point', 'property', 'status', 'value',)


class SubstanceFamilyFilter(django_filters.FilterSet):
    family_name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    chemycal_id = django_filters.CharFilter(field_name='chemycal_id', lookup_expr='iexact')

    class Meta:
        model = Substance
        fields = ('family_name', 'chemycal_id',)

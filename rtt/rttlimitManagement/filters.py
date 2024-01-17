import django_filters

from rttlimitManagement.models import RegulationSubstanceLimit, Exemption


class RegulationSubstanceLimitFilter(django_filters.FilterSet):
    regulatory_framework = django_filters.CharFilter(field_name='regulatory_framework__name', lookup_expr='icontains')
    regulation = django_filters.CharFilter(field_name='regulation__name', lookup_expr='icontains')

    class Meta:
        model = RegulationSubstanceLimit
        fields = ('regulatory_framework', 'regulation', 'status', )


class ExemptionFilter(django_filters.FilterSet):
    regulatory_framework = django_filters.CharFilter(field_name='regulatory_framework__name', lookup_expr='icontains')
    regulation = django_filters.CharFilter(field_name='regulation__name', lookup_expr='icontains')

    class Meta:
        model = Exemption
        fields = ('regulatory_framework', 'regulation', 'status', )

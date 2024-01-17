import django_filters

from rttdocument.models.models import Document


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class DocumentFilter(django_filters.FilterSet):
    type = NumberInFilter(field_name='type', lookup_expr='in')
    regulation_documents = NumberInFilter(field_name='regulation_documents', lookup_expr='in')

    class Meta:
        model = Document
        fields = ('type', 'regulation_documents')

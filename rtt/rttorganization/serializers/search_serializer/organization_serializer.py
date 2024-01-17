from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from rttorganization.models.search_models.organization import OrganizationDocument

__all__ = (
    'OrganizationDocumentSerializer',
)


class OrganizationDocumentSerializer(DocumentSerializer):

    class Meta(object):

        document = OrganizationDocument
        fields = ('id', 'name', 'description', 'address')

    def get_highlight(self, obj):
        if hasattr(obj.meta, 'highlight'):
            return obj.meta.highlight.__dict__['_d_']
        return {}

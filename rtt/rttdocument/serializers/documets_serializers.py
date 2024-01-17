from rest_framework.serializers import ModelSerializer

from rttdocument.models.models import DocumentType, Document, Help


class DocumentTypeSerializer(ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'


class DocumentTypeIdNameSerializer(ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name')


class DocumentSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.type:
            data['type'] = DocumentTypeIdNameSerializer(instance.type).data
        return data

    class Meta:
        model = Document
        fields = '__all__'


class DocumentDetailSerializer(ModelSerializer):
    type = DocumentTypeIdNameSerializer(read_only=True)

    class Meta:
        model = Document
        fields = '__all__'


class HelpSerializer(ModelSerializer):

    class Meta:
        model = Help
        fields = ['id', 'title', 'description', 'type', 'document']

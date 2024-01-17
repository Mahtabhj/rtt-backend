from rest_framework.serializers import ModelSerializer, ValidationError

from rttlimitManagement.models import LimitAttribute, RegulationSubstanceLimit, Exemption
from rttlimitManagement.services.additional_attributes_data_service import AdditionalAttributesDataService
from rttregulation.serializers.serializers import RegulationIdNameSerializer, RegulatoryFrameworkIdNameSerializer
from rttsubstance.serializers import SubstanceIdNameCasEcSerializer


class LimitAttributeIdNameSerializer(ModelSerializer):
    class Meta:
        model = LimitAttribute
        fields = ['id', 'name']


class RegulationSubstanceLimitDetailSerializer(ModelSerializer):
    regulation = RegulationIdNameSerializer(read_only=True)
    regulatory_framework = RegulatoryFrameworkIdNameSerializer(read_only=True)
    substance = SubstanceIdNameCasEcSerializer(read_only=True)

    class Meta:
        model = RegulationSubstanceLimit
        fields = ('id', 'regulation', 'regulatory_framework', 'substance', 'scope', 'limit_value',
                  'measurement_limit_unit', 'limit_note', 'status', 'date_into_force', 'modified')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.regulatory_framework:
            is_regulation = False
            regulation_id = instance.regulatory_framework.id
            data['regions'] = []
            for region in instance.regulatory_framework.regions.all():
                data['regions'].append({
                    'id': region.id,
                    'name': region.name
                })
        else:
            is_regulation = True
            regulation_id = instance.regulation.id
            data['regions'] = []
            if instance.regulation.regulatory_framework:
                for region in instance.regulation.regulatory_framework.regions.all():
                    data['regions'].append({
                        'id': region.id,
                        'name': region.name
                    })
        data['limit_attributes'] = AdditionalAttributesDataService.get_additional_attributes_data(
            instance.id, regulation_id, is_regulation)
        return data


class RegulationSubstanceLimitSerializer(ModelSerializer):

    class Meta:
        model = RegulationSubstanceLimit
        fields = '__all__'


class RegulationSubstanceLimitCreateSerializer(ModelSerializer):

    class Meta:
        model = RegulationSubstanceLimit
        fields = '__all__'

    def validate(self, data):
        if data.get('regulation', None) and data.get('regulatory_framework', None):
            raise ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not data.get('regulation', None) and not data.get('regulatory_framework', None):
            raise ValidationError("Both Regulation or Regulatory framework fields can't be set empty.")
        return data


class ExemptionDetailSerializer(ModelSerializer):
    regulation = RegulationIdNameSerializer(read_only=True)
    regulatory_framework = RegulatoryFrameworkIdNameSerializer(read_only=True)
    substance = SubstanceIdNameCasEcSerializer(read_only=True)

    class Meta:
        model = Exemption
        fields = ('id', 'regulation', 'regulatory_framework', 'substance', 'article', 'reference', 'application',
                  'expiration_date', 'date_into_force', 'status', 'modified')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.regulatory_framework:
            data['regions'] = []
            for region in instance.regulatory_framework.regions.all():
                data['regions'].append({
                    'id': region.id,
                    'name': region.name
                })
        else:
            data['regions'] = []
            if instance.regulation.regulatory_framework:
                for region in instance.regulation.regulatory_framework.regions.all():
                    data['regions'].append({
                        'id': region.id,
                        'name': region.name
                    })
        return data


class ExemptionSerializer(ModelSerializer):

    class Meta:
        model = Exemption
        fields = '__all__'


class ExemptionCreateSerializer(ModelSerializer):

    class Meta:
        model = Exemption
        fields = '__all__'

    def validate(self, data):
        if data.get('regulation', None) and data.get('regulatory_framework', None):
            raise ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not data.get('regulation', None) and not data.get('regulatory_framework', None):
            raise ValidationError("Both Regulation or Regulatory framework fields can't be set empty.")
        return data


class ExemptionUpdateSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ExemptionUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Exemption
        fields = '__all__'

    def validate(self, data):
        if data.get('regulation', None) and data.get('regulatory_framework', None):
            raise ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not data.get('regulation', None) and not data.get('regulatory_framework', None):
            raise ValidationError("Both Regulation or Regulatory framework fields can't be set empty.")
        return data

    def update(self, instance, validated_data):
        if validated_data.get('regulatory_framework', None):
            if instance.regulation:
                instance.regulation = None
            instance.regulatory_framework = validated_data['regulatory_framework']
        if validated_data.get('regulation', None):
            if instance.regulatory_framework:
                instance.regulatory_framework = None
            instance.regulation = validated_data['regulation']
        super(ExemptionUpdateSerializer, self).update(instance, validated_data)
        return instance

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from rttsubstance.models import Property, SubstanceUsesAndApplication, Substance, SubstancePropertyDataPoint, \
    PropertyDataPoint, SubstanceFamily


class PropertySerializer(ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'name', 'short_name', 'url_link']


class SubstanceUsesAndApplicationSerializer(ModelSerializer):
    class Meta:
        model = SubstanceUsesAndApplication
        fields = ['id', 'name', 'organization', 'created', 'modified']
        read_only_fields = ('substances', )
        validators = [
            UniqueTogetherValidator(
                queryset=SubstanceUsesAndApplication.objects.all(),
                fields=['name', 'organization'],
                message='The Use & application already exists!'
            )
        ]


class SubstanceUsesAndApplicationUpdateSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(SubstanceUsesAndApplicationUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = SubstanceUsesAndApplication
        fields = ['id', 'name', 'organization', 'created', 'modified']
        read_only_fields = ('substances', 'organization')
        validators = [
            UniqueTogetherValidator(
                queryset=SubstanceUsesAndApplication.objects.all(),
                fields=['name', 'organization'],
                message='The Use & application already exists!'
            )
        ]


class SubstanceIdNameCasEcSerializer(ModelSerializer):
    class Meta:
        model = Substance
        fields = ('id', 'name', 'cas_no', 'ec_no',)


class PropertyDataPointIdNameCasEcSerializer(ModelSerializer):
    class Meta:
        model = PropertyDataPoint
        fields = ('id', 'name',)


class SubstancePropertyDataPointListSerializer(ModelSerializer):
    substance = SubstanceIdNameCasEcSerializer(read_only=True)
    property_data_point = PropertyDataPointIdNameCasEcSerializer(read_only=True)

    class Meta:
        model = SubstancePropertyDataPoint
        fields = ('id', 'substance', 'property_data_point', 'value', 'status', 'modified',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['property'] = {
            'id': instance.property_data_point.property.id,
            'name': instance.property_data_point.property.name,
        }
        return data


class SubstancePropertyDataPointSerializer(ModelSerializer):

    class Meta:
        model = SubstancePropertyDataPoint
        fields = '__all__'

    def validate(self, data):
        substance = data.get('substance', None)
        property_data_point = data.get('property_data_point', None)
        status = data.get('status', None)
        queryset = SubstancePropertyDataPoint.objects.filter(substance=substance,
                                                             property_data_point=property_data_point, status='active')
        if queryset.count() == 1 and status == 'active':
            raise serializers.ValidationError("(substance_id, property_data_point_id, status=active) already exists.")
        return data


class SubstancePropertyDataPointUpdateSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(SubstancePropertyDataPointUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = SubstancePropertyDataPoint
        fields = '__all__'

    def validate(self, data):
        substance = data.get('substance', None)
        property_data_point = data.get('property_data_point', None)
        status = data.get('status', None)
        if substance.id == self.instance.substance_id and property_data_point.id == self.instance.property_data_point_id \
                and status == self.instance.status:
            return data
        queryset = SubstancePropertyDataPoint.objects.filter(substance=substance,
                                                             property_data_point=property_data_point, status='active')
        if queryset.count() == 1 and status == 'active':
            raise serializers.ValidationError("(substance_id, property_data_point_id, status=active) already exists.")
        return data


class SubstanceFamilySerializer(ModelSerializer):
    class Meta:
        model = Substance
        fields = ('id', 'name', 'chemycal_id', 'is_family')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['number_of_substances'] = SubstanceFamily.objects.filter(family_id=instance.id).count()
        return data


class SubstanceFamilyUpdateSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(SubstanceFamilyUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Substance
        fields = ('id', 'name', 'chemycal_id',)


class SubstanceSerializer(ModelSerializer):
    class Meta:
        model = Substance
        fields = '__all__'

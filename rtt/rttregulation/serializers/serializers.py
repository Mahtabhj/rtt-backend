from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from elasticsearch_dsl import Q

from rttauth.serializers.auth_serializers import UserIdUserNameFirstNameLastNameSerializer, \
    UserIdUserNameFirstNameLastNameAvatarSerializer
from rttdocument.serializers.documets_serializers import DocumentSerializer
from rttproduct.serializers.serializers import MaterialCategorySerializer, ProductCategorySerializer, \
    MaterialCategoryIdNameSerializer, ProductCategoryIdNameSerializer
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttregulation.models.core_models import Topic
from rttregulation.models.models import (Language, Status, Region, Url, RegulatoryFramework, MilestoneType,
                                         RegulationMilestone, IssuingBody, RegulationType, Regulation, QuestionType,
                                         Question, Answer, RegulationRatingLog, RegulatoryFrameworkRatingLog)
from rttsubstance.documents import SubstanceDocument


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'description', 'code']


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'description']


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class UrlSerializer(ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'


class RegulatoryFrameworkSerializer(ModelSerializer):
    class Meta:
        model = RegulatoryFramework
        fields = '__all__'


class RegionIdNameSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class IssuingBodyDetailSerializer(ModelSerializer):
    region = RegionIdNameSerializer(read_only=True)

    class Meta:
        model = IssuingBody
        fields = ['id', 'name', 'description', 'region', 'url']


class IssuingBodySerializer(ModelSerializer):
    class Meta:
        model = IssuingBody
        fields = '__all__'


class MilestoneTypeSerializer(ModelSerializer):
    class Meta:
        model = MilestoneType
        fields = ['id', 'name', 'description']


class MilestoneSerializer(ModelSerializer):
    def to_internal_value(self, data):
        data['regulatory_framework'] = data.get('regulatory_framework', None)
        data['regulation'] = data.get('regulation', None)
        return super().to_internal_value(data)

    class Meta:
        model = RegulationMilestone
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('name', 'regulation'),
                message=_('A milestone with the specified name already exists in this regulation.')
            ),
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('name', 'regulatory_framework'),
                message=_('A milestone with the specified name already exists in this regulatory framework.')
            )
        ]

    def validate(self, data):
        if data.get('regulation', None) and data.get('regulatory_framework', None):
            raise serializers.ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not data.get('regulation', None) and not data.get('regulatory_framework', None):
            raise serializers.ValidationError("Both Regulation or Regulatory framework fields can't be set empty.")
        return data


class MilestoneListSerializer(ModelSerializer):
    type = MilestoneTypeSerializer(read_only=True)

    class Meta:
        model = RegulationMilestone
        fields = '__all__'


class RegulationTypeSerializer(ModelSerializer):
    class Meta:
        model = RegulationType
        fields = ['id', 'name', 'description']


class RegulationTypeIdNameSerializer(ModelSerializer):
    class Meta:
        model = RegulationType
        fields = ['id', 'name']


class StatusIdNameSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description']


class TopicIdNameSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class RegulatoryFrameworkIdNameSerializer(ModelSerializer):
    class Meta:
        model = RegulatoryFramework
        fields = ['id', 'name']


class RegulationListSerializer(ModelSerializer):
    type = RegulationTypeIdNameSerializer(read_only=True)
    status = StatusIdNameSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    regulatory_framework = RegulatoryFrameworkIdNameSerializer(read_only=True)
    material_categories = MaterialCategoryIdNameSerializer(read_only=True, many=True)
    product_categories = ProductCategoryIdNameSerializer(read_only=True, many=True)
    urls = UrlSerializer(read_only=True, many=True)
    documents = DocumentSerializer(read_only=True, many=True)
    topics = TopicSerializer(read_only=True, many=True)

    class Meta:
        model = Regulation
        fields = '__all__'


class RegulationDetailSerializer(ModelSerializer):
    type = RegulationTypeIdNameSerializer(read_only=True)
    status = StatusIdNameSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    regulatory_framework = RegulatoryFrameworkIdNameSerializer(read_only=True)
    material_categories = MaterialCategoryIdNameSerializer(read_only=True, many=True)
    product_categories = ProductCategoryIdNameSerializer(read_only=True, many=True)
    urls = UrlSerializer(read_only=True, many=True)
    documents = DocumentSerializer(read_only=True, many=True)
    topics = TopicSerializer(read_only=True, many=True)
    substances = SerializerMethodField()

    class Meta:
        model = Regulation
        fields = '__all__'

    @staticmethod
    def get_substances(obj):
        substance_doc_qs: SubstanceDocument = SubstanceDocument.search().filter(
            'nested',
            path='substances_regulation',
            query=Q('match', substances_regulation__id=obj.id)
        )
        substance_doc_qs = substance_doc_qs[0:substance_doc_qs.count()]
        result = RelevantSubstanceService().get_substance_and_organization(substance_doc_qs)
        return result


class RegulationSerializer(ModelSerializer):
    class Meta:
        model = Regulation
        fields = '__all__'


class RegulationIdNameSerializer(ModelSerializer):
    class Meta:
        model = Regulation
        fields = ['id', 'name']


class RegulatoryFrameworkListSerializer(ModelSerializer):
    language = LanguageSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    issuing_body = IssuingBodySerializer(read_only=True)
    regions = RegionSerializer(read_only=True, many=True)
    documents = DocumentSerializer(read_only=True, many=True)
    material_categories = MaterialCategorySerializer(read_only=True, many=True)
    product_categories = ProductCategorySerializer(read_only=True, many=True)
    urls = UrlSerializer(read_only=True, many=True)
    regulation_regulatory_framework = RegulationSerializer(read_only=True, many=True)
    topics = TopicSerializer(read_only=True, many=True)

    class Meta:
        model = RegulatoryFramework
        fields = ['id', 'name', 'description', 'review_status', 'language', 'status', 'issuing_body',
                  'regions', 'documents', 'material_categories', 'product_categories', 'urls',
                  'regulation_regulatory_framework', 'topics']


class RegulatoryFrameworkDetailsSerializer(ModelSerializer):
    language = LanguageSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    issuing_body = IssuingBodySerializer(read_only=True)
    regions = RegionSerializer(read_only=True, many=True)
    documents = DocumentSerializer(read_only=True, many=True)
    material_categories = MaterialCategorySerializer(read_only=True, many=True)
    product_categories = ProductCategorySerializer(read_only=True, many=True)
    urls = UrlSerializer(read_only=True, many=True)
    regulation_regulatory_framework = RegulationSerializer(read_only=True, many=True)
    topics = TopicSerializer(read_only=True, many=True)
    substances = SerializerMethodField()

    class Meta:
        model = RegulatoryFramework
        fields = ['id', 'name', 'description', 'review_status', 'language', 'status', 'issuing_body',
                  'regions', 'documents', 'material_categories', 'product_categories', 'urls',
                  'regulation_regulatory_framework', 'topics', 'substances']

    @staticmethod
    def get_substances(obj):
        substance_doc_qs: SubstanceDocument = SubstanceDocument.search().filter(
            'nested',
            path='substances_regulatory_framework',
            query=Q('match', substances_regulatory_framework__id=obj.id)
        )
        substance_doc_qs = substance_doc_qs[0:substance_doc_qs.count()]
        result = RelevantSubstanceService().get_substance_and_organization(substance_doc_qs)
        return result


class QuestionTypeSerializer(ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('edited', 'pin_by',)

    def validate(self, data):
        if data.get('regulation', None) and data.get('regulatory_framework', None):
            raise serializers.ValidationError("Only Regulation OR Regulatory framework can be set.")
        elif not data.get('regulation', None) and not data.get('regulatory_framework', None):
            raise serializers.ValidationError("Both Regulation AND Regulatory framework fields can't be set empty.")
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.answered_by:
            data['answered_by'] = UserIdUserNameFirstNameLastNameAvatarSerializer(instance.answered_by).data
        if instance.pin_by:
            data['pin_by'] = UserIdUserNameFirstNameLastNameSerializer(instance.pin_by).data
        return data


class AnswerUpdateSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(AnswerUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('answered_by', 'pin_by',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.answered_by:
            data['answered_by'] = UserIdUserNameFirstNameLastNameAvatarSerializer(instance.answered_by).data
        if instance.pin_by:
            data['pin_by'] = UserIdUserNameFirstNameLastNameSerializer(instance.pin_by).data
        return data


class AnswerPinSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(AnswerPinSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('id', 'answer_text', 'question', 'regulation', 'regulatory_framework', 'answered_by',
                            'edited',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.answered_by:
            data['answered_by'] = UserIdUserNameFirstNameLastNameAvatarSerializer(instance.answered_by).data
        if instance.pin_by:
            data['pin_by'] = UserIdUserNameFirstNameLastNameSerializer(instance.pin_by).data
        return data


class RegionSerializerImpactAssessmentSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = ['name']


class RegulatoryFrameworkImpactAssessmentSerializer(ModelSerializer):
    issuing_body = IssuingBodySerializer(read_only=True)
    regions = RegionSerializerImpactAssessmentSerializer(read_only=True, many=True)

    class Meta:
        model = RegulatoryFramework
        fields = ['issuing_body', 'regions']


class ImpactAssessmentRegulationSerializer(ModelSerializer):
    regulatory_framework = RegulatoryFrameworkImpactAssessmentSerializer(read_only=True)

    class Meta:
        model = Regulation
        fields = ['name', 'regulatory_framework']


class RegulationRatingLogSerializer(ModelSerializer):

    def to_internal_value(self, data):
        user = self.context['request'].user
        data['user'] = user.id
        data['organization'] = user.organization.id
        return super().to_internal_value(data)

    class Meta:
        model = RegulationRatingLog
        fields = ['id', 'rating', 'comment', 'organization', 'regulation', 'user', 'prev_rating', 'parent']


class RegulatoryFrameworkRatingLogSerializer(ModelSerializer):
    def to_internal_value(self, data):
        user = self.context['request'].user
        data['user'] = user.id
        data['organization'] = user.organization.id
        return super().to_internal_value(data)

    class Meta:
        model = RegulatoryFrameworkRatingLog
        fields = ['id', 'rating', 'comment', 'organization', 'regulatory_framework', 'user', 'prev_rating', 'parent']

import requests
import logging
from rest_framework import serializers
from django.core.files.base import ContentFile
from rest_framework.fields import SerializerMethodField
from elasticsearch_dsl import Q

from rttauth.serializers.auth_serializers import UserIdUserNameFirstNameLastNameSerializer, \
    UserIdUserNameFirstNameLastNameAvatarSerializer
from rttnews.models.models import News, NewsCategory, Source, NewsRelevanceLog, SourceType, NewsAssessmentWorkflow, \
    NewsAnswer, NewsQuestion
from rttdocument.models.models import Document, DocumentType
from rttauth.models.models import User
from rttregulation.serializers.serializers import TopicIdNameSerializer, RegionIdNameSerializer, \
    RegulationIdNameSerializer, RegulatoryFrameworkIdNameSerializer
from rttproduct.serializers.serializers import ProductCategoryIdNameSerializer, \
    MaterialCategoryIdNameSerializer
from rttorganization.serializers.serializers import OrganizationIdNameSerializer
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttsubstance.documents import SubstanceDocument

logger = logging.getLogger(__name__)


class NewsDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'attachment')


class UserIdNameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name')

    @staticmethod
    def get_name(obj):
        return '{} {}'.format(obj.first_name, obj.last_name)


class SourceIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id', 'name')


class NewsCategorySerializer(serializers.ModelSerializer):
    topic = TopicIdNameSerializer(read_only=True)

    class Meta:
        model = NewsCategory
        fields = '__all__'


class NewsCategoryIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


class NewsIdTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', )


class NewsListSerializer(serializers.ModelSerializer):
    documents = NewsDocumentSerializer(read_only=True, many=True)
    selected_by = UserIdNameSerializer(read_only=True)
    discharged_by = UserIdNameSerializer(read_only=True)
    source = SourceIdNameSerializer(read_only=True)
    news_categories = NewsCategorySerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = '__all__'


class NewsDetailSerializer(serializers.ModelSerializer):
    documents = NewsDocumentSerializer(read_only=True, many=True)
    selected_by = UserIdNameSerializer(read_only=True)
    discharged_by = UserIdNameSerializer(read_only=True)
    source = SourceIdNameSerializer(read_only=True)
    news_categories = NewsCategorySerializer(read_only=True, many=True)
    substances = SerializerMethodField()
    product_categories = ProductCategoryIdNameSerializer(read_only=True, many=True)
    material_categories = MaterialCategoryIdNameSerializer(read_only=True, many=True)
    regions = RegionIdNameSerializer(read_only=True, many=True)
    regulations = RegulationIdNameSerializer(read_only=True, many=True)
    regulatory_frameworks = RegulatoryFrameworkIdNameSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = '__all__'

    @staticmethod
    def get_substances(obj):
        substance_doc_qs: SubstanceDocument = SubstanceDocument.search().filter(
            'nested',
            path='substances_news',
            query=Q('match', substances_news__id=obj.id)
        )
        substance_doc_qs = substance_doc_qs[0:substance_doc_qs.count()]
        result = RelevantSubstanceService().get_substance_and_organization(substance_doc_qs)
        return result


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class NewsPatchSerializer(serializers.ModelSerializer):
    substances = SerializerMethodField()

    class Meta:
        model = News
        fields = '__all__'

    @staticmethod
    def get_substances(obj):
        substance_doc_qs: SubstanceDocument = SubstanceDocument.search().filter(
            'nested',
            path='substances_news',
            query=Q('match', substances_news__id=obj.id)
        )
        substance_doc_qs = substance_doc_qs[0:substance_doc_qs.count()]
        result = RelevantSubstanceService().get_substance_and_organization(substance_doc_qs)
        return result


class NewsSerializerForNewsAssessmentWorkflow(serializers.ModelSerializer):
    source = SourceIdNameSerializer(read_only=True)
    news_categories = NewsCategoryIdNameSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ('id', 'pub_date', 'title', 'source', 'news_categories', )


class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class SourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceType
        fields = '__all__'


class NewsSourceDetailsSerializer(serializers.ModelSerializer):
    type = SourceTypeSerializer(read_only=True)
    news_source = SerializerMethodField()

    class Meta:
        model = Source
        fields = ['id', 'name', 'link', 'description', 'chemical_id', 'image', 'type', 'news_source']

    @staticmethod
    def get_news_source(obj):
        return obj.news_source.all().count()


class NewsRelevanceLogSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        user = self.context['request'].user
        data['user'] = user.id
        if 'organization' not in data or not user.is_superuser:
            data['organization'] = user.organization.id
        return super().to_internal_value(data)

    class Meta:
        model = NewsRelevanceLog
        fields = '__all__'


class NewsDocumentSaveSerializer(serializers.ModelSerializer):
    link = serializers.CharField(max_length=200)
    type = serializers.PrimaryKeyRelatedField(queryset=DocumentType.objects.all())

    class Meta:
        model = Document
        fields = ('title', 'description', 'type', 'link')

    def validate(self, attrs):
        try:
            link = attrs.get('link')
            try:
                response = requests.get(link)
            except requests.exceptions.SSLError as ex:
                logger.error(str(ex), exc_info=True)
                response = requests.get(link, verify=False)
            if response.status_code != requests.codes.ok:
                raise serializers.ValidationError('The file is not found!')
            file_name = link.split('/')[-1]
            file_content = ContentFile(response.content)
            attrs['file_content'] = file_content
            attrs['file_name'] = file_name
            return attrs
        except Exception as exc:
            logger.error(str(exc), exc_info=True)
        raise serializers.ValidationError('File cannot be accessed!')

    def save(self, link):
        title = self.validated_data.get('title')
        description = self.validated_data.get('description')
        document_type = self.validated_data.get('type')
        document = Document.objects.create(title=title, description=description, type=document_type)

        # Download and save file
        # response = requests.get(link)
        # if response.status_code == requests.codes.ok:
        #     raise FileNotFoundError('File not found')
        file_name = self.validated_data.get('file_name')
        file_content = self.validated_data.get('file_content')
        document.attachment.save(file_name, file_content)

        return document


class NewsAssessmentWorkflowSerializer(serializers.ModelSerializer):
    news = NewsSerializerForNewsAssessmentWorkflow(read_only=True)
    organization = OrganizationIdNameSerializer(read_only=True)

    class Meta:
        model = NewsAssessmentWorkflow
        fields = ('id', 'news', 'organization', 'status', )


class NewsAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAnswer
        fields = '__all__'
        read_only_fields = ('edited', 'pin_by',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.answered_by:
            data['answered_by'] = UserIdUserNameFirstNameLastNameAvatarSerializer(instance.answered_by).data
        if instance.pin_by:
            data['pin_by'] = UserIdUserNameFirstNameLastNameSerializer(instance.pin_by).data
        return data


class NewsAnswerUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(NewsAnswerUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = NewsAnswer
        fields = '__all__'
        read_only_fields = ('answered_by', 'pin_by',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.answered_by:
            data['answered_by'] = UserIdUserNameFirstNameLastNameAvatarSerializer(instance.answered_by).data
        if instance.pin_by:
            data['pin_by'] = UserIdUserNameFirstNameLastNameSerializer(instance.pin_by).data
        return data


class NewsAnswerPinSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(NewsAnswerPinSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = NewsAnswer
        fields = '__all__'
        read_only_fields = ('id', 'answer_text', 'question', 'news', 'answered_by', 'edited', )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.answered_by:
            data['answered_by'] = UserIdUserNameFirstNameLastNameAvatarSerializer(instance.answered_by).data
        if instance.pin_by:
            data['pin_by'] = UserIdUserNameFirstNameLastNameSerializer(instance.pin_by).data
        return data


class NewsQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsQuestion
        fields = '__all__'

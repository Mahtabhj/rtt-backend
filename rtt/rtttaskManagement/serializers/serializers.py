from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rtttaskManagement.models import Task, TaskComment
from rttregulation.models.models import Regulation, RegulatoryFramework
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttauth.serializers.auth_serializers import UserIdFirstNameLastNameAvatarSerializer
from rttproduct.serializers.serializers import ProductIdNameImageSerializer
from rttregulation.serializers.serializers import RegulatoryFrameworkIdNameSerializer, RegulationIdNameSerializer
from rttnews.serializers.serializers import NewsIdTitleSerializer
from rttsubstance.serializers import SubstanceIdNameCasEcSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('is_archive',)


class TaskCommentSerializer(ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_obj = User.objects.filter(id=instance.commented_by_id).first()
        data['commented_by'] = {
                'id': user_obj.id,
                'first_name': user_obj.first_name if user_obj.first_name else None,
                'last_name': user_obj.last_name if user_obj.last_name else None,
                'username': user_obj.username,
                'avatar': user_obj.avatar.url if user_obj.avatar else None
            }
        return data


class TaskCommentUpdateSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(TaskCommentUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ('task',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_obj = User.objects.filter(id=instance.commented_by_id).first()
        data['commented_by'] = {
                'id': user_obj.id,
                'first_name': user_obj.first_name if user_obj.first_name else None,
                'last_name': user_obj.last_name if user_obj.last_name else None,
                'username': user_obj.username,
                'avatar': user_obj.avatar.url if user_obj.avatar else None
            }
        return data


class TaskUpdateSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(TaskUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.created_by:
            data['created_by'] = UserIdFirstNameLastNameAvatarSerializer(instance.created_by).data
        if instance.assignee:
            data['assignee'] = UserIdFirstNameLastNameAvatarSerializer(instance.assignee).data
        if instance.products:
            data['products'] = ProductIdNameImageSerializer(instance.products, many=True).data
        if instance.regulatory_frameworks:
            data['regulatory_frameworks'] = RegulatoryFrameworkIdNameSerializer(instance.regulatory_frameworks,
                                                                                many=True).data
        if instance.regulations:
            data['regulations'] = RegulationIdNameSerializer(instance.regulations, many=True).data
        if instance.news:
            data['news'] = NewsIdTitleSerializer(instance.news, many=True).data
        if instance.substances:
            data['substances'] = SubstanceIdNameCasEcSerializer(instance.substances, many=True).data
        return data


class TaskDetailsSerializer(ModelSerializer):
    created_by = UserIdFirstNameLastNameAvatarSerializer(read_only=True)
    assignee = UserIdFirstNameLastNameAvatarSerializer(read_only=True)
    products = ProductIdNameImageSerializer(many=True, read_only=True)
    regulatory_frameworks = SerializerMethodField()
    regulations = SerializerMethodField()
    news = NewsIdTitleSerializer(many=True, read_only=True)
    substances = SubstanceIdNameCasEcSerializer(many=True, read_only=True)

    def get_regulations(self, task):
        organization_id = self.context['request'].user.organization_id
        rel_reg_ids = RelevantRegulationService().get_relevant_regulation_id_organization(organization_id)
        regulation_qs = Regulation.objects.filter(id__in=rel_reg_ids, task_regulations=task)
        serializer = RegulationIdNameSerializer(instance=regulation_qs, many=True, read_only=True)
        return serializer.data

    def get_regulatory_frameworks(self, task):
        organization_id = self.context['request'].user.organization_id
        rel_fw_ids = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(organization_id)
        framework_qs = RegulatoryFramework.objects.filter(id__in=rel_fw_ids, task_regulatory_frameworks=task)
        serializer = RegulatoryFrameworkIdNameSerializer(instance=framework_qs, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Task
        fields = '__all__'

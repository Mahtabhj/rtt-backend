from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from rttdocumentManagement.models import DocumentManagement, DocumentManagementComment
from rttregulation.serializers.serializers import RegulatoryFrameworkIdNameSerializer, RegulationIdNameSerializer
from rttproduct.serializers.serializers import ProductIdNameImageSerializer
from rttsubstance.serializers import SubstanceIdNameCasEcSerializer
from rttnews.serializers.serializers import NewsIdTitleSerializer
from rttauth.serializers.auth_serializers import UserIdUserNameFirstNameLastNameAvatarSerializer

User = get_user_model()


class DocumentManagementSerializer(ModelSerializer):
    class Meta:
        model = DocumentManagement
        fields = '__all__'

class DocumentManagementDetailSerializer(ModelSerializer):
    class Meta:
        model = DocumentManagement
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['regulatory_frameworks'] = RegulatoryFrameworkIdNameSerializer(instance=instance.regulatory_frameworks, many=True).data
        data['regulations'] = RegulationIdNameSerializer(instance=instance.regulations, many=True).data
        data['products'] = ProductIdNameImageSerializer(instance=instance.products, many=True).data
        data['substances'] = SubstanceIdNameCasEcSerializer(instance=instance.substances, many=True).data
        data['news'] = NewsIdTitleSerializer(instance=instance.news, many=True).data
        data['uploaded_by'] = UserIdUserNameFirstNameLastNameAvatarSerializer(instance=instance.uploaded_by).data
        return data


class DocumentManagementUpdateSerializer(ModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     kwargs['partial'] = True
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = DocumentManagement
        fields = '__all__'
        read_only_fields = ('uploaded_by',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['regulatory_frameworks'] = RegulatoryFrameworkIdNameSerializer(instance=instance.regulatory_frameworks, many=True).data
        data['regulations'] = RegulationIdNameSerializer(instance=instance.regulations, many=True).data
        data['products'] = ProductIdNameImageSerializer(instance=instance.products, many=True).data
        data['substances'] = SubstanceIdNameCasEcSerializer(instance=instance.substances, many=True).data
        data['news'] = NewsIdTitleSerializer(instance=instance.news, many=True).data
        data['uploaded_by'] = UserIdUserNameFirstNameLastNameAvatarSerializer(instance=instance.uploaded_by).data
        return data


class DocumentManagementCommentDefaultSerializer(ModelSerializer):
    class Meta:
        model = DocumentManagementComment
        fields = '__all__'


class DocumentManagementCommentUpdateSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)

    class Meta:
        model = DocumentManagementComment
        fields = '__all__'
        read_only_fields = ('document_management', 'commented_by',)

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


class DocumentManagementCommentSerializer(ModelSerializer):
    class Meta:
        model = DocumentManagementComment
        fields = '__all__'
        read_only_fields = ('edited',)

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

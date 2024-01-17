from django.contrib.auth import get_user_model
from rest_framework import serializers

from rttauth.models.models import UserInvite
from rttorganization.models.models import Organization
from rttorganization.serializers.serializers import OrganizationIdNameSerializer

User = get_user_model()


class UserIdUserNameFirstNameLastNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', )


class UserIdFirstNameLastNameAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar', )


class UserIdUserNameFirstNameLastNameAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar', )


class UserDetailSerializer(serializers.ModelSerializer):
    organization = OrganizationIdNameSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'organization', 'is_admin', 'city', 'country',
                  'avatar', 'is_active', 'status']


class OrganizationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'country', 'logo', 'primary_color', 'secondary_color', 'session_timeout',
                  'password_expiration')


class MeDetailSerializer(serializers.ModelSerializer):
    organization = OrganizationDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'organization', 'is_admin', 'city', 'country',
                  'avatar', 'is_active']


class UserSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'organization', 'is_admin', 'city', 'country',
                  'avatar', 'is_active']


class CreateUserSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'organization', 'is_admin', 'city',
                  'country', 'avatar', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'organization', 'is_admin', 'city', 'country',
                  'is_active']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar.url if instance.avatar else None
        return data


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']


class InvitedUserSerializer(serializers.ModelSerializer):
    organization = OrganizationIdNameSerializer(read_only=True)

    class Meta:
        model = UserInvite
        fields = ['email', 'organization', 'status']
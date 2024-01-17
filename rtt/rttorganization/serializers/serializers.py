from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.utils.translation import ugettext_lazy as _

from rttorganization.models.models import Organization, Subscription, SubscriptionType
from rttproduct.serializers.serializers import ProductSerializerDetails


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'address', 'tax_code', 'country', 'active', 'logo', 'primary_color',
                  'secondary_color', 'session_timeout', 'password_expiration')
        extra_kwargs = {
            'url': {'view_name': 'api:organization-detail', 'lookup_field': 'id'}
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('name', 'active', 'country'),
                message=_('Name, Active and Country should be unique!!')
            )
        ]


class OrganizationIdNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', )


class SubscriptionSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=SubscriptionType.objects.all())
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Subscription
        fields = ('id', 'start_date', 'end_date', 'paid', 'invoice_uid', 'amount', 'max_user', 'type', 'organization')


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = ('id', 'name', 'description')


class SubscriptionDetailsSerializer(serializers.ModelSerializer):
    type = SubscriptionTypeSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'type']


class OrganizationDetailsSerializer(serializers.ModelSerializer):
    organization_subscriptions = SubscriptionDetailsSerializer(read_only=True, many=True)
    organization_user = SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'country', 'active', 'organization_subscriptions', 'organization_user')

    @staticmethod
    def get_organization_user(obj):
        return obj.organization_user.all().count()


class RelevantOrganizationsSerializer(serializers.ModelSerializer):
    product_organization = ProductSerializerDetails(read_only=True, many=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'product_organization')

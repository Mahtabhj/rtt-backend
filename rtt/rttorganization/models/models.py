from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rttcore.models.models import BaseTimeStampedModel
from rttproduct.models.core_models import Industry


class Organization(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=200,  blank=True, null=True)
    tax_code = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)
    logo = models.FileField(upload_to='media/organization', blank=True, null=True)
    primary_color = models.CharField(max_length=100, blank=True, null=True)
    secondary_color = models.CharField(max_length=100, blank=True, null=True)
    session_timeout = models.IntegerField(default=0)
    password_expiration = models.IntegerField(default=0)
    industries = models.ManyToManyField(Industry, blank=True, related_name='organization_industries')
    public_api_key = models.TextField(blank=True, null=True)
    public_api_secret = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('created',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'active', 'country'], name='unique_organization'),
            models.UniqueConstraint(fields=['public_api_key', 'public_api_secret'],
                                    name='unique_organization_public_api_key_secret')
        ]

    def __str__(self):
        return self.name


class SubscriptionType(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active_substance_module = models.BooleanField(default=False)
    is_active_limits_management_module = models.BooleanField(default=False)
    is_active_task_management_module = models.BooleanField(default=False)
    is_active_reports_module = models.BooleanField(default=False)
    is_active_document_module = models.BooleanField(default=False)
    max_quota_for_all_documents = models.PositiveIntegerField(default=0)
    max_quota_for_one_document = models.PositiveIntegerField(default=0)

    live_assessment = models.BooleanField(_('Active live assessment'),
                                          help_text="Identify which organization is subscribed "
                                                    "to the “live assessment” service",
                                          default=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class Subscription(BaseTimeStampedModel):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    paid = models.BooleanField(default=False)
    invoice_uid = models.UUIDField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_user = models.IntegerField(default=0, blank=True, null=True)

    type = models.ForeignKey(SubscriptionType, on_delete=models.DO_NOTHING, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='organization_subscriptions')

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return str(self.start_date)

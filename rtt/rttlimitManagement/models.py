from django.db.models import Q
from django.core.exceptions import ValidationError
from rttcore.models.models import BaseTimeStampedModel
from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from rttregulation.models.models import RegulatoryFramework, Regulation
from rttsubstance.models import Substance

User = get_user_model()


class LimitAttribute(BaseTimeStampedModel):
    TYPE_CHOICES = [
        ('number', 'Number'),
        ('text_field', 'Text field'),
        ('list_field', 'List Field'),
    ]
    name = models.CharField(max_length=200)
    field_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='text_field')
    list_values = models.TextField(blank=True, null=True, help_text='Enter values separated by a comma')

    def clean(self):
        if self.field_type == 'list_field' and self.list_values == '':
            raise ValidationError("List values can not be set empty.")
        elif self.field_type != 'list_field' and self.list_values != '':
            raise ValidationError("List values will be set empty.")

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Limit attributes'
        constraints = [
            models.CheckConstraint(
                check=((Q(field_type='list_field') & ~Q(list_values='')) |
                       (~Q(field_type='list_field') & Q(list_values=''))),
                name='list_values_when_field_type_is_list_field',
            )
        ]

    def __str__(self):
        return self.name


class RegulationLimitAttribute(BaseTimeStampedModel):
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.CASCADE, blank=True, null=True,
                                             related_name='regulatory_framework_limit_attributes')
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='regulation_limit_attributes')
    limit_attribute = models.ForeignKey(LimitAttribute, on_delete=models.CASCADE,
                                        related_name='regulation_limit_attribute')

    def clean(self):
        if self.regulation and self.regulatory_framework:
            raise ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not self.regulation and not self.regulatory_framework:
            raise ValidationError("Both Regulation and Regulatory framework fields can't be set empty.")

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Regulation limit attributes'
        constraints = [
            models.UniqueConstraint(fields=['limit_attribute', 'regulation'],
                                    name='unique_regulation_limit_attribute'),
            models.UniqueConstraint(fields=['limit_attribute', 'regulatory_framework'],
                                    name='unique_framework_limit_attribute'),
            models.CheckConstraint(
                check=(Q(regulatory_framework__isnull=False) &
                       Q(regulation__isnull=True)) | (Q(regulatory_framework__isnull=True) &
                                                      Q(regulation__isnull=False)),
                name='only_regulatory_framework_or_regulation_in_regulation_limit_attribute',
            )
        ]


class RegulationSubstanceLimit(BaseTimeStampedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deleted', 'Deleted')
    ]
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE, related_name='regulation_substance_limit')
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.CASCADE, blank=True, null=True,
                                             related_name='regulatory_framework_regulation_substance_limit')
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='regulation_regulation_substance_limit')
    scope = models.TextField(blank=True, null=True)
    limit_value = models.FloatField(blank=True, null=True)
    measurement_limit_unit = models.TextField(blank=True, null=True)
    limit_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_into_force = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if kwargs.get('modified', False):
            self.modified = kwargs.pop('modified')
        else:
            self.modified = now()
        super(RegulationSubstanceLimit, self).save(*args, **kwargs)

    def clean(self):
        if self.regulation and self.regulatory_framework:
            raise ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not self.regulation and not self.regulatory_framework:
            raise ValidationError("Both Regulation and Regulatory framework fields can't be set empty.")

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Regulation substance limit'
        constraints = [
            models.CheckConstraint(
                check=(Q(regulatory_framework__isnull=False) &
                       Q(regulation__isnull=True)) | (Q(regulatory_framework__isnull=True) &
                                                      Q(regulation__isnull=False)),
                name='only_regulatory_framework_or_regulation_in_regulation_substance_limit',
            )
        ]


class LimitAdditionalAttributeValue(BaseTimeStampedModel):
    regulation_substance_limit = models.ForeignKey(RegulationSubstanceLimit, on_delete=models.CASCADE,
                                                   related_name='regulation_substance_limit_additional_attribute')
    regulation_limit_attribute = models.ForeignKey(RegulationLimitAttribute, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Limit additional attribute values'
        constraints = [
            models.UniqueConstraint(fields=['regulation_substance_limit', 'regulation_limit_attribute'],
                                    name='unique_regulation_substance_limit_additional_attribute')
        ]


class Exemption(BaseTimeStampedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deleted', 'Deleted')
    ]
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE, related_name='substance_exemption')
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.CASCADE, blank=True, null=True,
                                             related_name='regulatory_framework_exemption')
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='regulation_exemption')
    article = models.CharField(max_length=100, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    application = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    date_into_force = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    modified = models.DateTimeField(default=now)

    def clean(self):
        if self.regulation and self.regulatory_framework:
            raise ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not self.regulation and not self.regulatory_framework:
            raise ValidationError("Both Regulation and Regulatory framework fields can't be set empty.")

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Exemptions'
        constraints = [
            models.CheckConstraint(
                check=(Q(regulatory_framework__isnull=False) &
                       Q(regulation__isnull=True)) | (Q(regulatory_framework__isnull=True) &
                                                      Q(regulation__isnull=False)),
                name='only_regulatory_framework_or_regulation_in_exemption',
            )
        ]


class LimitUploadLog(BaseTimeStampedModel):
    LIMIT_UPLOAD_CHOICES = [
        ('regulation_substance_limit', 'Regulation Substance Limit'),
        ('exemption', 'Exemption'),
        ('limit_additional_attribute_value', 'Limit Additional Attribute Value'),
        ('limit_with_additional_attribute_value', 'Limit with Additional Attribute Value')
    ]
    STATUS_CHOICES = [
        ('in_queue', 'In Queue'),
        ('in_progress', 'In Progress'),
        ('success', 'Success'),
        ('fail', 'Fail')
    ]
    file_name = models.TextField()
    process_type = models.CharField(max_length=100, choices=LIMIT_UPLOAD_CHOICES, default='regulation_substance_limit')
    total_data_in_file = models.PositiveIntegerField(default=0)
    succeed_data_entry = models.PositiveIntegerField(default=0)
    failed_data_entry = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    file_url = models.URLField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Limit Upload Log'

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q

# Create your models here.
from rttcore.models.models import BaseTimeStampedModel
from rttorganization.models.models import Organization

app_label, *_ = __name__.partition('.')
User = get_user_model()


class ExternalLink(BaseTimeStampedModel):
    name = models.CharField(max_length=500)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'External Links'

    def __str__(self):
        return self.name


class Substance(BaseTimeStampedModel):
    name = models.TextField()
    ec_no = models.CharField(max_length=500, null=True, blank=True)
    cas_no = models.CharField(max_length=500, null=True, blank=True)
    molecular_formula = models.TextField(null=True, blank=True)
    chemycal_id = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='media/substance', blank=True, null=True)
    is_family = models.BooleanField(default=False, help_text='Define this substance as a family')
    families = models.ManyToManyField('self', related_name='substance_families', blank=True, through='SubstanceFamily')

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Substances'

    def __str__(self):
        return self.name


class SubstanceFamily(BaseTimeStampedModel):
    substance = models.ForeignKey(Substance, related_name='substance_family', on_delete=models.CASCADE)
    family = models.ForeignKey(Substance, related_name='family_substance', on_delete=models.CASCADE)
    family_source = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Substance families'
        constraints = [
            models.UniqueConstraint(fields=['substance', 'family'],
                                    name='unique_substance_family')
        ]


class SubstanceExternalLink(BaseTimeStampedModel):
    external_link = models.ForeignKey(ExternalLink, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE,
                                  related_name='substance_external_link_relation')
    value = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        db_table = "%s_%s" % (app_label, "substance_external_links")
        verbose_name_plural = 'Substance External Links'
        constraints = [
            models.UniqueConstraint(fields=['substance', 'external_link'],
                                    name='unique_substance_external_link')
        ]


class SubstanceUsesAndApplication(BaseTimeStampedModel):
    name = models.CharField(max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='substance_use_and_application_organization')
    substances = models.ManyToManyField(Substance, related_name='uses_and_application_substances', blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Substance Uses and Applications'
        constraints = [
            models.UniqueConstraint(fields=['name', 'organization'], name='unique_substance_name_organization')
        ]

    def __str__(self):
        return self.name


class Property(BaseTimeStampedModel):
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=500, blank=True, null=True)
    url_link = models.TextField(blank=True, null=True)

    # substances = models.ManyToManyField(Substance, related_name='property_substances', blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.name


class PropertyDataPoint(BaseTimeStampedModel):
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=500)
    property = models.ForeignKey(Property, on_delete=models.CASCADE,
                                 related_name='property_data_property')

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Property data point'

    def __str__(self):
        return self.name


class SubstancePropertyDataPoint(BaseTimeStampedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deleted', 'Deleted')
    ]
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE,
                                  related_name='substance_property_data_point_relation')
    property_data_point = models.ForeignKey(PropertyDataPoint, on_delete=models.CASCADE,
                                            related_name='substance_property_data_point_property_data_point')
    value = models.CharField(max_length=500)
    image = models.FileField(upload_to='media/substance_property_data_point', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-id',)
        db_table = "%s_%s" % (app_label, "substance_property_data_points")
        verbose_name_plural = 'Substance Property data point'
        constraints = [
            models.UniqueConstraint(fields=['substance', 'property_data_point', 'status'],
                                    condition=(Q(status='active')),
                                    name='unique_substance_property_data_point')
        ]

    def clean(self, *args, **kwargs):
        queryset = SubstancePropertyDataPoint.objects.filter(substance=self.substance,
                                                             property_data_point=self.property_data_point,
                                                             status='active')
        if queryset.count() == 1 and self.status == 'active':
            raise ValidationError(f'(substance_id: {self.substance.id}, property_data_point_id: '
                                  f'{self.property_data_point.id}, status=active) already exists.')


class PrioritizationStrategy(BaseTimeStampedModel):
    name = models.CharField(max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='prioritization_strategy_organization')
    properties = models.ManyToManyField(Property, through='PrioritizationStrategyProperty', blank=True,
                                        related_name='prioritization_strategy_properties')
    default_org_strategy = models.BooleanField(default=False)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Prioritization strategies'
        constraints = [
            models.UniqueConstraint(fields=['name', 'organization'],
                                    name='unique_organization_strategy'),
            models.UniqueConstraint(fields=['organization', 'default_org_strategy'],
                                    condition=(Q(default_org_strategy=True)),
                                    name='unique_organization_default_org_strategy')
        ]

    def clean(self, *args, **kwargs):
        queryset = PrioritizationStrategy.objects.filter(organization=self.organization,
                                                             default_org_strategy=True)
        if queryset.count() == 1 and self.default_org_strategy == True:
            raise ValidationError(f'organization_id: {self.organization.id} default_org_strategy True already exists.')

    def __str__(self):
        return self.name


class PrioritizationStrategyProperty(BaseTimeStampedModel):
    prioritization_strategy = models.ForeignKey(PrioritizationStrategy, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE,
                                 related_name='prioritization_strategy_property_relation')
    weight = models.FloatField(default=0.0, validators=[MinValueValidator(0),
                                                        MaxValueValidator(100)])

    class Meta:
        ordering = ('-id',)
        db_table = "%s_%s" % (app_label, "prioritizationstrategy_properties")
        verbose_name_plural = 'Prioritization strategy Properties'
        constraints = [
            models.UniqueConstraint(fields=['prioritization_strategy', 'property'],
                                    name='unique_prioritization_strategy_property')
        ]


class SubstanceUploadLog(BaseTimeStampedModel):
    SUBSTANCE_UPLOAD_CHOICES = [
        ('substance_basic_details', 'Substance Basic Details'),
        ('substances_with_uses_and_applications', 'Substances with Uses and Applications'),
        ('substance_related_products', 'Substance Related Products'),
        ('substance_data', 'Substance Data'),
        ('substances_in_Regulatory_frameworks_or_Regulations', 'Substances in Regulatory Frameworks/Regulations'),
        ('substance_families', 'Substance families'),
        ('admin_substance_data', 'Admin Substance Data'),
        ('admin_substance_families', 'Admin substance families'),
        ('substance_data_with_existing_data_decision', 'Substance Data With Existing Data Decision'),
    ]
    STATUS_CHOICES = [
        ('in_queue', 'In Queue'),
        ('success', 'Success'),
        ('in_progress', 'In Progress'),
        ('fail', 'Fail')
    ]
    file_name = models.TextField()
    process_type = models.CharField(max_length=100, choices=SUBSTANCE_UPLOAD_CHOICES, default='substance_basic_details')
    total_data_in_file = models.PositiveIntegerField(default=0)
    succeed_data_entry = models.PositiveIntegerField(default=0)
    failed_data_entry = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    file_url = models.URLField(max_length=1000, null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        db_table = "%s_%s" % (app_label, "substance_upload_log")
        verbose_name_plural = 'Substance Upload Log'


class UserSubstanceAddLog(BaseTimeStampedModel):
    SUBSTANCE_UPLOAD_CHOICES = [
        ('substance_add', 'Substance Add'),
        ('product_related_substances_add', 'Product Related Substances Add'),
    ]
    STATUS_CHOICES = [
        ('in_queue', 'In Queue'),
        ('success', 'Success'),
        ('in_progress', 'In Progress'),
        ('fail', 'Fail')
    ]
    OBJECT_TYPE_CHOICES = [
        ('uses_and_application', 'Uses And Application'),
        ('product', 'Product'),
    ]
    file_name = models.TextField()
    object_ids = models.TextField(null=True, blank=True)
    object_type = models.CharField(max_length=100, choices=OBJECT_TYPE_CHOICES, default='uses_and_application')
    substance_count = models.PositiveIntegerField(default=0)
    process_type = models.CharField(max_length=100, choices=SUBSTANCE_UPLOAD_CHOICES, default='substance_add')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_queue')
    file_url = models.URLField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    total_data_in_file = models.PositiveIntegerField(default=0)
    succeed_data_entry = models.PositiveIntegerField(default=0)
    failed_data_entry = models.PositiveIntegerField(default=0)
    traceback = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        db_table = "%s_%s" % (app_label, "user_substance_add_log")
        verbose_name_plural = 'User Substance Add Log'

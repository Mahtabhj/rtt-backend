from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from rttcore.models.models import BaseTimeStampedModel
from rttdocument.models.models import Document
from rttorganization.models.models import Organization
from rttproduct.models.models import MaterialCategory, ProductCategory
from rttregulation.models.core_models import Topic
from rttsubstance.models import Substance
from rttproduct.models.core_models import Industry

User = get_user_model()

MY_PUBLISH_CHOICES = [
    ('d', 'Draft'),
    ('o', 'Online'),
]


class Region(BaseTimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    chemical_id = models.CharField(max_length=40, blank=True, null=True)
    iso_name = models.CharField(max_length=40, blank=True, null=True)
    country_code = models.CharField(max_length=40, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    region_page = models.BooleanField(default=False)
    country_flag = models.FileField(upload_to='media/region', blank=True, null=True)
    industries = models.ManyToManyField(Industry, blank=True, related_name='region_industries')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class Language(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class Status(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Regulation Status'

    def __str__(self):
        return self.name


class Url(BaseTimeStampedModel):
    text = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('text',)

    def __str__(self):
        return self.text


class IssuingBody(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=512, blank=True, null=True)

    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class RegulatoryFramework(BaseTimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    review_status = models.CharField(max_length=1, choices=MY_PUBLISH_CHOICES, default='d', )

    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, blank=True, null=True,
                                 related_name='language_reg_framework')
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True,
                               related_name='regulatory_framework_status')
    issuing_body = models.ForeignKey(IssuingBody, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     related_name='regulatory_framework_issuing_body')

    regions = models.ManyToManyField(Region, blank=True, related_name='regulatory_framework_region')
    documents = models.ManyToManyField(Document, blank=True, related_name='framework_documents')
    material_categories = models.ManyToManyField(MaterialCategory, blank=True,
                                                 related_name='material_cat_reg_framework')
    product_categories = models.ManyToManyField(ProductCategory, blank=True, related_name='product_cat_reg_framework')
    urls = models.ManyToManyField(Url, blank=True, related_name='url_reg_framework')
    topics = models.ManyToManyField(Topic, blank=True, related_name='regulatory_framework_topics')
    substances = models.ManyToManyField(Substance, blank=True, related_name='substances_regulatory_framework')
    publish_limit_data = models.BooleanField(default=False,
                                             help_text='Decides if the limit data should be published to frontend')

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Regulatory Frameworks'

    def __str__(self):
        return self.name


"""
We need to add some extra fields in m2m relation table. So we create intermediate[01] relational table. 
But if this intermediate model is used with the ManyToManyField using the 'through'[02], 
elasticsearch data is not syncing.
Cause, due to using 'through' argument django calls custom signal instead of m2m_changed signal 
that can't make synchronization with the Elastic_search[03].
That is why here intermediate model is created without using 'through' argument and m2m_changed signal[04] is used
to make sure elasticsearch data synchronization.
Ref:
[01] https://docs.djangoproject.com/en/3.2/topics/db/models/#extra-fields-on-many-to-many-relationships
[02] https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.ManyToManyField.through
[03] https://code.djangoproject.com/ticket/32515
[04] https://docs.djangoproject.com/en/3.2/ref/signals/#m2m-changed
"""


class SubstanceRegulatoryFramework(BaseTimeStampedModel):
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE,
                                  related_name='substance_regulatory_framework_relation')
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.CASCADE,
                                             related_name='regulatory_framework_substance_relation')

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Substance RegulatoryFramework'
        constraints = [
            models.UniqueConstraint(fields=['substance', 'regulatory_framework'],
                                    name='unique_substance_regulatory_framework')
        ]


class RegulationType(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Regulatory Types'

    def __str__(self):
        return self.name


class Regulation(BaseTimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    review_status = models.CharField(max_length=1, choices=MY_PUBLISH_CHOICES, default='d', )

    type = models.ForeignKey(RegulationType, on_delete=models.DO_NOTHING, related_name='regulation_regulation_type')
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='regulation_status')
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='regulation_regulatory_framework')

    documents = models.ManyToManyField(Document, blank=True, related_name='regulation_documents')
    material_categories = models.ManyToManyField(MaterialCategory, blank=True,
                                                 related_name='regulation_material_categories')
    product_categories = models.ManyToManyField(ProductCategory, blank=True,
                                                related_name='regulation_product_categories')
    urls = models.ManyToManyField(Url, blank=True)
    topics = models.ManyToManyField(Topic, blank=True, related_name='regulation_topics')
    substances = models.ManyToManyField(Substance, blank=True, related_name='substances_regulation')
    publish_limit_data = models.BooleanField(default=False,
                                             help_text='Decides if the limit data should be published to frontend')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class RegulationMute(BaseTimeStampedModel):
    is_muted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='regulation_mute_org')
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='regulation_mute_regulation')
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.CASCADE, blank=True, null=True,
                                             related_name='regulation_mute_framework')

    def clean(self):
        if self.regulation and self.regulatory_framework:
            raise ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not self.regulation and not self.regulatory_framework:
            raise ValidationError("Both Regulation or Regulatory framework fields can't be set empty.")

    class Meta:
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(fields=['organization', 'regulation'],
                                    name='unique_org_regulation_regulation_mute'),
            models.UniqueConstraint(fields=['organization', 'regulatory_framework'],
                                    name='unique_org_framework_regulation_mute'),
            models.CheckConstraint(
                check=(Q(regulation__isnull=False) &
                       Q(regulatory_framework__isnull=True)) | (Q(regulation__isnull=True) &
                                                                Q(regulatory_framework__isnull=False)),
                name='only_regulation_or_regulatory_framework_in_user_regulation_mute',
            )
        ]

    def __str__(self):
        if self.regulation:
            field = f"regulation_id: {self.regulation_id}"
        else:
            field = f"regulatory_framework_id: {self.regulatory_framework_id}"
        action = "muted" if self.is_muted else "unmuted"
        return f"{field} is {action} for organization: {self.organization_id}"


class SubstanceRegulation(BaseTimeStampedModel):
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE, related_name='substance_regulation_relation')
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE, related_name='regulation_substance_relation')

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Substance Regulation'
        constraints = [
            models.UniqueConstraint(fields=['substance', 'regulation'],
                                    name='unique_substance_regulation')
        ]


class MilestoneType(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class RegulationMilestone(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)

    type = models.ForeignKey(MilestoneType, on_delete=models.DO_NOTHING, related_name='regulation_milestone_type')
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='regulation_milestone')
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.CASCADE, blank=True, null=True,
                                             related_name='regulatory_framework_milestone')

    documents = models.ManyToManyField(Document, blank=True, related_name='documents_regulation_milestone')
    urls = models.ManyToManyField(Url, blank=True, related_name='urls_regulation_milestone')
    substances = models.ManyToManyField(Substance, blank=True, related_name='substances_regulation_milestone')

    def clean(self):
        if self.regulation and self.regulatory_framework:
            raise ValidationError("Only Regulation or Regulatory framework can be set.")
        elif not self.regulation and not self.regulatory_framework:
            raise ValidationError("Both Regulation or Regulatory framework fields can't be set empty.")

    class Meta:
        verbose_name_plural = 'Milestones'
        ordering = ('created',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'regulation'], name='unique_regulation_milestone'),
            models.UniqueConstraint(fields=['name', 'regulatory_framework'], name='unique_framework_milestone'),
            models.CheckConstraint(
                check=(Q(regulation__isnull=False) &
                       Q(regulatory_framework__isnull=True)) | (Q(regulation__isnull=True) &
                                                                Q(regulatory_framework__isnull=False)),
                name='only_regulation_or_regulatory_framework',
            )
        ]

    def __str__(self):
        return self.name


class MilestoneMute(BaseTimeStampedModel):
    is_muted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='milestone_mute_org')
    milestone = models.ForeignKey(RegulationMilestone, on_delete=models.CASCADE,
                                  related_name='milestone_mute_milestone')

    class Meta:
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(fields=['organization', 'milestone'],
                                    name='unique_org_milestone_milestone_mute'),
        ]

    def __str__(self):
        action = "muted" if self.is_muted else "unmuted"
        return f"{self.milestone} is {action} for organization: {self.organization_id}"


class SubstanceRegulationMilestone(BaseTimeStampedModel):
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE,
                                  related_name='substance_regulation_milestone_relation')
    regulation_milestone = models.ForeignKey(RegulationMilestone, on_delete=models.CASCADE,
                                             related_name='regulation_milestone_substance_relation')

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Substance RegulationMilestone'
        constraints = [
            models.UniqueConstraint(fields=['substance', 'regulation_milestone'],
                                    name='unique_substance_regulation_milestone')
        ]


class QuestionType(BaseTimeStampedModel):
    name = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Question(BaseTimeStampedModel):
    name = models.TextField()
    description = models.TextField(blank=True)

    type = models.ForeignKey(QuestionType, on_delete=models.DO_NOTHING)
    in_charge = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.name


class Answer(BaseTimeStampedModel):
    answer_text = models.TextField(blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)

    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE, blank=True, null=True)
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.CASCADE, blank=True, null=True)
    answered_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_regulation_answer_by')
    pin_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_regulation_pin_by', blank=True,
                               null=True)
    edited = models.DateTimeField(blank=True, null=True, default=None)

    def clean(self):
        if self.regulation and self.regulatory_framework:
            raise ValidationError("Only Regulation OR Regulatory framework can be set.")
        elif not self.regulation and not self.regulatory_framework:
            raise ValidationError("Both Regulation AND Regulatory framework fields can't be set empty.")

    class Meta:
        ordering = ('-created', )
        constraints = [
            models.CheckConstraint(
                check=(Q(regulation__isnull=False) &
                       Q(regulatory_framework__isnull=True)) | (Q(regulation__isnull=True) &
                                                                Q(regulatory_framework__isnull=False)),
                name='only_regulation_or_regulatory_framework_in_answer',
            )
        ]

    def __str__(self):
        return self.answer_text


class RegulationRating(BaseTimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE, related_name='regulation_rating')

    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('rating',)
        constraints = [
            models.UniqueConstraint(fields=['organization', 'regulation'],
                                    name='unique_regulation_organization_relevancy')
        ]

    def __str__(self):
        return str(self.rating)


class RegulationRatingLog(BaseTimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    regulation = models.ForeignKey(Regulation, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='regulation_rating_log')

    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    prev_rating = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('rating',)

    def __str__(self):
        return str(self.rating)


class RegulatoryFrameworkRating(BaseTimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.CASCADE,
                                             related_name='regulatory_framework_rating')

    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('rating',)
        constraints = [
            models.UniqueConstraint(fields=['organization', 'regulatory_framework'],
                                    name='unique_regulatory_framework_organization_relevancy')
        ]

    def __str__(self):
        return str(self.rating)


class RegulatoryFrameworkRatingLog(BaseTimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    regulatory_framework = models.ForeignKey(RegulatoryFramework, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='regulatory_framework_rating_log')

    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    prev_rating = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('rating',)

    def __str__(self):
        return str(self.rating)

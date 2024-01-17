import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from rttcore.models.models import BaseTimeStampedModel
from rttorganization.models.models import Organization
from rttproduct.models.core_models import Industry
from rttproduct.models.models import ProductCategory, MaterialCategory
from rttregulation.models.models import (
    Region,
    Document,
    Regulation,
    RegulatoryFramework)
from rttregulation.models.core_models import Topic
from rttsubstance.models import Substance
from rttdocument.models.models import DocumentType

User = get_user_model()


class SourceType(BaseTimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Source(BaseTimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    chemical_id = models.CharField(max_length=40, blank=True, null=True)
    image = models.FileField(upload_to='media/news_source', blank=True, null=True)
    type = models.ForeignKey(SourceType, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class NewsCategory(BaseTimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to='media/category_icon', blank=True, null=True)
    active = models.BooleanField(default=False)
    chemical_id = models.CharField(max_length=40, blank=True, null=True)

    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='news_category_topic')
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)

    industries = models.ManyToManyField(Industry, blank=True)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % self.icon)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'News Categories'

    def __str__(self):
        return self.name


class News(BaseTimeStampedModel):
    NEWS_CHOICES = [
        ('n', 'New'),
        ('s', 'Selected'),
        ('d', 'Discharged'),
    ]

    title = models.CharField(max_length=500, unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField()
    cover_image = models.FileField(upload_to='media/news_cover', max_length=500, blank=True, null=True)
    chemical_id = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=1, choices=NEWS_CHOICES, default='n', )
    active = models.BooleanField(default=False)

    selected_on = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    discharged_on = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='news_source')
    selected_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='selected_by', blank=True,
                                    null=True)
    discharged_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='discharged_by', blank=True,
                                      null=True)

    regions = models.ManyToManyField(Region, blank=True, related_name='region_news')
    news_categories = models.ManyToManyField(NewsCategory, blank=True, related_name='news_categories')
    product_categories = models.ManyToManyField(ProductCategory, blank=True, related_name='product_category_news')
    material_categories = models.ManyToManyField(MaterialCategory, blank=True, related_name='material_category_news')
    documents = models.ManyToManyField(Document, blank=True, related_name='news_documents')
    regulations = models.ManyToManyField(Regulation, blank=True, related_name='regulation_news')
    regulatory_frameworks = models.ManyToManyField(RegulatoryFramework, blank=True,
                                                   related_name='news_regulatory_frameworks')
    organizations = models.ManyToManyField(Organization, blank=True)
    substances = models.ManyToManyField(Substance, blank=True, related_name='substances_news')
    review_yellow = models.BooleanField(default=False)
    review_green = models.BooleanField(default=False)
    review_comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.pub_date <= now


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


class SubstanceNews(BaseTimeStampedModel):
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE, related_name='substance_news_relation')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_substance_relation')

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Substance News'
        constraints = [
            models.UniqueConstraint(fields=['substance', 'news'],
                                    name='unique_substance_news')
        ]


class NewsRelevance(BaseTimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    news = models.ForeignKey(News, on_delete=models.DO_NOTHING, related_name='news_relevance')

    relevancy = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('relevancy',)
        constraints = [
            models.UniqueConstraint(fields=['organization', 'news'], name='unique_news_organization_relevancy')
        ]

    def __str__(self):
        return str(self.relevancy)


class NewsRelevanceLog(BaseTimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    news = models.ForeignKey(News, on_delete=models.DO_NOTHING, related_name='news_relevance_log')

    relevancy = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    prev_relevancy = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('relevancy',)

    def __str__(self):
        return str(self.relevancy)


class NewsAssessmentWorkflow(BaseTimeStampedModel):
    NewsAssessmentWorkflow = [
        ('to_be_assessed', 'To Be Assessed'),
        ('completed', 'Completed'),
    ]
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=NewsAssessmentWorkflow, default='to_be_assessed')

    def __str__(self):
        return str(self.news_id)

    class Meta:
        ordering = ('created',)
        constraints = [
            models.UniqueConstraint(fields=['news', 'organization'], name='unique_news_organization'),
        ]


class NewsUpdateLogForAssessmentWorkflowRemove(BaseTimeStampedModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


class NewsQuestionType(BaseTimeStampedModel):
    name = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.name


class NewsQuestion(BaseTimeStampedModel):
    name = models.TextField()
    description = models.TextField(blank=True)
    type = models.ForeignKey(NewsQuestionType, on_delete=models.DO_NOTHING, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.name


class NewsAnswer(BaseTimeStampedModel):
    answer_text = models.TextField()
    question = models.ForeignKey(NewsQuestion, on_delete=models.DO_NOTHING)
    news = models.ForeignKey(News, on_delete=models.DO_NOTHING)
    answered_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_news_answer_ans_by')
    pin_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_news_answer_pin_by', blank=True,
                               null=True)
    edited = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.answer_text


class AutomaticFileImportNewsSource(BaseTimeStampedModel):
    news_source = models.OneToOneField(Source, on_delete=models.DO_NOTHING)
    document_type = models.ForeignKey(DocumentType, on_delete=models.DO_NOTHING)

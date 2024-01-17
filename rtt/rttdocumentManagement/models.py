from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from rttcore.models.models import BaseTimeStampedModel
from rttproduct.models.models import Product
from rttsubstance.models import Substance
from rttregulation.models.models import RegulatoryFramework, Regulation
from rttnews.models.models import News
User = get_user_model()


class DocumentManagement(BaseTimeStampedModel):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    regulatory_frameworks = models.ManyToManyField(RegulatoryFramework, blank=True,
                                                   related_name='doc_management_frameworks')
    regulations = models.ManyToManyField(Regulation, blank=True, related_name='doc_management_regulations')
    products = models.ManyToManyField(Product, blank=True, related_name='doc_management_products')
    substances = models.ManyToManyField(Substance, blank=True, related_name='doc_management_substances')
    news = models.ManyToManyField(News, blank=True, related_name='doc_management_news')
    attachment_document = models.FileField(upload_to='media/attachment_document', blank=True, null=True, max_length=256)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='doc_management_uploaded_by',
                                    blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Document Managements'

    def __str__(self):
        return self.name


class DocumentManagementComment(BaseTimeStampedModel):
    comment_text = models.TextField()
    document_management = models.ForeignKey(DocumentManagement, on_delete=models.CASCADE,
                                            related_name='doc_management_comment')
    commented_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                     related_name='doc_management_user_comment_by')
    edited = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.comment_text[:70]


class DocManagementCollaborator(BaseTimeStampedModel):
    document_management = models.ForeignKey(DocumentManagement, on_delete=models.SET_NULL, null=True)
    collaborator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(fields=['document_management', 'collaborator'],
                                    condition=(~Q(collaborator__isnull=True)),
                                    name='unique_document_management_collaborator')
        ]

    def clean(self, *args, **kwargs):
        queryset = DocManagementCollaborator.objects.filter(document_management=self.document_management,
                                                             collaborator=self.collaborator)
        if queryset.count() == 1:
            raise ValidationError(f'(document_management_id: {self.document_management_id}, '
                                  f'collaborator_id: {self.collaborator_id}) already exists.')


class DocManagementHistory(BaseTimeStampedModel):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
    ]

    document_management = models.ForeignKey(DocumentManagement, on_delete=models.SET_NULL, null=True)
    action_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, default='updated')
    action_field = models.CharField(max_length=50, blank=True)
    prev_value = models.TextField(blank=True)
    curr_value = models.TextField(blank=True)
    extra = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"document_management_id: {self.document_management_id} {self.action} by {self.action_user}"

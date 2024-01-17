from django.db import models

from rttcore.models.models import BaseTimeStampedModel


class DocumentType(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Document Types'

    def __str__(self):
        return self.name

"""
This Document model is related to regulation/framework/news documents. This model is considered as attachment for 
regulation/framework/news.
"""
class Document(BaseTimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    attachment = models.FileField(upload_to='media/documents', blank=True, null=True)

    type = models.ForeignKey(DocumentType, on_delete=models.DO_NOTHING, related_name='document_type')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Help(BaseTimeStampedModel):
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    type = models.CharField(choices=[('faq', 'faq'), ('documents', 'documents')], default='faq', max_length=10)
    document = models.FileField(upload_to='media/help_docs', blank=True, null=True)

    def __str__(self):
        return self.title

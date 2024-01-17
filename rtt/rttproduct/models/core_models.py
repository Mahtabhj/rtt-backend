from django.db import models

from rttcore.models.models import BaseTimeStampedModel
from rttregulation.models.core_models import Topic


class Industry(BaseTimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    topics = models.ManyToManyField(Topic, blank=True, related_name='industry_topics')

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name

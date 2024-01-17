from django.db import models

from rttcore.models.models import BaseTimeStampedModel


class Topic(BaseTimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name

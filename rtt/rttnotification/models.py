from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from rttcore.models.models import BaseTimeStampedModel
from rttproduct.models.models import ProductCategory, MaterialCategory
from rttregulation.models.core_models import Topic
from rttregulation.models.models import Region, RegulatoryFramework

User = get_user_model()


class NotificationAlert(BaseTimeStampedModel):
    CONTENT_CHOICES = [
        ('news', 'News'),
        ('regulatory_updates', 'Regulatory updates'),
        ('assessments', 'Assessments'),
        ('limits', 'Limits'),
        ('substances', 'Substances'),
    ]

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notification_alert')
    name = models.CharField(max_length=500)
    content = models.CharField(max_length=255, choices=CONTENT_CHOICES)
    frequency = models.CharField(max_length=255, choices=FREQUENCY_CHOICES)
    active = models.BooleanField(default=True)
    regions = models.ManyToManyField(Region, blank=True)
    topics = models.ManyToManyField(Topic, blank=True)
    material_categories = models.ManyToManyField(MaterialCategory, blank=True)
    product_categories = models.ManyToManyField(ProductCategory, blank=True)
    regulatory_frameworks = models.ManyToManyField(RegulatoryFramework, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Notification Alerts'

    def __str__(self):
        return self.name


class NotificationAlertLog(BaseTimeStampedModel):
    notification_alert = models.ForeignKey(NotificationAlert, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=500)
    filter_criteria = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-notification_alert',)
        verbose_name_plural = 'Notification Alert Logs'


class CeleryTaskEmailReceiver(BaseTimeStampedModel):
    TASK_TYPE_CHOICES = (
        ('all', 'All'),
        ('fetch_news', 'Fetch News'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_celery_task_email_receiver')
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='all')

    class Meta:
        ordering = ('-created', )
        verbose_name_plural = 'Celery Task Email Receiver'
        constraints = [
            models.UniqueConstraint(fields=['user', 'task_type'], name='unique_user_task_type'),
        ]

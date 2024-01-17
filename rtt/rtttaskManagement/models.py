from django.db import models
from rttcore.models.models import BaseTimeStampedModel
from django.contrib.auth import get_user_model

from rttnews.models.models import News
from rttregulation.models.models import RegulatoryFramework, Regulation
from rttproduct.models.models import Product
from rttsubstance.models import Substance

User = get_user_model()


class Task(BaseTimeStampedModel):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('done', 'Done')
    ]
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='task_created_by_user', blank=True,
                                   null=True)
    assignee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='task_assignee', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='task_related_products', blank=True)
    regulatory_frameworks = models.ManyToManyField(RegulatoryFramework, blank=True,
                                                   related_name='task_regulatory_frameworks')
    regulations = models.ManyToManyField(Regulation, blank=True, related_name='task_regulations')
    news = models.ManyToManyField(News, blank=True, related_name='task_news')
    due_date = models.DateTimeField(null=True, blank=True)
    is_archive = models.BooleanField(default=False)
    substances = models.ManyToManyField(Substance, blank=True, related_name='task_substances')

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.name


class TaskEditor(BaseTimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    editor = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Task editors'
        constraints = [
            models.UniqueConstraint(fields=['task', 'editor'],
                                    name='unique_task_editor')
        ]


class TaskHistory(BaseTimeStampedModel):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('changed', 'Changed'),
        ('assigned', 'Assigned'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    action_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, default='changed')
    action_field = models.CharField(max_length=50, blank=True, null=True)
    prev_value = models.TextField(blank=True, null=True)
    curr_value = models.TextField(blank=True, null=True)
    extra = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Task history'

    def __str__(self):
        return f"task_id: {self.task_id}"


class TaskComment(BaseTimeStampedModel):
    comment_text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comment')
    commented_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_comment_by')
    edited = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.comment_text

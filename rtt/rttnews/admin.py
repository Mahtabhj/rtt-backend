from django.contrib import admin
from .models import models

admin.site.register(
    [models.NewsRelevanceLog, models.NewsCategory, models.Source, models.SourceType, models.NewsAnswer,
     models.NewsQuestionType])


@admin.register(models.NewsAssessmentWorkflow)
class NewsAssessmentWorkflowAdmin(admin.ModelAdmin):
    list_display = ('news_id', 'organization', 'status')
    list_per_page = 20
    list_filter = ('organization', 'status', )


@admin.register(models.AutomaticFileImportNewsSource)
class AutomaticFileImportNewsSourceAdmin(admin.ModelAdmin):
    list_display = ('news_source', 'document_type')


@admin.register(models.NewsQuestion)
class NewsQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name', 'description', 'organization__name')


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'active', 'review_yellow', 'review_green',)
    list_per_page = 100
    raw_id_fields = ('substances',)
    search_fields = ('title', 'body')
    list_filter = ('status', 'active', 'review_yellow', 'review_green',)

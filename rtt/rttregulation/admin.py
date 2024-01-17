from django.contrib import admin

from .models.core_models import Topic
from .models.models import (Regulation, RegulationType, RegulatoryFramework, Url, MilestoneType, RegulationMilestone,
                            Answer, Region, RegulatoryFrameworkRatingLog, RegulationRatingLog, Status, Language,
                            QuestionType, IssuingBody, Question, RegulationMute, MilestoneMute)

admin.site.register([RegulationType, Url, MilestoneType,
                     Topic, Answer, RegulatoryFrameworkRatingLog, RegulationRatingLog, Status, Language, QuestionType,
                     IssuingBody])


@admin.register(RegulatoryFramework)
class RegulatoryFrameworkAdmin(admin.ModelAdmin):
    raw_id_fields = ['substances']
    search_fields = ['name']


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    raw_id_fields = ['substances']
    search_fields = ['name']


@admin.register(RegulationMilestone)
class RegulationMilestoneAdmin(admin.ModelAdmin):
    raw_id_fields = ['substances']
    search_fields = ['name']


@admin.register(RegulationMute)
class RegulationMuteAdmin(admin.ModelAdmin):
    list_filter = ('is_muted',)
    list_display = ('id', 'regulation', 'regulatory_framework', 'organization_id', 'is_muted',)
    list_per_page = 20


@admin.register(MilestoneMute)
class MilestoneMuteAdmin(admin.ModelAdmin):
    list_filter = ('is_muted',)
    list_display = ('id', 'milestone', 'organization_id', 'is_muted',)
    list_per_page = 20


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    fields = (
        'name', 'description', 'chemical_id', 'iso_name', 'country_code', 'parent', 'latitude', 'longitude',
        ('region_page', 'industries'),
        'country_flag'
    )
    change_form_template = 'admin/region_page_on_industry_level.html'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name', 'description', 'organization__name')

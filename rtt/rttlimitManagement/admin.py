from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Q
from django.utils.translation import ngettext

from rttcore.services.admin_service import ExportCsvMixin
from rttcore.admin_filters.text_input_filter import TextInputFilter
from rttlimitManagement.models import LimitAttribute, RegulationLimitAttribute, RegulationSubstanceLimit, \
    LimitAdditionalAttributeValue, Exemption, LimitUploadLog

admin.site.register([LimitAttribute, LimitAdditionalAttributeValue])


@admin.register(LimitUploadLog)
class LimitUploadLogAdmin(admin.ModelAdmin):
    readonly_fields = ('file_url',)
    list_display = ('id', 'file_name', 'process_type', 'total_data_in_file', 'succeed_data_entry', 'failed_data_entry',
                    'status', 'start_time', 'end_time', 'download_file')

    def download_file(self, obj):
        if obj.file_url:
            return format_html('<a href="{}">{}</a>', obj.file_url, 'Download file')
        return format_html('<p style="color:red;">Not found</p>')

    download_file.allow_tags = True


class FrameworkIDFilterInLimit(TextInputFilter):
    parameter_name = 'framework_id'
    title = 'Regulatory Framework ID'

    def queryset(self, request, queryset):
        if self.value():
            framework_id = int(self.value())
            return queryset.filter(
                Q(regulatory_framework__id=framework_id)
            )


class RegulationIDFilterInLimit(TextInputFilter):
    parameter_name = 'regulation_id'
    title = 'Regulation ID'

    def queryset(self, request, queryset):
        if self.value():
            regulation_id = int(self.value())
            return queryset.filter(
                Q(regulation__id=regulation_id)
            )


class SubstanceIDFilterInLimit(TextInputFilter):
    parameter_name = 'substance_id'
    title = 'Substance ID'

    def queryset(self, request, queryset):
        if self.value():
            substance_id = int(self.value())
            return queryset.filter(
                Q(substance__id=substance_id)
            )


@admin.register(RegulationSubstanceLimit)
class RegulationSubstanceLimitAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_filter = (
        FrameworkIDFilterInLimit, RegulationIDFilterInLimit,
        SubstanceIDFilterInLimit, 'status'
    )
    readonly_fields = ('modified',)
    list_display = (
        'id', 'regulatory_framework_id', 'regulatory_framework_name', 'regulation_id', 'regulation_name',
        'substance_name', 'substance_ec_no', 'substance_cas_no',
        'scope', 'limit_value_with_unit', 'limit_note')
    list_per_page = 20
    autocomplete_fields = ('substance',)
    actions = ["export_as_csv", "mark_as_inactive"]

    def export_as_csv(self, request, queryset, field_names=None):
        field_names = ['id', 'created', 'modified',
                       'substance__name', 'substance__ec_no', 'substance__cas_no',
                       'regulatory_framework_id', 'regulatory_framework',
                       'regulation_id', 'regulation', 'scope',
                       'limit_value', 'measurement_limit_unit', 'limit_note', 'status', 'date_into_force']
        return super(RegulationSubstanceLimitAdmin, self).export_as_csv(request, queryset, field_names)

    def mark_as_inactive(self, request, queryset):
        updated = 0
        for limit in queryset:
            limit.status = 'deleted'
            limit.modified = timezone.now()
            limit.save()
            updated += 1
        self.message_user(request, ngettext(
            '%d regulation substance limit was successfully marked as inactive.',
            '%d regulation substance limits were successfully marked as inactive.',
            updated,
        ) % updated, messages.SUCCESS)

    def limit_value_with_unit(self, obj):
        value = str(obj.limit_value) if obj.limit_value else ''
        unit = ' ' + obj.measurement_limit_unit if obj.measurement_limit_unit else ''
        return value + unit

    limit_value_with_unit.short_description = 'limit value'

    @staticmethod
    def regulatory_framework_name(obj):
        return obj.regulatory_framework.name if obj.regulatory_framework else '-'

    @staticmethod
    def regulation_name(obj):
        return obj.regulation.name if obj.regulation else '-'

    @staticmethod
    def substance_name(obj):
        return obj.substance.name if obj.substance else '-'

    @staticmethod
    def substance_ec_no(obj):
        return obj.substance.ec_no if obj.substance else '-'

    @staticmethod
    def substance_cas_no(obj):
        return obj.substance.cas_no if obj.substance else '-'


@admin.register(Exemption)
class ExemptionAdmin(admin.ModelAdmin):
    list_filter = (
        FrameworkIDFilterInLimit, RegulationIDFilterInLimit,
    )
    list_display = ('id', 'regulatory_framework', 'regulation', 'substance', 'status')
    readonly_fields = ('modified',)
    list_per_page = 20


@admin.register(RegulationLimitAttribute)
class RegulationLimitAttributeAdmin(admin.ModelAdmin):
    autocomplete_fields = ('regulatory_framework', 'regulation')


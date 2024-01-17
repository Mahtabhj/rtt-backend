from django.contrib import admin
from django.db.models import Q
# Register your models here.
from django.utils.html import format_html
from rttcore.admin_filters.text_input_filter import TextInputFilterForMultipleFiltering

from rttcore.services.admin_service import ExportCsvMixin
from rttsubstance.models import Substance, SubstanceUsesAndApplication, Property, PropertyDataPoint, \
    PrioritizationStrategy, \
    PrioritizationStrategyProperty, ExternalLink, SubstanceExternalLink, SubstancePropertyDataPoint, SubstanceUploadLog, \
    SubstanceFamily, UserSubstanceAddLog


class SubstanceExternalLinkInline(admin.TabularInline):
    model = SubstanceExternalLink
    extra = 1


class SubstanceFamilyInline(admin.TabularInline):
    model = SubstanceFamily
    extra = 1
    fk_name = 'substance'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "family":
            kwargs["queryset"] = Substance.objects.filter(is_family=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CasEcNoFilterInSubstance(TextInputFilterForMultipleFiltering):
    parameter_name = 'ec_cas_value'
    title = 'EC/CAS No'

    def queryset(self, request, queryset):
        if self.value():
            search_value = str(self.value())
            return queryset.filter(
                Q(cas_no__icontains=search_value) |
                Q(ec_no__icontains=search_value)
            )


class ChemycalIdFilterInSubstance(TextInputFilterForMultipleFiltering):
    parameter_name = 'chemycal_id'
    title = 'Chemycal ID'

    def queryset(self, request, queryset):
        if self.value():
            search_value = str(self.value())
            return queryset.filter(
                Q(chemycal_id__icontains=search_value)
            )


@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'name', 'cas_no', 'ec_no')
    inlines = (SubstanceExternalLinkInline, SubstanceFamilyInline)
    actions = ["export_as_csv"]
    search_fields = ['name']
    list_filter = (CasEcNoFilterInSubstance, ChemycalIdFilterInSubstance,)
    list_per_page = 25


class PrioritizationStrategyPropertyInline(admin.TabularInline):
    model = PrioritizationStrategyProperty
    extra = 1
    min_num = 1


@admin.register(PrioritizationStrategy)
class PrioritizationStrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_name')
    inlines = (PrioritizationStrategyPropertyInline,)

    def organization_name(self, obj):
        return obj.organization.name


admin.site.register([ExternalLink, SubstanceUsesAndApplication, Property, PropertyDataPoint])


@admin.register(SubstanceUploadLog)
class SubstanceUploadLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'process_type', 'total_data_in_file', 'succeed_data_entry', 'failed_data_entry',
                    'status', 'start_time', 'end_time', 'download_file')
    readonly_fields = ('file_url', )

    def download_file(self, obj):
        if obj.file_url:
            return format_html('<a href="{}">{}</a>', obj.file_url, 'Download file')
        return format_html('<p style="color:red;">Not found</p>')

    download_file.allow_tags = True


@admin.register(UserSubstanceAddLog)
class UserSubstanceAddLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'process_type', 'status', 'total_data_in_file', 'succeed_data_entry',
                    'failed_data_entry', 'object_ids', 'object_type', 'download_file',)
    readonly_fields = ('file_url', )

    def download_file(self, obj):
        if obj.file_url:
            return format_html('<a href="{}">{}</a>', obj.file_url, 'Download file')
        return format_html('<p style="color:red;">Not found</p>')

    download_file.allow_tags = True


class SubstanceIDFilterInSubstancePropertyDataPoint(TextInputFilterForMultipleFiltering):
    parameter_name = 'substance_id'
    title = 'Substance ID'

    def queryset(self, request, queryset):
        if self.value():
            substance_id = int(self.value())
            return queryset.filter(
                Q(substance__id=substance_id)
            )


class SubstanceEcCasFilterInSubstancePropertyDataPoint(TextInputFilterForMultipleFiltering):
    parameter_name = 'substance_ec_cas'
    title = 'Substance EC/CAS'

    def queryset(self, request, queryset):
        if self.value():
            substance_ec_cas = self.value()
            return queryset.filter(
                Q(substance__ec_no__icontains=substance_ec_cas) |
                Q(substance__cas_no__icontains=substance_ec_cas)
            )


class PropertyDataPointIDFilterInSubstancePropertyDataPoint(TextInputFilterForMultipleFiltering):
    parameter_name = 'property_data_point_id'
    title = 'Property Data Point ID'

    def queryset(self, request, queryset):
        if self.value():
            property_data_point_id = int(self.value())
            return queryset.filter(
                Q(property_data_point_id=property_data_point_id)
            )


@admin.register(SubstancePropertyDataPoint)
class SubstancePropertyDataPointAdmin(admin.ModelAdmin, ExportCsvMixin):
    readonly_fields = ('modified',)
    raw_id_fields = ('substance',)

    list_filter = (
        SubstanceIDFilterInSubstancePropertyDataPoint,
        SubstanceEcCasFilterInSubstancePropertyDataPoint,
        PropertyDataPointIDFilterInSubstancePropertyDataPoint

    )
    list_display = (
        'id',  'property', 'property_data_point', 'substance_name', 'substance_cas_no', 'value', )
    list_per_page = 20

    @staticmethod
    def substance_name(obj):
        return obj.substance.name if obj.substance else '-'

    @staticmethod
    def substance_cas_no(obj):
        return obj.substance.cas_no if obj.substance else '-'

    @staticmethod
    def property(obj):
        return obj.property_data_point.property.name if obj.property_data_point.property else '-'

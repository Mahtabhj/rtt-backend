from django.contrib import admin
from django.utils.html import format_html
from rttdocumentManagement.models import DocumentManagement, DocumentManagementComment, DocManagementCollaborator, \
    DocManagementHistory


@admin.register(DocumentManagement)
class DocumentManagementAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_by', 'organization', 'download_file',)
    search_fields = ('name', 'description',)
    list_filter = ('uploaded_by',)
    raw_id_fields = ('regulatory_frameworks', 'regulations', 'products', 'substances', 'news',)
    list_per_page = 75

    def download_file(self, obj):
        if obj.attachment_document:
            return format_html('<a href="{}">{}</a>', obj.attachment_document.url, 'Download file')
        return format_html('<p style="color:red;">Not found</p>')

    def organization(self, obj):
        if obj.uploaded_by:
            return f"org {obj.uploaded_by.organization.id}: {obj.uploaded_by.organization.name}"
        return format_html('<p style="color:red;">Not found</p>')

    download_file.allow_tags = True
    organization.allow_tags = True


@admin.register(DocumentManagementComment)
class DocumentManagementAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'document_management', 'commented_by',)
    search_fields = ('comment_text',)
    list_filter = ('commented_by',)
    raw_id_fields = ('document_management',)
    readonly_fields = ('edited',)
    list_per_page = 75


@admin.register(DocManagementCollaborator)
class DocManagementCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'document_management', 'collaborator',)
    list_filter = ('collaborator',)
    raw_id_fields = ('document_management', 'collaborator',)
    list_per_page = 75


@admin.register(DocManagementHistory)
class DocManagementHistoryAdmin(admin.ModelAdmin):
    list_display = ('document_management', 'action_user', 'action', 'action_field',)
    list_filter = ('action_user',)
    raw_id_fields = ('document_management', 'action_user',)
    list_per_page = 75

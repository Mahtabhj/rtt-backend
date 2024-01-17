from django.contrib import admin
from rtttaskManagement.models import Task, TaskEditor, TaskHistory, TaskComment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'assignee', 'due_date', 'status', 'is_archive',)
    list_filter = ('status', 'is_archive',)
    search_fields = ('name', )


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_text', 'task', 'commented_by')


admin.site.register([TaskEditor, TaskHistory])

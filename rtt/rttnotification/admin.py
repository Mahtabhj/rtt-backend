from django.contrib import admin

from rttnotification.models import NotificationAlert, NotificationAlertLog, CeleryTaskEmailReceiver


class NotificationAlertAdmin(admin.ModelAdmin):
    search_fields = ('name', 'user__username')
    list_display = ('name', 'content', 'frequency', 'user')


class NotificationAlertLogAdmin(admin.ModelAdmin):
    search_fields = ('notification_alert__name', 'user__username')
    list_display = ('notification_alert', 'status', 'user', 'modified')


admin.site.register(NotificationAlert, NotificationAlertAdmin)
# admin.site.register(NotificationAlertLog, NotificationAlertLogAdmin)


@admin.register(CeleryTaskEmailReceiver)
class CeleryTaskEmailReceiverAdmin(admin.ModelAdmin):
    list_filter = ('task_type', )
    list_display = ('id', 'user', 'task_type', )

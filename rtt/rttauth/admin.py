from django.contrib import admin

from .models.models import User, UserInvite, FailedLoginAttempt

admin.site.register(User)
admin.site.register(UserInvite)


@admin.register(FailedLoginAttempt)
class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'timestamp')

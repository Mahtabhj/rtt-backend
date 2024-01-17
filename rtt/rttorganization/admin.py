from hashlib import sha256
from datetime import datetime
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models.models import Organization, Subscription, SubscriptionType

admin.site.register([Subscription])


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('public_api_key', 'public_api_secret',)
    change_form_template = "key_secret_generator_button.html"

    def response_change(self, request, obj):
        if "key_generator_request" in request.POST:
            try:
                time_stamp = datetime.now()
                api_key_seed = obj.name + str(time_stamp)
                secret_key_seed = str(time_stamp) + obj.name
                api_key_hash = sha256(api_key_seed.encode()).hexdigest()
                secret_key_hash = sha256(secret_key_seed.encode()).hexdigest()
                obj.public_api_key = api_key_hash
                obj.public_api_secret = secret_key_hash
                obj.save()
                self.message_user(request, "New API Key and Secret have been generated.")
            except Exception as ex:
                self.message_user(request, "Something went wrong. Try again later.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    pass
    fields = (
        'name', 'description', 'is_active_substance_module', 'is_active_limits_management_module',
        'is_active_task_management_module', 'is_active_reports_module', ('is_active_document_module',
                                             'max_quota_for_all_documents', 'max_quota_for_one_document'),
        'live_assessment'
    )
    change_form_template = 'admin/max_quota_show_or_hide.html'


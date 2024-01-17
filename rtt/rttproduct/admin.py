from django.contrib import admin

from rttproduct.models.core_models import Industry
from rttproduct.models.models import Product, MaterialCategory, ProductCategory

# Register your models here.
admin.site.register([ProductCategory, MaterialCategory, Industry])


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'related_substances')
    list_filter = ('organization',)
    search_fields = ('name', 'description',)
    raw_id_fields = ('substances', 'substance_use_and_apps',)
    list_per_page = 50

    def related_substances(self, obj):
        if obj.substances:
            return len(obj.substances.all())
        return 0

    related_substances.allow_tags = True

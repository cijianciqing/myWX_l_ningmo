from django.contrib import admin

# Register your models here.
from apps.models import App
import hashlib


@admin.register(App)
class ApisAppAdmin(admin.ModelAdmin):
    fields = ['name', 'application', 'category', 'url', 'publish_date', 'desc']
    # exclude = ['appid']

    def save_model(self, request, obj, form, change):
        src = obj.category + obj.application
        appid = hashlib.md5(src.encode('utf8')).hexdigest()
        obj.appid = appid
        super().save_model(request, obj, form, change)

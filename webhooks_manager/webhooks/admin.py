from django.contrib import admin

# Register your models here.
from webhooks_manager.webhooks.models import Source, Webhook


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    search_fields = ("source", "data")
    list_display = ("source", "created")
    list_filter = ("source", "created")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    pass

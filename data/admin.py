from django.contrib import admin

from data.models import ScrapedContent


@admin.register(ScrapedContent)
class ScrapedContentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScrapedContent._meta.fields]
    ordering = ['id']
    list_display_links = ['id']
    search_fields = ('name',)

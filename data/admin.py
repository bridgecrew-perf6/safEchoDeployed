from django.contrib import admin

from data.models import ScrapedData


@admin.register(ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScrapedData._meta.fields]
    ordering = ['id']
    list_display_links = ['id']
    search_fields = ('name',)

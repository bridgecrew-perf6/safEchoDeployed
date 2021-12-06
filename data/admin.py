from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin
from data.models import ScrapedContent, Document


@admin.register(ScrapedContent)
class ScrapedContentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'document', 'heading', 'page_number']
    ordering = ['id']
    list_display_links = ['id']
    search_fields = ('heading',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Document._meta.fields]
    ordering = ['id']
    list_display_links = ['id']
    search_fields = ('document_title', 'author_name')

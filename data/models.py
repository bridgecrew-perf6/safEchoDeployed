from datetime import datetime

from django.db import models
from chat.models import BaseModel


class Document(BaseModel):
    document_title = models.CharField(max_length=540)
    resource_url = models.URLField()
    author_name = models.CharField(max_length=250)
    published_year = models.DateField()
    description = models.TextField()
    number_of_pages = models.IntegerField()
    file = models.FileField()

    def __str__(self):
        return self.document_title


class ScrapedContent(BaseModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    language_default = models.TextField(null=True, blank=True)
    heading = models.TextField(null=True, blank=True)
    default_heading = models.TextField(null=True, blank=True)
    paragraph = models.TextField(null=True, blank=True)
    default_paragraph = models.TextField(null=True, blank=True)
    page_number = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.heading

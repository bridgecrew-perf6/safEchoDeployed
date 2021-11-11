from django.db import models


class ScrapedData(models.Model):
    heading = models.TextField(null=True, blank=True)
    paragraph = models.TextField(null=True, blank=True)

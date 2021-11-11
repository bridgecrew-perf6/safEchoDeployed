from django.db import models


class ScrapedContent(models.Model):
    heading = models.TextField(null=True, blank=True)
    paragraph = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.heading

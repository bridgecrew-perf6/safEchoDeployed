from data.models import ScrapedContent
from haystack import indexes
from datetime import datetime


class ContentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,template_name="search/scrapedcontent_text.txt")
    heading = indexes.CharField(model_attr='heading')
    paragraph = indexes.DateTimeField(model_attr='paragraph')

    def get_model(self):
        return ScrapedContent

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.now())

import os
import fitz
from django.conf import settings


def data_scraper(file_path):
    file = os.path.join(settings.MEDIA_ROOT, file_path)
    doc = fitz.open(file)
    print(doc.page_count,'count')
    text = ''
    with fitz.open(file) as doc:
        for page in doc:
            text += page.getText()
            # break
    print(text,'hfgf')

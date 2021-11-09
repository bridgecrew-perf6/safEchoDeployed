import os
import fitz
from django.conf import settings
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text


def data_scraper(file_path):
    file = os.path.join(settings.MEDIA_ROOT, file_path)
    doc = fitz.open(file)
    # page = doc.load_page(0)
    # page_text_html = page.get_textpage().extractHTML()
    # soup = BeautifulSoup(page_text_html, 'html.parser')
    #
    # for line in soup.find_all('p'):
    #     print(line)
    #     # if line.find('b'):
    #     #     print('heading: ' + line.get_text() + '\n')
    #     # else:
    #     #     print(line.get_text())

    with fitz.open(file) as doc:
        for page in doc:
            page_text_html = page.get_textpage().extractHTML()
            soup = BeautifulSoup(page_text_html, 'lxml')

            for line in soup.find_all('p'):
                if line.find('b'):
                    print('heading: ' + line.get_text() + '\n')
                else:
                    print(line.get_text())

    # print(doc.page_count, 'count')
    # text = ''
    # with fitz.open(file) as doc:
    #     for page in doc:
    #         text += page.getText()
    #         # break
    # print(text, 'hfgf')


def data_scraper_two(file_path):
    file = os.path.join(settings.MEDIA_ROOT, file_path)
    text = extract_text(file)
    print(text)


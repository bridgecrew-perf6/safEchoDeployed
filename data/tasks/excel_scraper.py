import pandas as pd
import os
from django.conf import settings
from chat.translation import translate_text_by_google
from data.models import ScrapedContent, Document
from Project.celery import app as celery_app


class BaseTask(celery_app.Task):
    ignore_result = False

    def __call__(self, *args, **kwargs):
        print("Starting %s" % self.name)
        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # exit point of the task whatever is the state
        print("End of %s" % self.name)


def translate_save_data(data, document, index):
    heading = ''
    paragraph = ''
    default_heading = data['default_heading']
    default_paragraph = data['default_paragraph']

    heading = translate_text_by_google('en', default_heading)
    paragraph = translate_text_by_google('en', default_paragraph)
    result = {'heading': heading, 'paragraph': paragraph, 'default_heading': default_heading,
              'default_paragraph': default_paragraph, 'document': document, 'page_number': index}

    print(index)

    obj = ScrapedContent(**result)
    obj.save()


# def excel_parser(document_id):
#     document = Document.objects.get(id=document_id)
#     columns = ['default_heading', 'default_paragraph']
#     file_path = os.path.join(settings.MEDIA_ROOT, document.file.url)
#     file_path = str(settings.BASE_DIR) + file_path
#     df = pd.read_excel(file_path)
#     df_headers = list(df.columns)
#     headers = []
#     for column in columns:
#         try:
#             headers.append({'index': df_headers.index(column), 'column': column})
#         except ValueError:
#             pass
#     for index, row in df.iloc[2:].iterrows():
#         result = {}
#         for idx, column in enumerate(headers):
#             result[column['column']] = row[column['index']]
#         if bool(result):
#             translate_save_data(result, document, index)


class ImportDataFromExcelTask(BaseTask):
    name = "ImportDataFromExcelTask"

    def run(self, document_id, *args, **kwargs):
        document = Document.objects.get(id=document_id)
        columns = ['default_heading', 'default_paragraph']
        file_path = os.path.join(settings.MEDIA_ROOT, document.file.url)
        file_path = str(settings.BASE_DIR) + file_path
        df = pd.read_excel(file_path)
        df_headers = list(df.columns)
        headers = []
        for column in columns:
            try:
                headers.append({'index': df_headers.index(column), 'column': column})
            except ValueError:
                pass
        for index, row in df.iloc[2:].iterrows():
            result = {}
            for idx, column in enumerate(headers):
                result[column['column']] = row[column['index']]
            if bool(result):
                translate_save_data(result, document, index)


@celery_app.task(bind=True, base=ImportDataFromExcelTask)
def excel_parser_task(self, *args, **kwargs):
    return super(type(self), self).run(*args, **kwargs)

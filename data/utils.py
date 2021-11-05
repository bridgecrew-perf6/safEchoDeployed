from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def in_memory_file_to_temp(in_memory_file):
    path = default_storage.save('tmp/%s' % in_memory_file.name, ContentFile(in_memory_file.read()))
    return path

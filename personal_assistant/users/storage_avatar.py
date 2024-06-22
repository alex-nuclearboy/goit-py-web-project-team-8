from django.core.files.storage import FileSystemStorage


class LocalStorage(FileSystemStorage):
    location = 'media'
    base_url = '/media/'

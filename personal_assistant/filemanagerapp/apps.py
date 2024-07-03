from django.apps import AppConfig


class FilemanagerappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filemanagerapp'

    def ready(self):
        import filemanagerapp.signals
        import filemanagerapp.templatetags.custom_tags

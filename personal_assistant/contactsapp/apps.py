from django.apps import AppConfig


class ContactsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contactsapp'

    def ready(self):
        import contactsapp.signals

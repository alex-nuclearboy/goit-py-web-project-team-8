from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Category


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = {
            'Uncategorised': 'Некатегоризовано',
            'Photos': 'Фотографії',
            'Videos': 'Відео',
            'Music': 'Музика',
            'Documents': 'Документи',
            'Archives': 'Архіви',
            'Other': 'Інше'
        }
        for en_name, uk_name in default_categories.items():
            Category.objects.create(name=en_name, user=instance)

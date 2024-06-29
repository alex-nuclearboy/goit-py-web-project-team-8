from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Group
from .localize import text_array as translations

@receiver(post_save, sender=User)
def create_default_contact_groups(sender, instance, created, **kwargs):
    if created:
        language = instance.profile.language if hasattr(instance, 'profile') else 'en'
        trans = translations.get(language, translations['en'])

        Group.objects.create(creator=instance, name_en=trans['family_group_en'], name_uk=trans['family_group_uk'])
        Group.objects.create(creator=instance, name_en=trans['friends_group_en'], name_uk=trans['friends_group_uk'])
        Group.objects.create(creator=instance, name_en=trans['work_group_en'], name_uk=trans['work_group_uk'])

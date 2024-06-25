# Generated by Django 5.0.6 on 2024-06-24 13:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notesapp", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=50),
        ),
        migrations.AddConstraint(
            model_name="note",
            constraint=models.UniqueConstraint(
                fields=("user", "title"), name="note_of_user"
            ),
        ),
        migrations.AddConstraint(
            model_name="tag",
            constraint=models.UniqueConstraint(
                fields=("user", "name"), name="tag_of_user"
            ),
        ),
    ]
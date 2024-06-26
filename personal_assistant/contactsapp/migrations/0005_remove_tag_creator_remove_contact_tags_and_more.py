# Generated by Django 5.0.6 on 2024-06-29 12:59

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactsapp', '0004_alter_contact_birth_month'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='tags',
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Contact', 'verbose_name_plural': 'Contacts'},
        ),
        migrations.RemoveField(
            model_name='contact',
            name='birth_day',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='birth_month',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='birth_year',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='creation_date',
        ),
        migrations.AddField(
            model_name='contact',
            name='birthday',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Birthday'),
        ),
        migrations.AddField(
            model_name='contact',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creation time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.CharField(blank=True, max_length=100, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=30, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=12, verbose_name='Phone'),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=100, verbose_name='Group Name (English)')),
                ('name_uk', models.CharField(max_length=100, verbose_name='Group Name (Ukrainian)')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.AddField(
            model_name='contact',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contactsapp.group', verbose_name='Group'),
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(fields=('creator', 'name'), name='contact_of_creator'),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddConstraint(
            model_name='group',
            constraint=models.UniqueConstraint(fields=('creator', 'name_en'), name='group_of_creator_en'),
        ),
        migrations.AddConstraint(
            model_name='group',
            constraint=models.UniqueConstraint(fields=('creator', 'name_uk'), name='group_of_creator_uk'),
        ),
    ]

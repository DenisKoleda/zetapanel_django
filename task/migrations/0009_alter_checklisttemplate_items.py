# Generated by Django 4.2.6 on 2024-02-15 21:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_checklisttemplate_alter_fileattachment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklisttemplate',
            name='items',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None, verbose_name='Элементы'),
        ),
    ]

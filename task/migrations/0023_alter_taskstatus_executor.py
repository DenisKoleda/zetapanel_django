# Generated by Django 4.2.6 on 2024-02-18 01:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0022_alter_taskstatus_options_taskstatus_executor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstatus',
            name='executor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='executor_statuses', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
            preserve_default=False,
        ),
    ]
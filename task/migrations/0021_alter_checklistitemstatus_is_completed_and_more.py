# Generated by Django 4.2.6 on 2024-02-18 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0020_remove_checklistitem_status_alter_task_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistitemstatus',
            name='is_completed',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Завершено'),
        ),
        migrations.AlterField(
            model_name='checklistitemstatus',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.checklistitem', verbose_name='Элемент'),
        ),
        migrations.AlterField(
            model_name='checklistitemstatus',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklist_statuses', to='task.task', verbose_name='Задача'),
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200, verbose_name='Статус')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='task.task', verbose_name='Задача')),
            ],
        ),
    ]

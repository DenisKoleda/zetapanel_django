# Generated by Django 4.2.6 on 2024-02-15 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_remove_checklisttemplate_items_checklistitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checklistitem',
            options={'verbose_name': 'элемент чеклиста', 'verbose_name_plural': 'Элементы чеклиста'},
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('1', 'Создано'), ('2', 'В работе'), ('3', 'Завершено'), ('4', 'Отложено'), ('5', 'Отменено'), ('6', 'В ожидании'), ('7', 'В планах'), ('8', 'На проверке'), ('9', 'На доработке'), ('10', 'На утверждении'), ('11', 'На согласовании')], max_length=200, verbose_name='Статус'),
        ),
    ]
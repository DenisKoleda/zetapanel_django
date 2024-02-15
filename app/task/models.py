from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class ChecklistTemplate(models.Model):
    name = models.CharField("Название", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Шаблон чеклиста"
        verbose_name_plural = "Шаблоны чеклистов"


class ChecklistItem(models.Model):
    template = models.ForeignKey(
        ChecklistTemplate, related_name='items', on_delete=models.CASCADE)
    name = models.CharField("Элемент", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "элемент чеклиста"
        verbose_name_plural = "Элементы чеклиста"


class Task(models.Model):
    date = models.DateField("Дата публикации")
    author = models.CharField("Автор", max_length=200)
    ticket = models.CharField("Тикет", max_length=200)
    ticket_comment = models.TextField(
        "Комментарий к тикету", blank=True, null=True)
    priority_choices = [
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
        (4, 'Очень высокий'),
        (5, 'Критический'),
    ]
    priority = models.CharField(
        "Приоритет", max_length=200, choices=priority_choices, default='1')
    status_choices = [
        (1, 'Создано'),
        (2, 'В работе'),
        (3, 'Завершено'),
        (4, 'Отложено'),
        (5, 'Отменено'),
        (6, 'В ожидании'),
        (7, 'В планах'),
        (8, 'На проверке'),
        (9, 'На доработке'),
        (10, 'На утверждении'),
        (11, 'На согласовании'),
    ]
    status = models.CharField("Статус", max_length=200,
                              choices=status_choices, default='1')
    executor = models.ForeignKey(
        User, verbose_name="Исполнитель", on_delete=models.CASCADE)
    deadline = models.DateField("Срок", blank=True, null=True)
    checklist_template = models.ForeignKey(
        ChecklistTemplate, verbose_name="Шаблон чеклиста", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.author} - {self.ticket}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-id']  # Пример сортировки по умолчанию


class Comment(models.Model):
    task = models.ForeignKey(
        Task, verbose_name="Задача", on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE)
    content = models.TextField("Содержание")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author} к задаче {self.task.id}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-id']


class FileAttachment(models.Model):
    def get_upload_path(instance, filename):
        return f'attachments/{instance.task.id}/{filename}'

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def filesize(self):
        try:
            size = self.file.size
        except FileNotFoundError:
            return "File not found"
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"

    def __str__(self):
        return f"Файл {self.filename} к задаче {self.task.id}"

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"
        ordering = ['-id']

    task = models.ForeignKey(
        Task, verbose_name="Задача", on_delete=models.CASCADE, related_name='attachments')
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Файл", upload_to=get_upload_path)
    description = models.CharField(
        "Описание", max_length=200, blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

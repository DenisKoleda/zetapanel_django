from django.db import models
from django.contrib.auth.models import User
import os

STATUS_CHOICES = [
    ('created', 'Создано'),
    ('in_progress', 'В работе'),
    ('completed', 'Завершено'),
    ('postponed', 'Отложено'),
    ('canceled', 'Отменено'),
    ('pending', 'В ожидании'),
    ('planned', 'В планах'),
    ('under_review', 'На проверке'),
    ('under_revision', 'На доработке'),
    ('under_approval', 'На утверждении'),
    ('under_consideration', 'На согласовании'),
]

PRIORITY_CHOICES = [
    ('low', 'Низкий'),
    ('medium', 'Средний'),
    ('high', 'Высокий'),
    ('very_high', 'Очень высокий'),
    ('critical', 'Критический'),
]


class ChecklistTemplate(models.Model):
    name = models.CharField("Название", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Шаблон чеклиста"
        verbose_name_plural = "Шаблоны чеклистов"


class Task(models.Model):
    date = models.DateField("Дата создания", auto_now_add=True)
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE, related_name='author_tasks')
    ticket = models.CharField("Задача", max_length=200)
    ticket_comment = models.TextField(
        "Комментарий к задаче", blank=True, null=True)
    priority = models.CharField(
        "Приоритет", max_length=200, choices=PRIORITY_CHOICES, default='low')
    status = models.CharField("Статус", max_length=200,
                              choices=STATUS_CHOICES, default='1')
    executor = models.ForeignKey(
        User, verbose_name="Исполнитель", on_delete=models.CASCADE, related_name='executor_tasks', blank=True, null=True)

    deadline = models.DateField("Дедлайн", blank=True, null=True)
    checklist_template = models.ForeignKey(
        ChecklistTemplate, verbose_name="Шаблон чеклиста", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.author} - {self.ticket}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-id']  # Пример сортировки по умолчанию


class TaskStatus(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='statuses', verbose_name="Задача")
    executor = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Исполнитель", related_name='executor_statuses')
    status = models.CharField(
        max_length=200, choices=STATUS_CHOICES, verbose_name="Статус")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self) -> str:
        return f"Статус {self.status} для задачи {self.task.id}"

    class Meta:
        verbose_name = "Статус задачи"
        verbose_name_plural = "Статусы задачи"
        ordering = ['-id']


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


class ChecklistItem(models.Model):
    template = models.ForeignKey(
        ChecklistTemplate, related_name='items', on_delete=models.CASCADE)
    name = models.CharField("Элемент", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "элемент чеклиста"
        verbose_name_plural = "Элементы чеклиста"


class ChecklistItemStatus(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='checklist_statuses', verbose_name="Задача")
    item = models.ForeignKey(
        ChecklistItem, on_delete=models.CASCADE, verbose_name="Элемент")
    is_completed = models.BooleanField(
        "Завершено", default=False, blank=True, null=True)

    def __str__(self):
        return f"Статус элемента чеклиста {self.item.name} для задачи {self.task.id}"

    class Meta:
        verbose_name = "Статус элемента чеклиста"
        verbose_name_plural = "Статусы элементов чеклиста"

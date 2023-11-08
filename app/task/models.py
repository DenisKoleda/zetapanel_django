from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    date = models.DateField("Дата публикации")
    author = models.CharField("Автор", max_length=200)
    ticket = models.CharField("Тикет", max_length=200)
    ticket_comment = models.TextField("Комментарий к тикету", blank=True, null=True)
    priority = models.CharField("Приоритет", max_length=200)
    status = models.CharField("Статус", max_length=200)
    executor = models.CharField("Исполнитель", max_length=200)
    deadline = models.DateField("Срок", blank=True, null=True)

    def __str__(self):
        return f"{self.author} - {self.ticket}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-id']  # Пример сортировки по умолчанию

class Comment(models.Model):
    task = models.ForeignKey(Task, verbose_name="Задача", on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    content = models.TextField("Содержание")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author} к задаче {self.task.id}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-id']

class FileAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Файл", upload_to='attachments/')
    description = models.CharField("Описание", max_length=200, blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    
    def __str__(self):
        return f"Вложение {self.file.name} к задаче {self.task.id}"
    
    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"
        ordering = ['-id']
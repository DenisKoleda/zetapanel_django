from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    # Django автоматически создает ID-поле, если иное не указано
    date = models.DateField("date published")
    author = models.CharField(max_length=200)
    ticket = models.CharField(max_length=200)
    ticket_comment = models.TextField(blank=True, null=True)  # Это поле предназначено для длинных строк текста
    priority = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    executor = models.CharField(max_length=200)
    deadline = models.DateField("deadline", blank=True, null=True)

    # Добавьте любые другие поля, необходимые для вашего приложения

    # Опционально: добавьте метод __str__ для более читаемого представления объектов модели
    def __str__(self):
        return f"{self.author} - {self.ticket}"

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on Task {self.task.id}"
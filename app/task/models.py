from django.db import models

class Task(models.Model):
    # Django автоматически создает ID-поле, если иное не указано
    date = models.DateTimeField("date published")
    author = models.CharField(max_length=200)
    ticket = models.CharField(max_length=200)
    ticket_comment = models.TextField()  # Это поле предназначено для длинных строк текста
    priority = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    executor = models.CharField(max_length=200)
    deadline = models.DateTimeField("deadline", blank=True, null=True)

    # Добавьте любые другие поля, необходимые для вашего приложения

    # Опционально: добавьте метод __str__ для более читаемого представления объектов модели
    def __str__(self):
        return f"{self.author} - {self.ticket}"

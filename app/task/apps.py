from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task'
    verbose_name = "Менеджер Задач"  # Имя, которое будет отображаться в админ-панели

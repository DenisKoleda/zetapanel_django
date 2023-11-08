from django.contrib import admin
from .models import Task, Comment

class TaskAdmin(admin.ModelAdmin):
    list_display = ('date', 'author', 'ticket', 'priority', 'status', 'executor', 'deadline')
    list_filter = ('date', 'author', 'priority', 'status', 'executor')
    search_fields = ['author', 'ticket', 'ticket_comment', 'priority', 'status', 'executor']

admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
from django.contrib import admin
from .models import Task, Comment, FileAttachment, ChecklistTemplate, ChecklistItem, ChecklistItemStatus

# Register your models here.


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1  # Number of extra "empty" forms


@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'author', 'ticket',
                    'priority', 'status', 'executor', 'deadline')
    list_filter = ('date', 'author', 'priority', 'status', 'executor')
    search_fields = ['author', 'ticket', 'ticket_comment',
                     'priority', 'status', 'executor']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'author', 'content', 'created_at')
    list_filter = ('task', 'author', 'created_at')
    search_fields = ['author', 'content']


@admin.register(FileAttachment)
class FileAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'author', 'file', 'created_at')
    list_filter = ('task', 'author', 'created_at')
    search_fields = ['author', 'file']


@admin.register(ChecklistItemStatus)
class ChecklistItemStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'item')
    list_filter = ('task', 'item')
    search_fields = ['task', 'item']

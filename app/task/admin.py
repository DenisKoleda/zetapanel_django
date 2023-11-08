from django.contrib import admin
from .models import Task, Comment, FileAttachment

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'author', 'ticket', 'priority', 'status', 'executor', 'deadline')
    list_filter = ('date', 'author', 'priority', 'status', 'executor')
    search_fields = ['author', 'ticket', 'ticket_comment', 'priority', 'status', 'executor']
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'author', 'content', 'created_at')
    list_filter = ('task', 'author', 'created_at')
    search_fields = ['author', 'content']
    
class FileAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'author', 'file', 'created_at')
    list_filter = ('task', 'author', 'created_at')
    search_fields = ['author', 'file']


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FileAttachment, FileAttachmentAdmin)
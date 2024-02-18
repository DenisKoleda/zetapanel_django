from django.contrib import admin
from django.http import FileResponse
import xlsxwriter
from io import BytesIO
from .models import Task, Comment, FileAttachment, ChecklistTemplate, ChecklistItem, ChecklistItemStatus, TaskStatus
from django.contrib.auth.models import User

# Register your models here.


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1  # Number of extra "empty" forms


@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemInline]


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'executor', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ['task', 'status']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'author', 'ticket',
                    'priority', 'status', 'executor', 'deadline')
    list_filter = ('date', 'author', 'priority', 'status', 'executor')
    search_fields = ['author', 'ticket', 'ticket_comment',
                     'priority', 'status', 'executor']

    def export_to_excel(modeladmin, request, queryset):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        worksheet = workbook.add_worksheet()

        fields = Task._meta.fields  # Get direct fields of the Task model
        # Get the names of the fields
        field_names = [field.verbose_name for field in fields]

        for i, field_name in enumerate(field_names):
            worksheet.write(0, i, field_name)

        # Get all Task objects
        for row_num, task in enumerate(Task.objects.all(), start=1):
            for col_num, field in enumerate(fields):
                value = getattr(task, field.name)
                if isinstance(value, User):  # If the value is a User object, get the username
                    value = value.username
                # If the value is a ChecklistTemplate object, get the name
                if isinstance(value, ChecklistTemplate):
                    value = value.name
                # Write the field values to the Excel
                worksheet.write(row_num, col_num, value)

        workbook.close()

        output.seek(0)

        response = FileResponse(
            output, as_attachment=True, filename='tasks.xlsx')
        return response

    export_to_excel.short_description = "Export All"

    actions = [export_to_excel]


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

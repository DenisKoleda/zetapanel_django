from django import forms
from .models import Task, Comment, FileAttachment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['date', 'author', 'ticket', 'ticket_comment', 'priority', 'status', 'executor', 'deadline']
        # Optionally, add widgets or other form options here

    # Example of custom clean method for a field
    def clean_author(self):
        author = self.cleaned_data['author']
        # Add your validation logic here
        return author

    # You can add more custom methods or customizations as needed

            
            
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileAttachment
        fields = ['file', 'description']
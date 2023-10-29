from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Для поля DateTime используйте виджеты, чтобы обеспечить правильный выбор даты/времени
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['date', 'author', 'ticket', 'ticket_comment', 'priority', 'status', 'executor', 'deadline']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Формат ввода для поля DateTime в соответствии со стандартом HTML5
        self.fields['date'].input_formats = ['%Y-%m-%dT%H:%M']
        if self.fields.get('deadline'):
            self.fields['deadline'].input_formats = ['%Y-%m-%dT%H:%M']
            
            
            

from django import forms
from .models import Task, Comment, FileAttachment
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'ticket': forms.TextInput(attrs={'class': 'form-control'}),
            'ticket_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'executor': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'checklist_template': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        # Добавляем параметр user для идентификации
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        # Настройка метода label_from_instance для author и executor
        self.fields['author'].label_from_instance = self.label_from_instance
        self.fields['executor'].label_from_instance = self.label_from_instance
        self.fields['author'].initial = user.id

        if user:
            # Помещаем текущего пользователя в начало списка
            self.fields['author'].queryset = User.objects.all().exclude(
                id=user.id).order_by('username')
            self.fields['executor'].queryset = User.objects.all().exclude(
                id=user.id).order_by('username')

            # Добавляем текущего пользователя в начало списка
            self.fields['author'].queryset = User.objects.filter(
                id=user.id) | self.fields['author'].queryset
            self.fields['executor'].queryset = User.objects.filter(
                id=user.id) | self.fields['executor'].queryset

        self.fields['author'].label_from_instance = lambda obj: "Я" if obj == user else obj.get_full_name(
        ) or obj.username
        self.fields['executor'].label_from_instance = lambda obj: "Я" if obj == user else obj.get_full_name(
        ) or obj.username

    # Определение отображения имени пользователя в выпадающем списке

    def label_from_instance(self, obj):
        # Возвращаем имя и фамилию, если они есть, иначе логин
        return obj.get_full_name() or obj.username


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileAttachment
        fields = ['file']

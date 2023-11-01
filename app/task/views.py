from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Task
from .forms import TaskForm

def tasks_list(request):
    # Поиск: получение строки запроса, если она есть
    query = request.GET.get("q")
    object_list = Task.objects.all()
    if query:
        object_list = object_list.filter(author__icontains=query)  # Можно добавить фильтры для других столбцов

    # Пагинация
    paginator = Paginator(object_list, 10)  # 10 задач на странице
    page = request.GET.get('page')

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу
        tasks = paginator.page(1)
    except EmptyPage:
        # Если страница вне диапазона (например, 9999), возвращаем последнюю страницу результатов
        tasks = paginator.page(paginator.num_pages)

    return render(request, 'tasks_list.html', {'page': page, 'tasks': tasks})

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_edit.html', {'form': form})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_edit.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'task_delete.html', {'task': task})

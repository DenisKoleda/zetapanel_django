from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, QueryDict, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from .models import Task, Comment
from .forms import TaskForm

def tasks_list(request):
    object_list = Task.objects.all().order_by('id')

    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
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


def task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = Comment.objects.filter(task=task).order_by('-created_at')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        author = request.user
        comment = Comment.objects.create(task=task, author=author, content=content)
        # Optionally, you can perform additional actions after creating the comment
        
    return render(request, 'task_view.html', {'task': task, 'comments': comments})

def add_comment(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        content = request.POST.get('content')
        author = request.user
        comment = Comment.objects.create(task=task, author=author, content=content)
        # Optionally, you can perform additional actions after creating the comment
    return HttpResponseRedirect(reverse('task_view', args=[pk]))

def delete_comment(request, pk, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        # Optionally, you can perform additional actions after deleting the comment
    return HttpResponseRedirect(reverse('task_view', args=[pk]))
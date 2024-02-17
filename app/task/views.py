from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from .models import Task, Comment, FileAttachment
from .forms import TaskForm, FileUploadForm
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User


@login_required
def tasks_list(request):
    # Получение значений фильтров из request.GET
    q = request.GET.get('q')
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    page_length = request.GET.get('page_length')
    executor = request.GET.get('executor')
    author = request.GET.get('author')

    priority_choices = Task._meta.get_field('priority').choices
    status_choices = Task._meta.get_field('status').choices
    users = User.objects.all()
    users_choices = [(user.id, f"{user.first_name} {
                      user.last_name}" if user.first_name and user.last_name else user.username) for user in users]

    form = TaskForm(user=request.user)

    # Применение фильтров к запросу данных
    object_list = Task.objects.all().order_by('id')

    if q:
        object_list = object_list.filter(
            Q(ticket__icontains=q.lower()) |
            Q(ticket_comment__icontains=q.lower()))

    if priority != 'all' and priority:
        object_list = object_list.filter(priority=priority)

    if status != 'all' and status:
        if status == 'active':
            object_list = object_list.exclude(
                status__in=['completed', 'canceled'])
        else:
            object_list = object_list.filter(status=status)

    if executor != 'all' and executor:
        object_list = object_list.filter(executor=executor)

    if author != 'all' and author:
        object_list = object_list.filter(author=author)

    paginator = Paginator(object_list, page_length or 10)
    page = request.GET.get('page')

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request, 'tasklist/index.html', {'page': page, 'tasks': tasks, 'priority_choices': priority_choices, 'status_choices': status_choices, 'form': form, 'users_choices': users_choices})


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    return HttpResponse('Invalid request method')


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_edit.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        task.delete()
        return redirect('task_list')


def task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = Comment.objects.filter(task=task).order_by('-created_at')
    files = FileAttachment.objects.filter(task=task).order_by('-created_at')
    form = TaskForm(instance=task, user=request.user)

    return render(request, 'taskview/task_view.html', {'task': task, 'comments': comments, 'files': files, 'form': form})


def add_comment(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        content = request.POST.get('content')
        author = request.user
        comment = Comment.objects.create(
            task=task, author=author, content=content)
        # Optionally, you can perform additional actions after creating the comment
        return HttpResponseRedirect(reverse('task_view', args=[pk]))
    return HttpResponse('Invalid request method')


def delete_comment(request, pk, comment_id):
    if request.method == 'GET':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        # Optionally, you can perform additional actions after deleting the comment
        return HttpResponseRedirect(reverse('task_view', args=[pk]))
    return HttpResponse('Invalid request method')


def add_file(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')  # Get list of uploaded files
            for file in files:
                file_obj = FileAttachment.objects.create(
                    task=task, author=request.user, file=file)
                # Optionally, you can perform additional actions after creating the file attachment
            return HttpResponseRedirect(reverse('task_view', args=[pk]))
    return HttpResponse('Invalid request method')


def download_file(request, pk):
    file = get_object_or_404(FileAttachment, pk=pk)
    if os.path.exists(file.file.path):
        return FileResponse(open(file.file.path, 'rb'), as_attachment=True, filename=file.file.name)
    raise Http404


def delete_file(request, pk):
    file = get_object_or_404(FileAttachment, pk=pk)
    file.file.delete()  # This will also delete the file from the filesystem
    file.delete()
    # Replace 'task_view' with the name of the view you want to redirect to
    return redirect('task_view', pk=file.task.pk)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import TaskForm, FileUploadForm
from .models import Task, Comment, FileAttachment, ChecklistItemStatus
import datetime
import os
from django.views.decorators.http import require_POST


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
        if executor == 'null':
            object_list = object_list.filter(executor=None)
        else:
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


# TODO: Добавить страницу статистики с фильтрами по дате и исполнителю
def task_statistics(request):
    # Получить все задачи за определенный срок(день, неделя, месяц или дата от и до) из request.GET.filter или из request.GET.time_filter
    # date_from = request.GET.get('date_from')
    # date_to = request.GET.get('date_to')
    time_filter = request.GET.get('time_filter')

    if time_filter == 'day':
        _tasks = Task.objects.filter(
            date=datetime.date.today())
    elif time_filter == 'week':
        _tasks = Task.objects.filter(date__range=[
            datetime.date.today() - datetime.timedelta(days=7), datetime.date.today()])
    elif time_filter == 'month':
        _tasks = Task.objects.filter(date__range=[
            datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()])
    # elif date_from and date_to:
    #     _tasks = Task.objects.filter(
    #         date__gte=date_from, date__lte=date_to)
    else:
        _tasks = Task.objects.all()

    print(datetime.date.today())
    print(_tasks.count())
    # Получить количество закрытых
    _closed_tasks = _tasks.filter(status='completed').count()

    # Получить количество закрытых задач по каждому пользователю за определенный срок
    _closed_tasks_per_user = _tasks.values('executor__id', 'executor__username', 'executor__first_name', 'executor__last_name').annotate(
        closed_count=Count('id')).filter(status='completed')

    context = {
        'tasks': _tasks,
        'closed_tasks': _closed_tasks,
        'closed_tasks_per_user': _closed_tasks_per_user,
    }

    return render(request, 'statistics.html', context)


# FIX: Добавить поддержку чеклистов
@require_POST
def save_checklist(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    items = task.checklist_template.items.all()

    for item in items:
        status, created = ChecklistItemStatus.objects.get_or_create(
            task=task, item=item)
        status.checked = f'item{item.id}' in request.POST
        status.save()

    return redirect('task_detail', task_id=task.id)

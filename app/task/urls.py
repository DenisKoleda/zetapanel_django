from django.urls import re_path, path
from django.contrib.auth.decorators import login_required

from . import views, consumers

urlpatterns = [
    path('', login_required(views.tasks_list), name='task_list'),
    path('new/', login_required(views.task_create), name='task_create'),
    path('<int:pk>/edit/', login_required(views.task_edit), name='task_edit'),
    path('<int:pk>/delete/', login_required(views.task_delete), name='task_delete'),
    path('<int:pk>/view/', login_required(views.task_view), name='task_view'),
    path('<int:pk>/add_comment/',
         login_required(views.add_comment), name='add_comment'),
    path('<int:pk>/delete_comment/<int:comment_id>/',
         login_required(views.delete_comment), name='delete_comment'),
    path('<int:pk>/add_file/', login_required(views.add_file), name='add_file'),
    # path('<int:pk>/save_checklist/', login_required(views.save_checklist), name='save_checklist'),
    path('download/<int:pk>/', login_required(views.download_file),
         name='download_file'),
    path('delete_file/<int:pk>/',
         login_required(views.delete_file), name='delete_file'),
    path('statistics/', login_required(views.task_statistics), name='statistics'),
    # Добавьте эту строку для WebSocket маршрута
    re_path(r'ws/tasks/$', consumers.TaskConsumer.as_asgi()),
]

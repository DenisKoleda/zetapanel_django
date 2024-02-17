from django.urls import re_path, path

from . import views, consumers

urlpatterns = [
    path('', views.tasks_list, name='task_list'),
    path('new/', views.task_create, name='task_create'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/view/', views.task_view, name='task_view'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('<int:pk>/add_file/', views.add_file, name='add_file'),
    # path('<int:pk>/save_checklist/', views.save_checklist, name='save_checklist'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    path('delete_file/<int:pk>/', views.delete_file, name='delete_file'),
    path('statistics/', views.task_statistics, name='statistics'),
    # Добавьте эту строку для WebSocket маршрута
    re_path(r'ws/tasks/$', consumers.TaskConsumer.as_asgi()),
]

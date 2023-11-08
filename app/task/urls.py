from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_list, name='task_list'),
    path('new/', views.task_create, name='task_create'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/view/', views.task_view, name='task_view'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    
]

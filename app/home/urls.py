# home/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]

# home/views.py

from django.shortcuts import render

def homepage_view(request):
    return render(request, 'home/homepage.html')

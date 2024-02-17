# home/views.py

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages


def homepage_view(request):
    return render(request, 'home/homepage.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

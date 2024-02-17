# home/views.py

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages


def homepage_view(request):
    return render(request, 'home/homepage.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Get the 'remember' checkbox value
        remember = request.POST.get('remember-me')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if remember:  # If 'remember' checkbox is checked
                # Set session expiry time to one week
                request.session.set_expiry(259200)  # 72 hours in seconds
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

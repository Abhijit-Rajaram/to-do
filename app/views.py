from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


@login_required
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('task_list')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('task_list')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('task_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from collections import defaultdict
from django.utils.timezone import localtime
from datetime import date
from django.utils import timezone

@login_required
def task_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(user=request.user, title=title)
            return redirect('task_list')

    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    grouped_tasks = defaultdict(list)
    today = timezone.localdate()
    yesterday = today - timezone.timedelta(days=1)

    for task in tasks:
        task_date = localtime(task.created_at).date()

        if task_date == today:
            label = "Today"
        elif task_date == yesterday:
            label = "Yesterday"
        else:
            label = task_date.strftime("%B %d, %Y")

        grouped_tasks[label].append(task)
    
    print(grouped_tasks, 'grouped_tasks')

    return render(request, 'task_list.html', {
        'grouped_tasks':  dict(grouped_tasks)
    })


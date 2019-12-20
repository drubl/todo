from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import AddTaskForm, LoginForm, DeleteTaskForm, CompliteTaskForm, RegisterForm
from django.contrib.auth.models import User
from .models import Task

class Tasks(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')
    def get(self, request):
        profile = request.user.profile

        category_id = request.GET.get('cat')
        if category_id is not None:
            try:
                tasks = profile.category_set.get(id=category_id).task_set.all()
            except exc:
                return Http404()
            
        else:
            tasks = profile.get_tasks()
        
        count_complited_tasks = profile.count_complited_tasks()

        form = AddTaskForm()
        form.fields['category'].queryset = profile.category_set.all()

        categories = profile.category_set.all()
        context = {
            'tasks': tasks,
            'count_complited_tasks': count_complited_tasks,
            'form': form,
            'categories': categories
        }
        return render(request, 'todo/main.html', context=context)


class TaskAdd(LoginRequiredMixin, View):
    def post(self, request):
        form = AddTaskForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            task = Task.objects.create(title=title, body=body, checked=False, user_id=user.id)
        return redirect('tasks_url')


class TaskDelete(LoginRequiredMixin, View):
    def post(self, request):
        form = DeleteTaskForm(request.POST)
        if form.is_valid():
            user = request.user
            task_id = form.cleaned_data.get('task_id')
            task = user.profile.task_set.get(id=task_id)
            task.delete()
        return redirect('tasks_url')


class TaskComplited(LoginRequiredMixin, View): #TODO use Mixin
    def post(self, request):
        form = CompliteTaskForm(request.POST)
        if form.is_valid():
            user = request.user
            task_id = form.cleaned_data.get('task_id')
            task = user.profile.task_set.get(id=task_id)
            task.change_complite_state()
        return redirect('tasks_url')

class CategoryAdd(LoginRequiredMixin, View):
    def post(self, request):
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            pass


class Login(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return render(request, 'todo/login.html', context={'form': form})
        return redirect('tasks_url')
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(username=username.lower(), password=password)
            if user is not None and user.is_active:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect('tasks_url')
            else:
                form = LoginForm()
                messages.add_message(request, messages.ERROR, 'Логин или пароль не верный')
                return render(request, 'todo/login.html', context={'form': form})
        return render(request, 'todo/login.html', context={'form': form})
            

class Register(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = RegisterForm()
            return render(request, 'todo/register.html', context = {'form': form})
        return redirect('tasks_url')
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if User.objects.filter(username=username.lower()).count() != 0:
                messages.add_message(request, messages.INFO, 'Данное имя уже занято')
                return render(request, 'todo/register.html', context = {'form': form})

            if password1 != password2:
                messages.add_message(request, messages.INFO, 'Пароли не совпадают')
                return render(request, 'todo/register.html', context = {'form': form})

            User.objects.create_user(username=username.lower(), email=None, password=password1)
            return redirect('login_url')
        messages.add_message(request, messages.INFO, 'Ошибка, попробуйте позже')
        return render(request, 'todo/register.html', context = {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login_url')


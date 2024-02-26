from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from task.form import TaskForm
from task.models import Task
from users.models import User
from utils.mixins import CreatorRequiredMixin


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('task:open_task_list'))
    else:
        task_count = Task.objects.all().count()
        active_task_count = Task.objects.exclude(status='CL').count()
        user_count = User.objects.all().count()

        context = {'task_count': task_count,
                   'active_task_count': active_task_count,
                   'user_count': user_count}
        return render(request, 'task/index.html', context)


@login_required(login_url='/')
def task_change_status(request, pk, status):
    try:
        task = Task.objects.get(id=pk)
    except:
        raise Http404("Задача не найдена!")
    if task.user != request.user:
        raise Http404("Страница не найдена!")
    task.status = status
    task.save()
    return HttpResponseRedirect(reverse('task:open_task_list'))


class TaskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user).order_by("-created_time")
        return queryset


class CloseTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/close_task_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user, status='CL').order_by("-created_time")

        return queryset


class OpenTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/open_task_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user, status='OP').order_by("deadline")

        return queryset


class ExpressTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/express_task_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user, status='OP').order_by("deadline")

        result_list = []
        for item in queryset:
            if item.get_status() == 'EX':
                result_list.append(item)

        return result_list


class OverdueTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/overdue_task_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user, status='OP').order_by("deadline")

        result_list = []
        for item in queryset:
            if item.get_status() == 'OV':
                result_list.append(item)

        return result_list


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task:open_task_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, CreatorRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task:open_task_list')


class TaskDeleteView(LoginRequiredMixin, CreatorRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task:open_task_list')


class TaskDetailView(LoginRequiredMixin, CreatorRequiredMixin, DetailView):
    model = Task

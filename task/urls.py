from django.urls import path

from task.apps import TaskConfig
from task.views import index, TaskListView, TaskCreateView, TaskDeleteView, TaskUpdateView, TaskDetailView, \
    task_change_status, CloseTaskListView, OpenTaskListView, ExpressTaskListView, OverdueTaskListView

app_name = TaskConfig.name

urlpatterns = [
    path('', index, name="index"),
    path('tasks', TaskListView.as_view(), name="task_list"),
    path('tasks/close', CloseTaskListView.as_view(), name="close_task_list"),
    path('tasks/open', OpenTaskListView.as_view(), name="open_task_list"),
    path('tasks/express', ExpressTaskListView.as_view(), name="express_task_list"),
    path('tasks/overdue', OverdueTaskListView.as_view(), name="overdue_task_list"),
    path('task/add', TaskCreateView.as_view(), name='task_add'),
    path('task/<int:pk>', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/update', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/<str:status>', task_change_status, name='task_change'),
]


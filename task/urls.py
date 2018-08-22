from django.conf.urls import url
from django.urls import path

from task.apps import TaskConfig
from task.views import create_task, get_info, start_workers, disable_workers

app_name = TaskConfig.name
urlpatterns = [
    path(r'create_task/', create_task, name='create task'),
    path(r'get_info/<int:task_id>/', get_info, name='get task info'),
    path(r'start_workers/', start_workers, name='start workers'),
    path(r'disable_workers/', disable_workers, name='disable workers'),
]

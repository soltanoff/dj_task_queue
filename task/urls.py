from django.conf.urls import url
from django.urls import path

from task.apps import TaskConfig
from task.views import create_task, get_info

app_name = TaskConfig.name
urlpatterns = [
    path(r'create_task/', create_task, name='create task'),
    path(r'get_info/<int:task_id>/', get_info, name='get task info'),
]

from datetime import datetime

from django.db import models
from enumfields import Enum
from enumfields import EnumField


class Status(Enum):
    """
    In Queue -- задача ждёт своей очереди на выполнение;
    Run -- произошел запуск задачи;
    Completed -- задача выполнена.
    """
    IN_QUEUE = 0
    RUN = 1
    COMPLETED = 2

    class Labels:
        IN_QUEUE = 'In Queue'
        RUN = 'Run'
        COMPLETED = 'Completed'


class TaskModel(models.Model):
    class Meta:
        ordering = ('-create_time', '-status',)
        verbose_name = 'Task'

    create_time = models.DateTimeField('Create time', default=datetime.now)
    start_time = models.DateTimeField('Start time', blank=True, null=True, default=None)
    exec_time = models.DateTimeField('Execution time', blank=True, null=True, default=None)
    status = EnumField(Status, max_length=1)

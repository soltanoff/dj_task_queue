from rest_framework import serializers

from task.models import TaskModel


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ('id', 'create_time', 'start_time', 'exec_time', 'status')

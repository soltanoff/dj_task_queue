from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes

from task.models import TaskModel, Status
from worker import WORKER_LIST
from worker.settings import NEW_TASK_EVENT


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_task(request):
    task = TaskModel(status=Status.IN_QUEUE)
    task.save()

    if NEW_TASK_EVENT.is_set():
        NEW_TASK_EVENT.clear()
    NEW_TASK_EVENT.set()
    return JsonResponse({"task_id": task.pk})


@api_view(['GET'])
def get_info(request, task_id):
    try:
        task = TaskModel.objects.get(pk=task_id)  # type: TaskModel
        return JsonResponse({
            'status': task.status.label,
            'create_time': task.create_time,
            'start_time': task.start_time,
            'time_to_execute': str(task.exec_time - task.start_time) if task.exec_time is not None else None,
        })
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Task #%s does not exists" % task_id}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.IsAdminUser,))
def start_workers(request):
    try:
        for x in WORKER_LIST:
            x.start()
        return JsonResponse({"message": "workers are running"})
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.IsAdminUser,))
def disable_workers(request):
    try:
        for x in WORKER_LIST:
            x.disable()
        return JsonResponse({"message": "workers are disabled"})
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

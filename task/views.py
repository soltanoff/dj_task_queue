from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from task.models import TaskModel, Status
from worker import WORKER_LIST
from worker.settings import NEW_TASK_EVENT


@csrf_exempt
def create_task(request):
    if request.method == 'GET':
        task = TaskModel(status=Status.IN_QUEUE)
        task.save()

        if NEW_TASK_EVENT.is_set():
            NEW_TASK_EVENT.clear()
        NEW_TASK_EVENT.set()
        return JsonResponse({"task_id": task.pk})
    else:
        raise Http404


@csrf_exempt
def get_info(request, task_id):
    if request.method == 'GET':
        try:
            task = TaskModel.objects.get(pk=task_id)  # type: TaskModel
            return JsonResponse({
                'status': task.status.label,
                'create_time': task.create_time,
                'start_time': task.start_time,
                'time_to_execute': str(task.exec_time - task.start_time) if task.exec_time is not None else None,
            })
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Task #%s does not exists" % task_id}, status=400)
    else:
        raise Http404


@csrf_exempt
def start_workers(request):
    if request.method == 'GET':
        try:
            # map(lambda x: x.start(), WORKER_LIST)
            for x in WORKER_LIST:
                x.start()
            return JsonResponse({"message": "workers are running"})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    else:
        raise Http404


@csrf_exempt
def disable_workers(request):
    if request.method == 'GET':
        try:
            # map(lambda x: x.disable(), WORKER_LIST)
            for x in WORKER_LIST:
                x.disable()
            return JsonResponse({"message": "workers are disabled"})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    else:
        raise Http404

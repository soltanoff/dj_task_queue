import asyncio
import os
from threading import Event, Thread

from django.db.models.query import QuerySet
from django.utils import timezone

from django_task_queue.settings import BASE_DIR
from task.models import TaskModel, Status
from worker.settings import MAIN_MUTEX


class Worker(object):
    """
    Класс воркера исполняющий по сигналу.

    Особенности:
    * Выполняться одновременно могут 2 задачи.
    * Несколько экземпляров воркеров будут синхронизироваться блягодаря MAIN_MUTEX.

    В случае добавлению приоритетов задач, можно задачи организовывать по SJF (Shortest-Job-First).
    Реализацию параллельной работы можно было организовать пустив 2 воркера с TASK_LIMIT = 1 или же запускать 2 потока,
    которые будут исполнять задачи синхронизируясь по дополнительному мьютексу.
    """
    TASK_LIMIT = 2  # количество задач доступных для параллельной обработки

    def __init__(self, new_task_event=None):
        """
        :param new_task_event: экземпляр события-признака добавления новых задач
        :type new_task_event: Event
        """
        assert new_task_event is not None, 'Worker: no instance of the event adding new tasks'
        self.__thread = Thread(target=self.__routine)

        self.__new_task_event = new_task_event
        self.__new_task_event.clear()

        self.enable = True  # флаг для приостановки работы воркера. @see: Worker.__routine()

    def __get_process(self):
        """
        Реализация метода взятия активных задач из списка.
        :return:
        """
        task_list = []
        try:
            MAIN_MUTEX.acquire()
            while True:
                task_list = TaskModel.objects.filter(status=0)[:self.TASK_LIMIT]  # type: QuerySet[TaskModel]
                if not task_list:
                    self.__wait_new_process()
                else:
                    break
        except Exception as e:
            print('[WORKER_ERROR] %s' % e)
            task_list = []
        finally:
            MAIN_MUTEX.release()
            return task_list

    def __wait_new_process(self):
        """
        Ожидание сигнала о поплнении списка задач.
        :return:
        """
        try:
            if self.enable:
                self.__new_task_event.clear()
                self.__new_task_event.wait()
        except Exception as e:
            print('[WORKER_ERROR] %s' % e)

    @staticmethod
    async def __execute_task(task):
        """
        Метод исполняющий активную задачу
        :param task: активная задача
        :type task: TaskModel
        :return:
        """
        print('[Worker] Task #%s started' % task.pk)
        task.start_time = timezone.now()
        task.status = Status.RUN
        task.save()
        os.system('python %s' % os.path.join(BASE_DIR, 'worker', 'task.py'))
        task.exec_time = timezone.now()
        task.status = Status.COMPLETED
        task.save()
        print('[Worker] Task #%s finished' % task.pk)

    async def __asynchronous(self, task_list):
        """
        Метод для асинхронного исполнения списка функций
        :param task_list: список активных задач
        :type task_list: QuerySet[TaskModel]
        :return:
        """
        tasks = [asyncio.ensure_future(self.__execute_task(i)) for i in task_list]
        await asyncio.wait(tasks)

    def __routine(self):
        """
        Основная рутина воркера
        :return:
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ioloop = asyncio.get_event_loop()
        try:
            while self.enable:
                task_list = self.__get_process()
                ioloop.run_until_complete(self.__asynchronous(task_list))
        finally:
            ioloop.close()

    def start(self):
        """
        Запуск воркера
        :return:
        """
        self.__thread.start()

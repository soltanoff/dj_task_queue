from worker.settings import NEW_TASK_EVENT
from worker.worker import Worker

WORKER = Worker(NEW_TASK_EVENT)
WORKER.start()

from worker.settings import NEW_TASK_EVENT
from worker.worker import Worker

WORKER_LIST = [Worker(NEW_TASK_EVENT)]

# map(lambda x: x.start(), WORKER_LIST)
for x in WORKER_LIST:
    x.start()

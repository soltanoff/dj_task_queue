# Django Task Queue

Prototype of the web service for organizing the task queue.

Functionality:
0. API schemas: `/`
1. `task/create_task` is a method that creates a task that is added to the queue, and the task number is returned to the user.
2. `task/get_info/<int: task_id>` - returns the status of the task in the format json {'status:'', 'create_time":'', 'start_time':'', 'time_to_execute':''}.
    Statuses:
     - In Queue - the task is waiting for its turn to execute;
     - Run - the task was started;
     - Completed - the task is completed.
3. The task execution is a simple python code (test.py):
    ```python
    import time
    import random
    time.sleep(random.randint(0,10))
    ```
4. `task/start_workers` is a method that all `Worker`'s run.
5. `task/disable_workers` is a method that disables all `Worker`'s.

Note:
* You can create many tasks, but at the same time it should not exceed 2.
* the results are written to the local database.


The class implementing the `Worker` works with` asyncio`.

Installation:
============
```
$ pip3 install -r requirements.txt
$ python3 manage.py migrate --run-syncdb
$ python3 manage.py createsuperuser
```
Run:
============
```
$ python3 manage.py runserver 0.0.0.0:8080 --insecure
```

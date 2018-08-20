# Django Task Queue

Прототип веб-сервиса по организации очереди задач.

Функциональность:
1. `task/create_task` -  метод создающий задачу, которая добавляется в очередь, и пользователю возвращается номер задачи.
2. `task/get_info/<int: task_id>` - возвращает статус задачи в формате json {'status:'', 'create_time":'', 'start_time':'', 'time_to_execute':''}.

    Статусы:
    - In Queue -- задача ждёт своей очереди на выполнение;
    - Run -- произошел запуск задачи;
    - Completed -- задача выполнена.
3. Выполнение задачи представляет собой простой python-код (test.py):
    ```python
    import time
    import random
    time.sleep(random.randint(0,10))
    ```

Обратите внимание:
* можно создавать множество задач, но выполняться одновременно должно не более 2.
* результаты записываются в локальную БД.


Класс реализующий воркера `Worker` работает с использованием `asyncio`.

Установка:
============
```
$ pip3 install -r requirements.txt
$ python3 manage.py migrate --run-syncdb
$ python3 manage.py collectstatic
$ python3 manage.py createsuperuser
```

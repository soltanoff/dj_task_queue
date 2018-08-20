from multiprocessing import Lock, Event

MAIN_MUTEX = Lock()
NEW_TASK_EVENT = Event()

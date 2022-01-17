import threading
from .log import *

__threads = {}
THREAD_CLOSE = False

def readfile(path, mode = "r"):
    content = None
    with open(path, mode) as f:
        content = f.read()
    return content

def THREAD_CLOSED():
    return THREAD_CLOSE

def add_thread(function, args, name):
    thread = threading.Thread(target = function, args = args)
    __threads[name] = {"thread": thread, "running": True}
    log("starting thread " + name)
    thread.start()

def send_exit():
    THREAD_CLOSE = True
    for i in __threads.keys():
        log("stopping thread " + i)
        __threads[i]["thread"].join()

    raise SystemExit()

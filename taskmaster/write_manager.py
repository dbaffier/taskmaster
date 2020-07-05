import os
import time
from select import select

from taskmaster.task_error import task_error

def write_manager(launcher):

    while 1: 
        launch = launcher.launch
        data = launch.join()

        fds = list()
        for proc in data.process:
            for fd in data.process[proc].target_fds:
                fds.append(fd)
            if len(fds) > 0:
                try:
                    rfds, wfds, xfds = select(fds, [], [])
                except (ValueError, OSError):
                    logging.info("serv ended")
                    task_error("too much fd")
            for fd in fds:
                if fd in rfds:
                    try:
                        arr = os.read(fd, 1024)
                        if arr:
                           file = data.process[proc].target_fds[fd]
                           try:
                               tmp = os.open(file, os.O_CREAT | os.O_WRONLY |
                                             os.O_APPEND)
                               os.write(tmp, arr)
                               os.close(tmp)
                           except IsADirectoryError:
                               pass
                    except BlockingIOError:
                        pass
        time.sleep(1)

import os
import time
import logging
from select import select

from taskmaster.task_error import task_error

def write_manager(task):

    while 1:
        fds = list()
        for fd in task.fds:
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
                        file = task.prg_fds[fd]
                        try:
                            tmp = os.open(file, os.O_CREAT | os.O_WRONLY |
                                    os.O_APPEND)
                            os.write(tmp, arr)
                            os.close(tmp)
                        except IsADirectoryError:
                            pass
                    if not arr:
                        if fd in task.old_fd:
                            try:
                                i = task.fds.index(fd)
                                task.fds.pop(i)
                                i = task.old_fd.index(fd)
                                task.old_fd.pop(i)
                                os.close(fd)
                            except OSError:
                                pass
                except BlockingIOError:
                    pass
        time.sleep(1)

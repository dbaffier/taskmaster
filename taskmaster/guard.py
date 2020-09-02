# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    guard.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/16 17:18:43 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/29 17:03:04 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import threading
import logging
import os
import time

from taskmaster.helper import watcher, watcher_backoff
from taskmaster.process import Process
from taskmaster.send_mail import reporter
from taskmaster.send_mail import start_reporter

import taskmaster.glob as glob

def clean_io(task, name):
    infd = task.process[name].fds[0]
    outfd = task.process[name].fds[1]
    errfd = task.process[name].fds[2]
    os.close(infd)
    task.old_fd.append(outfd)
    task.old_fd.append(errfd)


def proc_launch_guard(task, proc, name):
    pp = Process(name, proc.parent, proc.retries)
    pp.exec(task.jobs[pp.parent], task)
    task.queue[pp.pid] = name
    task.process[name] = pp
    task.lst_pid.append(pp.pid)

def guardian(task, pid, null):
    for p in task.process:
        if pid == task.process[p].pid:
            task.process[p].status = "UNKNOWN"
            name = task.queue[pid]
            logging.info("Process %s set to UNKNOWN", name)

def guard(task):
    while 1:
        while len(glob.queue_pid) > 1:
            pid = glob.queue_pid[0]
            # print("PID IN GUARD : ", pid)
            try:
                name = task.queue[pid]
                exitcode = glob.queue_pid[1]
                parent = task.process[name].parent
                watcher(task, name)
                watcher_backoff(task, name)
                clean_io(task, name)
                if str(exitcode) not in task.jobs[parent].exitcodes:
                    reporter(name, None)
                if ((str(exitcode) not in task.jobs[parent].exitcodes and  \
                    task.jobs[parent].autorestart == "unexpected")         \
                    or (task.jobs[parent].autorestart == "true"))          \
                    and task.process[name].status == "RUNNING":
                        logging.info("autorestart %s with status %s", name, task.jobs[parent].autorestart)
                        proc_launch_guard(task, task.process[name], name)
                elif task.process[name].status == "RUNNING":
                    task.process[name].status = "EXITED"
                elif task.process[name].status == "STOPPING":
                    task.process[name].status = "STOPPED"
                elif task.process[name].status == "BACKOFF":
                    if task.process[name].retries > 0:
                        task.process[name].retries -= 1
                        logging.info("start %s from backoff", name)
                        proc_launch_guard(task, task.process[name], name)
                    elif task.process[name].retries == 0:
                        logging.info("FATAL in %s", name)
                        task.process[name].status = "FATAL"
            except OSError: 
                t = threading.Thread(target=guardian, args=(task, pid, None))
                t.start()
            except KeyError:
                pass
            glob.queue_pid.pop(0)
            glob.queue_pid.pop(0)
        time.sleep(1)


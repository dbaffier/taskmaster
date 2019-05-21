# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    guard.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/16 17:18:43 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/21 15:05:36 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import threading
import os

from taskmaster.watcher import *
from taskmaster.server import *
from taskmaster.set_status import set_status
from taskmaster.send_mail import reporter


def clean_io(data, name):
    os.close(data.process[name].fds[0])

def child_guard(launcher):

    launch = launcher.launch
    data = launch.join()
    while True:
        try:
            pid = os.waitpid(0, 0)
            print(pid)
            data.queue_pid += pid
        except:
            pass

def guard(launcher):

    launch = launcher.launch
    while 1:
        print("Guard active")
        data = launch.join()
        time.sleep(1)
        while len(data.queue_pid) > 1:
            try:
                print("pid = :", data.queue_pid[0])
                pid = data.queue_pid[0]
                name = data.queue[pid]
                print("name = :", name);
                print("status = ", data.process[name].status);
                exitcode = data.queue_pid[1]
                print(exitcode)
                if exitcode not in data.process[name].parent.exitcodes:
                    reporter(name, None)
                watcher(data, name)
                watcher_backoff(data, name)
                set_status(data, name, exitcode)
            except KeyError:
                print("Key Error")
                pass
            data.queue_pid.pop(0)
            data.queue_pid.pop(0)
        time.sleep(1)


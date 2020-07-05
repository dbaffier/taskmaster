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

from taskmaster.watcher import *
from taskmaster.server import *
from taskmaster.set_status import set_status
from taskmaster.send_mail import reporter
from taskmaster.send_mail import start_reporter


def clean_io(data, name):
    os.close(data.process[name].fds[0])

def child_guard(launcher):

    while True:
        launch = launcher.launch
        try:
            data = launch.join()
            pid = os.waitpid(0, 0)
            print(pid)
            data.queue_pid += pid
        except:
            pass

def guard(launcher):

    while 1:
        launch = launcher.launch
        data = launch.join()
        while len(data.queue_pid) > 1:
            print(data.queue_pid)
            try:
                pid = data.queue_pid[0]
                name = data.queue[pid]
                exitcode = data.queue_pid[1]
                if str(exitcode) not in data.process[name].parent.exitcodes:
                    reporter(name, None)
                watcher(data, name)
                watcher_backoff(data, name)
                set_status(data, name, exitcode)
            except KeyError:
                logging.info("Error in guard\n")
            data.queue_pid.pop(0)
            data.queue_pid.pop(0)
        time.sleep(1)


# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    process.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/05 18:09:09 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/28 19:01:09 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import configparser
import time
import signal

from taskmaster.helper import task_error
from taskmaster.job import *

class Process:
    def __init__(self, name, job, retries):
        self.name = name
        self.target_fds = dict()
        self.pid = "Not started"
        self.fds = []
        self.status = "STOPPED"
        self.retries = retries
        self.parent = job
        self.time = 0

    def exec(self, job, task):
        read_in, write_in = os.pipe()
        read_out, write_out = os.pipe()
        read_err, write_err = os.pipe()
        try:
            self.pid = os.fork()
        except BlockingIOError:
            task_error("Fork failed")
        if self.pid == 0:
            signal.signal(signal.SIGCHLD, signal.SIG_DFL)
            os.dup2(read_in, sys.stdin.fileno())
            os.dup2(write_out, sys.stdout.fileno())
            os.dup2(write_err, sys.stderr.fileno())
            os.close(write_in)
            os.close(read_out)
            os.close(read_err)
            job.conf_apply()
            try:
                os.execve(job.command[0], job.command, os.environ)
            except:
                sys.exit(1)
        elif self.pid > 0:
            self.fds.append(write_in)
            self.fds.append(read_out)
            self.fds.append(read_err)

            task.fds.append(read_out)
            task.fds.append(read_err)

            task.prg_fds[read_out] = job.stdout
            task.prg_fds[read_err] = job.stderr

            os.close(read_in)
            os.close(write_out)
            os.close(write_err)
            
            if job.startsecs > 0:
                self.status = "STARTING"
            elif job.startretries > self.retries:
                self.status = "BACKOFF"
            else:
                self.status = "RUNNING"
            self.time = time.time()
    
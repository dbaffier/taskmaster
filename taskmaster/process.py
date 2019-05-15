# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    process.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/05 18:09:09 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/13 21:28:12 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import configparser

from taskmaster.launcher import *
from taskmaster.task_error import *
from taskmaster.job import *

class Process:
    def __init__(self, job, launcher):
        self.target_fds = list()
        self.pid = "Not started"
        self.fds = list()
        self.status = "STOPPED"

    def exec(self, job, launcher):
        read_in, write_in = os.pipe()
        read_out, write_out = os.pipe()
        read_err, write_err = os.pipe()
        try:
            self.pid = os.fork()
        except BlockingIOError:
            task_error("Fork failed")
        if self.pid == 0:
            os.dup2(read_in, 0)
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
            self.target_fds.append(read_out)
            self.target_fds.append(read_err)
            self.fds.append(write_in)
            self.fds.append(read_out)
            self.fds.append(read_err)
            os.close(read_in)
            os.close(write_out)
            os.close(write_err)

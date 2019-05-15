# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    launcher.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/06 09:29:22 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/15 17:23:19 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging

from taskmaster.job import *
from taskmaster.process import *
from taskmaster.io_read import *

def launcher(cfg, section):
    launcher = Launcher()
    for name in section:
        if name in launcher.jobs:
            pass
        else:
            job = Job(cfg, name);
            launcher.jobs[name] = job
            launcher.launch_loop(launcher, job, job.autostart, name)
    return launcher

class Launcher:
    def __init__(self):
        self.jobs = dict()
        self.process = dict()
        self.queue = dict()
        self.lst_pid = list()
 #       io_transfer(job, proc)


    def launch_loop(self, launcher, job, ok, name):
        n = 0
        proc = Process(job, launcher)
        if ok == "true" and job.command:
            while n < job.numprocs:
                if job.numprocs > 1:
                    process_cmd = name[8:] + "_" + str(n)
                else:
                    process_cmd = name[8:]
                logging.info("start %s", process_cmd)
                proc.exec(job, launcher)
                launcher.queue[proc.pid] = process_cmd
                launcher.process[process_cmd] = proc
                launcher.lst_pid.append(proc.pid)
                n += 1
        elif ok == "false" and job.command:
            while n < job.numprocs:
                if job.numprocs > 1:
                    process_cmd = name[8:] + "_" + str(n)
                else:
                    process_cmd = name[8:]
                launcher.process[process_cmd] = proc
                n += 1

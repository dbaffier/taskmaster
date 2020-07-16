# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    launcher.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/06 09:29:22 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/29 17:35:51 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging
import threading
import copy

from taskmaster.job import *
from taskmaster.process import *
from taskmaster.io_read import *


def launcher(server, task, cfg, section, old_prg):
    if old_prg:
        for name in old_prg:
            if name not in section:
                for proc in task.process:
                    if task.process[proc].parent == name:
                        server.launch_kill(task.process[proc].pid)    
    for name in section:
        if name in task.jobs:
            new_job = Job(cfg, name)
            prevjob = task.jobs[name]
            launch_again(server, task, new_job, prevjob, name)
        else:
            job = Job(cfg, name)
            task.jobs[name] = job
            launch_loop(task, job, job.autostart, name)
    return launcher

def launch_loop(task, job, ok, name):
    n = 0
    if ok == "true" and job.command:
        while n < job.numprocs:
            if job.numprocs > 1:
                process_cmd = name[8:] + "_" + str(n)
            else:
                process_cmd = name[8:]
            logging.info("start %s", process_cmd)
            # print("Launching job : ", process_cmd)
            proc = Process(process_cmd, name, copy.copy(job.startretries))
            proc.exec(job, task)
            proc.name = process_cmd
            task.queue[proc.pid] = process_cmd
            task.process[process_cmd] = proc
            task.lst_pid.append(proc.pid)
            n += 1
    elif ok == "false" and job.command:
        while n < job.numprocs:
            if job.numprocs > 1:
                process_cmd = name[8:] + "_" + str(n)
            else:
                process_cmd = name[8:]
            proc = Process(process_cmd, name, copy.copy(job.startretries))
            task.process[process_cmd] = proc
            n += 1

def launch_again(server, task, job, prevjob, name):
    numprocs = prevjob.numprocs
    # print("Launch again")
    # print("condition", job == prevjob)
    if job == prevjob:
        # print("Enter in if cmd etc are the same")
        if numprocs < job.numprocs:
            # print("Enter if new proc is superior\n")
            diff = numprocs
            while diff != job.numprocs:
                process_cmd = name[8:] + "_" + str(diff)
                logging.info("start %s", process_cmd)
                proc = Process(process_cmd, name, copy.copy(job.startretries))
                proc.exec(job)
                proc.name = process_cmd
                task.queue[proc.pid] = process_cmd
                task.process[process_cmd] = proc
                task.lst_pid.append(proc.pid)
                diff += 1
        if job != prevjob:
            # print("Enter if numprocs is differents")
            task.jobs.pop(name, None)
            task.jobs[name] = job
    else:
        # print("Enter if cmd are different")
        task.jobs.pop(name, None)
        task.jobs[name] = job
        for namep in task.process:
            # print("IN KILL : ", task.process[namep].parent, name)
            if task.process[namep].parent == name:
                # print("KILL : ", task.process[namep].pid)
                server.launch_kill(task.process[namep].pid)
        if job.autostart == "true":
            # print("Auto start on ")
            while numprocs > 0:
                if job.numprocs > 1:
                    process_cmd = name[8:] + "_" + str(numprocs)
                else:
                    process_cmd = name[8:]
                logging.info("Start %s", process_cmd)
                proc = Process(process_cmd, name, copy.copy(job.startretries))
                proc.name = process_cmd
                server.launch_proc(proc, process_cmd)
                numprocs -= 1
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    task_error.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/03 13:26:33 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/04 13:19:03 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import time
import configparser

def task_error(msg):
    print("Taskmaster: " + msg, file=sys.stderr)
    sys.exit(1)

def watcher(data, proc):
    timing = time.time()
    secs = timing - data.process[proc].time
    if secs >= data.jobs[data.process[proc].parent].startsecs \
            and (data.process[proc].status == "STARTING" \
            or data.process[proc].status == "BACKOFF"):
            data.process[proc].status = "RUNNING"

def watcher_backoff(data, proc):
    timing = time.time()
    secs = timing - data.process[proc].time
    if secs < data.jobs[data.process[proc].parent].startsecs           \
            and (data.process[proc].status == "STARTING"    \
            or data.process[proc].status == "BACKOFF"):
                data.process[proc].status = "BACKOFF"

def extract_job(lst):
    prog = list()
    for sections in lst:
        if sections[0:7] == "program":
            prog.append(sections)
    return (prog)

def cleaner(task, lst_job):

    lst = list()

    for name in task.process:
        if "program:" + name.split('_')[0] not in lst_job  \
            and  (task.process[name].status == "STOPPED" or \
            task.process[name].status == "EXITED" or \
            task.process[name].status == "FATAL" or \
            task.process[name].status == "UNKNOWN"):
                lst.append(name)

    for name in lst:
        task.process.pop(name, None)    
    
    rmv = list()

    for name in task.jobs:
        n = 0
        for namep in task.process:
            if task.process[namep].parent == name:
                n += 1
        if n == 0:
            rmv.append(name)
    for name in rmv:
        task.jobs.pop(name, None)

def get_status(data, proc):
    status = list()
    maxlen = 0
    pidmax = 0

    for p in proc:
        if len(p) > maxlen:
            maxlen = len(p) 
        if len(str(proc[p].pid)) > pidmax:
            pidmax = len(str(proc[p].pid))

    maxlen += 2
    pidmax += 2
    a = maxlen - 7 if maxlen - 7 > 2 else 2
    if pidmax - 3 < 0:
        pidmax = 5
    status.append('PID' + ' ' * (pidmax - 3) + 'COMMAND' + ' ' * a + 'STATE' + '\n')        
    for p in proc:
        watcher(data, p)
        pidpad = pidmax - len(str(proc[p].pid))
        ppad = maxlen - len(p) if maxlen > 9 else 9 - len(p)
        status.append(str(proc[p].pid) + ' ' * pidpad + p + ' ' * ppad + proc[p].status + '\n')
    return status

def parse_prog(sections):
    prog_list = list()
    for prog in sections:
        if prog[:7] == "program":
            prog_list.append(prog)
    return (prog_list)

def proc_max(prog_list, config):
    count = 0
    for prog in prog_list:
        try:
            count += int(config.get(prog, "numprocs"))
            if (count > 200):
                return True
        except configparser.NoOptionError:
            count += 1

    return False
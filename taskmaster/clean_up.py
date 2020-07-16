# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    clean_up.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/20 21:26:11 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/29 15:56:16 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

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

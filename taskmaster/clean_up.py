# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    clean_up.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/20 21:26:11 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/21 15:39:19 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def extract_job(lst):
    prog = list()
    for sections in lst:
        if sections[0:7] == "program":
            prog.append(sections)
    return (prog)

def cleaner(data):

    lst = list()

    for name in data.process:

        if "program:" + name.split('_')[0] not in list_progs \
            and  (data.process[name].status == "STOPPED" or \
            data.process[name].status == "EXITED" or \
            data.process[name].status == "FATAL" or \
            data.process[name].status == "UNKNOWN"):
                lst.append(name)

    for name in lst:
        data.process.pop(name, None)

    lst = list()

    for name_prog in data.jobs:

        num_process = 0
        for name_process in data.process:
            if data.process[name_process].father == name_prog:
                num_process += 1
        if num_process == 0:
            lst.append(name_prog)

    for name in lst:
        data.jobs.pop(name, None)

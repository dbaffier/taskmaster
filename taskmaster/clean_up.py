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

def cleaner(data, lst_job):

    lst = list()

    for name in data.process:
        print(name)

        if "program:" + name.split('_')[0] not in lst_job  \
            and  (data.process[name].status == "STOPPED" or \
            data.process[name].status == "EXITED" or \
            data.process[name].status == "FATAL" or \
            data.process[name].status == "UNKNOWN"):
                lst.append(name)

    for name in lst:
        data.process.pop(name, None)

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    set_status.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/20 15:44:28 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/20 16:56:23 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from taskmaster.server import *

def set_status(data, name, exitcode):
    parent = data.process[name].parent
    if ((str(exitcode) not in parent.exitcodes and  \
        parent.autorestart == "unexpected")         \
        or (parent.autorestart == "true"))          \
        and data.process[name].status == "RUNNING":
            logging.info("autorestart %s with status %s", name, parent.autorestart)
            proc_launch(data, data.process[name], name)
    if data.process[name].status == "RUNNING":
        data.process[name].status = "EXITED"
    elif data.process[name].status == "STOPPING":
        data.process[name].status = "STOPPED"
    elif data.process[name].status == "BACKOFF":
        if data.process[name].retries > 0:
            data.process[name].retries -= 1
            logging.info("start %s from backoff", name)
            proc_launch(data, data.process[name], name)
        elif data.process[name].retries == 0:
            # report
            logging.info("FATAL in %s", name)
            data.process[name].status = "FATAL"


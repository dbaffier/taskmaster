# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    watcher.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/16 18:24:01 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/20 19:35:19 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time

def watcher(data, proc):
    timing = time.time()
    secs = timing - data.process[proc].time
    if secs >= data.process[proc].parent.startsecs \
            and data.process[proc].status == "STARTING" \
            or data.process[proc].status == "BACKOFF":
            data.process[proc].status = "RUNNING"

def watcher_backoff(data, proc):
    timing = time.time()
    secs = timing - data.process[proc].time
    if secs < data.process[proc].parent.startsecs \
            and data.process[proc].status == "STARTING" \
            or data.process[proc].status == "BACKOFF":
            data.process[proc].status = "BACKOFF"

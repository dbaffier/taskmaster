# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    kill.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/16 09:10:41 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/16 14:17:29 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import signal
import time

def get_signal(stopsignal):
    signals = ["TERM", signal.SIGTERM, "HUP", signal.SIGHUP, "INT", signal.SIGINT, \
        "QUIT", signal.SIGQUIT, "KILL", signal.SIGKILL, "USR1", signal.SIGUSR1, \
        "USR2", signal.SIGUSR2] 

    a = 0
    for i in signals:
        
        if a == 1:
            return int(i)
        if stopsignal == i:
            a = 1

def kill(launch, pid):
    if pid == "Not started":
        return 1
    data = launch.join()
    name = data.queue[pid]
    proc = data.process[name]
    if proc.status != "STARTING" and proc.status != "RUNNING" \
        and proc.status != "BACKOFF":
        return 1
    if proc.status == "STOPPING":
        proc.status = "STOPPED"
    parent = proc.parent
    sig = get_signal(parent.stopsignal)
    proc.status = "STOPPING"
    try:
        os.kill(int(pid), sig)
    except ProcessLookupError:
        return 1
    time.sleep(parent.stopwaitsecs)
    try:
        if proc.status != "STOPPED":
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    except KeyError:
        pass

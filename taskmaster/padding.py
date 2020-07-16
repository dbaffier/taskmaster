# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    padding.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/05 18:04:25 by dbaffier          #+#    #+#              #
#    Updated: 2020/07/05 18:04:26 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from taskmaster.watcher import watcher, watcher_backoff


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
    status.append('PID' + ' ' * (pidmax - 3) + 'COMMAND' + ' ' * a + 'STATE' + '\n')
    for p in proc:
        # watcher(data, p)
        # watcher_backoff(data, p)
        pidpad = pidmax - len(str(proc[p].pid))
        ppad = maxlen - len(p) if maxlen - len(p) > 9 else 9 - len(p)
        status.append(str(proc[p].pid) + ' ' * pidpad + p + ' ' * ppad + proc[p].status + '\n')
    return status


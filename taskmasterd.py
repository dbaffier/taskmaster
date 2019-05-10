# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmaster.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/01 15:17:25 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/10 16:50:38 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os

from taskmaster.task_error import *
from taskmaster.server import *
from taskmaster.job import *

#def main();

if __name__ == '__main__':
    if len(sys.argv) < 2:
       task_error("Usage: <config_file>")
    try:
        config_file = os.path.abspath(sys.argv[1])
    except FileNotFoundError:
        task_error("Config file not found")
    print(config_file)
    server = Server(config_file);
    server.launch_job(server.cfg, server.job)
    try:
        while True:
            thread = 0
            server.c, server.addr = server.ss.accept()
            server.c.recv(1024)
            server.c.send(str(num_threads).encode('utf-7'))
            server.c.auth(thread)
            thread += 1
        server.ss.close()
    except InterruptedError:
        task_error("Interrupted syscall")

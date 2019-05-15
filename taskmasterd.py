# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmaster.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/01 15:17:25 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/15 16:36:18 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
import logging

from taskmaster.task_error import *
from taskmaster.server import *
from taskmaster.job import *
from taskmaster.daemon import Daemon

#def main();

if __name__ == '__main__':
    if len(sys.argv) < 2:
       task_error("Usage: <config_file>")
    try:
        config_file = os.path.abspath(sys.argv[1])
    except FileNotFoundError:
        task_error("Config file not found")
 #   daemon = Daemon('/tmp/.taskmaster_pid')
  #  daemon.start()
    logging.basicConfig(format='%(asctime)s , %(levelname)s : %(message)s', \
        filename='/tmp/.taskmasterdlog', level=logging.INFO)
    server = Server(config_file);
    server.launch_job(server.cfg, server.job)
    server.launch_server()


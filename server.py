# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmaster.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/01 15:17:25 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/29 17:35:48 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
import logging

from taskmaster.helper import task_error
from taskmaster.server import *
from taskmaster.job import *
from taskmaster.daemon import Daemon
import taskmaster.glob as glob


if __name__ == '__main__':
    if len(sys.argv) < 2:
        task_error("Usage: <config_file>")
    try:
        config_file = os.path.abspath(sys.argv[1])
    except FileNotFoundError:
        task_error("Config file not found")
    daemon = Daemon('/tmp/.taskmaster_pid')
    daemon.start()
    logging.basicConfig(format='%(asctime)s , %(levelname)s : %(message)s',
                        filename='/tmp/.taskmasterlog', level=logging.INFO)
    glob.init()
    server = Server(config_file)
    server.launch_guard()
    server.launch_wr_manager()
    server.launch_job(server.cfg, server.job, None)
    server.launch_server()

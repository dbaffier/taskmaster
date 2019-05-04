# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/03 14:03:51 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/04 17:30:19 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
import configparser
import socket
import signal

from taskmaster.task_error import *
from taskmaster.parse_prog import *
from taskmaster.drop_privilege import *

class Server:
    def __init__(self, path):
        self.cfg = configparser.ConfigParser()
        try:
            self.cfg.read(path)
        except configparser.DuplicateSectionError:
            task_error("Dupplicate section on config file")
        self.prog = parse_prog(self.cfg.sections())
        if proc_max(self.prog, self.cfg):
            task_error("numprocs number is too high")
        try:
            self.psswd = self.cfg.get('server', 'password')
        except:
            self.psswd = None
        try:
            self.port = int(self.cfg.get('server', 'port'))
        except configparser.NoSectionError:
            task_error("No port given in server field")
        except configparser.DuplicateSectionError:
            task_error("Dupplicate section on server")
        drop_privileges()
        self.pid = os.getpid()
        self.host = ''
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.ss.bind((self.host, self.port))
        except:
            task_error("Socket already used")
        self.ss.listen(5)

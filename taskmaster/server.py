# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/03 14:03:51 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/03 15:23:49 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
import configparser

import taskmaster.task_error import *

class Server:
    def __init__(self, path):
        self.cfg = configparser.ConfigParser()
        try:
            self.cfg.read(path)
        except configparser.DuplicateSectionError:
            task_error("Dupplicate section on config file")
        try:
            self.cfg.psswd = self.cfg.get('server', 'password')
        except:
            self.cfg.psswd = None
        try:
            self.cfg.port = int(self.cfg.get('server', 'port'))
        except cfg.NoSectionError:
            task_error("No port given in server field")
        except cfg.DuplicateSectionError:
            task_error("Dupplicate section on server")

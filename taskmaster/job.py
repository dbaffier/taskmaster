    # **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    process.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/05 16:21:07 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/17 21:24:41 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import configparser

from taskmaster.task_error import *

class Job:
    def __init__(self, cfg, name):
        try:
            self.command = cfg.get(name, "command")
        except configparser.NoOptionError:
            self.command = None
        try:
            self.numprocs = int(cfg.get(name, "numprocs"))
        except configparser.NoOptionError:
            self.numprocs = 1
        try:
            self.autostart = cfg.get(name, "autostart")
        except configparser.NoOptionError:
            self.autostart = True
        try:
            self.autorestart = cfg.get(name, "autorestart")
        except configparser.NoOptionError:
            self.autorestart = "unexpected"
        try:
            self.exitcodes = cfg.get(name, "exitcodes").split(',')
        except configparser.NoOptionError:
            self.exitcodes = list()
            self.exitcodes.append('0')
        try:
            self.startsecs = int(cfg.get(name, "startsecs"))
        except configparser.NoOptionError:
            self.startsecs = 1
        try:
            self.startretries = int(cfg.get(name, "startretries"))
        except configparser.NoOptionError:
            self.startretries = 3
        try:
            self.stopsignal = cfg.get(name, "stopsignal")
        except configparser.NoOptionError:
            self.stopsignal = "TERM"
        try:
            self.stopwaitsecs = int(cfg.get(name, "stopwaitsecs"))
        except configparser.NoOptionError:
            self.stopwaitsecs = 10
        try:
            self.stdout = cfg.get(name, "stdout_logfile")
        except configparser.NoOptionError:
            self.stdout = "/dev/null"
        try:
            self.stderr = cfg.get(name, "stderr_logfile")
        except configparser.NoOptionError:
            self.stderr = "/dev/null"
        try:
            self.env = cfg.get(name, "environment")
        except configparser.NoOptionError:
            self.env = None
        try:
            self.directory = cfg.get(name, "directory")
        except:
            self.directory = None
        try:
            self.umask = cfg.get(name, "umask")
        except:
            self.umask = None

    def conf_apply(self):
        if self.directory:
            try:
                os.chdir(self.directory)
            except (OSError, FileNotFoundError, PermissionError):
                sys.exit(1)
        if self.umask:
            os.umask(int(self.umask))
        if self.env:
            list_env = self.env.split(',')
            for i in list_env:
                j = i.split('=')
                os.environ[j[0]] = j[1]
        if self.command:
            self.command = self.command.split(' ')

    def __eq__(self, other):
        return isinstance(other, Job) and self.command == other.command    \
        and self.stdout == other.stdout and self.stderr == other.stderr and self.env == other.env \
        and self.directory == other.directory and self.umask == other.umask

    def __ne__(self, other):
        return isinstance(other, Job) and self.autorestart != other.autorestart or self.exitcodes != other.exitcodes           \
                or self.startsecs != other.startsecs or self.startretries != other.startretries     \
                or self.stopsignal != other.stopsignal or self.stopwaitsecs != other.stopwaitsecs   \
                or self.numprocs != other.numprocs

#!/usr/bin/env python3

import sys
import os
import configparser
import socket
import signal
import threading

from threading import Thread
from taskmaster.task_error import *
from taskmaster.parse_prog import *
from taskmaster.drop_privilege import *
from taskmaster.launcher import launcher
from taskmaster.job import *
from taskmaster.process import *
from taskmaster.auth import *

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

class Server:
    def __init__(self, path):
        self.cfg = configparser.ConfigParser()
        try:
            self.cfg.read(path)
        except configparser.DuplicateSectionError:
            task_error("Dupplicate section on config file")
        self.job = parse_prog(self.cfg.sections())
        if proc_max(self.job, self.cfg):
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
            self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ss.bind((self.host, self.port))
        except:
            task_error("Socket already used")
        self.ss.listen(5)
 #       signal.signal(signal.SIGCHLD, end_chld)
    def launch_job(self, cfg, section):
        self.launch = ThreadWithReturnValue(target=launcher, args=(cfg, section))
        self.launch.start()
 #       t = threading.Thread(target=launcher, args=(cfg, section))
  #      t.start()
     #   launcher(cfg, section)
    def launch_auth(self, thread):
        thread = threading.Thread(target=auth, args=(self.c, self.addr, self,
                                                     thread))
        thread.start()
    def launch_server(self):
        try:
            while True:
                thread = 0
                self.c, self.addr = self.ss.accept()
                self.c.recv(1024)
                self.c.send(str(thread).encode('utf-7'))
                self.launch_auth(thread)
                thread += 1
            self.ss.close()
        except InterruptedError:
            task_error("Interrupted syscall")


#!/usr/bin/env python3 
import sys
import os
import configparser
import socket
import signal
import threading
import time

from threading import Thread
from taskmaster.guard import *
from taskmaster.task_error import *
from taskmaster.parse_prog import *
from taskmaster.drop_privilege import *
from taskmaster.launcher import launcher
from taskmaster.clean_up import extract_job
from taskmaster.job import *
from taskmaster.process import *
from taskmaster.auth import *
from taskmaster.kill import kill
from taskmaster.write_manager import write_manager

def proc_st(self, proc, name_process):
    data = self.launch.join()
    while proc.status != "EXITED" and proc.status != "STOPPED" \
            and proc.status != "FATAL" and proc.status != "UNKNOWN":
        time.sleep(1)
    proc.exec(proc.parent, None)
    data.queue[proc.pid] = name_process
    data.process[name_process] = proc
    data.lst_pid.append(proc.pid)

def proc_launch(data, proc, name):
    proc.exec(proc.parent, None)
    data.queue[proc.pid] = name
    data.process[name] = proc
    data.lst_pid.append(proc.pid)


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
        self.thread = 1
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
        self.lst_job = extract_job(self.cfg.sections())
 #       self.lst_job = list()

    def launch_job(self, cfg, section):
        self.launch = ThreadWithReturnValue(target=launcher, args=(cfg, section))
        self.launch.start()

    def launch_guard(self):
        thread = threading.Thread(target=guard, args=(self,))
        thread.start()

    def launch_child_guard(self):
        thread = threading.Thread(target=child_guard, args=(self,))
        thread.start()

    def launch_auth(self, thread):
        thread = threading.Thread(target=auth, args=(self.c, self.addr, self,
                                                     thread))
        thread.start()
    def launch_kill(self, pid):
        thread = threading.Thread(target=kill, args=(self.launch, pid))
        thread.start()

    def launch_proc(self, proc, data, name):
        thread = threading.Thread(target=proc_st, args=(self, proc, name))
        thread.start()
    
    def launch_wr_manager(self):
        thread = threading.Thread(target=write_manager, args=(self,))
        thread.start()

    def launch_server(self):
        try:
            while True:
                self.c, self.addr = self.ss.accept()
                self.c.recv(1024)
                self.c.send(str(self.thread).encode('utf-7'))
                self.launch_auth(self.thread)
                self.thread += 1
            self.ss.close()
        except InterruptedError:
            task_error("Interrupted syscall")

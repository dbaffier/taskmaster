#!/usr/bin/env python3 
import sys
import os
import configparser
import socket
import signal
import threading
import time

import taskmaster.glob as glob
from threading import Thread
from taskmaster.guard import *
from taskmaster.helper import task_error, extract_job, parse_prog, proc_max
from taskmaster.drop_privilege import *
from taskmaster.launcher import launcher
from taskmaster.job import *
from taskmaster.process import *
from taskmaster.auth import *
from taskmaster.kill import kill
from taskmaster.write_manager import write_manager
from taskmaster.task import Task

def proc_st(task, proc, name):
    while proc.status != "EXITED" and proc.status != "STOPPED" \
            and proc.status != "FATAL" and proc.status != "UNKNOWN":
        time.sleep(1)
    pp = Process(name, proc.parent, proc.retries)
    pp.exec(task.jobs[pp.parent], task)
    task.queue[pp.pid] = name
    task.process[name] = pp
    task.lst_pid.append(pp.pid)

def child_guard(number, frame):
    while True:
        try:
            pid = os.waitpid(-1, os.WNOHANG)
            glob.queue_pid += pid
        except:
            break

class Server:
    def __init__(self, path):
        self.cfg = configparser.ConfigParser()
        self.thread = 1
        try:
            self.cfg.read(path)
        except configparser.DuplicateSectionError:
            task_error("Dupplicate section on config file")

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
        self.job = parse_prog(self.cfg.sections())
        if proc_max(self.job, self.cfg):
            task_error("numprocs number is too high")
        self.task = Task()
        signal.signal(signal.SIGCHLD, child_guard)


    def launch_job(self, cfg, section, old_prog):
        thread = threading.Thread(target=launcher, args=(self, self.task, cfg, section, old_prog))
        thread.start()

    def launch_guard(self):
        thread = threading.Thread(target=guard, args=(self.task,))
        thread.start()

    def launch_auth(self, thread):
        thread = threading.Thread(target=auth, args=(self.c, self.addr, self))
        thread.start()
    def launch_kill(self, pid):
        thread = threading.Thread(target=kill, args=(self.task, pid))
        thread.start()

    def launch_proc(self, proc, name):
        thread = threading.Thread(target=proc_st, args=(self.task, proc, name))
        thread.start()
    
    def launch_wr_manager(self):
        thread = threading.Thread(target=write_manager, args=(self.task,))
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

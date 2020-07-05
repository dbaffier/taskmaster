# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server_get.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/12 15:00:44 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/29 17:56:23 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import sys
import signal
import os
import logging
import configparser
import pprint

from taskmaster.clean_up import *
from taskmaster.parse_prog import proc_max
from taskmaster.launcher import launcher
from taskmaster.parse_prog import *

def status(command, client, server):
    data = server.launch.join()
    for name in data.process:
        prog_name = name[:name.index("_")]
        s = prog_name + ":" + name
        sp = s.ljust(30, ' ') + data.process[name].status + '\n'
        client.send(sp.encode('utf-8'))

def stop(command, client, server):
    data = server.launch.join()
    for cmd in command[1:]:
        try:
            if data.process[cmd].status != "STARTING" and data.process[cmd].status != "RUNNING":
               client.send(("process " + cmd + "isn't running \n").encode('utf-8'))
            else:
                logging.info("stop :%s", cmd)
                server.launch_kill(data.process[cmd].pid)
                client.send(("stopping process " + cmd + "\n").encode('utf-8'))
        except KeyError:
                client.send(("no such process " + cmd + "\n").encode('utf-8'))

def start(command, client, server):
    data = server.launch.join()
    for cmd in command[1:]:
        proc = data.process[cmd]
        try:
            if proc.status != "RUNNING" and proc.status != "STARTING"       \
            and proc.status != "BACKOFF":
                name = "program:" + cmd.split('_')[0]
                logging.info("Start %s", cmd)
                server.launch_proc(data.process[cmd], server.launch, cmd)
                client.send(("process "+ cmd + " is starting\n").encode("utf-8"))
            else:
                client.send(("taskmasterd: Process "+ cmd +" always running\n").encode("utf-8"))
        except KeyError:
            client.send(("taskmasterd: No such program " + cmd).encode("utf-8"))

def restart(command, client, server):
    data = server.launch.join()
    for cmd in command[1:]:
        proc = data.process[cmd]
        try:
            if proc.status != "STARTING" and proc.status != "RUNNING"       \
                and proc.status != "BACKOFF":
                client.send(("process " + cmd + "isn't running \n").encode('utf-8'))
            else:
                server.launch_kill(data.process[cmd].pid)
                client.send(("stopping process " + cmd + "\n").encode('utf-8'))
            name = "program:" + cmd.split('_')[0]
            logging.info("Restarting %s", cmd)
            server.launch_proc(data.process[cmd], server.launch, cmd)
            client.send(("process "+ cmd + " is starting\n").encode("utf-8"))
        except KeyError:
            client.send(("taskmasterd: No such program " + cmd).encode("utf-8"))

def log(command, client, server):
    try:
        file = open("/tmp/.taskmasterlog", "r")
        for line in file:
            client.send(line.encode('utf-8'))
        file.close()
    except FileNotFoundError:
            client.send(("no log file").encode("utf-8"))

def reload(command, client, server):
    logging.info("reload with config : %s", command[1])
    server.cfg = configparser.ConfigParser()
    data = server.launch.join()
    try:
        # cleaner(data, server.lst_job)
        if os.path.isfile(command[1]) == False:
              raise KeyError
        path_config = os.path.abspath(command[1])
        server.cfg.read(path_config)
        server.job = parse_prog(server.cfg.sections())
        old_list_progs = server.lst_job
        server.lst_job = extract_job(server.cfg.sections())
        if proc_max(server.lst_job, server.cfg):
            client.send("submit another config")
        else:
            server.launch_job(server.cfg, server.job)
    except KeyError :
        client.send(("No such file " + command[1]).encode("utf-8"))

def shutdown(command, client, server):
    logging.info("taskmaster is being shutdown")
    data = server.launch.join()
    for proc in data.process:
        server.launch_kill(data.process[proc].pid)
    client.send(("taskmaster is shutdown").encode('utf-8'))
    logging.info("Taskmaster ended")
    os.kill(server.pid, signal.SIGKILL)
        

def server_get(client, addr, server):
    func = {'status': status, 'stop': stop, 'start': start, 'restart': restart,
            'log': log, 'reload': reload, 'shutdown': shutdown}
    while True:
        rec = client.recv(2048)
        dec = rec.decode('utf-8')
        cmd = dec.split(' ')
        if cmd[0] == 'exit' or cmd[0] == 'quit' or not rec:
            break
        for f in func:
            if cmd[0] == f:
                func[f](cmd, client, server)
        client.send(("\r").encode('utf-8'))


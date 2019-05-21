# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server_get.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/12 15:00:44 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/21 15:06:37 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import sys
import os
import logging

from taskmaster.clean_up import cleaner

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
                client.send("process is not running\n".encode('utf-8'))
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
                server.launch_proc(data.process[cmd], server.launch)
                client.send(("process "+ cmd + " is starting\n").encode("utf-8"))
            else:
                client.send(("taskmasterd: Process "+ cmd +" always running\n").encode("utf-8"))
        except KeyError:
            client.send(("taskmasterd: No such program " + cmd).encode("utf-8"))

def reload(command, client, server):
    data = server.launch.join()
    cleaner(data)
    server.cfg = configparser.ConfigParser()
    try:
        if os.path.isfile(command[1]) == False:
            raise KeyError
        path_cfg = os.path.isfile(command[1])
        server.cfg.read(path_cfg)
        # data.old_lst = current_lst
    except:
        pass


def server_get(client, addr, server):
    func = {'status': status, 'stop': stop, 'start': start}
    while True:
        rec = client.recv(2048)
        dec = rec.decode('utf-8')
        cmd = dec.split(' ')
        data = server.launch.join()
        if cmd[0] == 'exit' or cmd[0] == 'quit' or not rec:
            break
        for f in func:
            if cmd[0] == f:
                func[f](cmd, client, server)
        client.send(("\r").encode('utf-8'))


# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmasterctl.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/09 13:09:30 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/14 09:49:52 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import socket
import os
import configparser
import readline
import signal

from taskmaster.auth import *
from taskmaster.welcome import *

def exit_ctl(n, f):
    sys.exit(1)

def ctl_start(host, port):
    # sigint maybe
    signal.signal(signal.SIGINT, exit_ctl)
    sock = socket.socket()
    sock.connect((host, port))
    sock.send(("\r\n").encode('utf-8'))
    cnum = (sock.recv(1024)).decode('utf-8')

    #error
    welcome(host, port)
    i = 3
    while True:
        auth_entries(sock, i)

if __name__ == '__main__':
    try:
        config_file = os.path.abspath(sys.argv[1])
    except:
        sys.stderr.write("taskmasterctl: no such file")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        host = config.get('server', 'host')
    except:
        sys.stderr.write("taskmasterctl: host is missing")
        sys.exit(1)
    try:
        port = int(config.get('server', 'port'))
    except:
        sys.stderr.write("taskmasterctl: host is missing")
        sys.exit(1)
    ctl_start(host, port)

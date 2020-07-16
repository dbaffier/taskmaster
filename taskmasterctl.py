# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmasterctl.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/09 13:09:30 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/29 17:35:44 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import socket
import os
import configparser
import readline
import signal
import termios
import struct
import fcntl

from taskmaster.auth import *
from taskmaster.welcome import *

def exit_ctl(n, f):
    sys.exit(1)

def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

def ctl_start(host, port):
    signal.signal(signal.SIGINT, exit_ctl)
    sock = socket.socket()
    sock.connect((host, port))
    sock.send(("\r\n").encode('utf-8'))
    cnum = (sock.recv(1024)).decode('utf-8')
    welcome(host, port, cnum)
    i = 3
    while True:
        auth_entries(sock, i)

if __name__ == '__main__':
    try:
        config_file = os.path.abspath(sys.argv[1])
    except:
        sys.stderr.write("taskmasterctl: no such file")
        sys.exit(1)
    set_winsize(1, 20, 20)
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

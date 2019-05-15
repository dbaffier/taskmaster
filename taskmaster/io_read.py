# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    io_read.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/08 15:59:06 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/11 16:42:40 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

from taskmaster.process import *
from select import select

def write_to(fd, data):
    while data:
        n = os.write(fd, data)
        data = data[n:]

def io_transfer(job, proc):

    client_attach = os.open("/tmp/client_attach", os.O_CREAT | os.O_RDONLY)
    file_out = os.open(job.stdout, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
    file_err = os.open(job.stderr, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
    
    while True:
        fds = [client_attach, proc.fds[1], proc.fds[2]]

        rfds, wfds, efds = select(fds, [], [])
        
        if proc.fds[1] in rfds:
            try:
                data = os.read(proc.fds[1], 1024)
            except BlockingIOError:
                pass
            if data:
                data = data.decode('utf-8')
                write_to(file_out, data.encode('utf-8'))
        if proc.fds[2] in rfds:
            try:
                data = os.read(proc.fds[2], 1024)
            except BlockingIOError:
                pass
            if data:
                data = data.decode('utf-8')
                write_to(file_err, data.encode('utf-8'))

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server_get.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/12 15:00:44 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/15 18:28:06 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import sys
import os

def status(client, server):
    data = server.launch.join()
    for name in data.process:
        prog_name = name.split('_')[0]
        s = prog_name + ":" + name
        sp = s.ljust(30, ' ') + "\n"
        client.send(sp.encode('utf-8'))


def server_get(client, addr, server):
    func = {'status': status }
    while True:
        rec = client.recv(2048)
        dec = rec.decode('utf-8')
        cmd = dec.split(' ')
        if cmd[0] == 'exit' or cmd[0] == 'quit' or not rec:
            break
        for f in func:
            if cmd[0] == f:
                func[f](client, server)
        client.send(("\r").encode('utf-8'))


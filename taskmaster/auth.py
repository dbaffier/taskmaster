# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/06 13:35:13 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/10 16:24:33 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket

def auth(client, addr, server, thread):
    retries = 0
    while retries < 3:
        passwd = (client.recv(1024)).decode('utf-8')
        if passwd == server.password:
            client.send(('Success').encode('utf-8'))
            retries = 3
            server_get(client, addr, server)
            # finish laster
        retries += 1
        if retries == 3:
            client.send(("Too many request").encode('utf-8'))
            break
        elif retries < 3:
            client.send("Wrong password").encode('utf-8'))
    thread -= 1
    client.close()

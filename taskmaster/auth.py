# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/06 13:35:13 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/16 09:32:22 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import sys
import getpass
import time
import os

from taskmaster.server_get import *
from taskmaster.builtin import builtin_ok

def print_delay(c):
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(0.03)

def print_delay_fast(c):
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(0.002)


def wait_as(sock):
    while True:
        try:
            reply = sock.recv(2048).decode('utf-8')
        except ConnectionResetError:
            raise ConnectionResetError
        if len(reply) > 0 and reply != '\r':
            print(reply.rstrip("\n\r"))
        if "\r" in reply:
            break

def prompt(sock):
    while True: 
        try:
            line = input("taskmaster> ")
            if builtin_ok(line) == True:
                sock.send(line.encode('utf-8'))
                if line == 'exit':
                    break
                try:
                    wait_as(sock)
                except ConnectionResetError:
                    print("Broken connection, exiting")
                    break
            else:
                print("taskmaster:", line, ": command not found")
        except EOFError:
            sys.stdout.write("\n")
            pass

def auth(client, addr, server, thread):
    retries = 0
    while retries < 3:
        passwd = (client.recv(1024)).decode('utf-8')
        if passwd == server.psswd:
            client.send(('Success').encode('utf-8'))
            retries = 3
            server_get(client, addr, server)
        retries += 1
        if retries == 3:
            client.send(("Good bye from Los Santos").encode('utf-8'))
            break
        elif retries < 3:
            client.send(("Wrong password").encode('utf-8'))
    thread -= 1
    client.close()


def auth_entries(sock, i):
    try:
        psswd = getpass.getpass()
        if len(psswd) == 0:
            psswd = "\r\n"
        sock.send(psswd.encode('utf-8'))
        answer =  sock.recv(1024).decode('utf-8')
        if answer == "Success":
            prompt(sock)
            sys.exit(0)
        print(answer)
        if "Santos" in answer:
            sys.exit(1)
    except EOFError:
        i -= 1
        if i == 0:
            print("Too many request, deconnecting")
            sys.exit(1)
        pass

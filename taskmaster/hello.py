# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/06 13:35:13 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/11 17:57:49 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import sys
import getpass
import time
import os

def print_delay(c):
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(0.03)

def print_delay_fast(c):
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(0)

def welcome(host, port):
    print("??????????")
    connect = "Connection is starting  "
    for c in connect:
        print_delay(c)
    wait = "..."
    for c in wait:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.4)
 #   print("\n\n")
    arr = "\033[0;31m################################################################################"
 #   for c in arr:
  #      print(c)
    print(arr)
 #       print_delay_fast(c)
    print("#################                                              #################")
    print("########                                                                ########")
    print("##                       ENTRY POINT EXECUTABLE TASKMASTER                    ##")
    print("##                                                                            ##")
    print("########                 host: \033[0;0m" + host + " \
          \033[0;31mport: \033[0;0m"  \
          + str(port) + "\033[0;31m           ########")
    print("#################                                              #################")
    print("################################################################################")
    print("\033[0;0m")

def prompt(sock):
    while True:
        try:
            line = input("taskmaster >")
            sock.send(line.encode('utf-8'))
        except:
            break

def auth(client, addr, server, thread):
    retries = 0
    while retries < 3:
        passwd = (client.recv(1024)).decode('utf-8')
        if passwd == server.psswd:
            client.send(('Success').encode('utf-8'))
            retries = 3
            #server_get(client, addr, server)
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

    sy

def welcome(host, port):
    connect = "Connection is starting"
    for c in connect:
        print_delay(c)
    wait = "..."
    for c in wait:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.6)
    print("\n\n")
    arr = "\033[0;31m################################################################################"
    for c in arr:
        print_delay(c)
    print("#################                                              #################")
    print("########                                                                ########")
    print("##                       ENTRY POINT EXECUTABLE TASKMASTER                    ##")
    print("##                                                                            ##")
    print("########                 host: \033[0;0m" + host + " \
          \033[0;31mport: \033[0;0m"  \
          + str(port) + "\033[0;31m           ########")
    print("#################                                              #################")
    print("################################################################################")
    print("\033[0;0m")

def prompt(sock):
    while True:
        try:
            line = input("taskmaster >")
            sock.send(line.encode('utf-8'))
        except:
            break

def auth(client, addr, server, thread):
    retries = 0
    while retries < 3:
        passwd = (client.recv(1024)).decode('utf-8')
        if passwd == server.psswd:
            client.send(('Success').encode('utf-8'))
            retries = 3
            #server_get(client, addr, server)
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


# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    welcome.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/11 18:17:19 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/24 15:53:27 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import time

from taskmaster.auth import *


def print_arr(arr):
    for c in arr:
        print_delay_fast(c);

def welcome(host, port, n):
    connect = "Connexion is starting  "
    for c in connect:
        print_delay(c)
    wait = "..."
    for c in wait:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.2)
    print("\n")
    arr = "\033[031m################################################################################\n"
    print_arr(arr)
    arr = "#################                                              #################\n"
    print_arr(arr)
    arr = "########                                                                ########\n"
    print_arr(arr)
    arr = "##                       ENTRY POINT EXECUTABLE TASKMASTER                    ##\n"
    print_arr(arr)
    arr = "##                                                                            ##\n"
    print_arr(arr)
    arr = "########                 host: \033[0;0m" + host + " \
          \033[0;31mport: \033[0;0m"  \
          + str(port) + "\033[0;31m           ########\n"
    print_arr(arr)
    arr = "#################    client number:\033[0;0m" + str(n) + "\033[0;31m                             #################\n"
    print_arr(arr)
    arr = "################################################################################\n"
    print_arr(arr)
    f = open('ascii-art.txt', "r")
    print(f.read())
    print("\033[0;0m")



# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmaster.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/01 15:17:25 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/03 15:23:50 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os

from taskmaster.task_error import *

#def main();

if __name__ == '__main__':
    if len(sys.argv) < 2:
       task_error("Usage: <config_file>")
    try:
        config_file = os.path.abspath(sys.argv[1])
    except FileNotFoundError:
        task_error("Config file not found")
    print(config_file)

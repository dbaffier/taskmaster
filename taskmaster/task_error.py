# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    task_error.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/03 13:26:33 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/04 13:19:03 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

def task_error(msg):
    print("Taskmaster: " + msg, file=sys.stderr)
    sys.exit(1);

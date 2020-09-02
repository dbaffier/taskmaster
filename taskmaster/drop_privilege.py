# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    drop_privilege.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/03 15:21:07 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/29 14:50:26 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import pwd
import grp

import logging


def drop_privileges():
    if os.getuid() == 0:
        running_uid = 1
        running_gid = 1

        os.setgroups([])
        os.setgid(running_gid)
        os.setuid(running_uid)

        logging.info('Dropped root privileges')

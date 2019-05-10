# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    launcher.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/06 09:29:22 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/09 11:00:09 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from taskmaster.job import *
from taskmaster.process import *
from taskmaster.io_read import *

def launcher(cfg, section):
    print(section)
    for name in section:
        job = Job(cfg, name)
        job.conf_apply()
        proc = Process(job)
        proc.exec(job)
        io_transfer(job, proc)

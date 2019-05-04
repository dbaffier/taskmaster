# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parse_prog.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/04 14:28:58 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/04 17:30:53 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import configparser

def parse_prog(sections):
    prog_list = list()
    for prog in sections:
        if prog[:7] == "program":
            prog_list.append(prog)
    return (prog_list)

def proc_max(prog_list, config):
    count = 0
    for prog in prog_list:
        try:
            count += int(config.get(prog, "numprocs"))
            if (count > 200):
                return True
        except configparser.NoOptionError:
            count += 1

    return False

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    builtin.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/15 16:36:41 by dbaffier          #+#    #+#              #
#    Updated: 2020/02/29 17:04:41 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #



def     builtin_ok(line):
    builtins = {'status', 'exit', 'stop', 'start', 'quit', 'restart', 'log',
                'reload', 'shutdown'}
    for b in builtins:
        if b in line:
            return True
    return False

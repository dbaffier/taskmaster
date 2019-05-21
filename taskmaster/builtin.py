# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    builtin.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/15 16:36:41 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/16 13:47:11 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #



def     builtin_ok(line):
    builtins = {'status', 'exit', 'stop', 'start'}
    for b in builtins:
        if b in line:
            return True
    return False

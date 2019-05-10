# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmasterctl.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/09 13:09:30 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/09 13:14:05 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

def ctl_start(host, port):


if __name__ == '__main__':
    try:
        config_file = os.path.abspath(sys.argv[1])
    except:
        sys.stderr.write("taskmasterctl: no such file")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        host = config.get('server', 'host')
    except:
        sys.stderr.write("taskmasterctl: host is missing")
        sys.exit(1)
    try:
        port = int(config.get('server', 'port'))
    except:
        sys.stderr.write("taskmasterctl: host is missing")
        sys.exit(1)
    ctl_start(host, port)

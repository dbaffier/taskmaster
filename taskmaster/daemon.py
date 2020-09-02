# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    daemon.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dbaffier <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/05/11 10:02:26 by dbaffier          #+#    #+#              #
#    Updated: 2019/05/11 11:37:39 by dbaffier         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
import time
import atexit
import resource
import signal

def daemon_success(number, frame):
    sys.exit(0)

class Daemon:
    
    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        try:
            fatherpid = os.getpid()
            pid = os.fork()
            if pid > 0:
                signal.signal(signal.SIGUSR1, daemon_success)
                sys.exit(0)
        except OSError as err:
            sys.exit(1)
        #leave parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)
        
        # fork himself again
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.exit(1)


        # close all fd
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        while soft > 2:
            try:
                os.close(soft)
            except:
                pass
            soft -= 1

        # clear fd
        sys.stdout.flush()
        sys.stderr.flush()
        # Redirect fd to /dev/null
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')
        os.kill(fatherpid, signal.SIGUSR2)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        if pid:
            msg = "Daemon already running\n"
            sys.stderr.write(msg.format(self.pidfile))
            sys.exit(1)
        self.daemonize()

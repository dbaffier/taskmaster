# taskmaster

Taskmaster is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.

I've did an Client/server archictecture to allow for two separate programs :
- A daemon, that does the actual job control
- A control program, that provides a shell for the user, and communicates with the daemon over UNIX or TCP sockets.

### Taskmasterd

The server piece of taskmaster is named taskmasterd. It is responsible for starting child programs at its own invocation, responding to commands from clients, restarting crashed or exited subprocesseses, logging its subprocess stdout and stderr output, and generating and handling “events” corresponding to points in subprocess lifetimes.

The server process uses a configuration file. This is located in config_file/server. This configuration file is a “Windows-INI” style config file. It is important to keep this file secure via proper filesystem permissions because it may contain unencrypted usernames and passwords.

### Taskmasterctl

The command-line client piece of the supervisor is named supervisorctl. It provides a shell-like interface to the features provided by taskmasterd. From taskmasterctl, a user can connect to different taskmasterd processes (one at a time), get status on the subprocesses controlled by, stop and start subprocesses of, and get lists of running processes of a taskmasterd.

The command-line client talks to the server across a UNIX domain socket or an internet (TCP) socket. The server can assert that the user of a client should present authentication credentials before it allows him to perform commands. The client process typically uses the same configuration file as the server but any configuration file with a [taskmasterctl] section in it will work.
 
#### Taskmasterd config file features
  - Command to use to launch the program
  - The number of processes to start and keep running
  - Whether to start this program at launch or not
  - Whether the program should be restarted always, never, or on unexpected exits
only
  - Which return codes represent an "expected" exit status
  - How long the program should be running after it’s started for it to be considered
"successfully started"
  - How many times a restart should be attempted before aborting
  - Which signal should be used to stop (i.e. exit gracefully) the program
  - How long to wait after a graceful stop before killing the program
  - Options to discard the program’s stdout/stderr or to redirect them to files
  - Environment variables to set before launching the program
  - A working directory to set before launching the program
  - An umask to set before launching the program

#### Taskmasterctl features 
  - See the status of all the programs described in the config file ("status" command)
  - Start / stop / restart programs
  - Reload the configuration file without stopping the main program
  - Logging info
 
#### bonus features
  - Privilege de-escalation on launch
  - advanced logging/reporting facilities (Alerts via email/http/syslog/etc...)
  - Client/server archictecture to allow for two separate programs

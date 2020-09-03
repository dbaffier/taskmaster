Taskmaster
==========

Supervisor is a client/server system that allows its users to
control a number of processes on UNIX-like operating systems.

What i implemented :

- Configuration file to start multiple job / processus
- Managing processus
  - Ability to restart, reload, stop, start, shutdown, show state
  - Handling signal
- Daemon ( Privilege de-escalation on launch )
- Client/server archictecture to allow for two separate programs : A daemon, that
does the actual job control, and a control program, that provides a shell for the
user, and communicates with the daemon over UNIX or TCP sockets
- advanced logging/reporting facilities (Alerts via email/http/syslog/etc...)

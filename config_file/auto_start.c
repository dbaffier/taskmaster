[program:hello]
command=/bin/ls
numprocs=2
autostart=true
autorestart=false
exitcodes=10
startsecs=0
startretries=1
stopsignal=QUIT
stopwaitsecs=5
stdout_logfile=/tmp/log1
stderr_logfile=/tmp/log2
environment=hello="hello",world="world"
directory=/tmp
umask=022

[server]
port=4242
password=4242

[unix_http_server]
file={{ run_root }}/tmp/supervisor.sock   ; (the path to the socket file)
chmod=0700                 ; socket file mode (default 0700)
;chown=root:root       ; socket file uid:gid owner
;username={{ username }}              ; (default is no username (open server))
;password={{ password }}               ; (default is no password (open server))

[supervisord]
logfile={{ run_root }}/logs/supervisord.log ; (main log file;default $CWD/supervisord.log)
logfile_maxbytes=50MB        ; (max main logfile bytes b4 rotation;default 50MB)
logfile_backups=10           ; (num of main logfile rotation backups;default 10)
loglevel=info                ; (log level;default info; others: debug,warn,trace)
pidfile={{ run_root }}/tmp/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
nodaemon=false               ; (start in foreground if true;default false)
minfds=1024                  ; (min. avail startup file descriptors;default 1024)
minprocs=200                 ; (min. avail process descriptors;default 200)
umask=022                   ; (process file creation umask;default 022)
identifier=supervisor       ; (supervisord identifier, default is 'supervisor')
directory={{ run_root }}             ; (default is not to cd during start)
nocleanup=false              ; (don't clean up tempfiles at start;default false)
childlogdir={{ run_root }}/tmp            ; ('AUTO' child log dir, default $TEMP)
strip_ansi=false            ; (strip ansi escape codes in logs; def. false)
;user=chrism                 ; (default is current user, required if root)
;environment=KEY=value       ; (key value pairs to add to environment)

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix://{{ run_root }}/tmp/supervisor.sock ; use a unix:// URL  for a unix socket
;username={{ username }}              ; should be same as http_username if set
;password={{ supervisor_password }}                ; should be same as http_password if set
prompt=supervisor         ; cmd line prompt (default "supervisor")
history_file={{ run_root }}/.sc_history  ; use readline history if available

[program:{{ project }}]
command={{ run_root }}/bin/gunicorn {{ project }}.{{ project }}.wsgi:application
    --workers 8 
    --timeout 30 
    --log-level info 
    --error-logfile '-' 
    --bind 0.0.0.0:{{ port }}%(process_num)1d
process_name=%(program_name)s_%(process_num)d
umask=022
startsecs=10
stopwaitsecs=0
redirect_stderr=true
stdout_logfile={{ run_root }}/logs/process_%(process_num)02d.log
numprocs={{ process_count }}
numprocs_start=0
environment={{ project }}={{ profile }}=VIRTUALENV_NAME={{ venv_dir }}       ; (key value pairs to add to environment)

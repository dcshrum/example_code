set -x
export PATH="$PATH:/opt/mssql-tools18/bin" 

/usr/bin/cp -vf /SSL/id_rsa /id_rsa 
/usr/bin/chmod -v 0700 /id_rsa 
export GIT_SSH_COMMAND='ssh -i /id_rsa -o StrictHostKeyChecking=accept-new' 

/usr/bin/git clone git@github.com:xxxxxxx/reporting.git /reporting 
/usr/bin/cp -vf /SSL/database_credentials.py /reporting/python/root/database_credentials.py 

cd /reporting/python/root/flask/$application

/usr/bin/echo "Starting Flask server"
/usr/local/bin/gunicorn  --log-level debug --backlog 2 --workers 2 --bind 0.0.0.0:443 --keep-alive 300 --graceful-timeout 300 --timeout 300 --keyfile /certs/server.key --certfile /certs/server.crt main:app
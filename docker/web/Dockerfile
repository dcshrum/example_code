FROM ubuntu:latest

LABEL xxxxxx.reporting.authors="dcshrum@ufl.edu"

ENV TZ=America/New_York

WORKDIR /

RUN <<EOF
/usr/bin/ln -vsnf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
apt-get update && apt-get upgrade -y && apt-get install -y build-essential telnet curl nano python3 python3-pip python3-dev git unixodbc jq netcat-traditional mysql-client nginx libssl-dev libffi-dev python3-setuptools python3-lxml redis-tools unixodbc-dev  lsb-release
/usr/bin/rm -rvf /usr/lib/python3/dist-packages/pip-24.0.dist-info/
/usr/bin/find / -name 'EXTERNALLY-MANAGED' -exec rm -vf {} \;
/usr/bin/pip3 install --upgrade pip
/usr/bin/curl https://packages.microsoft.com/keys/microsoft.asc | /usr/bin/gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
/usr/bin/curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | /usr/bin/tee /etc/apt/sources.list.d/mssql-release.list
/usr/bin/pip3 install mysql-connector-python pyyaml pandas python-Levenshtein requests setuptools-rust pysftp pyodbc fastparquet pyarrow numpy dropbox openpyxl azure-storage-blob azure.identity QualtricsAPI sqlalchemy sshtunnel pydrive filelock flask gunicorn flask-sqlalchemy flask-login Flask-RESTful flasgger Flask-Caching redis pympler flask-saml2
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18
ACCEPT_EULA=Y apt-get install -y mssql-tools18
/usr/bin/curl -sL https://aka.ms/InstallAzureCLIDeb | bash
echo '/usr/bin/cp -vf /SSL/database_credentials.py /reporting/python/root/database_credentials.py' >> /root/.bashrc
echo 'PS1="WEB\w:"' >> /root/.bashrc
echo '\ncd /reporting/python/root/flask/\nexport FLASK_DEBUG=1\n' >> /root/.bashrc
echo 'echo -e "\n\nweb server bare:\n/usr/local/bin/flask run -h 0.0.0.0 -p 443 --cert /certs/server.crt --key /certs/server.key"' >> /root/.bashrc
echo 'echo -e "\n\nweb server with gunicorn:\n/usr/local/bin/gunicorn --backlog 2 --workers 2 --bind 0.0.0.0:443 --keep-alive 300 --graceful-timeout 300 --timeout 300 --keyfile /certs/server.key --certfile /certs/server.crt main:app"' >> /root/.bashrc
EOF

ENV FLASK_APP=main
ENV FLASK_DEBUG=0

ADD start.sh /start.sh

ENTRYPOINT [ "/bin/bash", "/start.sh" ]
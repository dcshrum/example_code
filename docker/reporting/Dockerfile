FROM ubuntu:latest
 
LABEL xxxxxx.reporting.authors="dcshrum@ufl.edu"

ENV TZ=America/New_York

WORKDIR /

## openSSL stuff... 
# line 21, there is conflict between flask-saml and pyopenssl
#  Thus the upgrade because stack overflow told me to do that

RUN <<EOF
/usr/bin/ln -vsnf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
apt-get update && apt-get upgrade -y && apt-get install -y build-essential telnet curl nano python3 python3-pip python3-dev git unixodbc jq netcat-traditional mysql-client ruby apt-utils r-base r-base-dev nginx libssl-dev libffi-dev python3-setuptools python3-lxml redis-tools unixodbc-dev libtirpc-dev redis-tools lsb-release
/usr/bin/rm -rvf /usr/lib/python3/dist-packages/pip-24.0.dist-info/
/usr/bin/find / -name 'EXTERNALLY-MANAGED' -exec rm -vf {} \;
/usr/bin/pip3 install --upgrade pip
/usr/bin/curl https://packages.microsoft.com/keys/microsoft.asc | /usr/bin/gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
/usr/bin/curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | /usr/bin/tee /etc/apt/sources.list.d/mssql-release.list
/usr/bin/pip3 install mysql-connector-python pyyaml pandas python-Levenshtein requests setuptools-rust pysftp pyodbc fastparquet pyarrow numpy dropbox openpyxl azure-storage-blob azure.identity QualtricsAPI sqlalchemy sshtunnel pydrive filelock psutil simple-salesforce xlrd chardet redis rpy2 matplotlib seaborn flask gunicorn flask-sqlalchemy flask-login Flask-RESTful flasgger Flask-Caching redis pympler flask-saml2
/usr/bin/pip3 install pyopenssl --upgrade
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18
ACCEPT_EULA=Y apt-get install -y mssql-tools18
/usr/bin/curl -sL https://aka.ms/InstallAzureCLIDeb | bash
/usr/bin/echo 'cd /reporting/python/ && git config --global --add safe.directory /reporting && PS1="DOCKER-Reporting\w:" && /usr/bin/chmod -v 777 /reporting/python/main.py' >> /root/.bashrc
/usr/bin/echo 'echo -e "\nCommand to run live\n./main.py -v 1 -y /reports/queries.yaml"' >> /root/.bashrc
EOF
ADD start.sh /start.sh

ENTRYPOINT [ "/bin/bash", "/start.sh" ]
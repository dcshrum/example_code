START_TIME=$(/usr/bin/python3 -c "import pytz; from pytz import timezone; from datetime import datetime; format = '%Y-%m-%d %H:%M:%S'; start=datetime.now(timezone('America/New_York')); print(start.strftime(format))")
REPORTS_PATH=$(/usr/bin/grep '/reports' /proc/1/task/1/mountinfo)
LOG_FILE_NAME=$(/usr/bin/python3 -c "import sys; reports_path = sys.argv[1:]; print('/logs/' + reports_path[3].split('/volumes/')[1].split('/_data')[0] + '.log');" $REPORTS_PATH)
JSON_FILE_NAME=$(/usr/bin/python3 -c "import sys; reports_path = sys.argv[1:]; print('/logs/' + reports_path[3].split('/volumes/')[1].split('/_data')[0] + '.json');" $REPORTS_PATH)

handle_error() {
    END_TIME=$(python3 -c "import pytz; from pytz import timezone; from datetime import datetime; format = '%Y-%m-%d %H:%M:%S'; start=datetime.now(timezone('America/New_York')); print(start.strftime(format))")
    /usr/bin/python3 /reporting/python/root/exit_status/exit_status.py "${START_TIME}" "${END_TIME}" "${JSON_FILE_NAME}" "${LOG_FILE_NAME}" "FAILED" >> ${LOG_FILE_NAME} 2>&1
    exit 1
}

trap handle_error ERR

set -x
export PATH="$PATH:/opt/mssql-tools18/bin" > ${LOG_FILE_NAME} 2>&1

/usr/bin/cp -vf /SSL/keys/id_rsa /id_rsa >> ${LOG_FILE_NAME} 2>&1
/usr/bin/chmod -v 0700 /id_rsa >> ${LOG_FILE_NAME} 2>&1
export GIT_SSH_COMMAND='ssh -i /id_rsa -o StrictHostKeyChecking=accept-new' >> ${LOG_FILE_NAME} 2>&1

/usr/bin/git clone git@github.com:xxxxxxx/reporting.git /reporting >> ${LOG_FILE_NAME} 2>&1
/usr/bin/cp -vf /SSL/database_credentials.py /reporting/python/root/database_credentials.py >> ${LOG_FILE_NAME} 2>&1

cd /reporting/python/

/usr/bin/chmod -v 777 /reporting/python/main.py >> ${LOG_FILE_NAME} 2>&1

./main.py -v 1 -y /reports/queries.yaml >> ${LOG_FILE_NAME} 2>&1

END_TIME=$(python3 -c "import pytz; from pytz import timezone; from datetime import datetime; format = '%Y-%m-%d %H:%M:%S'; start=datetime.now(timezone('America/New_York')); print(start.strftime(format))")

/usr/bin/python3 /reporting/python/root/exit_status/exit_status.py "${START_TIME}" "${END_TIME}" "${JSON_FILE_NAME}" "${LOG_FILE_NAME}" "SUCCESS" >> ${LOG_FILE_NAME} 2>&1
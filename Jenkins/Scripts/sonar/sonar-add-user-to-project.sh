
#!/bin/bash
SONAR_TOKE="TOKEN"
SONAR_HOST="HOST"
SONAR_USER="USER"
SONAR_PROJECT="PROJECT"
curl -X POST -o /dev/null -s -d "" -u "${SONAR_TOKE}:"  -w "%{http_code}" "https://${SONAR_HOST}/api/permissions/add_user?login=${SONAR_USER}&permission=admin&projectKey=${SONAR_PROJECT}"

#!/bin/bash
SONAR_TOKE="TOKEN"
SONAR_HOST="HOST"
SONAR_GROUP="GROUP"
SONAR_PROJECT="PROJECT"


curl -X POST -o /dev/null -s -d "" -u "${SONAR_TOKE}:"  -w "%{http_code}" "https://${SONAR_HOST}/api/permissions/add_group?groupName=${SONAR_GROUP}&permission=codeviewer&projectKey=${SONAR_PROJECT}"

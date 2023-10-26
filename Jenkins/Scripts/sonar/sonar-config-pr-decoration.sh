#!/bin/bash
SONAR_TOKE="TOKEN"
SONAR_HOST="HOST"
SONAR_USER="USER"
SONAR_PROJECT="PROJECT"
GIT-ORG="GIT-ORG"
GIT-REPO="GIT-REPO"

curl -X POST -s -o /dev/null -w "%{http_code}" -u "${SONAR_TOKE}:" "https://${SONAR_HOST}/api/alm_settings/set_github_binding?almSetting=SonarQubeEE-PRChecks&monorepo=false&project=${SONAR_PROJECT}&repository=${GIT-ORG}/${GIT-REPO}"
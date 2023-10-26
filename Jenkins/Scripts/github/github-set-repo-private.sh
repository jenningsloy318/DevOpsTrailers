#!/bin/bash
GITHUB_TOKEN="Token"
GITHUB_HOST="GITHUB_HOST"
GITHUB_ORG="GIT-ORG"
GITHUB_REPO="GIT-REPO"



curl  -Ls -X PATCH "https://${GITHUB_HOST}/api/v3/repos/${GITHUB_ORG}/${GITHUB_REPO}" \
        -H "Accept: application/vnd.github.nebula-preview+json" \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -d '{ "visibility": "internal"}'

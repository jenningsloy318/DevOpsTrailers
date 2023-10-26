#!/bin/bash
GITHUB_TOKEN="Token"
GITHUB_HOST="GITHUB_HOST"
GITHUB_ORG="GIT-ORG"
GITHUB_REPO="GIT-REPO"
GITHUB_BRANCH="GIT-BRANCH"
curl -L  -H "Accept: application/vnd.github.v3+json" -H "Authorization: token ${GITHUB_TOKEN}" "https://${GITHUB_HOST}/api/v3/repos/${GITHUB_ORG}/${GITHUB_REPO}/branches/${GITHUB_BRANCH}/protection" | jq -r

#!/bin/bash
GITHUB_TOKEN="Token"
GITHUB_HOST="GITHUB_HOST"
GITHUB_ORG="GIT-ORG"
GITHUB_REPO="GIT-REPO"
GITHUB_BRANCH="GIT-BRANCH"
curl  -L -X PUT "https://${GITHUB_HOST}/api/v3/repos/${GITHUB_ORG}/${GITHUB_REPO}/branches/$GITHUB_BRANCH/protection" \
                -H "Accept: application/vnd.github.v3+json" \
                -H "Authorization: token ${GITHUB_TOKEN}" \
                -H 'Accept: application/vnd.github.luke-cage-preview+json' \
                -H 'Content-Type: text/plain' \
                -d '{
                    "required_pull_request_reviews": {
                        "bypass_pull_request_allowances":{
                            "users":["service-tip-git"]
                        },
                        "required_approving_review_count": 1
                    },
                    "required_status_checks": {
                        "strict": true,
                        "contexts": []
                    },
                    "restrictions": {"users": [],"teams": [], "apps": []},
                    "enforce_admins": null
                }'




#!/bin/bash
GITHUB_TOKEN="Token"
GITHUB_HOST="GITHUB_HOST"
GITHUB_ORG="GIT-ORG"
GITHUB_REPO="GIT-REPO"
GITHUB_BRANCH="GIT-BRANCH"

team_slugs=$(curl -s https://${GITHUB_HOST}/api/v3/orgs/${GITHUB_ORG}/teams \
-H "Accept: application/vnd.github.v3+json" \
-H "Authorization: token ${GITHUB_TOKEN}" | jq -r .[].slug)


for team_slug in $team_slugs
    do
        case  $team_slug in
            "admin")
                permission=admin
                ;;
            "user")
                permission=maintain
                ;;
        esac

                curl -H "Authorization: token ${GITHUB_TOKEN}" \
                -X PUT   https://${GITHUB_HOST}/api/v3/orgs/${GITHUB_ORG}/teams/$team_slug/repos/${GITHUB_ORG}/${GITHUB_REPO} \
                -H "Accept: application/vnd.github.v3+json" \
                -d '{"permission":"'$permission'"}'

    done


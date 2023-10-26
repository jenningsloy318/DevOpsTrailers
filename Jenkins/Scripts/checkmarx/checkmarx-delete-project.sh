#!/bin/bash
CX_USER="USER"
CX_PASSWD="Pass"
CX_HOST="cxhost"
CX_client_id="client_id"
CX_client_secret="client_secret"

token=$(curl -k --location --request POST "https://${CX_HOST}/CxRestAPI/auth/identity/connect/token" --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode "username=${CX_USER}" --data-urlencode "password=${CX_PASSWD}" --data-urlencode 'grant_type=password' --data-urlencode 'scope=sast_rest_api' --data-urlencode "client_id=${CX_client_id}" --data-urlencode "client_secret=${CX_client_secret}" | jq -r '.access_token')


curl -k -X DELETE  -H  "Authorization: Bearer $token"  "https://${CX_HOST}/CxRestAPI/projects/86407"

#!/bin/bash
WS_HOST="WS_HOST"
curl -H 'Content-Type: application/json'  -d @whitesource-get-all-projects.json "https://${WS_HOST}/api/v1.3"


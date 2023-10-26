
#!/bin/bash
WSHOST="sap.whitesourcesoftware.com"
curl    -H 'Content-Type: application/json' -d @whitesource-add-user-as-admin-to-product.json "https://${WSHOST}/api/v1.3"


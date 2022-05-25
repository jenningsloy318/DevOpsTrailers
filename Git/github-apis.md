github API
---
        
- set repo visibiliy, can be `public`, `private`, `internal`
    ```sh
        
        curl  -Ls -X PATCH https://api.github.com/repos/OWNER/REPO \
        -H "Accept: application/vnd.github.nebula-preview+json" \
        -H 'Authorization: token c3e11670092eed30883ec2cbace2154ea54cbd5a' \
        -d '{ "visibility": "internal"}' 
      ```
      > note: Header `"Accept: application/vnd.github.nebula-preview+json" `  is explained in [https://developer.github.com/changes/3/](https://developer.github.com/changes/3/)
      > quote " To access the visibility field for any of these endpoints, you must provide a custom media type in the Accept header: `application/vnd.github.nebula-preview+json` "
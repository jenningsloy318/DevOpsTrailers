# Deploy binary on CF

## Deploy directly with the binary

Since all applications deployed to CF, all the files this application owns are under **/home/vcap/app**.so when deploy binary application, we need to know where the binary files and its configuration reside.

Let deploy prometheus to CF(SAP Cloud Foundry platform) as an example,

1. the content of the manifest

    ```yaml
    manifest.yml

    ---
    applications:
    - name: alertmanager
      memory: 2G
      routes:
      - route: alertmanager.cfapps.sap.hana.ondemand.com
      path: alertmanager-0.14.0.linux-amd64/
      disk_quota: 4G
      buildpack: binary_buildpack
      command: /home/vcap/app/alertmanager  --config.file=/home/vcap/app/alertmanager.yml --storage.path=/home/vcap/app/data/ --web.listen-address=0.0.0.0:8080 --web.external-url=https://alertmanager.cfapps.sap.hana.ondemand.com
    ```

    - we need to download and extract alertmanager to local filesystem, in the meanwhile we need to point to the path to the directory of alertmanager
    - add/modify the alertmanager configuration alertmanager.yml  in alertmanager directory
    - set route
    - set buildpack to **binary_buildpack**
    - modify the command to the full start up command line and parameter, to change the listen port to 8080 as CF only support application in this way

2. just cf push to deploy it.

    ```sh
    cf push
    ```

## Deploy with docker image

Alternatively we can deploy it as a docker image, package all configuration and binary into one docker image. Don't forget to declare **`EXPOST 9093`** in the `Dockerfile`, CF platform will search this entry to do loadbalance, when use Docker image, it search this entry, which can expose the application to outside. in this way, it will not restrict the port 8080.

1. the content of the manifest

    ```yaml
    mainfest.yml
    ---
    applications:
    - name: alertmanager-docker
      memory: 2G
      routes:
      - route: alertmanager-docker.cfapps.sap.hana.ondemand.com
      disk_quota: 4G
      docker:
          image: prom/alertmanager
    ```

2. just cf push to deploy it.

    ```sh
    cf push
    ```

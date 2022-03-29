Tips for groovy scipted pipeline
- create/set env in groovy 
  - create local env, following will create an env, can be used in both shell scripts or common groovy statements
    ```
    node {
      env.Project = 'hyper'
      sh 'echo ${Project}
     }       
    ```
- if we want to pass the credentials, 
      ```
      withCredentials([usernamePassword(credentialsId: credentialsiD, usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
          sh 'echo $USER'
      }
      ```

- save credential file locally 
    ```
        withCredentials([file(credentialsId: 'cnpe-kubeconfig ', variable: 'KUBECONFIG')])  {
            writeFile file: 'cnpe.kubeconfig', text: readFile(KUBECONFIG)
        }
    ```
- get credentials 
  ```
  def credentials = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
    com.cloudbees.plugins.credentials.common.StandardCredentials.class,
    Jenkins.instance
    )
    def prodCred = credentials.findResult { it.id == prodCredID ? it : null }
    env.CLIENT_ID = prodCred.username
    env.CLIENT_SECRET = prodCred.password
    ```
    following statments can get all credentials 
    ```
    def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(

    com.cloudbees.plugins.credentials.common.StandardCredentials.class,
        Jenkins.instance,
        null,
        null
    );
    for (int i; i < creds.size(); i++) {
    println "\n========== Credential ${i+1} Start =========="
    creds[i].properties.each { println it }
    println "========== Credential ${i+1} End   ==========\n"
    }
    ```
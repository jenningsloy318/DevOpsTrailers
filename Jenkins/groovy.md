# Tips for groovy scripted pipeline

- create/set env in groovy
  - create local env, following will create an env, can be used in both shell scripts or common groovy statements

    ```groovy
    node {
      env.Project = 'hyper'
      sh 'echo ${Project}
     }
    ```

- if we want to pass the credentials,
      ```groovy
      withCredentials([usernamePassword(credentialsId: credentialsiD, usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
          sh 'echo $USER'
      }
      ```

- save credential file locally

    ```groovy
        withCredentials([file(credentialsId: 'cnpe-kubeconfig ', variable: 'KUBECONFIG')])  {
            writeFile file: 'cnpe.kubeconfig', text: readFile(KUBECONFIG)
        }
    ```

- get credentials

  ```groovy
  def credentials = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
    com.cloudbees.plugins.credentials.common.StandardCredentials.class,
    Jenkins.instance
    )
    def prodCred = credentials.findResult { it.id == prodCredID ? it : null }
    env.CLIENT_ID = prodCred.username
    env.CLIENT_SECRET = prodCred.password
    ```

    following statements can get all credentials

    ```groovy
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

- lint config for groovy file
  - use [npm-groovy-lint](https://github.com/nvuillam/npm-groovy-lint)
    - https://github.com/oxsecurity/megalinter/blob/main/TEMPLATES/.groovylintrc.json
    - https://github.com/nvuillam/npm-groovy-lint/blob/main/lib/.groovylintrc-recommended-jenkinsfile.json
    - https://github.com/nvuillam/npm-groovy-lint/blob/main/lib/.groovylintrc-recommended.json
  - rule of https://codenarc.org/codenarc-rule-index.html
  - config file [.groovylintrc.json](./.groovylintrc.json) can be places
    - root directory of the repository
    - vscode set  `groovyLint.basic.config`  to the path of  `.groovylintrc.json` , in settings.json `"groovyLint.basic.config": "~/.groovylintrc.json"`

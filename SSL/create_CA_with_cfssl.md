1. create  /etc/cfssl/csr_ca.json
    ```
    cat /etc/cfssl/csr_ca.json
    {
      "CN": "Suning sports internal CA",
      "key": {
        "algo": "rsa",
        "size": 2048
      },
        "names": [
           {
             "C": "US",
             "L": "San Francisco",
             "O": "My Awesome Company",
             "OU": "CA Services",
             "ST": "California"
           }
        ]
    }
    ```
2. Create CA
    ```
    cfssl gencert -initca  /etc/cfssl/csr_ca.json | cfssljson -bare /etc/cfssl/ca
    ```

3. create auth_key 
    ```
    hexdump -n 16 -e '4/4 "%08X" 1 "\n"' /dev/random
    41ED055262266AE2C9F5095BD211B7B6
    ```
4. generate cert for ocsp which is used for ocsp responder, optional
    ```
    cfssl gencert -ca=/etc/cfssl/ca.pem -ca-key=/etc/cfssl/ca-key.pem -config=/etc/cfssl/config_ca.json -profile="ocsp" /etc/cfssl/ocsp_csr.json |cfssljson -bare /etc/cfssl/ocsp
    ```
5. create /etc/cfssl/ca_config.json

    ```json
    {
        "signing": {
            "default": {
                "auth_key": "key1",
                "expiry": "35040h",
                "crl_url": "http://cfssl.lan.amos:8888/crl",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "profiles": {
                "CA": {
    				"usages": ["cert sign"],
    				"expiry": "720h"
    			},
                "intermediate": {
                    "auth_key": "key1",
                    "expiry": "35040h",
                    "usages": [
                        "signing",
                        "key encipherment",
                        "cert sign",
                        "crl sign"
                    ],
                    "ca_constraint": {
                        "is_ca": true,
                        "max_path_len":1
                    }
                },
                "ocsp": {
                    "auth_key": "key1",
                    "usages": [
                      "digital signature",
                      "ocsp signing"
                    ],
                    "expiry": "35040h"
                  },
                  "serverCA": {
                    "auth_key": "key1",
                    "expiry": "35040h",
                    "usages": [
                      "signing",
                      "key encipherment",
                      "server auth",
                      "cert sign",
                      "crl sign"
                    ]
                  },
                "server": {
                    "auth_key": "key1",
                    "expiry": "35040h",
                    "usages": [
                        "signing",
                        "key encipherment",
                        "server auth"
                    ]
                },
                "client": {
                    "auth_key": "key1",
                    "expiry": "35040h",
                    "usages": [
                        "signing",
                        "key encipherment",
                        "client auth"
                    ]
                },
                "peer": {
                    "auth_key": "key1",
                    "expiry": "35040h",
                    "usages": [
                        "signing",
                        "key encipherment",
                        "server auth",
                        "client auth"
                    ]
                }
            }
        },
        "auth_keys": {
            "key1": {
                "key": "41ED055262266AE2C9F5095BD211B7B6",
                "type": "standard"
            }
        }
    }
    ```

6. chose which db backend is used, and create the table accordingly;here I chose postgresql.
    
    ```sql
    CREATE TABLE certificates (
      serial_number            bytea NOT NULL,
      authority_key_identifier bytea NOT NULL,
      ca_label                 bytea,
      status                   bytea NOT NULL,
      reason                   int,
      expiry                   timestamptz,
      revoked_at               timestamptz,
      pem                      bytea NOT NULL,
      PRIMARY KEY(serial_number, authority_key_identifier)
    );

    CREATE TABLE ocsp_responses (
      serial_number            bytea NOT NULL,
      authority_key_identifier bytea NOT NULL,
      body                     bytea NOT NULL,
      expiry                   timestamptz,
      PRIMARY KEY(serial_number, authority_key_identifier),
      FOREIGN KEY(serial_number, authority_key_identifier) REFERENCES certificates(serial_number,   authority_key_identifier)
    );
    ```    
7. create /etc/cfssl/db-config.json
    ```json
    {"driver":"postgres","data_source":"postgres://user:password@host/db"}

    ```
8. create a certificate for cfssl api service itself

    8.1 create cfssl-api.csr
    ```json
    {
        "hosts": [
        	"cfss-api.snfc.org"
      ],
        "CN": "cfss-api",
        "key": {
          "algo": "rsa",
          "size": 4096
        },
        "names": [
          {
            "C": "CN",
            "L": "Nanjing",
            "OU": "Suning Sports",
            "ST": "Jiangsu"
          }
        ]
    }
  
     ```

   8.2 create certificate for cfssl api
    
    ```shell
    cfssl gencert -ca /etc/cfssl/ca.pem -ca-key /etc/cfssl/ca-key.pem /etc/cfssl/client_csr.json| cfssljson -bare /etc/cfssl/cfssl-api
    ```
9. launch cfssl api service
    ```shell

    [Unit]
    Description=cfssl api server

    [Service]
    ExecStart=/usr/bin/cfssl serve -ca-key /etc/cfssl/ca-key.pem  -ca /etc/cfssl/ca.pem  -config    /etc/cfssl/config_ca.json  -db-config /etc/cfssl/db-config.json -address  0.0.0.0 -port 443 -tls-key   /etc/cfssl/cfssl-api-key.pem -tls-cert /etc/cfssl/cfssl-api.pem 

    [Install]
    WantedBy=multi-user.target
    ```

    and then start cfssl-api service 
    ```
    systemctl start ssl-api 

    Mar 12 09:23:08 centos7 systemd[1]: Started cfssl api server.
    Mar 12 09:23:08 centos7 systemd[1]: Starting cfssl api server...
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] Initializing signer
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [WARNING] couldn't initialize ocsp signer: open : no such file or directory
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/info' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/crl' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/gencrl' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] setting up key / CSR generator
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/newkey' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/init_ca' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/scaninfo' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/certinfo' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/revoke' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/scan' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [WARNING] endpoint 'ocspsign' is disabled: signer not initialized
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/sign' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/authsign' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/newcert' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] bundler API ready
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/api/v1/cfssl/bundle' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] endpoint '/' is enabled
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] Handler set up complete.
    Mar 12 09:23:08 centos7 cfssl[441]: 2018/03/12 09:23:08 [INFO] Now listening on https://0.0.0.0:443
    ```
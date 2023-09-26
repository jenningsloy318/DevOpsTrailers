certs for goproxy
---

1. Create CA

* create ca.config

```conf
[ req ]
default_bits = 4096
default_keyfile = ca.key
distinguished_name = dn
req_extensions = v3_req
prompt = no
[ dn ]
C = CN
ST = SC
L = CD
O = Lmy
OU = LMY Dev
CN = dev@lmy.com

[v3_req]
# Extensions to add to a certificate request
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment

```

* create CA

```
openssl genrsa -aes256 -passout pass:xxx -out ca.pass.key 4096
openssl rsa -passin pass:xxxx -in ca.pass.key -out ca.key
openssl req -new -x509 -days 3650 -key ca.key   -config ca.config -out ca.pem

```

2. client cert

* create csr.conf

```conf

[ req ]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = v3_req
distinguished_name = dn

[ dn ]
C = CN
ST = SC
L = CD
O = Lmy
OU = LMY Dev
CN = dev@lmy.com
[v3_req]
# Extensions to add to a certificate request
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, serverAuth
subjectAltName = @alt_names
[ alt_names ]
IP.1 = {IP}

```

* generate key

```
openssl genrsa -aes256 -passout pass:xxx -out client.pass.key 4096
openssl rsa -passin pass:xxx -in client.pass.key -out client.key
openssl req -new -key client.key -out client.csr -config openssl-client.conf

openssl x509 -req -days 3650 -in client.csr -CA ca.pem -CAkey ca.key   -extfile openssl-client.conf   -out client.pem

```

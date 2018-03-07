PEM
---
1. Convert PEM to DER
```
$ openssl x509 -outform der -in certificate.pem -out certificate.der
```
2. Convert PEM to P7B
```
$ openssl crl2pkcs7 -nocrl -certfile certificate.cer -out certificate.p7b -certfile CAcert.cer
```

3. Convert PEM to PFX
```
$ openssl pkcs12 -export -out certificate.pfx -inkey privateKey.key -in certificate.crt -certfile CAcert.crt
```

DER
---
1. Convert DER to PEM
```
$ openssl x509 -inform der -in certificate.cer -out certificate.pem
```


P7B
---
1. Convert P7B to PEM
```
$ openssl pkcs7 -print_certs -in certificate.p7b -out certificate.cer
```
2.Convert P7B to PFX
```
$ openssl pkcs7 -print_certs -in certificate.p7b -out certificate.cer
$ openssl pkcs12 -export -in certificate.cer -inkey privateKey.key -out certificate.pfx -certfile CAcert.cer
```


PFX
---
1. Convert PFX to PEM
```
$ openssl pkcs12 -in certificate.pfx -out certificate.cer -nodes
```





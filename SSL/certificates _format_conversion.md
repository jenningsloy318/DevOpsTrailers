# Certificates Conversion

## PEM

1. Convert PEM to DER

```sh
openssl x509 -outform der -in certificate.pem -out certificate.der
```

2. Convert PEM to P7B

```sh
openssl crl2pkcs7 -nocrl -certfile certificate.cer -out certificate.p7b -certfile CAcert.cer
```

3. Convert PEM to PFX

```sh
openssl pkcs12 -export -out certificate.pfx -inkey privateKey.key -in certificate.crt -certfile CAcert.crt
```

## DER

1. Convert DER to PEM

```
openssl x509 -inform der -in certificate.cer -out certificate.pem
```

## P7B

1. Convert P7B to PEM

```sh
openssl pkcs7 -print_certs -in certificate.p7b -out certificate.cer
```

2. Convert P7B to PFX

```sh
openssl pkcs7 -print_certs -in certificate.p7b -out certificate.cer
openssl pkcs12 -export -in certificate.cer -inkey privateKey.key -out certificate.pfx -certfile CAcert.cer
```

## PFX


1. Convert PFX to PEM

```sh
openssl pkcs12 -in certificate.pfx -out certificate.cer -nodes
```

# Summary
The toniebox communicates over https with its servers. It uses its Certificate Authority certifcate (flash:/cert/ca.der) to verify the tls connection. The box authenticates itself with a client certificate (flash:/cert/client.der) + private rsa key (flash:/cert/private.der).
## Known domains
* prod.de.tbs.toys
* rtnl.bxcl.de

# Attention!
Your certificate may be banned if you send to many wrong requests to the Boxine servers. Also currently only one request/response cycle works. So you won't be able to fully man in the middle the box currently. TBD!

# Certificates

## Certificate conversion
To use the certificates and the rsa key with most tools you will need to convert it from DER to PEM
```
openssl x509 -inform DER -outform PEM -in ca.der -out ca.cer
openssl x509 -inform DER -outform PEM -in client.der -out client.cer
openssl rsa -inform DER -outform PEM -in private.der -out private.key
```

## Generate self signed root CA
```
openssl genrsa -out ca.key 4096
faketime '2015-11-04 00:00:00' openssl req -new -x509 -key ca.key -out ca.cer -days 9000 -subj '/C=DE/ST=NW/L=Duesseldorf/O=Boxine GmbH/CN=Boxine CA'
```

## Generate domains certificates
```
openssl req -new -key ca.key -out rtnl.bxcl.de.req -subj '/C=DE/ST=NW/L=Duesseldorf/O=Boxine GmbH/CN=rtnl.bxcl.de'
openssl req -new -key ca.key -out prod.de.tbs.toys.req -subj '/C=DE/ST=NW/L=Duesseldorf/O=Boxine GmbH/CN=prod.de.tbs.toys'
faketime '2015-11-05 00:00:00' openssl x509 -req -in rtnl.bxcl.de.req -CA ca.cer -CAkey ca.key -set_serial 101 -days 10950 -outform PEM -out rtnl.bxcl.de.cer
faketime '2015-11-05 00:00:00' openssl x509 -req -in prod.de.tbs.toys.req -CA ca.cer -CAkey ca.key -set_serial 101 -days 10950 -outform PEM -out prod.de.tbs.toys.cer
```

## Generate client certificate
```
openssl genrsa -out private.key 2048
openssl req -utf8 -new -key private.key -out client.req -subj '/C=DE/ST=NRW/L=Düsseldorf/O=Boxine GmbH'
openssl x509 -req -in client.req -CA ca.cer -CAkey ca.key -set_serial 101 -extensions client -days 10950 -outform PEM -out client.cer

```

## Certificate conversion
To use your generated certificates/ley for the toniebox you will have to convert it back to DER format.
```
openssl x509 -inform PEM -outform DER -in ca.cer -out ca.der
openssl x509 -inform PEM -outform DER -in client.cer -out client.der
openssl rsa -inform PEM -outform DER -in private.key -out private.der
```

## Certificate upload
```
cc.py -p COM6 write_file z:\fakessl\box_fake\client.der /cert/client.der write_file z:\fakessl\box_fake\private.der /cert/private.der write_file z:\fakessl\fake\ca.der /cert/ca.der
```

## Concat certificates to PEM
```
cat ca.key ca.cer > ca.pem
cat ca.key rtnl.bxcl.de.cer > rtnl.bxcl.de.pem
cat ca.key prod.de.tbs.toys.cer > prod.de.tbs.toys.pem
```

# WIP Fake Server / Client
https://github.com/toniebox-reverse-engineering/toniebox/tree/master/tools

# SSLSplit
As sslsplit doesn't clone the timestamps. You will have to compile sslsplit yourself, including this [Pull request](https://github.com/droe/sslsplit/pull/265).
Sslsplit doesn't verify the client certificate, so you only need to replace the ca.der on the toniebox.
```
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -F
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443

sslsplit -D -l /root/sslsplit/connections.log -j /root/sslsplit/ -S /root/sslsplit/logdir/ -a /root/sslsplit/toniebox/client.cer -b /root/sslsplit/toniebox/private.key -W /root/sslsplit/gendir/ -M /root/sslsplit/sslkeylogfile.log -t /root/sslsplit/certdir/ -c /root/sslsplit/ca.cer -k /root/sslsplit/ca.key https 0.0.0.0 8443
```

# Debian openssl fix
For debian you need to set minimum tls level from tlsv1.2 to tlsv1.0.
See /etc/ssl/openssl.cnf 
```
MinProtocol = TLSv1.2
```

# SSLSplit Tutorial
https://blog.heckel.io/2013/08/04/use-sslsplit-to-transparently-sniff-tls-ssl-connections/
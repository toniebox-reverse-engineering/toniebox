# Summary
The toniebox communicates over https with its servers. It uses its Certificate Authority certifcate (flash:/cert/ca.der) to verify the tls connection. The box authenticates itself with a client certificate (flash:/cert/client.der) + private rsa key (flash:/cert/private.der). The communication is based on https and protobuf.

## Known domains
* prod.de.tbs.toys
* rtnl.bxcl.de

# Attention!
Your certificate may be banned if you send to many wrong requests to the Boxine servers. 

# Using mitmproxy
The Toniebox can be man-in-the-middled by replacing the CA of the box with one you can control. You need to use [mitmproxy v8.0.0](https://github.com/mitmproxy/mitmproxy/releases/tag/v8.0.0) and use the [mitmproxy-validity addon](https://github.com/toniebox-reverse-engineering/mitmproxy-toniebox).
You should prepare a system for [transparent proxing with mitmproxy](https://docs.mitmproxy.org/stable/howto-transparent/). The easiest way in my opinion to use an VM and set up the DHCP for the WiFi the way that the Toniebox gets the VM as gateway.

## Don't use the latest mitmproxy

Don't use mitmproxy v9 as it doesn't support the needed sha-1 signature algoritms! Stick to 8.0.0 until further notice!
```
(OpenSSL Error([('SSL routines', '', 'no shared signature algorithms')]))
```

## Create **CA**
mitmproxy creates its CA on first run (/root/.mitmproxy/). I suggest to start it with the tool faketime or change your systems date to 2015-11-04. (It may work without, but no warranty) Don't forget to run it as root.

## Conversion to **DER**-format
Afterwards you need convert the mitmproxy-ca-cert.cer into the **DER**-format
```
openssl x509 -inform PEM -outform DER -in mitmproxy-ca-cert.cer -out mitmproxy-ca-cert.der
```
## Backup original files
Afterwards you'll need to **backup the Toniebox' CA** and its **client.der/private.der**
```
cc3200tool read_file /cert/ca.der ca.der read_file /cert/client.der client.der read_file /cert/private.der private.der
```
## Upload **mitmproxy CA** to the Toniebox
```
cc3200tool write_file mitmproxy-ca-cert.der /cert/ca.der 
```
## Convert **client certificate** to **PEM**-format
```
openssl x509 -inform DER -outform PEM -in client.der -out client.cer
openssl rsa -inform DER -outform PEM -in private.der -out private.key
cat client.cer private.key > client.pem
```
## Dump SSL-keys
I suggest you to set the SSLKEYLOGFILE enviroment variable so you can record your traffic with Wireshark and decrypt it afterwards (Edit-Preferences-Protocols-TLS-(Pre)-Master-Secret log filename)
```
export SSLKEYLOGFILE=/root/keylogfile.txt
```

## Run mitmproxy / mitmweb / mitmdump
You can use mitmproxy, mitmweb or mitmdump. I prefered mitmweb
```
./mitmweb --verbose --web-host 0.0.0. --mode transparent --set client_certs=/root/client.pem --ssl-insecure -s /root/toniebox.cert-validity.py
```

## Using wireshark over ssh
You'll need to install tcpdump on you target system. I also disabled password auth for sudoing tcpdump.
```
$ nano /etc/sudoers.d/tcpdump

%pcap ALL=NOPASSWD: /usr/bin/tcpdump
```
Attach pcap-group to tcpdump
```
sudo chgrp pcap /usr/bin/tcpdump
sudo chmod 750 /usr/bin/tcpdump
```
I suggest you to ssh once into your machine to confirm the signature. Then you can run wireshark over the command and then enter the password to start tcpdump
```
ssh user@hackiebox sudo tcpdump -i ens19 -U -s0 -w - 'not port 22' | wireshark -k -i -
```

# Certificates helpers (just for legacy reasons!)
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

#!/usr/bin/env python3

import socket
import ssl
from cert_config import *

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile=ca_fake_certfile,
    keyfile=ca_fake_keyfile
)
context.load_verify_locations(cafile=box_client_certfile)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('0.0.0.0', 443))
    sock.listen(5)
    print("Start listening...")
    while True:
        print("Waiting for client...")
        conn, addr = sock.accept()
        print(conn)
        sslsoc = context.wrap_socket(conn, server_side=True)
        print(sslsoc)
        sslsoc.write(b'GET / HTTP/1.1\n')
        print("Data:", sslsoc.recv().decode())
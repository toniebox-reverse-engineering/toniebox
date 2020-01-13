#!/usr/bin/env python3

import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl

from cert_config import *

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=ca_fake_certfile)
context.verify_mode = ssl.CERT_REQUIRED #CERT_NONE CERT_REQUIRED CERT_OPTIONAL
context.load_cert_chain(
    certfile=host_fake_certfile,
    keyfile=host_fake_keyfile
)
context.load_verify_locations(cafile=box_client_certfile)

bindsocket = socket.socket()
bindsocket.bind(("prod.de.tbs.toys", 443))
#bindsocket.bind(("0.0.0.0", 443))
bindsocket.listen(5)

while True:
    print("Waiting for client")
    newsocket, fromaddr = bindsocket.accept()
    print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))
    conn = context.wrap_socket(newsocket, server_side=True)
    print("SSL established. Peer: {}".format(conn.getpeercert()))
    buf = b''  # Buffer to hold received client data
    try:
        while True:
            data = conn.recv(4096)
            if data:
                # Client sent us data. Append to buffer
                buf += data
                print(data)
            else:
                # No more data from client. Show buffer and close connection.
                #print("Received:", buf)
                break
    finally:
        print("Closing connection")
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
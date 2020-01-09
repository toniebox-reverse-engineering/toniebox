#!/usr/bin/env python3

import socket
import ssl
from cert_config import *

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=box_certfile)
context.load_cert_chain(
    certfile=box_client_certfile,
    keyfile=box_keyfile
)
   
print("Connecting to prod.de.tbs.toys...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    conn = context.wrap_socket(sock, server_side=False, server_hostname="prod.de.tbs.toys")
    conn.connect(("prod.de.tbs.toys", 443))
    print("SSL established. Peer: {}".format(conn.getpeercert()))
    print("Data:", conn.recv().decode())

print("Connecting to rtnl.bxcl.de...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    conn = context.wrap_socket(sock, server_side=False, server_hostname="rtnl.bxcl.de")
    conn.connect(("rtnl.bxcl.de", 443))
    print("SSL established. Peer: {}".format(conn.getpeercert()))
    print("Data:", conn.recv().decode())
    

#!/usr/bin/env python3
"""unix_client.py — клиент Unix-сокета: одновременно можно запускать много штук."""
import socket, sys

a, b = sys.argv[1], sys.argv[2]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect('/tmp/oscourse.sock')
s.sendall(f"{a} {b}".encode())
print(f"{a} + {b} = {s.recv(1024).decode()}")
s.close()


#!/usr/bin/env python3
"""fifo_client.py — клиент FIFO: шлёт два числа серверу и ждёт сумму."""
import os, sys

pid = str(os.getpid())
reply = f'/tmp/osfifo_reply_{pid}'
if os.path.exists(reply):
    os.unlink(reply)
os.mkfifo(reply)

a, b = sys.argv[1], sys.argv[2]
with open('/tmp/osfifo_req', 'w') as f:
    f.write(f"{pid} {a} {b}\n")

with open(reply) as r:
    print(f"{a} + {b} = {r.read()}")
os.unlink(reply)

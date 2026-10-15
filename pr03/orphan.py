
#!/usr/bin/env python3
"""orphan.py — родитель умирает первым, ребёнок становится сиротой."""
import os, time

pid = os.fork()
if pid > 0:
    print(f"parent {os.getpid()} exits, child = {pid}")
    os._exit(0)
print(f"child {os.getpid()} initial PPID = {os.getppid()}")
time.sleep(30)
print(f"child {os.getpid()} new PPID = {os.getppid()}  (усыновитель)")

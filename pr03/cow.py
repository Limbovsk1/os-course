
#!/usr/bin/env python3
"""cow.py — ленивое копирование памяти при fork (copy-on-write)."""
import os

SIZE = 64 * 1024 * 1024          # 64 МБ буфер
blob = bytearray(SIZE)

def rss_kb():
    for line in open('/proc/self/status'):
        if line.startswith('VmRSS'):
            return int(line.split()[1])

print(f"parent rss before fork: {rss_kb()} KB")
pid = os.fork()
if pid == 0:
    print(f"child rss right after fork: {rss_kb()} KB")
    for i in range(0, SIZE, 4096):   # пишем в каждую страницу -> ядро копирует их
        blob[i] = 1
    print(f"child rss after writing: {rss_kb()} KB  (выросло примерно на размер буфера)")
    os._exit(0)
os.waitpid(pid, 0)
print(f"parent rss at end: {rss_kb()} KB  (родитель не менял буфер -> его память общая)")

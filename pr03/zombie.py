
#!/usr/bin/env python3
"""zombie.py — родитель не вызывает wait 30 секунд, ребёнок висит зомби."""
import os, time

pid = os.fork()
if pid == 0:
    os._exit(0)            # ребёнок завершился сразу
print(f"parent={os.getpid()} zombie child={pid} — 30 секунд смотри: ps -o pid,stat,cmd -p {pid}")
time.sleep(30)
os.waitpid(pid, 0)         # теперь зомби «смывается»

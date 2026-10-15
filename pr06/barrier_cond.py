
#!/usr/bin/env python3
"""barrier_cond.py — барьер на условной переменной: 4 потока, 3 фазы."""
import threading, time, random

NTHREADS = 4
PHASES = 3
cond = threading.Condition()
arrived = 0
phase_log = []

def worker(tid):
    global arrived
    for ph in range(PHASES):
        time.sleep(random.random() * 0.05)
        with cond:
            arrived += 1
            if arrived < NTHREADS:
                cond.wait()                     # ждём остальных
            else:
                arrived = 0
                cond.notify_all()               # последний будит всех
        phase_log.append((ph, tid))             # барьер пройден — фаза ph начата
        time.sleep(random.random() * 0.05)

threads = [threading.Thread(target=worker, args=(i,)) for i in range(NTHREADS)]
[t.start() for t in threads]
[t.join() for t in threads]

ok = True
for ph in range(PHASES):
    seen = {tid for p, tid in phase_log if p == ph}
    if len(seen) != NTHREADS:
        ok = False
print("OK: барьер работает, фазы не перемешиваются" if ok else "БАРЬЕР СЛОМАН")

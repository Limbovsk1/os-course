
#!/usr/bin/env python3
"""runner.py — N дочерних процессов, каждый exec'ит команду; родитель ждёт всех."""
import os, sys, time

def main():
    if len(sys.argv) < 3:
        print("Usage: runner.py N command [args...]", file=sys.stderr)
        sys.exit(1)
    n = int(sys.argv[1])
    cmd = sys.argv[2:]
    pids = {}
    t0 = time.time()
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            try:
                os.execvp(cmd[0], cmd)
            except FileNotFoundError:
                print(f"child {i}: command not found: {cmd[0]}", file=sys.stderr)
                os._exit(127)
        pids[pid] = (i, time.time())
    results = {}
    while pids:
        pid, status = os.wait()
        i, start = pids.pop(pid)
        results[i] = (pid, os.waitstatus_to_exitcode(status), time.time() - start)
    print(f"total wall time: {time.time() - t0:.3f}s")
    for i in sorted(results):
        pid, code, dur = results[i]
        print(f"child {i}: pid={pid} exit={code} time={dur:.3f}s")

if __name__ == '__main__':
    main()

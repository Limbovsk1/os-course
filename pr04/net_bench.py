
#!/usr/bin/env python3
"""net_bench.py — загрузка 20 URL: последовательно / ThreadPool / ProcessPool."""
import time
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

URLS = [f"http://localhost:8000/file{i:02d}.bin" for i in range(20)]

def fetch(u):
    with urlopen(u, timeout=30) as r:
        return len(r.read())

def timed(fn, label):
    t0 = time.perf_counter()
    res = fn()
    dt = time.perf_counter() - t0
    print(f"{label:<28} {dt:.3f}s  bytes={sum(res)}")
    return dt

if __name__ == '__main__':
    timed(lambda: [fetch(u) for u in URLS], "последовательно")
    timed(lambda: list(ThreadPoolExecutor(8).map(fetch, URLS)), "ThreadPoolExecutor(8)")
    timed(lambda: list(ProcessPoolExecutor(8).map(fetch, URLS)), "ProcessPoolExecutor(8)")

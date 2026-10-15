
#!/usr/bin/env python3
"""bench_sum.py — сумма 10 млн чисел: 1 поток / 4 потока / 4 процесса.
Для каждого способа 3 повтора, берётся медиана. Генерация файла в замер не входит."""
import time, statistics
from threading import Thread
from multiprocessing import Process, Queue

PARTS = 4
REPS = 3

def read_nums(path='numbers.txt'):
    with open(path) as f:
        return [int(x) for x in f]

def make_chunks(nums, parts):
    n = len(nums); step = n // parts
    return [nums[i*step:(i+1)*step if i < parts - 1 else n] for i in range(parts)]

def run_single(chunk):
    t0 = time.perf_counter()
    s = sum(chunk)
    return time.perf_counter() - t0, s

def run_threads(chunks):
    res = [None] * len(chunks)
    def w(i, c): res[i] = sum(c)
    t0 = time.perf_counter()
    ts = [Thread(target=w, args=(i, c)) for i, c in enumerate(chunks)]
    [t.start() for t in ts]; [t.join() for t in ts]
    return time.perf_counter() - t0, sum(res)

def run_procs(chunks):
    q = Queue()
    def w(c, q): q.put(sum(c))
    t0 = time.perf_counter()
    ps = [Process(target=w, args=(c, q)) for c in chunks]
    [p.start() for p in ps]; [p.join() for p in ps]
    s = sum(q.get() for _ in ps)
    return time.perf_counter() - t0, s

def bench(fn, chunks, label):
    times, sums = [], None
    for _ in range(REPS):
        dt, s = fn(chunks if fn is not run_single else chunks[0] + chunks[1] + chunks[2] + chunks[3])
        times.append(dt); sums = s
    med = statistics.median(times)
    print(f"{label:<12} median={med:.3f}s  runs={[f'{t:.3f}' for t in times]}  sum={sums}")
    return med

if __name__ == '__main__':
    print("читаем файл (вне замера)...")
    nums = read_nums()
    chunks = make_chunks(nums, PARTS)
    bench(run_single, chunks, "1 поток")
    bench(run_threads, chunks, "4 потока")
    bench(run_procs, chunks, "4 процесса")

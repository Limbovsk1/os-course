
#!/usr/bin/env python3
"""shm_bench.py — передача 10^7 чисел между процессами: Pipe vs разделяемая память.

Pipe: pickle-сериализация + копирование через ядро (parent->kernel->child).
SharedMemory: одно копирование в общий сегмент, дочерний процесс (fork)
наследует отображение mmap и читает данные напрямую, без участия ядра.
"""
import time, array
import multiprocessing as mp
from multiprocessing import shared_memory

N = 10_000_000

def make_array():
    return array.array('q', range(N))

def via_pipe(arr):
    parent, child = mp.Pipe()
    t0 = time.perf_counter()
    p = mp.Process(target=lambda: (child.send(arr), child.close()))
    p.start()
    got = parent.recv()
    p.join()
    return time.perf_counter() - t0, sum(got)

def via_shm(arr):
    t0 = time.perf_counter()
    shm = shared_memory.SharedMemory(create=True, size=arr.itemsize * len(arr))
    done, ready = mp.Queue(), mp.Queue()
    p = mp.Process(target=child_shm, args=(shm, len(arr), done, ready))
    p.start()
    shm.buf[:] = arr.tobytes()          # единственное копирование — в общий сегмент
    ready.put(True)                     # без этого дочерний процесс прочитал бы мусок
    p.join()
    total = done.get()
    shm.close(); shm.unlink()
    return time.perf_counter() - t0, total

def child_shm(shm, n, q, ready):
    ready.get()                         # ждём, пока родитель запишет данные
    a = array.array('q')                # дочерний процесс УЖЕ видит mmap (наследство fork)
    a.frombytes(shm.buf[:n * 8])
    q.put(sum(a))

if __name__ == '__main__':
    print("генерация массива...")
    arr = make_array()
    dt, s = via_pipe(arr)
    print(f"Pipe:         {dt:.3f}s  sum={s}")
    dt, s = via_shm(arr)
    print(f"SharedMemory: {dt:.3f}s  sum={s}")

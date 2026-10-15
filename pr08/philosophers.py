
#!/usr/bin/env python3
"""philosophers.py — обедающие философы: deadlock и два исправления.

Режимы: naive (deadlock), ordered (вилки по возрастанию номеров), waiter (семафор N-1).
Синхронный старт через барьер гарантирует, что в naive все схватят левую вилку разом.
Статистика: сколько раз поел каждый, максимальное время ожидания вилки.
"""
import threading, time, sys, os

N = 5
ROUNDS = 20

def run(mode):
    forks = [threading.Lock() for _ in range(N)]
    waiter = threading.Semaphore(N - 1)            # официант: не более N-1 за столом
    start_gate = threading.Barrier(N)              # все берут левую одновременно
    held_gate = threading.Barrier(N)               # все ДЕРЖАТ левую -> naive = deadlock
    meals = [0] * N
    max_wait = [0.0] * N

    def philosopher(i):
        left, right = forks[i], forks[(i + 1) % N]
        if mode == 'ordered' and id(left) > id(right):
            left, right = right, left              # глобальный порядок захвата
        for _ in range(ROUNDS):
            start_gate.wait()
            t0 = time.time()
            if mode == 'waiter':
                waiter.acquire()
            left.acquire()
            if mode == 'naive':
                held_gate.wait()
            right.acquire()
            max_wait[i] = max(max_wait[i], time.time() - t0)
            time.sleep(0.002)                      # ест
            meals[i] += 1
            right.release()
            left.release()
            if mode == 'waiter':
                waiter.release()
            time.sleep(0.002)                      # думает

    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(N)]
    [t.start() for t in threads]
    t0 = time.time()
    for t in threads:
        t.join(timeout=2)                          # naive зависнет — не ждём вечно
    alive = sum(1 for t in threads if t.is_alive())
    dt = time.time() - t0
    print(f"mode={mode}: time={dt:.1f}s meals={meals} max_wait={[f'{w:.3f}' for w in max_wait]}"
          + (f"  <- ЗАВИС: {alive} потоков держат левые вилки (deadlock)" if alive else "  OK"), flush=True)
    os._exit(0)   # зависшие (non-daemon) потоки не дают процессу выйти — выходим явно

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else 'naive')

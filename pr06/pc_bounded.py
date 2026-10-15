
#!/usr/bin/env python3
"""pc_bounded.py — «производитель–потребитель», кольцевой буфер на 5 элементов.

Вариант (a): два семафора empty/full + мьютекс.
Вариант (b): мьютекс + условная переменная.
3 производителя, 2 потребителя, 1000 элементов.
"""
import threading, sys

BUF_SIZE = 5
ITEMS = 1000
NPROD, NCONS = 3, 2

buffer = [None] * BUF_SIZE
count = 0
head = tail = 0
consumed = [0] * ITEMS
errors = []

def run_semaphores():
    global count, head, tail
    empty = threading.Semaphore(BUF_SIZE)
    full = threading.Semaphore(0)
    mutex = threading.Lock()

    def producer(pid):
        global tail
        for i in range(ITEMS):
            if i % NPROD != pid:
                continue
            empty.acquire()
            with mutex:
                buffer[tail % BUF_SIZE] = i
                tail += 1
            full.release()

    def consumer(cid):
        global head
        quota = ITEMS // NCONS + (ITEMS % NCONS if cid == 0 else 0)
        for _ in range(quota):
            full.acquire()
            with mutex:
                item = buffer[head % BUF_SIZE]
                head += 1
            empty.release()
            consumed[item] += 1

    threads = ([threading.Thread(target=producer, args=(p,)) for p in range(NPROD)] +
               [threading.Thread(target=consumer, args=(c,)) for c in range(NCONS)])
    [t.start() for t in threads]
    [t.join() for t in threads]

def run_condition():
    global count, head, tail
    cond = threading.Condition()

    def producer(pid):
        global tail, count
        for i in range(ITEMS):
            if i % NPROD != pid:
                continue
            with cond:
                while count == BUF_SIZE:      # ждём, пока не освободится место
                    cond.wait()
                buffer[tail % BUF_SIZE] = i
                tail += 1
                count += 1
                cond.notify()

    def consumer(cid):
        global head, count
        quota = ITEMS // NCONS + (ITEMS % NCONS if cid == 0 else 0)
        for _ in range(quota):
            with cond:
                while count == 0:             # ждём появления элемента
                    cond.wait()
                item = buffer[head % BUF_SIZE]
                head += 1
                count -= 1
                cond.notify()
            consumed[item] += 1

    threads = ([threading.Thread(target=producer, args=(p,)) for p in range(NPROD)] +
               [threading.Thread(target=consumer, args=(c,)) for c in range(NCONS)])
    [t.start() for t in threads]
    [t.join() for t in threads]

def check(label):
    bad = [i for i in range(ITEMS) if consumed[i] != 1]
    if bad:
        print(f"[{label}] НАРУШЕНИЕ: элементов с нарушением: {len(bad)}, первые: {bad[:5]}")
    else:
        print(f"[{label}] OK: все {ITEMS} элементов потреблены ровно один раз")
    for i in range(ITEMS):
        consumed[i] = 0

if __name__ == '__main__':
    variant = sys.argv[1] if len(sys.argv) > 1 else 'sem'
    if variant == 'sem':
        run_semaphores()
        check('семафоры')
    else:
        run_condition()
        check('условная переменная')

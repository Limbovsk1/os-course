
#!/usr/bin/env python3
"""tracked_lock.py — TrackedLock: обёртка над threading.Lock, которая ведёт
граф ожидания в реальном времени и бросает исключение вместо зависания."""
import threading

class DeadlockError(RuntimeError):
    pass

class TrackedLock:
    _registry_lock = threading.Lock()
    _holders = {}        # lock_id -> thread_id владельца
    _edges = {}          # thread_id -> set(threads it waits for)

    def __init__(self, name):
        self._lock = threading.Lock()
        self.name = name

    def _would_deadlock(self, me, owner):
        seen, stack = set(), [owner]
        while stack:
            u = stack.pop()
            if u == me:
                return True
            if u in seen:
                continue
            seen.add(u)
            stack.extend(TrackedLock._edges.get(u, ()))
        return False

    def acquire(self):
        me = threading.get_ident()
        lid = id(self._lock)
        while True:
            with TrackedLock._registry_lock:
                owner = TrackedLock._holders.get(lid)
                if owner is None:
                    TrackedLock._holders[lid] = me
                    return
                if self._would_deadlock(me, owner):
                    raise DeadlockError(
                        f"deadlock: поток {me} ждёт {self.name}, удерживаемый {owner}")
                TrackedLock._edges.setdefault(me, set()).add(owner)
            # ждём владельца, не держа реестр
            while TrackedLock._holders.get(lid) is not None:
                threading.Event().wait(0.001)
            with TrackedLock._registry_lock:
                TrackedLock._edges.get(me, set()).discard(owner)

    def release(self):
        with TrackedLock._registry_lock:
            TrackedLock._holders.pop(id(self._lock), None)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *a):
        self.release()

if __name__ == '__main__':
    a, b = TrackedLock('a'), TrackedLock('b')

    def t1():
        with a:
            import time; time.sleep(0.1)
            with b:
                pass

    def t2():
        with b:
            import time; time.sleep(0.1)
            try:
                with a:                       # обратный порядок -> цикл
                    pass
            except DeadlockError as e:
                print(f"пойман вместо зависания: {e}")

    threading.Thread(target=t1).start()
    threading.Thread(target=t2).start()
    import time; time.sleep(1)

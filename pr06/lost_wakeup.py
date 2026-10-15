
#!/usr/bin/env python3
"""lost_wakeup.py — демонстрация потерянного пробуждения при if вместо while.

Ошибка: проверка условия и cond.wait() сделаны не атомарно — сигнал notify
успевает прийти ДО того, как поток встаёт в очередь ожидания, и теряется.
"""
import threading, time

cond = threading.Condition()
count = 0

def consumer():
    with cond:
        need_wait = (count == 0)
    # <-- окно: проверка сделана, но wait ещё не вызван
    if need_wait:                       # БАГ: должно быть while внутри одного with
        with cond:
            time.sleep(0.1)             # имитация задержки до wait()
            cond.wait(timeout=2)
            if count == 0:
                print("ПОТЕРЯННОЕ ПРОБУЖДЕНИЕ: notify пришёл раньше wait — сигнал потерян, жду дальше")
            else:
                print("сигнал пойман, данные есть")

def producer():
    time.sleep(0.05)                    # залетаем точно в окно между проверкой и wait
    with cond:
        count = 1
        cond.notify_all()
    print("producer: count=1, notify отправлен", flush=True)

c = threading.Thread(target=consumer)
c.start()
producer()
c.join()
print("лечение: проверять условие while-ом внутри той же критической секции")

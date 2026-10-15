
#!/usr/bin/env python3
"""memory_demo.py — потоки разделяют память, процессы (fork) — нет."""
import threading
import multiprocessing as mp

data = [0] * 1000

def tchange():
    for i in range(len(data)):
        data[i] = 1

t = threading.Thread(target=tchange)
t.start(); t.join()
print("после потока, родитель видит:", data[:5], "-> поток изменил ОБЩУЮ память")

data2 = [0] * 1000

def pchange():
    for i in range(len(data2)):
        data2[i] = 1

p = mp.Process(target=pchange)
p.start(); p.join()
print("после процесса, родитель видит:", data2[:5], "-> процесс работал со СВОЕЙ копией")

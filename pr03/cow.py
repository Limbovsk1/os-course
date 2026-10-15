#!/usr/bin/env python3
"""cow.py — ленивое копирование памяти при fork (copy-on-write).

Смотрим не на VmRSS (на новых ядрах сумма почти не меняется — страницы
уже учтены), а на Shared_Dirty -> Private_Dirty: общие страницы при записи
копируются и становятся личными ребёнка.
"""
import os

SIZE = 64 * 1024 * 1024            # 64 МБ буфер
blob = bytearray(SIZE)

def show(tag):
    m = {}
    for line in open('/proc/self/smaps_rollup'):
        if line.startswith(('Rss', 'Shared_Dirty', 'Private_Dirty')):
            k, v = line.split(':')
            m[k.strip()] = int(v.split()[0])
    print(f"{tag:<26} RSS={m['Rss']:>7} KB  Shared_Dirty={m['Shared_Dirty']:>7} KB  "
          f"Private_Dirty={m['Private_Dirty']:>7} KB")

show("parent before fork:")
pid = os.fork()
if pid == 0:
    show("child right after fork:")
    for i in range(0, SIZE, 4096):   # пишем в каждую страницу -> ядро копирует её
        blob[i] = 1
    show("child after writing:")
    os._exit(0)
os.waitpid(pid, 0)
show("parent at end:")

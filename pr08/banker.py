
#!/usr/bin/env python3
"""banker.py — алгоритм банкира: проверка безопасности + обработка запросов.

Формат файла состояния:
    available 3 3 2
    max 7 5 3
    max 3 2 2
    ...
    allocation 0 1 0
    ...
Запросы читаются со stdin: "PID r1 r2 ..." (пример: "P1 1 0 2"), пустая строка — выход.
"""
import sys

def load(path):
    avail, maxv, alloc = [], [], []
    for line in open(path):
        p = line.split()
        if not p or p[0].startswith('#'):
            continue
        if p[0] == 'available':
            avail = list(map(int, p[1:]))
        elif p[0] == 'max':
            maxv.append(list(map(int, p[1:])))
        elif p[0] == 'allocation':
            alloc.append(list(map(int, p[1:])))
    return avail, maxv, alloc

def is_safe(avail, alloc, maxv):
    n, m = len(alloc), len(avail)
    need = [[maxv[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    work, finish, seq = avail[:], [False] * n, []
    while len(seq) < n:
        progressed = False
        for i in range(n):
            if (not finish[i]) and all(need[i][j] <= work[j] for j in range(m)):
                work = [work[j] + alloc[i][j] for j in range(m)]
                finish[i] = True
                seq.append(f"P{i}")
                progressed = True
        if not progressed:
            return False, seq
    return True, seq

def request(avail, alloc, maxv, i, req):
    m = len(avail)
    if any(req[j] > maxv[i][j] - alloc[i][j] for j in range(m)):
        return 'ERROR: запрос превышает заявку (Need)'
    if any(req[j] > avail[j] for j in range(m)):
        return 'WAIT: ресурсов сейчас нет'
    for j in range(m):                      # пробуем выделить
        avail[j] -= req[j]
        alloc[i][j] += req[j]
    safe, _ = is_safe(avail, alloc, maxv)
    if safe:
        return 'GRANT (состояние осталось безопасным)'
    for j in range(m):                      # откат
        avail[j] += req[j]
        alloc[i][j] -= req[j]
    return 'ROLLBACK: состояние стало небезопасным, запрос отклонён'

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'bank1.txt'
    avail, maxv, alloc = load(path)
    safe, seq = is_safe(avail, alloc, maxv)
    print(f'{"SAFE" if safe else "UNSAFE"}, последовательность: {" ".join(seq) if safe else "-"}')
    print('Вводи запросы вида "P1 1 0 2", пустая строка — выход:')
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        p = line.split()
        i, req = int(p[0][1:]), list(map(int, p[1:]))
        print(f'  request {p[0]} {req}: {request(avail, alloc, maxv, i, req)}')

if __name__ == '__main__':
    main()

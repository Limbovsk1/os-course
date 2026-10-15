
#!/usr/bin/env python3
"""dd.py — детектор взаимоблокировок по журналу событий для единичных ресурсов.

Журнал (файл): строки вида
    P1 acquire R1
    P2 wait R1
    P3 release R2
Граф ожидания: ребро A -> B, если A ждёт ресурс, удерживаемый B. Цикл = deadlock.
"""
import sys
from collections import defaultdict

def build_graph(logfile):
    holder, waiting = {}, {}
    edges = defaultdict(set)
    for line in open(logfile):
        p = line.split()
        if len(p) < 3:
            continue
        pid, ev, res = p[0], p[1], p[2]
        if ev == 'acquire':
            holder[res] = pid
            waiting.pop(pid, None)
        elif ev == 'release':
            holder.pop(res, None)
        elif ev == 'wait':
            waiting[pid] = res
            if res in holder:
                edges[pid].add(holder[res])
    return edges

def find_cycle(edges):
    color, stack, cycles = {}, [], []
    sys.setrecursionlimit(10000)
    def dfs(u):
        color[u] = 1
        stack.append(u)
        for v in edges.get(u, ()):
            if color.get(v) == 1:
                cycles.append(stack[stack.index(v):] + [v])
            elif color.get(v, 0) == 0:
                dfs(v)
        stack.pop()
        color[u] = 2
    for u in list(edges):
        if color.get(u, 0) == 0:
            dfs(u)
    return cycles

if __name__ == '__main__':
    edges = build_graph(sys.argv[1])
    print('рёбра графа ожидания:', {k: sorted(v) for k, v in edges.items()})
    cycles = find_cycle(edges)
    if cycles:
        for c in cycles:
            print('DEADLOCK: ' + ' -> '.join(c))
    else:
        print('циклов нет — deadlock не обнаружен')

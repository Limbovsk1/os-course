
#!/usr/bin/env python3
"""ptree.py — дерево процессов текущего пользователя по данным /proc (без ps)."""
import os
from collections import defaultdict

ME = os.getuid()
procs = {}

for pid in filter(str.isdigit, os.listdir('/proc')):
    try:
        info = {}
        for line in open(f'/proc/{pid}/status'):
            if ':\t' in line:
                k, v = line.split(':\t', 1)
                info[k] = v.strip()
        cmd = open(f'/proc/{pid}/comm').read().strip()
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        continue
    try:
        uid = int(info['Uid'].split()[0])
        ppid = int(info['PPid'])
    except KeyError:
        continue
    if uid != ME:
        continue
    procs[int(pid)] = (ppid,
                       info['State'].split()[0],
                       int(info['VmRSS'].split()[0]) if 'VmRSS' in info else 0,
                       cmd)

children = defaultdict(list)
for pid, (ppid, *_rest) in procs.items():
    children[ppid].append(pid)

def walk(pid, depth):
    if pid not in procs:
        return
    _ppid, state, rss, cmd = procs[pid]
    print('  ' * depth + f'{pid} [{state}] {rss:>8} KB  {cmd}')
    for c in sorted(children.get(pid, [])):
        walk(c, depth + 1)

roots = [p for p in procs if procs[p][0] not in procs]
for r in sorted(roots):
    walk(r, 0)

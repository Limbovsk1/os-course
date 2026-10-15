
#!/usr/bin/env python3
"""sched.py — симулятор планирования CPU: FCFS, SJF, SRTF, Priority, RR.

Формат входного файла (строка на процесс):
    PID arrival burst priority
Соглашение для RR: процесс, прибывший в момент t, ставится в очередь
раньше процесса, вытесненного в тот же момент t.
"""
import argparse

class Proc:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid, self.arrival, self.burst, self.priority = pid, arrival, burst, priority
        self.remaining = burst
        self.start = None
        self.completion = None
    def turnaround(self): return self.completion - self.arrival
    def waiting(self):    return self.turnaround() - self.burst
    def response(self):   return self.start - self.arrival

def parse(path):
    procs = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        p = line.split()
        procs.append(Proc(p[0], int(p[1]), int(p[2]), int(p[3]) if len(p) > 3 else 0))
    return procs

def simulate(processes, algorithm, quantum=None, aging=False):
    procs  = [Proc(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    n      = len(procs)
    by_arr = sorted(procs, key=lambda p: (p.arrival, p.pid))
    ready, waiting = [], {p.pid: 0 for p in procs}
    t = 0; idx = 0; done = 0
    cur = None; preempted = None; qleft = 0
    intervals = []

    def eff(p):  # эффективный приоритет (меньше = лучше)
        return p.priority - waiting[p.pid] if aging else p.priority

    def pick():
        if algorithm == 'fcfs':
            ready.sort(key=lambda p: (p.arrival, p.pid))
        elif algorithm == 'sjf':
            ready.sort(key=lambda p: (p.remaining, p.arrival))
        elif algorithm == 'srtf':
            ready.sort(key=lambda p: (p.remaining, p.arrival))
        elif algorithm == 'priority':
            ready.sort(key=lambda p: (eff(p), p.arrival))
        return ready.pop(0)

    while done < n:
        while idx < n and by_arr[idx].arrival <= t:
            ready.append(by_arr[idx]); idx += 1
        if preempted is not None:            # вытесненный — ПОСЛЕ прибывших в момент t
            ready.append(preempted); preempted = None
        if not ready and cur is None:
            t = by_arr[idx].arrival
            continue
        # вытеснение
        if cur is not None and ready:
            if algorithm == 'srtf':
                rival = min(ready, key=lambda p: (p.remaining, p.arrival))
                if rival.remaining < cur.remaining:
                    ready.append(cur); cur = None
            elif algorithm == 'priority':
                rival = min(ready, key=lambda p: (eff(p), p.arrival))
                if eff(rival) < eff(cur):
                    ready.append(cur); cur = None
        if cur is None:
            cur = pick()
            if cur.start is None:
                cur.start = t
            qleft = quantum if algorithm == 'rr' else 0
            intervals.append([cur.pid, t, t])
        # один тик CPU
        intervals[-1][2] = t + 1
        cur.remaining -= 1
        for p in ready:
            waiting[p.pid] += 1
        t += 1
        if cur.remaining == 0:
            cur.completion = t; done += 1; cur = None
        elif algorithm == 'rr' and (qleft := qleft - 1) == 0:
            preempted = cur; cur = None

    return procs, [tuple(x) for x in intervals]

def metrics(procs, intervals):
    avg_w   = sum(p.waiting() for p in procs) / len(procs)
    avg_tat = sum(p.turnaround() for p in procs) / len(procs)
    avg_r   = sum(p.response() for p in procs) / len(procs)
    busy    = sum(e - s for _p, s, e in intervals)
    span    = max(p.completion for p in procs) - min(p.arrival for p in procs)
    cpu     = 100.0 * busy / span
    return avg_w, avg_tat, avg_r, cpu, len(intervals)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--algo', required=True,
                    choices=['fcfs', 'sjf', 'srtf', 'priority', 'rr'])
    ap.add_argument('--quantum', type=int, default=3)
    ap.add_argument('--aging', action='store_true')
    ap.add_argument('--gantt', action='store_true')
    ap.add_argument('file')
    a = ap.parse_args()

    procs, intervals = simulate(parse(a.file), a.algo, a.quantum, a.aging)
    if a.gantt:
        for pid, s, e in intervals:
            print(f'  {s:>3}-{e:<3} {pid}')
    w, tat, r, cpu, cs = metrics(procs, intervals)
    print(f'algo={a.algo} q={a.quantum}' + (' aging' if a.aging else ''))
    print(f'avg_waiting={w:.2f} avg_turnaround={tat:.2f} avg_response={r:.2f} '
          f'cpu={cpu:.1f}% ctx_switches={cs}')
    for p in sorted(procs, key=lambda p: p.pid):
        print(f'  {p.pid}: completion={p.completion} turnaround={p.turnaround()} '
              f'waiting={p.waiting()} response={p.response()}')

if __name__ == '__main__':
    main()

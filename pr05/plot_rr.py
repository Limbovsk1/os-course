
#!/usr/bin/env python3
"""plot_rr.py — график «квант RR (1..10) -> среднее ожидание и число переключений».
Данные — реальные замеры на set2.txt (см. README, задание 3)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

QUANTUM = list(range(1, 11))
WAITING = [123.35, 120.10, 115.15, 114.80, 124.85, 105.35, 100.15, 103.45, 95.45, 97.15]
SWITCHES = [196, 101, 69, 53, 44, 38, 34, 31, 29, 27]

fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.plot(QUANTUM, WAITING, 'bo-', label='среднее ожидание')
ax1.set_xlabel('квант RR')
ax1.set_ylabel('среднее ожидание', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(QUANTUM, SWITCHES, 'rs--', label='переключения контекста')
ax2.set_ylabel('число переключений контекста', color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title('RR на set2: компромисс кванта')
fig.tight_layout()
fig.savefig('rr_sweep.png', dpi=120)
print("сохранено: rr_sweep.png")

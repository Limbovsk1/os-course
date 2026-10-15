
"""gen_sets.py — генерирует set2.txt (CPU-bound) и set3.txt (короткие + один длинный)
и starve.txt (демонстрация голодаания приоритетного планирования)."""
import random
random.seed(7)

with open('set2.txt', 'w') as f:
    for i in range(20):
        f.write(f"P{i} {random.randint(0, 30)} {random.randint(5, 20)} {random.randint(1, 5)}\n")

with open('set3.txt', 'w') as f:
    for i in range(19):
        f.write(f"P{i} {random.randint(0, 10)} {random.randint(1, 3)} {random.randint(1, 5)}\n")
    f.write("P19 1 40 3\n")   # один длинный процесс

# голодаание: низкоприоритетный длинный процесс + поток высокоприоритетных
with open('starve.txt', 'w') as f:
    f.write("LP 0 60 10\n")
    for k in range(15):
        f.write(f"HP{k} {2 + k*4} 3 1\n")
print("set2.txt, set3.txt, starve.txt созданы")

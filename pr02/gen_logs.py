
import random, os

random.seed(42)
os.makedirs('data', exist_ok=True)
mods = ['net', 'auth', 'db', 'disk', 'fs']

for i in range(1, 51):
    with open(f'data/{i:02d}.log', 'w') as f:
        for j in range(random.randint(50, 200)):
            t = (f"2026-02-{random.randint(10, 28):02d} "
                 f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}")
            lvl = random.choices(['ERROR', 'WARN', 'INFO'], weights=[2, 3, 10])[0]
            f.write(f"{t} {lvl} module={random.choice(mods)} msg=event {j}\n")

print("50 файлов создано в data/")

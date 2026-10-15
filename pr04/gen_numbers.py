
import random

random.seed(1)
with open('numbers.txt', 'w') as f:
    for _ in range(10_000_000):
        f.write(f"{random.randint(-10**9, 10**9)}\n")
print("numbers.txt: 10 млн чисел")

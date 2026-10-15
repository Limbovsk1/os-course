
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data/01.log"

total = 0
with open(path, "rb") as f:
    while True:
        chunk = f.read(65536)
        if not chunk:
            break
        total += len(chunk)

print(f"{path}: {total} bytes")

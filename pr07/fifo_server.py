
#!/usr/bin/env python3
"""fifo_server.py — сервер на именованном канале: принимает "pid a b", возвращает сумму."""
import os

REQ = '/tmp/osfifo_req'

def main():
    if os.path.exists(REQ):
        os.unlink(REQ)
    os.mkfifo(REQ)
    print(f"server: жду запросов в {REQ} (Ctrl+C для выхода)")
    try:
        while True:
            with open(REQ) as f:            # блокируемся, пока клиент не откроет на запись
                for line in f:
                    pid, a, b = line.split()
                    reply = f'/tmp/osfifo_reply_{pid}'
                    with open(reply, 'w') as r:
                        r.write(str(int(a) + int(b)))
    except KeyboardInterrupt:
        pass
    finally:
        if os.path.exists(REQ):
            os.unlink(REQ)

if __name__ == '__main__':
    main()

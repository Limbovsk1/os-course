
#!/usr/bin/env python3
"""unix_server.py — то же на Unix-сокете: процесс на каждого клиента (параллельно)."""
import os, socket, multiprocessing as mp

SOCK = '/tmp/oscourse.sock'

def handle(conn):
    data = conn.recv(1024).decode()
    a, b = data.split()
    conn.sendall(str(int(a) + int(b)).encode())
    conn.close()

def main():
    if os.path.exists(SOCK):
        os.unlink(SOCK)
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(SOCK)
    srv.listen(5)
    print(f"server: слушаю {SOCK} (Ctrl+C для выхода)")
    try:
        while True:
            conn, _ = srv.accept()
            mp.Process(target=handle, args=(conn,), daemon=True).start()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        if os.path.exists(SOCK):
            os.unlink(SOCK)

if __name__ == '__main__':
    main()

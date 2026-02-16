import socket
import sys
import time

s = socket.socket()
port = int(sys.argv[1])
s.bind(('', port))
s.listen(5)
print('Server ready')

while True:
    conn, addr = s.accept()
    data = conn.recv(1024).decode()
    if data.startswith('s'):
        conn.send(b'200 OK: Ready\n')
        for i in range(100):
            msg = conn.recv(65536).decode()
            if msg.startswith('m'):
                conn.send(msg.encode())
        conn.send(b'200 OK: Closing\n')
    conn.close()

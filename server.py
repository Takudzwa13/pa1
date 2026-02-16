import socket
import sys
import time

# Handle client connection - receives probes and echoes back
def handle_client(conn):
    # Receive setup message from client
    data = conn.recv(1024).decode().strip()
    parts = data.split()
    
    # Check if message is valid setup phase
    if parts[0] != 's':
        conn.sendall(b'404 ERROR\n')
        return
    
    # Get measurement parameters
    msg_size = int(parts[2])
    probes = int(parts[3])
    delay = float(parts[4])
    
    # Send ready message
    conn.sendall(b'200 OK: Ready\n')
    print(f"Client connected - Size:{msg_size} Probes:{probes}")
    
    # Echo each probe back to client
    for i in range(probes):
        probe = conn.recv(65536).decode().strip()
        if not probe or probe == 't':
            break
        p_parts = probe.split(' ', 2)
        if delay > 0:
            time.sleep(delay/1000)
        conn.sendall(f'm {p_parts[1]} {p_parts[2]}\n'.encode())
    
    # Close connection
    conn.sendall(b'200 OK: Closing\n')
    conn.close()

# Main server
port = int(sys.argv[1])
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
s.listen(5)
print(f'Server listening on port {port}')

while True:
    conn, addr = s.accept()
    handle_client(conn)

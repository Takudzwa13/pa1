import socket
import time
import sys
import statistics
import random
import string

# Generate random payload of given size
def make_payload(size):
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size))

# Payload sizes from assignment
sizes = [11, 101, 201, 420, 840, 1200, 1100, 2200, 4700, 8300, 16000, 32000]

print('=' * 60)
print('RTT MEASUREMENTS')
print('=' * 60)
print(f"{'Size(B)':>8} {'Mean(ms)':>12} {'95% CI':>20}")
print('-' * 60)

# Test each payload size
for size in sizes:
    rtts = []
    print(f"\nTesting {size} bytes...")
    
    # Send 100 probes for this size
    for probe in range(100):
        try:
            # Create socket and connect
            s = socket.socket()
            s.connect(('10.0.0.2', 58000))
            
            # Send setup message
            s.sendall(f's rtt {size} 100 0\n'.encode())
            response = s.recv(1024).decode()
            if '200 OK' not in response:
                s.close()
                continue
            
            # Send probe and measure time
            payload = make_payload(size)
            start = time.perf_counter()
            s.sendall(f'm {payload} {probe+1}\n'.encode())
            
            # Receive echo
            received = b''
            while len(received) < len(f'm {payload} {probe+1}\n'):
                received += s.recv(4096)
            end = time.perf_counter()
            
            # Calculate RTT in milliseconds
            rtts.append((end - start) * 1000)
            s.close()
            
            # Show progress
            if (probe + 1) % 20 == 0:
                print(f"  Completed {probe+1}/100 probes")
                
        except Exception as e:
            continue
    
    # Calculate statistics
    if rtts:
        mean = sum(rtts) / len(rtts)
        if len(rtts) > 1:
            variance = sum((x - mean) ** 2 for x in rtts) / (len(rtts) - 1)
            std = variance ** 0.5
            ci = 1.96 * std / (len(rtts) ** 0.5)
        else:
            ci = 0
        
        print(f"{size:>8} {mean:>11.2f}   [{mean-ci:>7.2f}, {mean+ci:>7.2f}]")
    else:
        print(f"{size:>8} {'FAILED':>12}")

print('\n' + '=' * 60)
print('DONE')
print('=' * 60)

import socket
import time
import statistics

sizes = [11, 101, 201, 420, 840, 1200, 1100, 2200, 4700, 8300, 16000, 32000]

print('Size    Mean(ms)    95% CI')
print('---------------------------')

for size in sizes:
    times = []
    for i in range(100):
        try:
            s = socket.socket()
            s.connect(('10.0.0.2', 58000))
            s.send(('s rtt ' + str(size) + ' 100 0\n').encode())
            s.recv(1024)
            
            data = 'x' * size
            start = time.time()
            s.send(('m ' + data + ' ' + str(i+1) + '\n').encode())
            s.recv(65536)
            end = time.time()
            
            times.append((end - start) * 1000)
            s.close()
        except:
            pass
    
    if times:
        m = sum(times)/len(times)
        std = (sum((x-m)**2 for x in times)/len(times))**0.5
        ci = 1.96 * std/(len(times)**0.5)
        print(str(size) + '     ' + str(round(m,2)) + '      [' + str(round(m-ci,2)) + ', ' + str(round(m+ci,2)) + ']')

print('\nDone')

#!/usr/bin/env python3

import socket
import time as time
HOST = '192.168.0.7'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

while True:    
    s.listen()
    conn, addr = s.accept()
    
    time.sleep(0.5)
    conn.sendall(b'ok to send')
    
    print('waiting for packets')
    while True:
    
            data = conn.recv(1024)
            if not data:
                print('break')
                break
            print(data.decode())
            
            
            
            
            
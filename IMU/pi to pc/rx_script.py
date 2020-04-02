#!/usr/bin/env python3

import socket
import time as time
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
while True:    
    s.listen()
    conn, addr = s.accept()
    
    time.sleep(1)
    conn.sendall(b'not ok to send')

    while True:
    
            data = conn.recv(1024)
            if not data:
                print('break')
                break
            print(data.decode())
            
            
            
            
            
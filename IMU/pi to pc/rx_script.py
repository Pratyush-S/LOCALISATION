#!/usr/bin/env python3

import socket

HOST = '192.168.0.7'  # Standard loopback interface address (localhost)
PORT = 6543        # Port to listen on (non-privileged ports are > 1023)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
while True:

    s.listen()
    conn, addr = s.accept()
    #with conn:
       # print('Connected by', addr)
    while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data.decode())
            #conn.sendall(data)
            
        
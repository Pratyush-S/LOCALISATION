#!/usr/bin/env python3

import socket

HOST = '192.168.0.7'  # The server's hostname or IP address
PORT = 65432        # The port used by the server







status=0
while True:
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    while status==0:
        print('waiting for ok')
        data = s.recv(1024)
        if data.decode()=='ok to send':
            status=1
     
    #can use pass
    s.sendall(b'send')

    status=0    
    






    
    
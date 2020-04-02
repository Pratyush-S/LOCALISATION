
import socket

HOST = '192.168.0.15'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

x='Loop Time  0.07 # -0.82  0.09 -9.77#'

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(x.encode())
   # data = s.recv(1024)

#print('Received', repr(data))

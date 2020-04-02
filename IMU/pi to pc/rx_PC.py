#!/usr/bin/env python3

import socket
import pandas as pd
HOST = '192.168.0.7'  # Standard loopback interface address (localhost)
PORT = 6543        # Port to listen on (non-privileged ports are > 1023)

#buffer dataframe
sensor_dataframe=pd.read_excel('sensor-dataframe.xlsx')
#sensor_dataframe=pd.DataFrame()

    
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
                #conn.close()
            
            
                #string.replace(old, new, count)
                #a=data.split(',')
                
                #removing blank spaces
                data_string=data.replace(' ','')
                #splitting strings at ,      
                data_list=data_string.split(',')
              
                d=[float(i) for i in data_list]
                
                #creating dataframe row for insertion
                
                
                row_df_pres = pd.DataFrame([d])
                
            
                #appending to dataframe
                sensor_dataframe = pd.concat([sensor_dataframe,row_df], ignore_index=True)    
                  
                sensor_dataframe.to_excel('sensor-dataframe.xlsx')

            
    
            
            
            
            
            
        
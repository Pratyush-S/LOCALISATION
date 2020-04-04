#!/usr/bin/env python3

import socket
import pandas as pd
import time as time
import matplotlib.pyplot as plt

HOST = '192.168.0.7'  # Standard loopback interface address (localhost)
PORT = 6543        # Port to listen on (non-privileged ports are > 1023)
################################################################################

          
def send_to_excel(data_byte):
    global sensor_dataframe
    
    data_char=data_byte.decode()
    #removing blank spaces
    data_string=data_char.replace(' ','')
    #splitting strings at ,      
    data_list=data_string.split(',')
              
    #creating dataframe row for insertion        
    row_df = pd.DataFrame([data_list])
            
    #appending to dataframe
    sensor_dataframe = pd.concat([sensor_dataframe,row_df], ignore_index=False)    

    sensor_dataframe.to_excel('sensor-dataframe.xlsx')
     

################################################################################
def send_buffer_plot(data_byte):
    global  sensor_dataframe
    
    data_char=data_byte.decode()
    #removing blank spaces
    data_string=data_char.replace(' ','')
    #splitting strings at ,      
    data_list=data_string.split(',')
              
    #creating dataframe row for insertion        
    row_df = pd.DataFrame([data_list])
        
        
    #appending to dataframe
    sensor_dataframe = pd.concat([sensor_dataframe,row_df], ignore_index=False)    
    
    j=3
    plt.subplot(311)
    plt.plot([float(i) for i in sensor_dataframe[j+0].values])
    plt.subplot(312)
    plt.plot([float(i) for i in sensor_dataframe[j+1].values])
    plt.subplot(313)
    plt.plot([float(i) for i in sensor_dataframe[j+2].values])


    plt.show()
                                                                                               


#buffer dataframe
#sensor_dataframe=pd.read_excel('sensor-dataframe.xlsx')
sensor_dataframe=pd.DataFrame()
#sensor_dataframe.columns
#sensor_dataframe=sensor_dataframe[[0,1,2,3,4,5,6,7]]
 
   
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

while True:

    s.listen()
    conn, addr = s.accept()
       
       
    conn.sendall(b'ok to send')
    while True:
                data = conn.recv(1024)
                if not data:
                    break
                    print('break')
                print(data.decode())
                
#                send_to_excel(data)
                send_buffer_plot(data)
                print('sent to excel')
                
                conn.sendall(b'ok to send')
                #conn.close()
                
                  
            

        
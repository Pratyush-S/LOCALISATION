from flask import Flask
from flask_restful import Resource, Api
import IMU
import time
import math
import datetime
import os

app = Flask(__name__)
api = Api(app)


# If the IMU is upside down (Skull logo facing up), change this value to 1
IMU_UPSIDE_DOWN = 1
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant
g=9.80665


IMU.detectIMU()
IMU.initIMU()


print('apple')
    
 

Accx_bias=0
Accy_bias=0
Accz_bias=0
    
class TempHum(Resource):

        
    def sensor_caliberate():
        k=0        
        ax=[]
        ay=[]
        az=[]
        
        global Accx_bias
        global Accy_bias
        global Accz_bias
        
        while k<20:
            ACCx = IMU.readACCx()
            ACCy = IMU.readACCy()
            ACCz = IMU.readACCz()
            GYRx = IMU.readGYRx()
            GYRy = IMU.readGYRy()
            GYRz = IMU.readGYRz()
            MAGx = IMU.readMAGx()
            MAGy = IMU.readMAGy()
            MAGz = IMU.readMAGz()
        
            Ay = (((ACCy * g* 0.244)/1000))
            Ax = (((ACCx * g* 0.244)/1000))
            Az = (((ACCz * g* 0.244)/1000))
          
            ax.append(xG)
            ay.append(yG)
            az.append(zG)
          
            
        Accx_bias=sum(ax)/len(ax)
        Accy_bias=sum(ay)/len(ay)
        Accz_bias=sum(az)/len(az)
        
        Dict = {'Accx_bias':Accx_bias, 'Accy_bias':Accy_bias,'Accz_bias':Accz_bias}
        return Dict
        
            
            
    def get(self):

        k=0        
        ax=[]
        ay=[]
        az=[]
        
        global Accx_bias
        global Accy_bias
        global Accz_bias
        
        while k<20:
            ACCx = IMU.readACCx()
            ACCy = IMU.readACCy()
            ACCz = IMU.readACCz()
            GYRx = IMU.readGYRx()
            GYRy = IMU.readGYRy()
            GYRz = IMU.readGYRz()
            MAGx = IMU.readMAGx()
            MAGy = IMU.readMAGy()
            MAGz = IMU.readMAGz()
        
            Ay = (((ACCy * g* 0.244)/1000))
            Ax = (((ACCx * g* 0.244)/1000))
            Az = (((ACCz * g* 0.244)/1000))
          
            ax.append(xG)
            ay.append(yG)
            az.append(zG)
          
            
        meanx=sum(ax)/len(ax)-Accx_bias
        meany=sum(ay)/len(ay)-Accy_bias
        meanz=sum(az)/len(az)-Accz_bias
        

#       Dict = {xG: 'accx', yG: 'Accy', zG: 'accz',gyrx: 'gyrx', gyry: 'gyry', gyrz: 'gyrz',maxx: 'maxx', magy: 'magy', magz: 'magz'}    
        Dict = {'accx':meanx, 'Accy':meany,'accz':meanz}
        return Dict
        

api.add_resource(TempHum, '/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8050, debug=True)

    
    
#!/usr/bin/python
#
#       This is the base code needed to get usable angles from a BerryIMU
#       using a Complementary filter. The readings can be improved by
#       adding more filters, E.g Kalman, Low pass, median filter, etc..
#       See berryIMU.py for more advanced code.
#
#       For this code to work correctly, BerryIMU must be facing the
#       correct way up. This is when the Skull Logo on the PCB is facing down.
#
#       Both the BerryIMUv1 and BerryIMUv2 are supported
#
#       This script is python 2.7 and 3 compatible
#
#       Feel free to do whatever you like with this code.
#       Distributed as-is; no warranty is given.
#
#       http://ozzmaker.com/


import time
import math
import IMU
import datetime
import os
import socket



HOST = '192.168.0.7'  # The server's hostname or IP address
PORT = 6543        # The port used by the server


g=9.8
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.30      # Complementary filter constant

################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading values.

magXmin =  0
magYmin =  0
magZmin =  0
magXmax =  0
magYmax =  0
magZmax =  0

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0
CFangleZ = 0.0



IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


a = datetime.datetime.now()


#def read_sensors():
while True:
    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()

########################################################################################## magnetic field intensity
    #Apply compass calibration
    MAGx -= (magXmin + magXmax) /2
    MAGy -= (magYmin + magYmax) /2
    MAGz -= (magZmin + magZmax) /2

    ##Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)
    outputString = ""
    outputlist=[]
    #outputString = "Loop Time %5.2f " % ( LP )


    #Convert Gyro raw to degrees per second
    rate_gyr_x =  GYRx * G_GAIN
    rate_gyr_y =  GYRy * G_GAIN
    rate_gyr_z =  GYRz * G_GAIN



########################################################################################## Linear Acceleration in m/s^2
    yG = (ACCy * g* 0.244)/1000
    xG = (ACCx *g* 0.244)/1000
    zG = (ACCz * g *0.244)/1000

########################################################################################## GYRO in ANGLE degrees
    #Calculate the angles from the gyro.
    gyroXangle+=rate_gyr_x*LP
    gyroYangle+=rate_gyr_y*LP
    gyroZangle+=rate_gyr_z*LP

########################################################################################## angular acceleration 

    #Convert Accelerometer values to degrees
    AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
    AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG
    AccZangle =  (math.atan2(ACCx,ACCy)*RAD_TO_DEG)

    #convert the values to -180 and +180
    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0

    outputString += " %5.2f, %5.2f, %5.2f," % (xG,yG,zG)
    outputString += " %5.2f, %5.2f, %5.2f  " % (gyroXangle,gyroYangle,gyroZangle)
    
    
    print(outputString)

    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(outputString.encode())



    #slow program down a bit, makes the output more readable
    time.sleep(1)



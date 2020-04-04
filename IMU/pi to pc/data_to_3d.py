from mpl_toolkits import mplot3d

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')


from matplotlib.pyplot import figure
figure(num=None, figsize=(1, 1), dpi=80, facecolor='w', edgecolor='k')



# Data for a three-dimensional line
zline = []
xline = []
yline = []


append_val(1000,1000,1000)

def append_val(x,y,z):
    global zline
    global yline
    global xline

    zline.append(z)
    xline.append(x)
    yline.append(y)


    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection='3d')    
    ax.plot3D(xline, yline, zline, 'gray')






















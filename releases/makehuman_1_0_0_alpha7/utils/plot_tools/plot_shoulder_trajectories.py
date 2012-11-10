import sys
sys.path.append("/home/manuel/archive/archive_makehuman/makehuman_src/mh_core")
sys.path.append("C:\Documents and Settings\Segreteria\Desktop\makehuman\mh_core")

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from aljabr import *
fig = plt.figure()
ax = Axes3D(fig)    

def rotation(point, theta, center = (0,0,0)):
    rotX = theta[0]/57.295779506
    rotY = theta[1]/57.295779506
    rotZ = theta[2]/57.295779506
    Rmt = makeRotEulerMtx3D(rotX,rotY,rotZ)    
    return rotatePoint(center,point,Rmt)

    
def interpolateVector(vect1,vect2,fact):
    vectDiff = vmul(vsub(vect2, vect1),fact)
    return vadd(vect1,vectDiff)

def drawTrajectory(target):
    x = []
    y = []
    z = []
    vect1 = (0,0,0)
    vect2 = target  
    for i in range(31):
        n = i/30.0
        theta = interpolateVector(vect1,vect2,n)        
        startPoint = (1,0,0)
        r = rotation(startPoint, theta)
        x.append(r[0])
        y.append(r[1])
        z.append(r[2])
    ax.plot(x,y,z)

def drawTrajectory2(angles):
    x = []
    y = []
    z = []    
    for angle in angles:      
        startPoint = (1,0,0)
        r = rotation(startPoint, angle)
        x.append(r[0])
        y.append(r[1])
        z.append(r[2])
    ax.plot(x,y,z,lw=4.0,ls = ":")

def printAngles(path,angles):
    path = "angles.txt"
    try:
        fileDescriptor = open(path, 'w')
    except:
        print 'Impossible to save %s' % path
    for angle in angles:
        fileDescriptor.write('%i,%i,%i\n' % (angle[0],angle[1],angle[2]))
        

    fileDescriptor.close()

def drawAll(angles):
    drawTrajectory2(angles)
    for angle in angles:
        drawTrajectory(angle)    

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()
    

upper_back_quadrant = [(0,0,90),                                               
                        (0,30,60),
                        (0,30,30),
                        (0,30,0)]

lower_back_quadrant = [(0,45,-30),
                        (0,45,-60),
                        (0,45,-90),
                        (0,45,-115),
                        (0,22,-115)]

lower_front_quadrant = [(0,-30,-115),
                        (0,-60,-115),
                        (0,-90,-115),
                        (0,-115,-115),
                        (0,-135,-115),
                        (0,-135,-90),
                        (0,-135,-60),
                        (0,-135,-30)]


upper_front_quadrant = [(0,-135,0),
                        (0,-135,30),
                        (0,-135,60),
                        (0,-135,90),
                        (0,-115,90),
                        (0,-90,90),
                        (0,-60,90),
                        (0,-30,90)]



angles = upper_back_quadrant+lower_back_quadrant+lower_front_quadrant+upper_front_quadrant


printAngles("angles.txt",angles)


drawAll(angles)


        






import aljabr

import scipy as sp
import numpy as np
import math
from scipy import linspace, polyval, polyfit, sqrt, stats, randn, linalg
from scipy.linalg import eigh,pinv

        
def findOptimalTransformation(vertsM, normM, facesM, vertsB, normB):
    """
    Find and apply the transformation to align meshes
    """
    #find the average of normal vector
    noB = [0,0,1]
    
    nox = 0
    noy = 0
    noz = 0
    
    #if the normals are storaged in the obj file
    if len(normM) > 0:
        for i in normM:
            nox += i[0]
            noy += i[1]
            noz += i[2]
    #if the normals aren't storaged in the obj file
    elif len(facesM) > 0:
        for f in facesM:
            if len(f) >= 3:
                n = aljabr.planeNorm(vertsM[f[0]], vertsM[f[1]], vertsM[f[2]])
            else:
                n = [0,0,1] #edges
                
            nox += n[0]
            noy += n[1]
            noz += n[2]      
            normM.append(n)
    else:
        nox = 0
        noy = 0
        noz = 1
        normM.append(1)
        
    noM = [nox/len(normM), noy/len(normM), noz/len(normM)]   
    
    
    #find the rotation matrix
    matrixR = aljabr.vectorsToRotMatrix(noB,noM) 
    #apply the rotation matrix
    applyTransformation(vertsM, matrixR)
    
    #special case: if the normal vector is -1 on z-axis then rotate the mesh 180 degrees on z
    if noM[2] < -0.30:
        matrixR1 = sp.mat([[math.cos(math.pi),-math.sin(math.pi),0], [math.sin(math.pi),math.cos(math.pi),0], [0,0,1]])
        #applica la matrice di rotazione
        applyTransformation(vertsM, matrixR1)
    
    #linear regression
    angle = fitline(vertsM)
    angleDeg = angle*(180/math.pi)
    #stop condition: angle < 1 or condStop = 0
    condStop = -1
    while math.fabs(angle*(180/math.pi)) > 1 and condStop == -1:
        matrixR2 = sp.mat([[math.cos(-angle),-math.sin(-angle),0], [math.sin(-angle),math.cos(-angle),0], [0,0,1]])
         #apply the rotation matrix
        applyTransformation(vertsM, matrixR2)
        angleOld = angle
        angle = fitline(vertsM)
        if math.fabs(angle) > math.fabs(angleOld):
            condStop = 0
    
    #find the scale matrix
    bbM = calcbb(vertsM)
    factor1 = math.sqrt(math.pow(1.74, 2) / math.pow(bbM[0] - bbM[1], 2));
    factor2 = math.sqrt(math.pow(2.72, 2) / math.pow(bbM[2] - bbM[3], 2));
    factor3 = math.sqrt(math.pow(1.2, 2) / math.pow(bbM[4] - bbM[5], 2));
    factor = max(factor1, factor2, factor3);
    matrixS = sp.mat([[factor,0,0], [0,factor,0], [0,0,factor]])
    #apply the scale matrix
    applyTransformation(vertsM, matrixS)
    
    #adjust the pivot
    bb = calcbb(vertsM)
    dx = (math.sqrt(math.pow(bb[0] - bb[1], 2)) / 2) - bb[1]
    dy = (math.sqrt(math.pow(bb[2] - bb[3], 2)) / 2) - bb[3]
    for v in vertsM:
        v[0] = v[0] + dx
        v[1] = v[1] + dy
    return (vertsM, facesM)
    
    
def fitline(verts):
    """
    Calculate the linear regression on the scan
    """
    datax = []
    datay = []
    for i in verts:
        datax.append(i[0])
        datay.append(i[1])
    datax = np.array(datax)
    datay = np.array(datay)
    #find the coefficients of the regression
    (a,b) = polyfit(datax,datay,1)
    #find the angle
    angle = math.atan(a)
    return angle
    
    

def applyTransformation(verts, matrix):
    """"
    Apply trasformation matrix
    """
    matrix = np.array(matrix)
    for v in range(0,len(verts)):
        ver = np.array(verts[v])
        verts[v] = np.dot(ver,matrix)
    
    return verts   


def calcbb(verts):
    """
    Calcultate bounding box
    """
    minX = verts[0][0]
    maxX = minX
    minY = verts[0][1]
    maxY = minY
    minZ = verts[0][2]
    maxZ = minZ

    for v in verts:
        if v[0] < minX:
            minX = v[0]
        if v[0] > maxX:
            maxX = v[0]
            
        if v[1] < minY:
            minY = v[1]
        if v[1] > maxY:
            maxY = v[1]
          
        if v[2] < minZ:
            minZ = v[2]
        if v[2] > maxZ:
            maxZ = v[2]
    
    return [minX, maxX, minY, maxY, minZ, maxZ]

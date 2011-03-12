#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Common 3D Algebric functions.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2011

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

This module contains the most common 3D algebraic operations used in MakeHuman.
These are mostly the vector and matrix operations core to any 3D application. For efficiency and speed, all matrix
operation will be done thru flat arrays. Function with matrices as flat arrays are written with underscore "_", whilst
functions with matrices as list of lists will have the same name without the underscore.

The name is a tribute to I{"Al-jabr wa'l muqabalah"} the most important paper of Mohammed ibn-Musa al-Khuwarizmi (VII - VIII sec d.C.)
The paper was so important that Al-jabr is the root of modern word I{algebra} and al-Khuwarizmi is the root of word I{algorithm}.
"""

from math import sqrt, cos, sin, tan, atan2, fabs, acos, pow, pi, exp
from random import random
#from array import array

machine_epsilon = 1.0e-16
degree2rad = pi/180

"""
Vector Operations
"""

def vsub(u, v):
    """
    This function returns the difference between two vectors of the same dimension. Works also for flat matrices

    @rtype: double array
    @return: The resulting vector M{vect1-vect2}
    @type  u: float iterable
    @param u: the subrahend
    @type  v: float iterable
    @param v: the minuend
    """
    #ret=array('d')
    ret = []
    for i in xrange(len(u)):
        ret.append(u[i]-v[i])
    return ret

def vadd(*vlist):
    """
    This function sums several vectors of the same dimension. If for instance one has vectors v1,v2,v3,v4 all four having dimension n, then one can use
    vadd(v1,v2,v3,v4). This works for arbitrary number of vectors (with the same dimension), vadd(v1) is also valid. Works also for flat matrices

    @rtype:       double or integer array
    @return:      the sum of vectors to be added
    @type  vlist: a sequence of list of integers of doubles
    @param vlist: the sequence without paranthesis, that determines all the vectors to be added together. See above for usage.
    """
    returnValue=[] #array('d')
    for i in xrange(len(vlist[0])):
        a=0
        for j in xrange(len(vlist)):
            a=a+vlist[j][i]
        returnValue.append(a)
    return returnValue

def vmul(vect, s):
    """
    This function returns the vector result of multiplying each entries of a vector by a scalar. Works also for flat matrices

    @rtype:       double iterable
    @return:      The resulting vector M{s(vect1)}
    @type     s: double or integer
    @param    s: the scalar value
    @type  vect: double or integer iterable
    @param vect: the vector to be multiplied with the scalar value
    """
    ret=[] #array('d')
    for x in vect:
        ret.append(x*s)
    return ret

def vdot(u, v):
    """
    This function returns the dot product between two vectors of the same dimension

    @rtype:  double or integer
    @return: dot-Product of X{u} and X{v}
    @type  u: float or integer iterable
    @param u: The first vector
    @type  v: float or integer iterable
    @param v: The second vector
    """
    a=0
    for i in xrange(len(u)):
        a=a+u[i]*v[i]
    return a

def vlen(v):
    """
    This function returns the norm (length) of a vector (as a float).

    @rtype:       double
    @return:      euclidean norm of X{v}
    @type  vect: float or integer iterable
    @param vect: The vector
    """
    return sqrt(vdot(v,v))


def vnorm(vect):
    """
    This function returns a normalized vector ie a unit length
    vector pointing in the same direction as the input vector.  This performs
    essentially the same function as vunit(vect) except that this function
    handles potential zero length vectors.

    @rtype:       double array
    @return:      normalized form of X{vect}
    @type  vect: double iterable
    @param vect: The vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    length = vlen(vect)

    # Keep the program from blowing up by providing an acceptable
    # value for vectors whose length may be calculated too close to zero.

    if length == 0.0:
        return len(vect)*[0.0] #*array('d',[0.0])

    # Dividing each element by the length will result in a
    # unit normal vector.
    #ret = array('d')
    ret = []
    for x in vect:
        ret.append(x/length)
    return ret


def vdist(vect1, vect2):
    """
    This function returns the euclidean distance (the straight-line distance)
    between two vector coordinates.
    The distance between two points is the length of the vector joining them.

    @rtype:       double
    @return:      euclidean distance between X{vect1} and X{vect2} in 3D space
    @type  vect1: double iterable
    @param vect1: The vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    @type  vect2: double iterable
    @param vect2: The vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """
    return vlen(vsub(vect1,vect2))


def vcross(vect1, vect2):
    """
    This function returns the cross product of two vectors.

    @rtype:       double list
    @return:      cross product M{vect1 S{times} vect2}
    @type  vect1: double list
    @param vect1: The vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    @type  vect2: double list
    @param vect2: The vector - in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    return [vect1[1] * vect2[2] - vect1[2] * vect2[1], vect1[2] * vect2[0] - vect1[0] * vect2[2], vect1[0] * vect2[1] - vect1[1] * vect2[0]]


"""
Matrix Operations
"""

def mulmatvec3x3(m, vect):
    """
    This function returns a 3D vector which consists of the 3D input
    vector multiplied by a 3x3 matrix.

    Parameters
    ----------

    m:
        *float list*. List of list. The 3x3 matrix.

    vect:
        *float list*. The vector - in the format[x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """


    r = [0.0, 0.0, 0.0]
    r[0] = vect[0] * m[0][0] + vect[1] * m[1][0] + vect[2] * m[2][0]
    r[1] = vect[0] * m[0][1] + vect[1] * m[1][1] + vect[2] * m[2][1]
    r[2] = vect[0] * m[0][2] + vect[1] * m[1][2] + vect[2] * m[2][2]
    return r


def makeRotEulerMtx3D(rx, ry, rz):
    """
    This function returns a 3x3 euler rotation matrix based on the 3 angles
    rx, ry and rz.

    Parameters
    ----------

    rx:
        *float*. The angle of rotation (in radians) around the x-axis

    ry:
        *float*. The angle of rotation (in radians) around the y-axis

    rz:
        *float*. The angle of rotation (in radians) around the z-axis
    """

    SRX = sin(rx)
    SRY = sin(ry)
    SRZ = sin(rz)
    CRX = cos(rx)
    CRY = cos(ry)
    CRZ = cos(rz)

    return [[CRY * CRZ, CRY * SRZ, -SRY], [(CRZ * SRX) * SRY - CRX * SRZ, CRX * CRZ + (SRX * SRY) * SRZ, CRY * SRX], [SRX * SRZ + (CRX * CRZ) * SRY, (CRX * SRY) * SRZ
             - CRZ * SRX, CRX * CRY]]


def makeRotEulerMtx2D(theta, rotAxe):
    """
    This function returns a 3x3 euler matrix that rotates a point on
    a plane perpendicular to a specified rotational axis.

    Parameters
    ----------

    theta:
        *float*. The angle of rotation (in radians).

    rotAxe:
        *string*. The axis of rotation, which can be \"X\", \"Y\" or \"Z\".
    """

    if rotAxe == 'X':
        Rmtx = makeRotEulerMtx3D(theta, 0, 0)
    elif rotAxe == 'Y':
        Rmtx = makeRotEulerMtx3D(0, theta, 0)
    elif rotAxe == 'Z':
        Rmtx = makeRotEulerMtx3D(0, 0, theta)
    return Rmtx


def makeRotMatrix(angle, axis):
    """
    This function returns a 3x3 transformation matrix that represents a
    rotation through the specified angle around the specified axis.
    This matrix is presented in Graphics Gems (Glassner, Academic Press, 1990),
    and discussed here: http://www.gamedev.net/reference/programming/features/whyquats/

    Parameters
    ----------

    angle:
        *float*. The angle of rotation (rad) around the specified axis

    axis:
        *float list*. A 3d vector [x,y,z] defining the axis of rotation
        (this should already be normalized to avoid strange results).
    """

    a = angle
    x = axis[0]
    y = axis[1]
    z = axis[2]
    t = 1 - cos(a)
    c = cos(a)
    s = sin(a)
    M11 = (t * x) * x + c
    M12 = (t * x) * y + s * z
    M13 = (t * x) * z - s * y
    M21 = (t * x) * y - s * z
    M22 = (t * y) * y + c
    M23 = (t * y) * z + s * x
    M31 = (t * x) * z + s * y
    M32 = (t * y) * z - s * x
    M33 = (t * z) * z + c
    return [[M11, M12, M13], [M21, M22, M23], [M31, M32, M33]]

def flatten(M):
    """
    For readability it is easier to write matrices as list of list of doubles. In most cases we do this. But for speed and efficiency,
    we it is best to have these matrices as an (flattened matrix) array. This function converts a list of list into an array.
    """
    N=array('f')
    for i in xrange(len(M)):
        for j in xrange(len(M[0])):
            N.append(M[i][j])
    return N

def _unFlatten(M,rows,cols):
    N=[]
    for i in xrange(rows):
        row = []
        n=i*cols
        for j in xrange(cols):
            row.append(N[n+j])
        N.append(row)
    return N

def zeros(*shape):
    """
    This function returns an multidimensional zero-matrix (row-major, list of lists) or zero-vector (list of doubles). For instance: If you want to have a zero-vector of 3-dimensions you type
    zeros(3). If you want a 2x3 zero-matrix, we write zeros(2,3).

    @rtype:    list of double lists
    @return:   a matrix represented as list of lists. Each entry of the list represents a row of the matrix (if this is a nxm matrix). The representation is a row-major order.
    @type  shape:  sequence of integers (e.g. 2,3 or 2)
    @param shape:  this represent the dimensions (in integer tuples) of the output matrix (e.g. for 2x3 matrix shape is 2,2)
    """
    if len(shape) == 0:
        return 0.0
    car = shape[0]
    cdr = shape[1:]
    return [zeros(*cdr) for i in xrange(car)]

def _unitMatrix(n):
    """
    This function returns an nxn unit matrix of doubles.

    @rtype:    array of doubles
    @return:   an nxn flat unit-matrix, row-major order.
    @type  n:  integer
    @param n:  the size of the row of the unit-matrix
    """
    M=array('d')
    for i in xrange(n):
        for j in xrange(n):
            if (i==j): M.append(1.0)
            else: M.append(0.0)
    return M

def _transpose(M,rows=0,cols=0):
    """
    This function returns the transpose of a flat matrix

    @rtype:    double array
    @return:   a matrix that is the transpose of the input matrix (row-major)
    @type  M:  iterable of doubles or integers
    @param M:  the input flat matrix (row-major) that we want to transpose
    """
    ret = array('d')
    for i in xrange(cols):
        for j in xrange(rows):
            ret.append(M[i+j*rows])
    return ret

def _vmulv(u,v):
    """
    This function returns the matrix B{uv^T} (where T here means transpose).

    @rtype:    array of doubles
    @return:   flat matrix B{uv^T} (row-major)
    @type  u:  double iterable
    @param u:  the vector multiplied from left
    @type  v:  double iterable
    @param v:  the vector multiplied whose adjoint is multiplied from right
    """
    M=array('d')
    for i in xrange(len(u)):
        for j in xrange(len(v)):
            M.append(u[i]*v[j])
    return M

# Warning: Unfinished! 
def _QR(M,n):
    """
    QR-Decomposition of a flat singular square matrix using Householder transformations. WARNING: Unfinished!

    @rtype:    tuple of array of doubles
    @return:   a tuple of flat matrices first matrix is an array representing Q, second matrix represents R for the QR-decomposition of M
    @type  M:  array of doubles
    @param M:  flat square matrix (row-major) that we want to take the QR-decomposition
    @type  n:  integer
    @param n:  dimension of the square matrix M
    """
    A=M[:] #deep copy for a flat iterable. warning [:] does shallow copy for multidimensional iterables
    R=n*n*array('d',[0]) #zero matrix
    for j in xrange(n):
        m=n-j
        x=array('d')
        e=m*array('d',[0])
        e[0]=1.0
        for i in xrange(m):
            x.append(A[i])
        v = vadd(x,vmul(vlen(x),e))
        d=vlen(v) #nonzero because A is singular
        d=2/(d*d)
        P=vsub(unitMatrix(m),vmul(vmulv(v,v),d))
        #A=_mmul(P,A,n,n,n)

        B=array('d')
        #smart matrix matrix multiplication extracting the lower submatrix into B
        #i.e. : removing the first row and column of the multiplication of P and A and assigning B to it
        # see how Householder Transformation are created in QR-Decomposition!
        for i in xrange(m):
            m=i*(n-j)
            for j2 in xrange(m):
                a=0
                for k in xrange(m):
                    a=a+P[m+k]*A[k*m+j2]
                if j2==0:
                    R[j2+j+j*n]=a
                else: B.append(a)
        A=B
        #A= A
    #v is not zero because the matrix is singular
    #jocapsco: Todo .. finish this...

def _mmul(M,N,rowsM,colsM,colsN):
    """
    This is the naive matrix multiplication. There are faster matrix multiplication algorithms (like those by
    U{Strassen <http://en.wikipedia.org/wiki/Strassen_algorithm>} or
    U{Coppersmith-Winograd <http://en.wikipedia.org/wiki/Coppersmith-Winograd_algorithm>}. But fast algorithms will make our
    code uneccessarily long and complicated and for small sized matrix (in 3D programming most matrix
    operation are limited to 3x3 matrices) the performance improvement is insignifcant.

    @rtype:    array of doubles
    @return:   a flat mxp matrix reprenting the product of M and N
    @type  M:  array of doubles
    @param M:  flat mxn matrix (row-major), that is supposed to be the left-multiplier
    @type  rowsM:  integer
    @param rowsM:  number of rows of M
    @type  colsM:  integer
    @param colsM:  number of columns of M = number of rows of N
    @type  colsN:  integer
    @param colsN:  number of columns of N
    """
    P=array('d')
    for i in xrange(rowsM):
        n=i*colsM
        for j in xrange(colsN):
            a=0
            for k in xrange(colsM):
                a=a+M[n+k]*N[k*colsM+j]
            P.append(a)
    return P

    
"""
Quaternions
"""

def quaternionVectorTransform(q, v):
    return [q[3]*q[3]*v[0] + 2*q[1]*q[3]*v[2] - 2*q[2]*q[3]*v[1] + q[0]*q[0]*v[0] + 2*q[1]*q[0]*v[1] + 2*q[2]*q[0]*v[2] - q[2]*q[2]*v[0] - q[1]*q[1]*v[0],
            2*q[0]*q[1]*v[0] + q[1]*q[1]*v[1] + 2*q[2]*q[1]*v[2] + 2*q[3]*q[2]*v[0] - q[2]*q[2]*v[1] + q[3]*q[3]*v[1] - 2*q[0]*q[3]*v[2] - q[0]*q[0]*v[1],
            2*q[0]*q[2]*v[0] + 2*q[1]*q[2]*v[1] + q[2]*q[2]*v[2] - 2*q[3]*q[1]*v[0] - q[1]*q[1]*v[2] + 2*q[3]*q[0]*v[1] - q[0]*q[0]*v[2] + q[3]*q[3]*v[2]]

def axisAngleToQuaternion(axis, angle):
    s = sin(angle/2.0)
    qx = axis[0] * s
    qy = axis[1] * s
    qz = axis[2] * s
    qw = cos(angle/2.0)
    return (qx, qy, qz, qw)
    
def quaternionTranslationToDual(q, t):
    return [q,
            [0.5 * ( t[0] * q[3] + t[1] * q[2] - t[2] * q[1]),
             0.5 * (-t[0] * q[2] + t[1] * q[3] + t[2] * q[0]),
             0.5 * ( t[0] * q[1] - t[1] * q[0] + t[2] * q[3]),
            -0.5 * ( t[0] * q[0] + t[1] * q[1] + t[2] * q[2])]]
            
def dualToMatrix(d):
    # Since the rotation part is a unit quaternion, we don't need to divide I think
    #length = vdot(d[0], d[0])
    x, y, z, w = d[0]
    t1, t2, t3, t0 = d[1]
    m = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        
    m[0][0] = w*w + x*x - y*y - z*z
    m[1][0] = 2.0*x*y - 2.0*w*z
    m[2][0] = 2.0*x*z + 2.0*w*y
    m[0][1] = 2.0*x*y + 2.0*w*z
    m[1][1] = w*w + y*y - x*x - z*z
    m[2][1] = 2.0*y*z - 2.0*w*x
    m[0][2] = 2.0*x*z - 2.0*w*y
    m[1][2] = 2.0*y*z + 2.0*w*x
    m[2][2] = w*w + z*z - x*x - y*y
    
    m[3][0] = -2.0*t0*x + 2.0*t1*w - 2.0*t2*z + 2.0*t3*y
    m[3][1] = -2.0*t0*y + 2.0*t1*z + 2.0*t2*w - 2.0*t3*x
    m[3][2] = -2.0*t0*z - 2.0*t1*y + 2.0*t2*x + 2.0*t3*w
    
    m[0][3] = 0.0
    m[1][3] = 0.0
    m[2][3] = 0.0
    m[3][3] = 1.0
    
    #mdiv(m, length)
    
    return m

#Note: Quaternions have to of normalized form
# Quaternions are of the form (x,y,z,w)
def quaternionToMatrix(q):
    m = [[0,0,0],[0,0,0],[0,0,0]]  # will be a 3x3 euler rotation matrix
    m[0][0] = float(q[3]*q[3] + q[0]*q[0] - q[1]*q[1] - q[2]*q[2])
    m[0][1] = 2.0*(q[0]*q[1]-q[3]*q[2])
    m[0][2] = 2.0*(q[0]*q[2]+q[3]*q[1])

    m[1][0] = 2.0*(q[1]*q[0]+q[3]*q[2])
    m[1][1] = float(q[3]*q[3]-q[0]*q[0]+q[1]*q[1]-q[2]*q[2])
    m[1][2] = 2.0*(q[1]*q[2]-q[3]*q[0])

    m[2][0] = 2.0*(q[2]*q[0]-q[3]*q[1])
    m[2][1] = 2.0*(q[2]*q[1]+q[3]*q[0])
    m[2][2] = float(q[3]*q[3]-q[0]*q[0]-q[1]*q[1]+q[2]*q[2])

    return m

def quaternionLerp(q1, q2, alpha):
    
    return vnorm([q1[0] + alpha * (q2[0] - q1[0]),
                  q1[1] + alpha * (q2[1] - q1[1]),
                  q1[2] + alpha * (q2[2] - q1[2]),
                  q1[3] + alpha * (q2[3] - q1[3])])

'''    
def quaternionSlerp2(q1, q2, alpha):
    
    dot = vdot(q1, q2)
    
    if dot > 0.1:
        return vnorm([q1[0] + alpha * (q2[0] - q1[0]),
                      q1[1] + alpha * (q2[1] - q1[1]),
                      q1[2] + alpha * (q2[2] - q1[2]),
                      q1[3] + alpha * (q2[3] - q1[3])])
                      
    dot = max(-1.0, min(dot, 1.0))
    theta0 = acos(dot)
    theta = theta0 * alpha

    q = vnorm([q2[0] - alpha * q1[0],
               q2[1] - alpha * q1[1],
               q2[2] - alpha * q1[2],
               q2[3] - alpha * q1[3]])

    return vadd(vmul(q1, cos(theta)), vmul(q, sin(theta)))
'''
            
def quaternionSlerp(q1, q2, alpha):
        
    cosHalfTheta = q1[3] * q2[3] + q1[0] * q2[0] + q1[1] * q2[1] + q1[2] * q2[2]
    
    if abs(cosHalfTheta) >= 1.0:
        return q1

    halfTheta = acos(cosHalfTheta)
    sinHalfTheta = sqrt(1.0 - cosHalfTheta * cosHalfTheta)

    if abs(sinHalfTheta) < 0.001:
        return [q1[0] * 0.5 + q2[0] * 0.5,
                q1[1] * 0.5 + q2[1] * 0.5,
                q1[2] * 0.5 + q2[2] * 0.5,
                q1[3] * 0.5 + q2[3] * 0.5]

    ratioA = sin((1 - t) * halfTheta) / sinHalfTheta;
    ratioB = sin(t * halfTheta) / sinHalfTheta; 

    return [q1[0] * ratioA + q2[0] * ratioB,
            q1[1] * ratioA + q2[1] * ratioB,
            q1[2] * ratioA + q2[2] * ratioB,
            q1[3] * ratioA + q2[3] * ratioB]



"""
Geometric Operations
"""
 
def centroid(vertsList):
    """
    This function returns the baricenter of a set of coordinate vectors
    [[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]], returning a coordinate vector
    formatted as a double list [double X,double Y, double Z].
    This is the sum of all of the vectors divided by the number of vectors.

    @rtype:       double list
    @return:      the centroid of the convex hull of all the vertices in M(vertsList)
    @type  vertsList: list of double lists
    @param vertsList: each vector in the list is in the format [x,y,z]
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    nVerts = len(vertsList)
    xTot = 0.0
    yTot = 0.0
    zTot = 0.0
    for v in vertsList:
        xTot += v[0]
        yTot += v[1]
        zTot += v[2]
    if nVerts != 0:
        centrX = xTot / nVerts
        centrY = yTot / nVerts
        centrZ = zTot / nVerts
    else:
        print 'Warning: no verts to calc centroid'
        return 0
    return [centrX, centrY, centrZ]

    
def rotatePoint(center, vect, rotMatrix):
    """
    This function returns the 3D vector coordinates of a
    vector rotated around a specified centre point using a
    3x3 rotation matrix.

    Parameters
    ----------

    center:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the center of rotation.

    vect:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the point to be rotated.

    rotMatrix:
        *float list of lists*. A 3x3 rotation matrix.
    """

    # subtract rotation point

    tv = vsub(vect, center)

    # rotate

    nv = mulmatvec3x3(rotMatrix, tv)

    # add the rotation point back again

    nv = vadd(nv, center)
    return nv


def scalePoint(center, vect, scale, axis=None):
    """
    This function returns the 3D vector coordinates of a
    coordinate vector scaled relative to a specified centre point using a
    scalar value.

    Parameters
    ----------

    center:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the center point.

    vect:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the point to be scaled.

    scale:
        *float*. Scale factor.

    axis:
        *string*. An optional axis to constrain scaling (\"X\", \"Y\", \"Z\" or None).
        If an axis is specified then no scaling takes place along that axis.
    """

    # subtract centre point

    tv = vsub(vect, center)

    # scale

    if axis == 'X':
        nv = [tv[0], tv[1] * scale, tv[2] * scale]
    elif axis == 'Y':
        nv = [tv[0] * scale, tv[1], tv[2] * scale]
    elif axis == 'Z':
        nv = [tv[0] * scale, tv[1] * scale, tv[2]]
    else:
        nv = [tv[0] * scale, tv[1] * scale, tv[2] * scale]

    # add the centre point back again

    nv = vadd(nv, center)
    return nv


def planeNorm(vect1, vect2, vect3):
    """
    This function returns the vector of the normal to a plane, where the
    plane is defined by the vector coordinates of 3 points on that plane.
    This function calculates two direction vectors eminating from
    vect2, and calculates the normalized cross product to derive
    a vector at right angles to both direction vectors.
    This function assumes that the input coordinate vectors
    do not all lie on the same straight line.

    Parameters
    ----------

    vect1:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the first point.
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect2:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the second point.
        (or [x,y,z,0] for affine transformations in an homogeneous space).

    vect3:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the third point.
        (or [x,y,z,0] for affine transformations in an homogeneous space).
    """

    # Calculate two vectors from the three points

    v1 = [vect1[0] - vect2[0], vect1[1] - vect2[1], vect1[2] - vect2[2]]
    v2 = [vect2[0] - vect3[0], vect2[1] - vect3[1], vect2[2] - vect3[2]]

    # Take the cross product

    normal = [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]
    
    return normal
    '''
    # Normalize
    length = sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2])
    if length < machine_epsilon: #should not happen but it does for badly formed meshes
      return [0.0,0.0,0.0]
    else:
      return [normal[0] / length, normal[1] / length, normal[2] / length]
    '''

def focalToFov(dimension, focal):
    if focal == 0:
        return 0
    else:
        return 2 * atan2(dimension * 0.5, focal)


def fovToFocal(dimension, fov):
    return dimension / (2 * tan(fov / 2))


def in2pts(point1, point2, t):
    """
    This function returns a vector that lies on the directed line between points, given
    a parameter t. The paraemeter t is between 0 and 1 and it parametrizes our directed line
    between point1 and point2


    Parameters
    ----------

    point1:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the first point (i.e. starting point) of a directed line.

    point2:
        *float list*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the second point (i.e. endpoint) of a directed line.

    t:
        *float*. A real number between 0 and 1, that linearly parametrizes
        the directed line between point1 and point2. In other words, when t is 0 the
        return value for this function is point1 and when t is 1 the return value
        for this function is point2.
    """

    return vadd(vmul(point1, 1 - t), vmul(point2, t))

def vectorsToRotMatrix(v1,v2):
    """
    Given two points v1 and v2 in 3D space. Suppose furthermore that v2 is generated by v1 
    multiplied by a rotation matrix over the origin. We will determine this rotation matrix using this method
    
    @rtype:    float list
    @return:   Rotation matrix (unhomegenized) in 3D space that rotated v1 to v2 (center at origin)
    @type  v1: float list
    @param v1: original point in 3D 
    @type  v2: float list
    @param v2: the point for which v1 has rotated to
    """
    normal = vcross(v1,v2)
    normal = vnorm(normal)
    angle = acos(vdot(v1,v2)/(vlen(v1)*vlen(v2)))
    q = axisAngleToQuaternion(normal, angle)
    return quaternionToMatrix(q)

def randomPointFromNormal(v):
    """
    Suppose you have a vector v. Then this vector defines a plane that passes the origin and for which the vector v is a normal to it
    This method gets a random point in 3D that lies on this plane. Beware: v should not be of length 0!
    """
    x = random()
    y = random()
    z = random()
    if (v[0] != 0):
      x = -(y*v[1]+z*v[2])/v[0]
    elif (v[1] !=0):
      y = -(x*v[0]+z*v[2])/v[1]
    else:
      z = -(x*v[0]+y*v[1])/v[2]
    return [x,y,z]
    
def convexQuadrilateralArea(v1,v2,v3,v4):
    """
    This function returns the area of a Quadrilateral. See U{http://mathworld.wolfram.com/Quadrilateral.html}.

    @rtype:    float
    @return:   The area of a Quadrilateral determined by v1 to v4 (clockwise or counterclockwise order)
    @type  v1: float list
    @param v1: first vertex of a parallelogram - in the format [x,y,z]
    @type  v2: float list
    @param v2: second vertex of a parallelogram - in the format [x,y,z]
    @type  v3: float list
    @param v3: third vertex of a parallelogram - in the format [x,y,z]
    @type  v4: float list
    @param v4: fourth vertex of a parallelogram - in the format [x,y,z]
    """
    #a=vdist(v2,v1)
    #b=vdist(v3,v2)
    #c=vdist(v4,v3)
    #d=vdist(v1,v4)
    p=vdist(v2,v4)
    q=vdist(v1,v3)
    pq = vdot(vsub(v3,v1),vsub(v4,v2))
    return 0.5*sqrt(p*p*q*q - pq*pq)
    #return sqrt(4*p*p*q*q - pow((b*b+d*d-a*a-c*c),2))/4


"""
Various Functions
"""
    
def bump(x, width=1.0):
    """
    This is the bump function (see U<Wikipedia - Bump Function>{http://en.wikipedia.org/wiki/Bump_function}). Height is always 1, if we 
    need higher bump we just scale it

    @rtype:    double
    @return:   the bump function scaked to have height of 1 
    @type  x:  double
    @param x:  the value of the function at x (>= 0)
    @type  width:  double
    @param width:  radius of the bump
    """
    if (x < width):
      return exp(-width*width/(width*width - x*x) + 1.0)
    else:
      return 0.0
    
# u and m must be float 0<=m<=1
# returns : sn,cn,dn,phi
#TODO : Add reference: Louis V. King; Hofsommer; Salzer (after reading it yourself :P)
#pg. 9 eq'n 35 of Louis V. King for m within 1.0e-9 range
def jacobianEllipticFunction(u,m):
    """
    This function returns a triple consisting of the Jacobian elliptic functions, namely the
    Jacobian sine (sn), Jacobian cosine (cn), Jacobian *TODO.. dn*, angle (in radians)

    Parameters
    ----------

    u:
        *float*. A 3D vector - in the format[x,y,z] containing the
        coordinates of the first point (i.e. starting point) of a directed line.

    k:
        *float* a value between 0 and 1 which represent the modulus of the Jacobian elliptic function

    """
    if (m< 0) or (m >1):
        print "Coefficient for Elliptic Integral should be between 1 and 0"
        return  #error-code!
    a=[0]*9
    c=[0]*9
    if m < 1.0e-9:
        t = sin(u)
        b = cos(u)
        ai = 0.25*m*(u-t*b)
        sn = t-ai*b
        cn = b+ai*t
        ph = u-ai
        dn = 1.0 - 0.5*m*t*t
        return sn,cn,dn,ph
    if m>=1.0 - 1.0e-9:
        ai = 0.25*(1.0-m)
        b = math.cosh(u)
        t= math.tanh(u)
        phi = 1.0/b
        twon = b*math.sinh(u)
        sn = t+a*(twon-u)/(b*b)
        ph = 2.0*math.atan(math.exp(u))-math.pi/2+ai*(twon-u)/b
        ai=ai*t*phi
        cn = phi - ai*(twon-u)
        dn=phi+ai*(twon+u)
        return sn,cn,dn,ph

    a[0] = 1.0;
    b=math.sqrt(1.0-m)
    c[0]=math.sqrt(m)
    twon=1.0
    i=0

    while fabs(c[i]/a[i])>machine_epsilon:
        if i>7:
            print "Overflow in the calculation of Jacobian elliptic functions"
            break
        ai = a[i]
        i=i+1
        c[i]=0.5*(ai-b)
        t=sqrt(ai*b)
        a[i]=0.5*(ai+b)
        b=t
        twon=twon*2.0

    phi=twon*a[i]*u
    while i!=0:
        t=c[i]*sin(phi)/a[i]
        b=phi
        phi=(math.asin(t)+phi)/2.0
        i=i-1
    return sin(phi),cn,cn/cos(phi-b),phi


def newton_raphson(f, f_diff, value, start, iterations=4, epsilon = 1e-4):
    """ Returns a root of the polynomial, with a starting value.
    To get both roots in a quadratic, try using with n = 1 and n = -1."""

    x = start - (float(f(start)-value) / f_diff(start))

    x = start
    counter = 0

    while fabs(x-start)>epsilon or counter<iterations:
        x = x - (float(f(x)-value) / f_diff(x))
        counter += 1
        return x
        

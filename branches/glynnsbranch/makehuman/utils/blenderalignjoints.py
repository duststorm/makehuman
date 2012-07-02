# You may use, modify and redistribute this module under the terms of the GNU GPL.
"""


"""

__docformat__ = 'restructuredtext'

import Blender
import aljabr
import scipy
from scipy.spatial import KDTree
import numpy as np

def closerVert(diamondIndices):
    """

    """

    activeObjs = Blender.Object.GetSelected()
    obj = activeObjs[0].getData(mesh=True)

    centroidVerts = [[obj.verts[i].co[0],obj.verts[i].co[1],obj.verts[i].co[2]] for i in diamondIndices]
    center = aljabr.centroid(centroidVerts)

    vertsList = []
    vertsListIndices = []
    vertsToUse = getSkinVerts()
    for i in vertsToUse:
        v = obj.verts[i]
        vertsList.append([v.co[0],v.co[1],v.co[2]])
        vertsListIndices.append(v.index)          
    
    kd = KDTree(vertsList)
    dist,indx = kd.query([center])
    i = vertsListIndices[indx]

    return i


def getSkinVerts():
    """
    

    """ 
   
    activeObjs = Blender.Object.GetSelected()
    obj = activeObjs[0].getData(mesh=True)
    vertsGroupsNames = obj.getVertGroupNames()    

    forbiddenWords = ("joint","lash","teeth","eyebrow")
    skinVerts = set()
    for name in vertsGroupsNames:
        words = set(name.split('-'))
        proceed = True
        for fWord in forbiddenWords:
            if fWord in words:
                proceed = None

        if proceed:
            verts = obj.getVertsFromGroup(name)
            for i in verts:
                v = obj.verts[i]
                v.sel = 1
                skinVerts.add(v.index)

    return skinVerts





def saveJointDeltas(path):
    """


    Parameters
    ----------

    path:
      *path*.  The file system path to the file to be written.
    prefix:
      *string*.  The group name of the faces to export.
    """

    activeObjs = Blender.Object.GetSelected()
    obj = activeObjs[0].getData(mesh=True)
    vertsGroupsNames = obj.getVertGroupNames()

    try:
        fileDescriptor = open(path, "w")
    except:
        print "Unable to open %s",(path)
        return  None

    for name in vertsGroupsNames:
        
        if name.split('-')[0] == "joint":
            diamondIndices = obj.getVertsFromGroup(name)
            n = closerVert(diamondIndices)
            v = [obj.verts[n].co[0],obj.verts[n].co[1],obj.verts[n].co[2]]
            for i in diamondIndices:
                diamondVert = [obj.verts[i].co[0],obj.verts[i].co[1],obj.verts[i].co[2]]
                delta = aljabr.vsub(diamondVert,v)
                #index od base vert, index of joint vert, coord 0, coord1 and coord2 of the delta vector
                fileDescriptor.write("%d %d %f %f %f\n" % (n, i, delta[0],delta[1],delta[2]))
        else:
            print name, name.split('-')[0] 
            
    fileDescriptor.close()
    
    return 1
    


def loadJointDelta(path):
    """
    

    Parameters
    ----------

    targetPath:
        *string*. A string containing the operating system path to the
        file to be read.

    """    
    
    activeObjs = Blender.Object.GetSelected()
    if len(activeObjs) > 0:
        activeObj = activeObjs[0]
    else:
        Draw.PupMenu("No object selected")
        return None
        
    wem = Blender.Window.EditMode()
    Blender.Window.EditMode(0)

    obj = activeObj.getData(mesh=True)

    try:
        fileDescriptor = open(path)
    except:
        Draw.PupMenu("Unable to open %s",(path))
        return  None
    jointsData = fileDescriptor.readlines()
    fileDescriptor.close()


    for jData in jointsData:
        deltas = jData.split()

        baseVertIndex = int(deltas[0])
        jointVertIndex = int(deltas[1])
        
        dX = float(deltas[2])
        dY = float(deltas[3])
        dZ = float(deltas[4])

        vJoint = obj.verts[jointVertIndex]
        vBase = obj.verts[baseVertIndex]
        
        vJoint.co[0] = vBase.co[0] + dX
        vJoint.co[1] = vBase.co[1] + dY
        vJoint.co[2] = vBase.co[2] + dZ
        
    obj.update()
   
    Blender.Window.EditMode(wem)
    Blender.Window.RedrawAll()


    return 1

#saveJointDeltas("data.joints")
#loadJointDelta("data.joints")
#getSkinVerts()

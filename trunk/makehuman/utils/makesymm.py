# You may use, modify and redistribute this module under the terms of the GNU GPL.
"""
Saves Blender obj in wavefront format.

===========================  ==================================================================
Project Name:                **MakeHuman**
Module File Location:        utils/blendersaveobj.py
Product Home Page:           http://www.makehuman.org/
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2013
Licensing:                   AGPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
===========================  ==================================================================

This module symmetrize the left target. It check for abnormal left targets too (they are left targets that affect some right vertices).
The abnormal targets are copied into the tmp folder, and then fixed.

"""

__docformat__ = 'restructuredtext'

import sys
sys.path.append("../core")

import os
import aljabr
import math
import types
import shutil

theta = 0.01
failedToOpen = []
symmCouples = {}
corrupted = []

if not os.path.isdir("../tmp"):
    os.mkdir("../tmp")

def loadSymmData(path):
    global symmCouples, corrupted
    try:
        fileDescriptor = open(path)
    except:
        print 'Error loading %s file' % path        
        return    
    data = fileDescriptor.readlines()
    for targetData in data:
        
        symmData = targetData.split(',')
        if len(symmData) > 0:            
            symmCouples[int(symmData[0])] = int(symmData[1])
    fileDescriptor.close()   


def doMirror(path1, path2):
    global symmCouples,corrupted
    fileDescriptor = open(path1)        
    simmetrizedData = []
    originalData = fileDescriptor.readlines()
    for targetData in originalData:
        vectorData = targetData.split()
        if len(vectorData) > 0:
            try:
                simmIndex = symmCouples[int(vectorData[0])]
            except:
                corrupted.append(path1)
                return
            simmetrizedVector = [simmIndex, -1*float(vectorData[1]),float(vectorData[2]),float(vectorData[3])]
            simmetrizedData.append(simmetrizedVector)
    fileDescriptor.close()
    
    fileDescriptor = open(path2, 'w')       
    for simmetrizedVector in simmetrizedData:
        fileDescriptor.write('%i %f %f %f\n' % (simmetrizedVector[0], simmetrizedVector[1], simmetrizedVector[2], simmetrizedVector[3]))
    fileDescriptor.close()
    

def fixAbnormalTargets(path):
    """
    This function replace the abnormal target with the one that use only left verts.
    """
    global symmCouples
    fileDescriptor = open(path)        
    fixedData = []
    originalData = fileDescriptor.readlines()
    for targetData in originalData:
        vectorData = targetData.split()
        if len(vectorData) > 0:
            try:
                simmIndex = symmCouples[int(vectorData[0])] #This line check it's a left vert
                fixedVector = [int(vectorData[0]), float(vectorData[1]),float(vectorData[2]),float(vectorData[3])]
                fixedData.append(fixedVector)
            except:                
                print "skipped index %i"%(int(vectorData[0]))         
    fileDescriptor.close()
    
    #Overwrite the old corrupted target
    fileDescriptor = open(path, 'w')       
    for fixedVector in fixedData:
        fileDescriptor.write('%i %f %f %f\n' % (fixedVector[0], fixedVector[1], fixedVector[2], fixedVector[3]))
    fileDescriptor.close()


def symmetrize(path):
    loadSymmData("./maketarget/base.sym")
    nTargets = 0
    for leftTarget in os.listdir(path):
        if "svn" not in leftTarget:
            if leftTarget.split("-")[0] == "l":
                nTargets += 1
                rightTarget = "r"+leftTarget[1:]
                tPath1 = os.path.join(path, leftTarget)
                tPath2 = os.path.join(path, rightTarget)
                doMirror(tPath1,tPath2)
    
    for corruptedTarget in corrupted:
        #print corruptedTarget
        corruptedTarget2 = os.path.join("../tmp",os.path.basename(corruptedTarget))
        shutil.copyfile(corruptedTarget, corruptedTarget2)
        fixAbnormalTargets(corruptedTarget2)        
    print "Found %i abnormal left targets (that affect right vertices)"%(len(corrupted))
    print "I've simmetrized %i left target"%(nTargets)

#symmetrize("/home/manuel/archive/archive_makehuman/makehuman_src/data/targets/microdetails")
if len(sys.argv) < 2:
    print "Usage: checksymm directory"
else:
	symmetrize(sys.argv[1])

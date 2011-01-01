# You may use, modify and redistribute this module under the terms of the GNU GPL.
"""
Saves Blender obj in wavefront format.

===========================  ==================================================================
Project Name:                **MakeHuman**
Module File Location:        utils/blendersaveobj.py
Product Home Page:           http://www.makehuman.org/
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2010
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards
===========================  ==================================================================

This module implements a utility function to check if each target has a good symmetric one.

"""

__docformat__ = 'restructuredtext'

import sys
sys.path.append("../core")

import os
import aljabr
import math
import types

theta = 0.01
failedToOpen = []
symmCouples = {}
corrupted = []

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
            simmetrizedVector = [simmIndex, -float(vectorData[1]),float(vectorData[2]),float(vectorData[3])]
            simmetrizedData.append(simmetrizedVector)
    fileDescriptor.close()
    
    fileDescriptor = open(path2, 'w')       
    for simmetrizedVector in simmetrizedData:
        fileDescriptor.write('%i %f %f %f\n' % (simmetrizedVector[0], simmetrizedVector[1], simmetrizedVector[2], simmetrizedVector[3]))
    fileDescriptor.close()
    

def symmetrize(path):
    loadSymmData("./maketarget/base.sym")
    for leftTarget in os.listdir(path):
        if "svn" not in leftTarget:
            if leftTarget.split("-")[0] == "l":
                rightTarget = "r"+leftTarget[1:]
                tPath1 = os.path.join(path, leftTarget)
                tPath2 = os.path.join(path, rightTarget)
                doMirror(tPath1,tPath2)
    print "Found %i abnormal left targets (that affect right vertices):"%(len(corrupted))
    for corruptedTarget in corrupted:
        print corruptedTarget


symmetrize("/home/manuel/archive/archive_makehuman/makehuman_src/data/targets/details")
#if len(sys.argv) < 2:
    #print "Usage: checksymm directory"
#else:
	#check_symm(sys.argv[1])

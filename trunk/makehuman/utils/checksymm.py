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

This module implements a utility function to check if each target has a good symmetric one.

"""

__docformat__ = 'restructuredtext'

import sys
sys.path.append("../core")
import os
import aljabr
import math
import types
import shutil

if not os.path.isdir("../tmp2"):
    os.mkdir("../tmp2")

theta = 0.01
failedToOpen = []

def translLenght(path):
    try:
        fileDescriptor = open(path)
    except:
        print 'Error opening %s file' % path
        failedToOpen.append(path)
        return
    fullTransl = 0
    data = fileDescriptor.readlines()
    for targetData in data:
        vectorData = targetData.split()
        if len(vectorData) > 0:
            vector = [float(vectorData[1]),float(vectorData[2]),float(vectorData[3])]
            fullTransl += aljabr.vlen(vector)
    fileDescriptor.close()
    return fullTransl

def analyze_target(path1, path2):
    lenght1 = translLenght(path1)
    lenght2 = translLenght(path2)
    if (type(lenght1) != types.NoneType) and (type(lenght2) != types.NoneType):
        return math.fabs(lenght1-lenght2)
    else:
        return 1000

def check_symm(path):
    n = 0
    for leftTarget in os.listdir(path):
        if "svn" not in leftTarget:
            if leftTarget.split("-")[0] == "l":
                if leftTarget.find("trans-in") != -1:
                    rightTarget = "r"+leftTarget[1:].replace("trans-in","trans-out")
                elif leftTarget.find("trans-out") != -1:
                    rightTarget = "r"+leftTarget[1:].replace("trans-out","trans-in")  
                else:
                    rightTarget = "r"+leftTarget[1:]
                    
                tPath1 = os.path.join(path, leftTarget)
                tPath2 = os.path.join(path, rightTarget)
                if analyze_target(tPath1,tPath2) > theta:                    
                    #shutil.copyfile(os.path.join(path,os.path.basename(leftTarget)), os.path.join("../tmp2",os.path.basename(leftTarget)))
                    print "-> %s"%(rightTarget)
                    n += 1
    print "Found %i problem in symmetric targets"%(n)
    print "Found %i missed symmetric targets"%(len(failedToOpen))

#check_symm("/home/manuel/archive/archive_makehuman/makehuman_src/data/targets/details")

if len(sys.argv) < 2:
    print "Usage: checksymm directory"
else:
	check_symm(sys.argv[1])

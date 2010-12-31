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

This module implements a utility function to check if each facegroup has the
correspondent transformations targets.

"""

__docformat__ = 'restructuredtext'

import sys

sys.path.append("../core")
import os
import aljabr
import math

theta = 0.01
def translLenght(path):
    try:
        fileDescriptor = open(path)
    except:
        print 'Error opening %s file' % path
        return
    fullTransl = 0
    data = fileDescriptor.readlines()
    for targetData in data:
        vectorData = targetData.split()        
        if len(vectorData) > 0:                      
            vector = [float(vectorData[1]),float(vectorData[2]),float(vectorData[3])]            
            #print aljabr.vlen(vector)
            fullTransl += aljabr.vlen(vector)
    fileDescriptor.close()
    return fullTransl

def analyze_target(path1, path2):
    lenght1 = translLenght(path1)
    lenght2 = translLenght(path2)
    return math.fabs(lenght1-lenght2)

def check_symm(path):
    n = 0
    for leftTarget in os.listdir(path):
        if "svn" not in leftTarget:            
            #print target.split("-")
            if leftTarget.split("-")[0] == "l":
                #print target
                rightTarget = "r"+leftTarget[1:]
                    
                tPath1 = os.path.join(path, leftTarget)
                tPath2 = os.path.join(path, rightTarget)               
                
                if analyze_target(tPath1,tPath2) > theta:
                    print "-> %s"%(rightTarget)
                    n += 1
    print "Found %i problem in symmetric targets"%(n)
    
    
        
        
#check_symm("/home/manuel/archive/archive_makehuman/makehuman_src/data/targets/details")

import sys

if len(sys.argv) < 2:
    print "Usage: checksymm directory"
else:	
	check_symm(sys.argv[1])

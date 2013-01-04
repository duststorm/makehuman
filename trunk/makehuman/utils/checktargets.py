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

This module implements a utility function to check if each facegroup has the
correspondent transformations targets.

"""

__docformat__ = 'restructuredtext'

import Blender
import os
def checkTargets(path,prefix="part"):
    """
    main function to check targets.
    
    Parameters
    ----------
   
    path:     
      *path*.  Path of folder to examine.
    prefix:     
      *string*.  The group name of the faces to check.
    """
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)   
    vertsGroups = data.getVertGroupNames() 
    vertsGroups.sort()
    numberOfNotMatched = 0
    nameToExclude = ["joint","tongue","molar","incisor","cuspid","bicuspid","lash",\
    "pupil","nail1","nail2","nail3","nail4","nail5","lid","eyebrow","eye"]
    targetsFiles = os.listdir(path)
    targetsNames = []
    for targetFile in targetsFiles:
        fileName = os.path.splitext(targetFile)
        targetName = fileName[0]
        targetsNames.append(targetName)
    targetsNames.sort()

    for group in vertsGroups:        
        groupNameData = group.split('_')
        if len(groupNameData) > 1:

            groupNamePieces = groupNameData[1].split("-")


            if groupNameData[0] == prefix:
                jumpIt = None
                for namePiece in groupNamePieces:
                    if namePiece in nameToExclude:
                        jumpIt = 1
                if not jumpIt:
                    groupBaseName = groupNameData[1]
                    filesTocheck = [groupBaseName + "-scale-depth-decr",\
                    groupBaseName + "-scale-depth-incr",\
                    groupBaseName + "-scale-horiz-decr",\
                    groupBaseName + "-scale-horiz-incr",\
                    groupBaseName + "-scale-vert-decr",\
                    groupBaseName + "-scale-vert-incr",\
                    groupBaseName + "-trans-backward",\
                    groupBaseName + "-trans-forward",\
                    groupBaseName + "-trans-left",\
                    groupBaseName + "-trans-right",\
                    groupBaseName + "-trans-up",\
                    groupBaseName + "-trans-down"]

                    for fName in filesTocheck:
                        correspondenceOK = None
                        for tname in targetsNames:
                            if tname == fName:
                                correspondenceOK = 1
                                break
                        if not correspondenceOK:
                            numberOfNotMatched += 1
                            print "Target %s not present"%(fName)
    print "Groups without targets %i of %i"%(numberOfNotMatched,12*len(vertsGroups) )

           

    
    
    
checkTargets("/home/manuel/Desktop/maketarget/targets")

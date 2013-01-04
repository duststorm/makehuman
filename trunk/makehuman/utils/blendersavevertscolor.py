# You may use, modify and redistribute this module under the terms of the GNU GPL.
""" 
Save vertex Colors in Blender format.

===========================  ==================================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        utils/blendersavevertscolor.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni (individual developers look into the AUTHORS file)                                       
Copyright(c):                MakeHuman Team 2001-2013                                       
Licensing:                   AGPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ==================================================================  

This module implements a utility function to save vertex colors in Blender format.

"""

__docformat__ = 'restructuredtext'

import Blender


def saveVertsColors(path):
    """
    This function saves vertex colors in Blender format.  
    
    Parameters
    ----------
   
    path:     
      *path*.  The file system path to the file to be written.

    """
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    me = activeObj.getData(mesh=True)
    me.vertexColors= True   # Enable face, vertex colors
    try:    
        vertsAlpha = me.getVertsFromGroup("alpha")
    except:
        vertsAlpha = []
 
    try:
        fileDescriptor = open(path, "w")
    except:
        print "error to save obj file"
        return 0    
        
    for f in me.faces:
    
        alpha0 = 255
        alpha1 = 255
        alpha2 = 255
        alpha3 = 255
        if len(f.verts) == 4:
            #split quad colors in 2 trigs colors 
            c0 = f.col[0]
            c1 = f.col[1]
            c2 = f.col[2]
            c3 = f.col[3]
            i0 = f.verts[0].index
            i1 = f.verts[1].index
            i2 = f.verts[2].index
            i3 = f.verts[3].index
            
            if i0 in vertsAlpha:
                alpha0 = 0
            if i1 in vertsAlpha:
                alpha1 = 0
            if i2 in vertsAlpha:
                alpha2 = 0
            if i3 in vertsAlpha:
                alpha3 = 0
            
            fileDescriptor.write("%i %i %i %i " % (c0.r,c0.g,c0.b,alpha0))
            fileDescriptor.write("%i %i %i %i " % (c1.r,c1.g,c1.b,alpha1))
            fileDescriptor.write("%i %i %i %i\n" % (c2.r,c2.g,c2.b,alpha2))

            fileDescriptor.write("%i %i %i %i " % (c2.r,c2.g,c2.b,alpha2))
            fileDescriptor.write("%i %i %i %i " % (c3.r,c3.g,c3.b,alpha3))
            fileDescriptor.write("%i %i %i %i\n" % (c0.r,c0.g,c0.b,alpha0))

        if len(f.verts) == 3:
            #split quad colors in 2 trigs colors 
            c0 = f.col[0]
            c1 = f.col[1]
            c2 = f.col[2]   
            i0 = f.verts[0].index
            i1 = f.verts[1].index
            i2 = f.verts[2].index  
            
            if i0 in vertsAlpha:
                alpha0 = 0
            if i1 in vertsAlpha:
                alpha1 = 0
            if i2 in vertsAlpha:
                alpha2 = 0
                
                      
            fileDescriptor.write("%i %i %i %i " % (c0.r,c0.g,c0.b,alpha0))
            fileDescriptor.write("%i %i %i %i " % (c1.r,c1.g,c1.b,alpha1))
            fileDescriptor.write("%i %i %i %i\n" % (c2.r,c2.g,c2.b,alpha2))

    fileDescriptor.close()

saveVertsColors("/home/manuel/myworks/makehuman/data/3dobjs/upperbar.obj.colors")
        
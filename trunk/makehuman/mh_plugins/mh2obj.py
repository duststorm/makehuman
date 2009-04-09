# You may use, modify and redistribute this module under the terms of the GNU GPL.
""" 
Export mesh data as a Wavefront obj format file.

===========================  ===============================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        mh_plugins/exportobj.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Marc Flerackers                                            
Copyright(c):                MakeHuman Team 2001-2009                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================  

This module implements a plugin to export a mesh object in Wavefront obj format.
Requires:

- base modules

"""

__docformat__ = 'restructuredtext'

import files3d

def exportObj(obj, filename):
    """
    This function exports a mesh object in Wavefront obj format. 
    
    Parameters
    ----------
   
    obj:     
      *Object3D*.  The object to export.
    filename:     
      *string*.  The filename of the file to export the object to.
    """
    
    # Write obj file
    f = open(filename, 'w')
    f.write("# MakeHuman exported OBJ\n")
    f.write("# www.makehuman.org\n")
    f.write("mtllib " + filename + ".mtl\n")
    
    for v in obj.verts:
        f.write("v %f %f %f\n" %(v.co[0], v.co[1], v.co[2]))
      
    for uv in obj.uvValues:
        f.write("vt %f %f\n" %(uv[0], uv[1]))
      
    for v in obj.verts:
        f.write("vn %f %f %f\n" %(v.no[0], v.no[1], v.no[2]))
      
    f.write("usemtl basic\n")
    f.write("s off\n")
    
    faces = files3d.loadFacesIndices("data/3dobjs/base.obj")
    for fc in faces:
        f.write("f")
        for v in fc:
          f.write(" %i/%i/%i " %(v[0] + 1, v[1] + 1, v[0] + 1))
        f.write("\n")
    f.close()
    
    # Write material file
    f = open(filename + ".mtl", 'w')
    f.write("# MakeHuman exported MTL\n")
    f.write("# www.makehuman.org\n")
    f.write("newmtl basic\n")
    f.write("Ka 1.0 1.0 1.0\n")
    f.write("Kd 1.0 1.0 1.0\n")
    f.write("Ks 0.33 0.33 0.52\n")
    f.write("illum 5\n")
    f.write("Ns 50.0\n")
    f.write("map_Kd -clamp on " + obj.texture + "\n")
    f.close()
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

This module implements a utility function to save a wavefront object from Blender.
It's needed because default Blender exporter don't support face groups.

"""

__docformat__ = 'restructuredtext'

import Blender
def saveObj(path,prefix="no"):
    """
    This function saves an object from Blender.

    Parameters
    ----------

    path:
      *path*.  The file system path to the file to be written.
    prefix:
      *string*.  The group name of the faces to export.
    """
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    data = activeObj.getData(mesh=True)
    faceUsed = []
    vertsUsed = 0
    vertsUVsUnordered = set()
    vertsUVs = {}
    vertsGroups = data.getVertGroupNames()
    vertsGroups.sort()


    checkList = range(len(data.verts))
    print len(checkList)
    try:
        fileDescriptor = open(path, "w")
    except:
        print "error to save obj file"
        return 0

    for v in data.verts:
        fileDescriptor.write("v %f %f %f\n" % (v.co[0],v.co[1],v.co[2]))

    uvIndex1 = 0
    for i,f in enumerate(data.faces):
        for uv in f.uv:
            vertsUVs[(i,uv[0],uv[1])] = uvIndex1
            fileDescriptor.write("vt %f %f\n" % (uv[0],uv[1]))
            uvIndex1 += 1
   

    for g in vertsGroups:
        print "Exporting facegroup:", g
        groupNameData = g.split('_')
        if groupNameData[0] != prefix:
            fileDescriptor.write("g %s\n" % (g))
            vIndxList = data.getVertsFromGroup(g)

            #Check if the face is contained into a facegroup
            #unfortunately, Blender don't have face group, but
            #only verts group, so a bit of work is needed here
            for nf,f in enumerate(data.faces):
                isFaceInVgroup = 1
                for v in f.verts:
                    if v.index not in vIndxList:
                        isFaceInVgroup = 0
                        break
                if isFaceInVgroup == 1 and f.index not in faceUsed:
                    faceUsed.append(f.index)
                    fileDescriptor.write("f ")
                    for i,v in enumerate(f.verts):
                        vertUV = (nf,f.uv[i][0],f.uv[i][1])
                        #+1 obj indices are 1 based, not 0 based as python
                        uvIndex = vertsUVs[vertUV] + 1
                        fileDescriptor.write("%i/%i " % (v.index+1,uvIndex))
                        vertsUsed += 1
                    fileDescriptor.write("\n")
    fileDescriptor.close()

    totVerts = 0
    for f in data.faces:
        for v in f.verts:
            totVerts += 1

    vertsNotExported = totVerts - vertsUsed
    if vertsNotExported != 0:
        print "Warning! %i verts are not associated to a part group!"%(vertsNotExported)
        print "Total faces: %i, faces exported: %i"%(len(data.faces),len(faceUsed))
        print "The %i faces not exported are selected in edit mode"%(len(data.faces)-len(faceUsed))
        for f in data.faces:
            if f.index not in faceUsed:
                print f.index
                for v in f.verts:
                    v.sel = 1



    else:
        print "Ok, done! Exported %i faces"%(len(faceUsed))

    return 1
    data.update()

saveObj("baseUUUU.obj")

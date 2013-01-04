#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ad Hoc wavefront exporter for Blender.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni

B{Copyright(c):}      MakeHuman Team 2001-2013

B{Licensing:}         AGPL3 (see also U{http://www.makehuman.org/node/318})

B{Coding Standards:}  See U{http://www.makehuman.org/node/165}

Abstract
========

This module is a special and minimal wavefront exporter, from Blender 2.4x to MH.
It include some custom features, like the placement of the special face groups at
the end of obj file, according the zbuffer drawing.
"""

import Blender
from Blender import Types
import time
import os

class SortedSet:
    """
    I use this enhanced version of the list, that use a set to 
    avoid double entries.
    """
    def __init__(self):
        self.checkElements = set()
        self.elements = []
        self.indices = {}        

    def add(self, element):
        if element not in self.checkElements:
            index = len(self.elements)
            self.checkElements.add(element)
            self.elements.append(element)
            self.indices[element] = index

    def clear(self):
        self.checkElements = set()

    def reinit(self):
        for e in self.elements:
            self.checkElements.add(e)

    def index(self,element):
        return self.indices[element]

class Element:

    """
    Because Blender has different interface to face and edge,
    I've used this simple wrapper to have a more uniform access to verts and uv.
    """

    def __init__(self, element):

        if type(element) == Types.MFaceType:
            self.verts = element.verts
            try:
                self.uv = element.uv
            except:
                self.uv = [[0,0] for x in element.verts]
        if type(element) == Types.MEdgeType:
            self.verts = [element.v1,element.v2]
            self.uv = [[0,0],[0,0]]
        self.index = element.index




class Blender2obj:
    def __init__(self, blenderObj,raw=None):
        """
        @return: None
        @type  blenderObj: Blender.Mesh obj
        @param blenderObj: It the Mesh obj of Blender 2.4x

        The init function extract some features from the Blender obj.
        - self.mesh: an istance of blender Mesh data
        - self.UV: an sorted set of the UV coords
        - self.groupNames: a list of names of verts group
        - self.vertGroups: a dictionary that use as key the group name,
          and as value the list of grouped verts
        - self.xNames: a list of names of special groups, to be moved at the end of the obj
          in order to be draw at the correct zbuffer position (for example,
          eyelashes have do be draw after the eye.
        - self.toSave: all element to export, usually the faces. If the obj has no faces,
          the elements are the edges.
        - self.specialGroups: the special groups to be draw at the end of the zbuffer.
        """

        self.mesh = blenderObj.getData(mesh=True)
        self.matrix = blenderObj.getMatrix()
        self.UV = SortedSet()
        self.groupNames = self.mesh.getVertGroupNames()
        self.groupNames.sort()
        self.grouped = set()
        self.vertGroups = {}
        self.xNames = ("lash","eyebrown","cornea")
        self.toSave = set()
        self.specialGroups = set()
        self.materialByGroups = {}

        if len(self.mesh.faces) > 0:
            print "Exporting: faces"
            for f in self.mesh.faces:
                self.toSave.add(Element(f))
        elif len(self.mesh.edges) > 0:
            print "Exporting: edges"
            for e in self.mesh.edges:
                self.toSave.add(Element(e))
        else:
            print "No faces or edges to save"
            return
        for n in self.toSave:
            for uv in n.uv:
                self.UV.add((uv[0],uv[1]))
        self.UV.clear()

        #Get the special groups, and put them at the end of the
        #group names list.
        for xName in self.xNames:
            for g in self.groupNames:
                if xName in g.split('-'):
                    self.specialGroups.add(g)
        for sGroup in self.specialGroups:
            self.groupNames.remove(sGroup)
            self.groupNames.append(sGroup)

        #Assigning the elements to facegroup (it's a bit messy, because
        #Blender doesn't have facegroups, but vertgroups only.
        
        if not raw:
            for g in self.groupNames:
                vIndices = set(self.mesh.getVertsFromGroup(g))
                groupElements = []
                for e in self.toSave:
                    isFaceInVgroup = 1
                    for v in e.verts:
                        if v.index not in vIndices:
                            isFaceInVgroup = 0
                            break
                    if isFaceInVgroup == 1:
                        if e not in self.grouped:
                            self.grouped.add(e)
                            groupElements.append(e)
                self.vertGroups[g] = groupElements
            self.ungrouped = self.toSave.difference(self.grouped)
        else:
            self.groupNames = ["raw"]
            self.vertGroups["raw"] = self.toSave
            self.ungrouped = set()        


    def write(self,path,worldSpace = None):
        """
        @return: None
        @type  path: string
        @param path: The path of wavefront obj to save
        """

        print "Saving... %s"%(os.path.basename(path))
        a = time.time()
        exportedElements = 0
        fileDescriptor = open(path, "w")
        verts = self.mesh.verts[:]          # Save a copy of the vertices
        if worldSpace:
            self.mesh.transform(self.matrix)      # Convert verts to world space
        for v in self.mesh.verts:
            fileDescriptor.write("v %f %f %f\n" % (v.co[0],v.co[1],v.co[2]))
        self.mesh.verts = verts             # Restore the original verts
        for vt in self.UV.elements:
            fileDescriptor.write("vt %f %f\n" % (vt[0],vt[1]))
        for g in self.groupNames:
            try:
                fileDescriptor.write("usemtl %s\n" % (self.materialByGroups[g]))
            except:
                pass
            fileDescriptor.write("g %s\n" % (g))
            for e in self.vertGroups[g]:
                fileDescriptor.write("f ")
                exportedElements += 1
                for i,v in enumerate(e.verts):
                    vertUV = (e.uv[i][0],e.uv[i][1])
                    #+1 obj indices are 1 based, not 0 based as python
                    uvIndex = self.UV.index(vertUV)+1
                    #uvIndex = 1
                    fileDescriptor.write("%i/%i " % (v.index+1,uvIndex))
                fileDescriptor.write("\n")
        print "Exported %d elements"%(exportedElements)

        print "Ungrouped elements: ", len(self.ungrouped)
        for e in self.ungrouped:
            fileDescriptor.write("f ")
            for i,v in enumerate(e.verts):
                vertUV = (e.uv[i][0],e.uv[i][1])
                uvIndex = self.UV.index(vertUV)+1 #+1 obj indices are 1 based
                fileDescriptor.write("%i/%i " % (v.index+1,uvIndex))
            fileDescriptor.write("\n")
        fileDescriptor.close()


        if len(self.ungrouped) != 0:
            print "Warning! %i elements are not associated to a vertgroup!"%(len(self.ungrouped))
            print "The ungrouped elements are selected in edit mode"
            for e in self.ungrouped:
                for v in e.verts:
                    v.sel = 1
        print "Exported in %s sec"%(time.time()-a)
        
    def writeGroup(self,path):
        """
        Little utility to save name groups
        """
        
        fileDescriptor = open(path, "w")        
        for g in self.groupNames:
            fileDescriptor.write("%s\n" % (g))
        fileDescriptor.close()
        
    def loadMaterial(self, path):
        fileDescriptor = open(path) 
        for data in fileDescriptor:
            dataList = data.split() 
            if len(dataList) > 1:      
                self.materialByGroups[dataList[0]] = dataList[1]

#Autotest is called as main
if __name__ == '__main__':
    activeObjs = Blender.Object.GetSelected()
    activeObj = activeObjs[0]
    bExporter = Blender2obj(activeObj,None)
    bExporter.loadMaterial("groups.dat")
    bExporter.write("base-rib.obj")
    #bExporter.writeGroup("groups.dat")

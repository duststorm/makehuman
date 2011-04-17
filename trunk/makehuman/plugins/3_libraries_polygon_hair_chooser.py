"""
B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2011

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

TO DO

"""

import gui3d, mh, os
from os import path
from aljabr import in2pts, vadd, vsub

def calculateBBox(verts):
    bbox =  [verts[0].co[:],verts[0].co[:]]
    for v in verts:
        if v.co[0] < bbox[0][0]: #minX
            bbox[0][0] = v.co[0]
        if v.co[0] > bbox[1][0]: #maxX
            bbox[1][0] = v.co[0]
        if v.co[1] < bbox[0][1]: #minY
            bbox[0][1] = v.co[1]
        if v.co[1] > bbox[1][1]: #maxY
            bbox[1][1] = v.co[1]
        if v.co[2] < bbox[0][2]: #minZ
            bbox[0][2] = v.co[2]
        if v.co[2] > bbox[1][2]: #maxX
            bbox[1][2] = v.co[2]
    return bbox

class HairTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Polygon hair')
        self.filechooser = gui3d.FileChooser(self, 'data/hairstyles', 'obj', 'png')
        
        self.prevHeadCentroid = [0.0, 7.436, 0.03 + 0.577]
        self.prevHeadBBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]]

        @self.filechooser.event
        def onFileSelected(filename):
            
            filename
            
            obj = os.path.join('data/hairstyles', filename)
            png = obj.replace('.obj', '.png')
            
            human = self.app.selectedHuman
            
            if human.hairObj:
                self.app.scene3d.clear(human.hairObj.mesh)

            human.hairObj = gui3d.Object(self.app, human.getPosition(), obj, png)
            human.hairObj.mesh.setCameraProjection(0)
            human.hairObj.mesh.setTransparentQuads(len(human.hairObj.mesh.faces))
            self.app.scene3d.update()
            self.adaptHairToHuman(human)
            
            self.app.switchCategory('Modelling')
            
    def adaptHairToHuman(self, human):

        if human.hairObj:
            
            headNames = [group.name for group in human.meshData.facesGroups if ("head" in group.name or "jaw" in group.name or "nose" in group.name or "mouth" in group.name or "ear" in group.name or "eye" in group.name)]
            headVertices = human.meshData.getVerticesAndFacesForGroups(headNames)[0]
            headBBox = calculateBBox(headVertices)
            
            headCentroid = in2pts(headBBox[0], headBBox[1], 0.5)
            delta = vsub(headCentroid, self.prevHeadCentroid)
            
            sx = (headBBox[1][0]-headBBox[0][0])/float(self.prevHeadBBox[1][0]-self.prevHeadBBox[0][0])
            sy = (headBBox[1][1]-headBBox[0][1])/float(self.prevHeadBBox[1][1]-self.prevHeadBBox[0][1])
            sz = (headBBox[1][2]-headBBox[0][2])/float(self.prevHeadBBox[1][2]-self.prevHeadBBox[0][2])
            
            self.prevHeadCentroid = headCentroid
            self.prevHeadBBox = headBBox
            
            for v in human.hairObj.mesh.verts:
                co = vsub(v.co, headCentroid)
                co[0] *= sx
                co[1] *= sy
                co[2] *= sz
                v.co = vadd(vadd(co, headCentroid), delta)
            human.hairObj.mesh.update()
        
    def onShow(self, event):
        # When the task gets shown, set the focus to the file chooser
        self.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

    def onHide(self, event):
        self.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onHumanChanged(self, event):
        
        human = event.human
        if event.change == 'reset':
            if human.hairObj:
                self.app.scene3d.clear(human.hairObj.mesh)
        def updateClosure():
            self.adaptHairToHuman(human)
        mh.callAsync(updateClosure)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = HairTaskView(category)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


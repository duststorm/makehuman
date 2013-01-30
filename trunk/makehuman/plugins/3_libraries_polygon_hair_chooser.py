#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import gui3d
import mh
import files3d
import mh2proxy
import gui
import filechooser as fc
import log

class HairTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Hair')        
        hairDir = os.path.join(mh.getPath(''), 'data', 'hairstyles')
        if not os.path.exists(hairDir):
            os.makedirs(hairDir)
        self.filechooser = self.addTopWidget(fc.FileChooser([hairDir , 'data/hairstyles'], 'obj', 'thumb', 'data/hairstyles/notfound.thumb'))
        self.addLeftWidget(self.filechooser.sortBox)
      
        self.oHeadCentroid = [0.0, 7.436, 0.03 + 0.577]
        self.oHeadBBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]]

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            
            mhclo = filename.replace('.obj', '.mhclo')
            self.setHair(gui3d.app.selectedHuman, filename, mhclo)
            if gui3d.app.settings.get('jumpToModelling', True):
                mh.changeCategory('Modelling')

    def setHair(self, human, obj, mhclo):

        if human.hairObj:
            gui3d.app.removeObject(human.hairObj)
            human.hairObj = None
            human.hairProxy = None

        if os.path.basename(obj) == "clear.obj":
            return
            
        mesh = files3d.loadMesh(obj)
        if mesh:
            human.hairProxy = mh2proxy.readProxyFile(human.meshData, mhclo, False)
            if human.hairProxy.texture:
                (folder, name) = human.hairProxy.texture
                tex = os.path.join(folder, name)
                mesh.setTexture(tex)
            else:
                tex = obj.replace('.obj', '_texture.png')
                mesh.setTexture(tex)

            human.hairObj = gui3d.app.addObject(gui3d.Object(human.getPosition(), mesh))
            human.hairObj.setRotation(human.getRotation())
            human.hairObj.mesh.setCameraProjection(0)
            human.hairObj.mesh.setSolid(human.mesh.solid)
            if human.hairProxy.cull:
                human.hairObj.mesh.setCull(1)
            else:
                human.hairObj.mesh.setCull(None)
            human.hairObj.mesh.setTransparentPrimitives(len(human.hairObj.mesh.faces))
            human.hairObj.mesh.priority = 20
                
            hairName = human.hairObj.mesh.name.split('.')[0]

            self.adaptHairToHuman(human)
            human.hairObj.setSubdivided(human.isSubdivided())

    def adaptHairToHuman(self, human):

        if human.hairObj and human.hairProxy:
            
            mesh = human.hairObj.getSeedMesh()
            human.hairProxy.update(mesh, human.meshData)
            mesh.update()
            if human.hairObj.isSubdivided():
                human.hairObj.getSubdivisionMesh()
        
    def onShow(self, event):
        # When the task gets shown, set the focus to the file chooser
        gui3d.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onHumanChanging(self, event):
        
        human = event.human
        if event.change == 'reset':
            if human.hairObj:
                human.hairObj.mesh.clear()
                human.hairObj = None
                human.hairProxy = None
        
    def onHumanChanged(self, event):
        
        human = event.human
        self.adaptHairToHuman(human)

    def loadHandler(self, human, values):
        
        mhclo = values[1]
        if not os.path.exists(os.path.realpath(mhclo)):
            log.notice('HairTaskView.loadHandler: %s does not exist. Skipping.', mhclo)
            return
        obj = mhclo.replace(".mhclo", ".obj")
        self.setHair(human, obj, mhclo)
        
    def saveHandler(self, human, file):
        
        if human.hairProxy:
            file.write('hair %s\n' % human.hairProxy.file)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addTask(HairTaskView(category))

    app.addLoadHandler('hair', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


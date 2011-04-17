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

class HairTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Polygon hair')
        self.filechooser = gui3d.FileChooser(self, 'data/hairstyles', 'obj', 'png')

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
            self.adaptHairToHuman(human)
            self.app.scene3d.update()
            
            self.app.switchCategory('Modelling')
            
    def adaptHairToHuman(self, human):
        
        if human.hairObj:
            for v in human.hairObj.mesh.verts:
                v.co[2] -= 0.577
            #human.hairObj.mesh.update() Uncomment once we have a decent hair adaption

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
        self.adaptHairToHuman(human)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = HairTaskView(category)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


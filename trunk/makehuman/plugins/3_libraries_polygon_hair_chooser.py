"""
B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2011

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

TO DO

"""

import gui3d, mh, os
import files3d
from aljabr import in2pts, vadd, vsub, calcBBox
import mh2proxy
import export_config
import qtgui as gui
import filechooser as fc

class HairTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Hair')        
        hairDir = os.path.join(mh.getPath(''), 'data', 'hairstyles')
        if not os.path.exists(hairDir):
            os.makedirs(hairDir)
        self.filechooser = self.addWidget(mh.addWidget(mh.Frame.Top, fc.FileChooser([hairDir , 'data/hairstyles'], 'obj', 'png', 'data/hairstyles/notfound.png')))
      
        self.oHeadCentroid = [0.0, 7.436, 0.03 + 0.577]
        self.oHeadBBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]]

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            
            mhclo = filename.replace('.obj', '.mhclo')
            self.setHair(gui3d.app.selectedHuman, filename, mhclo)            
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
            human.hairObj.mesh.setTransparentPrimitives(len(human.hairObj.mesh.faces))
            human.hairObj.mesh.originalHairVerts = [v.co[:] for v in human.hairObj.mesh.verts]
                
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
            print mhclo, "does not exist. Skipping."
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
    taskview = category.addView(HairTaskView(category))

    app.addLoadHandler('hair', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


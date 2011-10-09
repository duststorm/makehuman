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
import files3d
import mh2proxy

class ClothesTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Clothes')
        self.filechooser = gui3d.FileChooser(self, 'data/clothes', 'obj', 'png', 'notfound.png')

        @self.filechooser.event
        def onFileSelected(filename):
            
            self.setClothes(self.app.selectedHuman, filename)

            self.app.switchCategory('Modelling')
        
    def setClothes(self, human, obj):

        print("Clothes file", obj)
        (name, ext) = os.path.splitext(os.path.basename(obj))
        tif = None

        try:
            clo = human.clothesObjs[name]
        except:
            clo = None
        if clo:
            self.app.scene3d.delete(clo.mesh)
            del human.clothesObjs[name]
            return

        mesh = files3d.loadMesh(self.app.scene3d, obj)
        #mesh.setTexture(tif)
        
        clo = gui3d.Object(self.app, human.getPosition(), mesh)
        clo.setRotation(human.getRotation())
        clo.mesh.setCameraProjection(0)
        clo.mesh.setSolid(human.mesh.solid)
        clo.mesh.setTransparentPrimitives(len(clo.mesh.faces))
        clo.mesh.originalClothesVerts = [v.co[:] for v in clo.mesh.verts]
        human.clothesObjs[name] = clo
        
        file = "data/clothes/%s/%s.mhclo" % (name,name)
        print("Loading %s" % file)
        human.clothesProxies[name] = mh2proxy.readProxyFile(human.meshData, file, False)

        self.app.scene3d.update()
        self.adaptClothesToHuman(human)
        clo.setSubdivided(human.isSubdivided())
        
        #self.clothesButton.setTexture(obj.replace('.obj', '.png'))
    
    def adaptClothesToHuman(self, human):

        for (name,clo) in human.clothesObjs.items():            
            if clo:
                mesh = clo.getSeedMesh()
                human.clothesProxies[name].update(mesh, human.meshData)
                mesh.update()
                if clo.isSubdivided():
                    clo.getSubdivisionMesh()

    def onShow(self, event):
        # When the task gets shown, set the focus to the file chooser
        self.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

    def onHide(self, event):
        self.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onResized(self, event):
        self.filechooser.onResized(event)

    def onHumanChanged(self, event):
        
        human = event.human
        if event.change == 'reset':
            for (name,clo) in human.clothesObjs.items():
                if clo:
                    self.app.scene3d.delete(clo.mesh)
                del human.clothesObjs[name]
                del human.clothesProxies[name]
            # self.clothesButton.setTexture('data/clothes/clear.png')
        def updateClosure():
            self.adaptClothesToHuman(human)
        mh.callAsync(updateClosure)

    def loadHandler(self, human, values):
        
        self.setClothes(human, values[1])
        
    def saveHandler(self, human, file):
        
        for clo in human.clothesObjs.values():
            if clo:
                file.write('clothes %s\n' % clo.mesh.name)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = ClothesTaskView(category)

    app.addLoadHandler('clothes', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


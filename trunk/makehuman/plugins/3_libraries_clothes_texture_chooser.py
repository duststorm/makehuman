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
import download
import files3d
import mh2proxy
import export_config
import qtgui as gui
import filechooser as fc
import log

#
#   Textures
#

class TexturesTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        self.systemTextures = os.path.join('data', 'clothes', 'textures')
        self.userTextures = os.path.join(mh.getPath(''), 'data', 'clothes', 'textures')
        self.defaultTextures = [self.systemTextures, self.userTextures]  
        self.textures = self.defaultTextures

        gui3d.TaskView.__init__(self, category, 'Textures')
        if not os.path.exists(self.userTextures):
            os.makedirs(self.userTextures)

        self.filewidget = mh.addWidget(mh.Frame.Top, fc.FileChooser(self.defaultTextures, 'png', 'png'))
        self.filechooser = self.addWidget(self.filewidget)
        self.update = self.filechooser.sortBox.addWidget(gui.Button('Check for updates'))
        self.mediaSync = None 
        self.activeClothing = None
        
        #self.clothesBox = mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Textures'))
        #self.cloGroup = []
        #for i, uuid in enumerate(theClothesList):
        #    filepath = human.clothesProxies[uuid].file
        #    print "  ", filepath
        #    self.clothesBox.addWidget(RadioButton(self.cloGroup, filepath, False))
        

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            human = gui3d.app.selectedHuman
            uuid = human.activeClothing
            if uuid:
                clo = human.clothesObjs[uuid]
                clo.mesh.setTexture(filename)
            mh.changeCategory('Modelling')

        #@self.clothesBox.mhEvent
        #def onClicked(event):
        #    print "ClothesBox clicked", event, event.change
            
        @self.update.mhEvent
        def onClicked(event):
            self.syncMedia()

    def onShow(self, event):
        human = gui3d.app.selectedHuman

        print "onShow", human.clothesObjs
        #if human.activeClothing is None:
        #    self.onHide(event)
        #    return
            
        gui3d.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)

        if human.activeClothing != self.activeClothing:
            uuid = human.activeClothing
            self.activeClothing = uuid
            if uuid:
                clo = human.clothesObjs[uuid]
                filepath = human.clothesProxies[uuid].file
                print "onShow", clo, filepath
                self.textures = [os.path.dirname(filepath)] + self.defaultTextures            
            else:
                self.textures = self.defaultTextures            
            
            fc = self.filechooser
            print "  fc", fc, fc.children.count(), fc.files
            print "  added"

        self.filechooser.setFocus()
        
        #if not os.path.isdir(self.userClothes) or not len([filename for filename in os.listdir(self.userClothes) if filename.lower().endswith('mhclo')]):    
        #    gui3d.app.prompt('No user clothes found', 'You don\'t seem to have any user clothes, download them from the makehuman media repository?\nNote: this can take some time depending on your connection speed.', 'Yes', 'No', self.syncMedia)

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onHumanChanging(self, event):        
        human = event.human
        if event.change == 'reset':
            log.message("deleting textures")
            # self.clothesButton.setTexture('data/clothes/clear.png')

    def onHumanChanged(self, event):
        pass        

    def loadHandler(self, human, values):
        pass
        
    def saveHandler(self, human, file):
        pass
        
    def syncMedia(self):
        
        if self.mediaSync:
            return
        if not os.path.isdir(self.userTextures):
            os.makedirs(self.userTextures)
        self.mediaSync = download.MediaSync(gui3d.app, self.userTextures, 'http://download.tuxfamily.org/makehuman/clothes/textures/', self.syncMediaFinished)
        self.mediaSync.start()
        
    def syncMediaFinished(self):
        
        self.mediaSync = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addTask(TexturesTaskView(category))

    app.addLoadHandler('textures', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass




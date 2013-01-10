#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import gui3d, mh, os
import download
import files3d
import mh2proxy
import export_config
import gui
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

        gui3d.TaskView.__init__(self, category, 'Clothes Textures')
        if not os.path.exists(self.userTextures):
            os.makedirs(self.userTextures)

        self.filechooser = self.addTopWidget(fc.FileChooser(self.defaultTextures, 'png', 'png'))
        self.addLeftWidget(self.filechooser.sortBox)
        self.update = self.filechooser.sortBox.addWidget(gui.Button('Check for updates'))
        self.mediaSync = None
        self.activeClothing = None
        
        #self.clothesBox = self.addLeftWidget(gui.GroupBox('Textures'))
        #self.cloGroup = []
        #for i, uuid in enumerate(theClothesList):
        #    filepath = human.clothesProxies[uuid].file
        #    log.debug("  " + filepath)
        #    self.clothesBox.addWidget(RadioButton(self.cloGroup, filepath, False))

        self.clothesBox = self.addRightWidget(gui.GroupBox('Clothes'))
        self.appliedClothes = []
        self.clothesSelections = []

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            if not self.activeClothing:
                return
            uuid = self.activeClothing
            self.applyTexture(uuid, filename)
            mh.changeCategory('Modelling')

        #@self.clothesBox.mhEvent
        #def onClicked(event):
        #    log.debug("ClothesBox clicked %s %s" % (event, event.change)
            
        @self.update.mhEvent
        def onClicked(event):
            self.syncMedia()

    def onShow(self, event):
        human = gui3d.app.selectedHuman

        for radioBtn in self.appliedClothes:
            radioBtn.hide()
            radioBtn.destroy()
        self.appliedClothes = []
        self.clothesSelections = []
        theClothesList = human.clothesObjs.keys()
        self.activeClothing = None
        for i, uuid in enumerate(theClothesList):
            if i == 0:
                self.activeClothing = uuid
            radioBtn = self.clothesBox.addWidget(gui.RadioButton(self.appliedClothes, human.clothesProxies[uuid].name, selected=len(self.appliedClothes) == 0))
            self.clothesSelections.append( (radioBtn, uuid) )

            @radioBtn.mhEvent
            def onClicked(event):
                for radio, uuid in self.clothesSelections:
                    if radio.selected:
                        self.activeClothing = uuid
                        log.debug( 'Selected clothing "%s" (%s)' % (radio.text(), uuid) )
                        self.reloadTextureChooser()
                        return

        gui3d.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)

        self.reloadTextureChooser()
        
        #if not os.path.isdir(self.userClothes) or not len([filename for filename in os.listdir(self.userClothes) if filename.lower().endswith('mhclo')]):    
        #    gui3d.app.prompt('No user clothes found', 'You don\'t seem to have any user clothes, download them from the makehuman media repository?\nNote: this can take some time depending on your connection speed.', 'Yes', 'No', self.syncMedia)

    def applyTexture(self, uuid, filename):
        human = gui3d.app.selectedHuman
        clo = human.clothesObjs[uuid]
        clo.mesh.setTexture(filename)

    def reloadTextureChooser(self):
        human = gui3d.app.selectedHuman
        if self.activeClothing:
            uuid = self.activeClothing
            clo = human.clothesObjs[uuid]
            filepath = human.clothesProxies[uuid].file
            log.debug("onShow %s %s", clo, filepath)
            self.textures = [os.path.dirname(filepath)] + self.defaultTextures            
        else:
            # TODO maybe dont show anything?
            self.textures = self.defaultTextures            
            
            fc = self.filechooser
            log.debug("fc %s %s %s added", fc, fc.children.count(), str(fc.files))

        # Reload filechooser
        self.filechooser.paths = self.textures
        self.filechooser.refresh()
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onHumanChanging(self, event):
	pass

    def onHumanChanged(self, event):
        pass

    def loadHandler(self, human, values):
        uuid = values[1]
        filepath = values[2]
        if not uuid in human.clothesProxies.keys():
            log.error("Could not load texture for object with uuid %s!" % uuid)
            return
        proxy = human.clothesProxies[uuid]
        if not os.path.dirname(filepath):
            proxy = human.clothesProxies[uuid]
            clothesPath = os.path.dirname(proxy.file)
            filepath = os.path.join(clothesPath, filepath)
        self.applyTexture(uuid, filepath)

    def saveHandler(self, human, file):
        for name, clo in human.clothesObjs.items():
            if clo:
                proxy = human.clothesProxies[name]
                if clo.mesh.texture != proxy.texture[0]+"/"+proxy.texture[1]:
                    clothesPath = os.path.dirname(proxy.file)
                    if os.path.dirname(clo.mesh.texture) == clothesPath:
                        texturePath = os.path.basename(clo.mesh.texture)
                    else:
                        texturePath = clo.mesh.texture
                    file.write('textures %s %s\n' % (proxy.getUuid(), texturePath))

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

    #app.addLoadHandler('textures', taskview.loadHandler)
    #app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass




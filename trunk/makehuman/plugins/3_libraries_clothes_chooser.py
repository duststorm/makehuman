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

import gui3d, mh, os
import download
import files3d
import mh2proxy
import export_config
import gui
import filechooser as fc
import log

KnownTags = [
    "shoes",
    "dress",
    "tshirt",
    "stockings",
    "trousers",
    "shirt",
    "underwearbottom",
    "underweartop",
]

#
#   Clothes
#

class ClothesTaskView(gui3d.TaskView):
    
    def __init__(self, category):

        self.systemClothes = os.path.join('data', 'clothes')
        self.userClothes = os.path.join(mh.getPath(''), 'data', 'clothes')

        self.taggedClothes = {}
        self.clothesList = []
        
        gui3d.TaskView.__init__(self, category, 'Clothes')
        if not os.path.exists(self.userClothes):
            os.makedirs(self.userClothes)
        self.filechooser = self.addTopWidget(fc.FileChooser([self.systemClothes, self.userClothes], 'mhclo', 'png', 'data/clothes/notfound.png'))
        self.addLeftWidget(self.filechooser.sortBox)
        self.update = self.filechooser.sortBox.addWidget(gui.Button('Check for updates'))
        self.mediaSync = None

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            self.setClothes(gui3d.app.selectedHuman, filename)
            mh.changeCategory('Modelling')

        @self.update.mhEvent
        def onClicked(event):
            self.syncMedia()

        
    def setClothes(self, human, filepath):
        if os.path.basename(filepath) == "clear.mhclo":
            for name,clo in human.clothesObjs.items():
                gui3d.app.removeObject(clo)
                del human.clothesObjs[name]
            self.clothesList = []
            human.activeClothing = None
            return

        proxy = mh2proxy.readProxyFile(human.meshData, filepath, False)
        
        if not proxy:
            return

        uuid = proxy.getUuid()
        
        if proxy.clothings:
            t = 0
            dt = 1.0/len(proxy.clothings)
            folder = os.path.dirname(filepath)
            for piece in proxy.clothings:
                gui3d.app.progress(t, text="Loading %s" % piece)
                t += dt
                piecedir = os.path.join(folder, piece)
                log.message("Find %s", piecedir)
                if os.path.exists(piecedir):
                    piecefile = os.path.join(piecedir, piece + ".mhclo")
                else:
                    piecefile = piecedir + ".mhclo"
                self.setClothes(human, piecefile)
            gui3d.app.progress(1, text="%s loaded" % proxy.name)
            return
            
        #folder = os.path.dirname(filepath)
        (folder, name) = proxy.obj_file
        obj = os.path.join(folder, name)

        try:
            clo = human.clothesObjs[uuid]
        except:
            clo = None
        if clo:
            gui3d.app.removeObject(clo)
            del human.clothesObjs[uuid]
            self.clothesList.remove(uuid)
            if human.activeClothing == uuid:
                human.activeClothing = None
            log.message("Removed clothing %s %s", proxy.name, uuid)
            return

        mesh = files3d.loadMesh(obj)
        if proxy.texture:
            (dir, name) = proxy.texture
            tex = os.path.join(folder, name)
            if not os.path.exists(tex):
                tex = os.path.join(self.systemClothes, "textures", name)
            mesh.setTexture(tex)
        else:
            pass
        
        clo = gui3d.app.addObject(gui3d.Object(human.getPosition(), mesh))
        clo.setRotation(human.getRotation())
        clo.mesh.setCameraProjection(0)
        clo.mesh.setSolid(human.mesh.solid)
        clo.mesh.setTransparentPrimitives(len(clo.mesh.faces))
        clo.mesh.originalClothesVerts = [v.co[:] for v in clo.mesh.verts]
        clo.mesh.priority = 10
        human.clothesObjs[uuid] = clo        
        human.clothesProxies[uuid] = proxy
        human.activeClothing = uuid
        self.clothesList.append(uuid)
        
        for tag in proxy.tags:
            tag = tag.lower()
            if tag in KnownTags:
                try:
                    oldUuids = self.taggedClothes[tag]
                except KeyError:
                    oldUuids = []
                newUuids = []
                for oldUuid in oldUuids:
                    if oldUuid == uuid:
                        pass
                    elif True:
                        try:
                            oldClo = human.clothesObjs[oldUuid]
                        except KeyError:
                            continue
                        log.message("Removed clothing %s", oldUuid)
                        gui3d.app.removeObject(oldClo)
                        del human.clothesObjs[oldUuid]
                        self.clothesList.remove(oldUuid)
                        if human.activeClothing == oldUuid:
                            human.activeClothing = None
                    else:
                        log.message("Kept clothing %s", oldUuid)
                        newUuids.append(oldUuid)
                newUuids.append(uuid)
                self.taggedClothes[tag] = newUuids

        self.adaptClothesToHuman(human)
        clo.setSubdivided(human.isSubdivided())
        
        #self.clothesButton.setTexture(obj.replace('.obj', '.png'))

    
    def adaptClothesToHuman(self, human):

        for (uuid,clo) in human.clothesObjs.items():            
            if clo:
                mesh = clo.getSeedMesh()
                human.clothesProxies[uuid].update(mesh, human.meshData)
                mesh.update()
                if clo.isSubdivided():
                    clo.getSubdivisionMesh()

    def onShow(self, event):
        # When the task gets shown, set the focus to the file chooser
        gui3d.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()
        
        #if not os.path.isdir(self.userClothes) or not len([filename for filename in os.listdir(self.userClothes) if filename.lower().endswith('mhclo')]):    
        #    gui3d.app.prompt('No user clothes found', 'You don\'t seem to have any user clothes, download them from the makehuman media repository?\nNote: this can take some time depending on your connection speed.', 'Yes', 'No', self.syncMedia)

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onHumanChanging(self, event):
        
        human = event.human
        if event.change == 'reset':
            log.message("deleting clothes")
            for (uuid,clo) in human.clothesObjs.items():
                if clo:
                    gui3d.app.removeObject(clo)
                del human.clothesObjs[uuid]
                del human.clothesProxies[uuid]
            self.clothesList = []
            human.activeClothing = None
            # self.clothesButton.setTexture('data/clothes/clear.png')

    def onHumanChanged(self, event):
        
        human = event.human
        self.adaptClothesToHuman(human)

    def loadHandler(self, human, values):

        mhclo = export_config.getExistingProxyFile(values, "clothes")
        if not mhclo:
            log.notice("%s does not exist. Skipping.", values[1])
        else:            
            self.setClothes(human, mhclo)
        
    def saveHandler(self, human, file):
        
        for name in self.clothesList:
            clo = human.clothesObjs[name]
            if clo:
                proxy = human.clothesProxies[name]
                file.write('clothes %s %s\n' % (os.path.basename(proxy.file), proxy.getUuid()))
                
    def syncMedia(self):
        
        if self.mediaSync:
            return
        if not os.path.isdir(self.userClothes):
            os.makedirs(self.userClothes)
        self.mediaSync = download.MediaSync(gui3d.app, self.userClothes, 'http://download.tuxfamily.org/makehuman/clothes/', self.syncMediaFinished)
        self.mediaSync.start()
        
    def syncMediaFinished(self):
        
        self.mediaSync = None


# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addTask(ClothesTaskView(category))

    app.addLoadHandler('clothes', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


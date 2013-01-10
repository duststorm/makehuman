#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Jonas Hauquier, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO

"""

__docformat__ = 'restructuredtext'


import gui3d, mh, os
import download
import files3d
import module3d
import mh2proxy
import export_config
import gui
import filechooser as fc
import log

class Action:

    def __init__(self, human, before, after, postAction=None):
        self.name = 'Change texture'
        self.human = human
        self.before = before
        self.after = after
        self.postAction = postAction

    def do(self):
        self.human.setTexture(self.after)
        self.human.mesh.setShadeless(False)
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        self.human.setTexture(self.before)
        if self.postAction:
            self.postAction()
        return True

class TextureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Texture', label='Textures')

        self.systemSkins = os.path.join('data', 'skins')
        self.systemTextures = os.path.join('data', 'clothes', 'textures')

        self.userSkins = os.path.join(mh.getPath(''), 'data', 'skins')
        self.userTextures = os.path.join(mh.getPath(''), 'data', 'clothes', 'textures')
        if not os.path.exists(self.userSkins):
            os.makedirs(self.userSkins)
        if not os.path.exists(self.userTextures):
            os.makedirs(self.userTextures)

        self.defaultTextures = [self.systemTextures, self.userTextures]  
        self.textures = self.defaultTextures
        self.activeClothing = None
        self.eyeTexture = None

        # TODO
        self.filechooser = self.addTopWidget(fc.FileChooser(self.defaultTextures, 'png', ['thumb', 'png'], 'data/skins/notfound.thumb'))
        #self.filechooser = self.addTopWidget(fc.FileChooser([self.systemSkins, self.userSkins], 'png', 'thumb', 'data/skins/notfound.thumb'))
        self.addLeftWidget(self.filechooser.sortBox)
        self.update = self.filechooser.sortBox.addWidget(gui.Button('Check for updates'))
        self.mediaSync = None
        self.mediaSync2 = None

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            # TODO add undo action
            if self.skinRadio.selected:
                gui3d.app.do(Action(gui3d.app.selectedHuman,
                gui3d.app.selectedHuman.getTexture(),
                filename))
            elif self.hairRadio.selected:
                gui3d.app.selectedHuman.hairObj.mesh.setTexture(filename)
            elif self.eyesRadio.selected:
                self.setEyes(gui3d.app.selectedHuman, filename)
            else: # Clothes
                if self.activeClothing:
                    uuid = self.activeClothing
                    self.applyClothesTexture(uuid, filename)

            mh.changeCategory('Modelling')
            
        @self.update.mhEvent
        def onClicked(event):
            self.syncMedia()

        self.objectSelector = []
        self.humanBox = self.addRightWidget(gui.GroupBox('Human'))
        self.skinRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Skin", selected=True))
        self.hairRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Hair", selected=False))
        self.eyesRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Eyes", selected=False))

        @self.skinRadio.mhEvent
        def onClicked(event):
            if self.skinRadio.selected:
                self.reloadTextureChooser()

        @self.hairRadio.mhEvent
        def onClicked(event):
            if self.hairRadio.selected:
                self.reloadTextureChooser()

        @self.eyesRadio.mhEvent
        def onClicked(event):
            if self.eyesRadio.selected:
                self.reloadTextureChooser()

        self.clothesBox = self.addRightWidget(gui.GroupBox('Clothes'))
        self.clothesSelections = []


    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        human = gui3d.app.selectedHuman
        human.hide()

        self.skinRadio.setChecked(True)
        self.reloadTextureChooser()

        if human.hairObj:
            self.hairRadio.setEnabled(True)
        else:
            self.hairRadio.setEnabled(False)

        self.populateClothesSelector()

        # Offer to download skins if none are found    
        self.numSkin = len([filename for filename in os.listdir(os.path.join(mh.getPath(''), 'data', 'skins')) if filename.lower().endswith('png')])
        if self.numSkin < 1:    
            gui3d.app.prompt('No skins found', 'You don\'t seem to have any skins, download them from the makehuman media repository?\nNote: this can take some time depending on your connection speed.', 'Yes', 'No', self.syncMedia)


    def populateClothesSelector(self):
        """
        Builds a list of all available clothes.
        """
        human = gui3d.app.selectedHuman
        for radioBtn in self.objectSelector[3:]:
            radioBtn.hide()
            radioBtn.destroy()
        self.objectSelector = self.objectSelector[:3] # Only keep first 3 radio btns (human body parts)
        self.clothesSelections = []
        theClothesList = human.clothesObjs.keys()
        self.activeClothing = None
        for i, uuid in enumerate(theClothesList):
            if i == 0:
                self.activeClothing = uuid
            radioBtn = self.clothesBox.addWidget(gui.RadioButton(self.objectSelector, human.clothesProxies[uuid].name, selected=False))
            self.clothesSelections.append( (radioBtn, uuid) )

            @radioBtn.mhEvent
            def onClicked(event):
                for radio, uuid in self.clothesSelections:
                    if radio.selected:
                        for bodyRdio in self.objectSelector[:3]:
                            print bodyRdio
                            bodyRdio.setChecked(False) # Because radiobuttons group gets disconnected after repopulating
                        self.activeClothing = uuid
                        log.debug( 'Selected clothing "%s" (%s)' % (radio.text(), uuid) )
                        self.reloadTextureChooser()
                        return

    def applyClothesTexture(self, uuid, filename):
        human = gui3d.app.selectedHuman
        clo = human.clothesObjs[uuid]
        clo.mesh.setTexture(filename)

    def setEyes(self, human, mhstx):
        # TODO this will change, for now eyes might only be compatible with the original skin
        f = open(mhstx, 'rU')
        try:
            subTextures = eval(f.read(), {"__builtins__":None}, {'True':True, 'False':False})
        except:
            log.warning("setEyes(%s)", mhstx, exc_info=True)
            f.close()
            return
        f.close()
        
        texture = module3d.getTexture(human.getTexture())
        img = mh.Image(human.getTexture())
        
        for subTexture in subTextures:
            path = os.path.join('data/eyes', subTexture['txt'])
            subImg = mh.Image(path)
            x, y = subTexture['dst']
            img.blit(subImg, x, y)
            
        texture.loadSubImage(img, 0, 0)
        self.eyeTexture = mhstx

    def reloadTextureChooser(self):
        human = gui3d.app.selectedHuman
        # TODO this is temporary, until new eye texturing approach
        if 'data/eyes' in self.filechooser.paths:
            self.filechooser.previewExtension = 'thumb'
            self.filechooser.previewExtensions = ['thumb', 'png']
            self.filechooser.extension = 'png'
            
        if self.skinRadio.selected:
            self.textures = [self.systemSkins, self.userSkins] + self.defaultTextures
        elif self.hairRadio.selected:
            proxy = human.hairProxy
            self.textures = [os.path.dirname(proxy.file)] + self.defaultTextures
        elif self.eyesRadio.selected:
            self.filechooser.previewExtension = 'png'
            self.filechooser.previewExtensions = ['png']
            self.filechooser.extension = 'mhstx'
            self.textures = ['data/eyes']
        else: # Clothes
            if self.activeClothing:
                uuid = self.activeClothing
                clo = human.clothesObjs[uuid]
                filepath = human.clothesProxies[uuid].file
                self.textures = [os.path.dirname(filepath)] + self.defaultTextures            
            else:
                # TODO maybe dont show anything?
                self.textures = self.defaultTextures            
                
                filec = self.filechooser
                log.debug("fc %s %s %s added", filec, filec.children.count(), str(filec.files))

        # Reload filechooser
        self.filechooser.paths = self.textures
        self.filechooser.refresh()
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onHumanChanging(self, event):
        pass
        
    def loadHandler(self, human, values):
        
        if values[0] == 'skinTexture':
            (fname, ext) = os.path.splitext(values[1])
            if fname != "texture":
                path = os.path.join(os.path.join(mh.getPath(''), 'data', 'skins', values[1]))
                if os.path.isfile(path):                    
                    human.setTexture(path)
                elif ext == ".tif":
                    path = path.replace(".tif", ".png")
                    human.setTexture(path)
        elif values[0] == 'textures':
            uuid = values[1]
            filepath = values[2]
            if human.hairProxy and human.hairProxy.getUuid() == uuid:
                if not os.path.dirname(filepath):
                    proxy = human.hairProxy
                    hairPath = os.path.dirname(proxy.file)
                    filepath = os.path.join(hairPath, filepath)
                human.hairObj.mesh.setTexture(filePath)
            elif not uuid in human.clothesProxies.keys():
                log.error("Could not load texture for object with uuid %s!" % uuid)
                return
            proxy = human.clothesProxies[uuid]
            if not os.path.dirname(filepath):
                proxy = human.clothesProxies[uuid]
                clothesPath = os.path.dirname(proxy.file)
                filepath = os.path.join(clothesPath, filepath)
            self.applyClothesTexture(uuid, filepath)
        elif values[0] == 'eyeTexture':
            self.setEyes(human, values[1])
       
    def saveHandler(self, human, file):
        
        file.write('skinTexture %s\n' % os.path.basename(human.getTexture()))
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
        if self.eyeTexture:
            file.write('eyeTexture %s' % self.eyeTexture)

    def syncMedia(self):
        
        if self.mediaSync:
            return
        if not os.path.isdir(self.skinsFolder):
            os.makedirs(self.skinsFolder)
        self.mediaSync = download.MediaSync(gui3d.app, self.skinsFolder, 'http://download.tuxfamily.org/makehuman/skins/', self.syncMediaFinished)
        self.mediaSync.start()
        self.mediaSync2 = None
        
    def syncMediaFinished(self):
        '''
        if not self.mediaSync2:
            if not os.path.isdir(self.userTextures):
                os.makedirs(self.userTextures)
            self.mediaSync2 = download.MediaSync(gui3d.app, self.userTextures, 'http://download.tuxfamily.org/makehuman/clothes/textures/', self.syncMediaFinished)
            self.mediaSync2.start()
            self.mediaSync = None
        else:
            self.mediaSync = None
            self.filechooser.refresh()
        '''

        self.mediaSync = None
        self.filechooser.refresh()
        
# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addTask(TextureTaskView(category))

    app.addLoadHandler('textures', taskview.loadHandler)
    app.addLoadHandler('skinTexture', taskview.loadHandler)
    app.addLoadHandler('eyeTexture', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)



# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass

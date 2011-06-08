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

#import zipfile
import gui3d, mh
from os import path

HairButtonStyle = gui3d.Style(**{
    'width':32,
    'height':32,
    'mesh':None,
    'normal':None,
    'selected':None,
    'focused':None,
    'fontSize':gui3d.defaultFontSize,
    'border':None
    })

class HairTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, "Hair")
        self.human = None
        self.filechooser = gui3d.FileChooser(self, "data/hairs", "hair", "png")
        self.default = True
        self.saveAsCurves = True
        self.path = None
        self.guides = []
        self.widthFactor = 1.0
        self.oHeadCentroid = [0.0, 7.436, 0.03]
        self.oHeadBoundingBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]]
        self.hairDiameterMultiStrand = 0.006
        self.tipColor = [0.518, 0.325, 0.125]
        self.rootColor = [0.109, 0.037, 0.007]
        self.interpolationRadius = 0.09
        self.clumpInterpolationNumber = 0
        #self.app.categories["Rendering"].hairsClass = self
        
        hairTexture = self.app.selectedHuman.hairFile.replace('.hair', '.png')
        self.currentHair = gui3d.Button(self.app.categories['Modelling'], [800-216, 600-36, 9.2], style=HairButtonStyle._replace(normal=hairTexture))

        @self.currentHair.event
        def onClicked(event):
            self.app.switchCategory('Library')
            self.app.switchTask("Hair")

        @self.filechooser.event
        def onFileSelected(filename, update=1):
            #hair files comes in pair, .obj and .hair.
            #.obj files contain geometric detail of the hair (can be edited by any 3rd party modelling software that opens wavefront .obj)
            #.hair files contain metadata of hair used by the makehair utility
            filename = path.splitext(filename)[0]
            print("Loading %s" %(filename))
            human = self.app.selectedHuman
            if human.hairObj: human.scene.clear(human.hairObj)

            human.hairObj = human.hairs.loadHair(path="./data/hairs/"+filename, update=update)

            self.app.switchCategory("Modelling")
            human.setHairFile(path.join('data/hairs', filename + ".obj"))
            hairTexture = human.hairFile.replace('.obj', '.png')
            self.currentHair.setTexture(hairTexture)

    def onShow(self, event):
        # When the task gets shown, set the focus to the file chooser
        self.app.selectedHuman.hide()
        if self.default:
          self.default = False
          self.filechooser.selectedFile = self.filechooser.files.index("default.hair")
          self.filechooser.onShow(event)
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

    def onHide(self, event):
        self.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
    
    def onResized(self, event):
        self.currentHair.setPosition([event.width-216, event.height-36, 9.2])
        self.filechooser.onResized(event)

    def onHumanChanged(self, event):
        
        human = event.human
        if event.change == 'reset':
            self.filechooser.selection = 'default.hair'
        if human.hairObj:
            self.human = human
            mh.callAsync(self.updateHair)

    def updateHair(self):
        if self.human and self.human.hairObj:
            if self.filechooser.files:
                self.filechooser.onFileSelected(self.filechooser.selection, update=1)
            self.human.hairObj.update()
            self.app.redraw()
        self.human = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = HairTaskView(category)

    print 'Hair chooser loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    print 'Hair chooser unloaded'


#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, aljabr, mh
    
class CensorTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Censor')
        
        self.mouseBox = gui3d.GroupBox(self, [10, 80, 9.0], 'Censor', gui3d.GroupBoxStyle._replace(height=25+25*3+24+6))
        self.enableCensor = gui3d.CheckBox(self.mouseBox, "Enable", self.app.settings.get('censor', False))
        type = []
        self.blackSquare = gui3d.RadioButton(self.mouseBox, type, "Black", self.app.settings.get('censorType', 'black') == 'black');
        self.mosaic = gui3d.RadioButton(self.mouseBox, type, "Mosaic", self.app.settings.get('censorType', 'black square') == 'mosaic');
        
        human = self.app.selectedHuman

        self.breastVertices, _ = human.mesh.getVerticesAndFacesForGroups(['l-torso-nipple', 'r-torso-nipple'])
        mesh = gui3d.RectangleMesh(100, 100)
        self.breastCensorship = gui3d.Object(self.app, [0, 0, 9], mesh)
        mesh.setColor([0, 0, 0, 255])
        mesh.setPickable(0)
        
        self.genitalbreastVertices, _ = human.mesh.getVerticesAndFacesForGroups(['pelvis-genital-area'])
        mesh = gui3d.RectangleMesh(100, 100)
        self.genitalCensorship = gui3d.Object(self.app, [0, 0, 9], mesh)
        mesh.setColor([0, 0, 0, 255])
        mesh.setPickable(0)
        
        if self.app.settings.get('censor', False):
            self.updateCensor()
        else:
            self.breastCensorship.hide()
            self.genitalCensorship.hide()
            
        @self.enableCensor.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.enableCensor, event)
            self.app.settings['censor'] = self.enableCensor.selected
            if self.enableCensor.selected:
                self.updateCensor()
                self.breastCensorship.show()
                self.genitalCensorship.show()
            else:
                self.breastCensorship.hide()
                self.genitalCensorship.hide()
        
    def calcProjectedBBox(self, vertices):
    
        human = self.app.selectedHuman
        
        vmin, vmax = aljabr.calcBBox(vertices)
        
        box = [
            vmin,
            [vmax[0], vmin[1], vmin[2]],
            [vmax[0], vmax[1], vmin[2]],
            [vmin[0], vmax[1], vmin[2]],
            [vmin[0], vmin[1], vmax[2]],
            [vmax[0], vmin[1], vmax[2]],
            vmax,
            [vmin[0], vmax[1], vmax[2]]
        ]
        
        for i, v in enumerate(box):
            box[i] = mh.cameras[0].convertToScreen(v[0], v[1], v[2], human.mesh.object3d)
            
        return min([v[0] for v in box]), min([v[1] for v in box]), max([v[0] for v in box]), max([v[1] for v in box])
        
    def updateCensor(self):
    
        x1, y1, x2, y2 = self.calcProjectedBBox(self.breastVertices)
        self.breastCensorship.setPosition([x1, y1, 9])
        self.breastCensorship.mesh.resize(x2 - x1, y2 - y1)
        
        x1, y1, x2, y2 = self.calcProjectedBBox(self.genitalbreastVertices)
        self.genitalCensorship.setPosition([x1, y1, 9])
        self.genitalCensorship.mesh.resize(x2 - x1, y2 - y1)
    
    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.enableCensor.setFocus()
    
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        self.app.saveSettings()
        
    def onResized(self, event):
        
        self.updateCensor()
        
    def onHumanChanged(self, event):
    
        if self.app.settings.get('censor', False):
            mh.callAsync(lambda:self.updateCensor())
        
    def onHumanTargetsReapplied(self, event):
    
        if self.app.settings.get('censor', False):
            mh.callAsync(lambda:self.updateCensor())
            
    def onHumanTranslated(self, event):
    
        if self.app.settings.get('censor', False):
            mh.callAsync(lambda:self.updateCensor())
            
    def onHumanRotated(self, event):
    
        if self.app.settings.get('censor', False):
            mh.callAsync(lambda:self.updateCensor())

    def onCameraChanged(self, event):
    
        if self.app.settings.get('censor', False):
            mh.callAsync(lambda:self.updateCensor())

def load(app):
    category = app.getCategory('Settings')
    taskview = CensorTaskView(category)

def unload(app):
    pass

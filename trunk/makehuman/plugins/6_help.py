#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import gui3d
import webbrowser
import mh
import gui

class HelpTaskView(gui3d.TaskView):

    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Help')

        optionsBox = self.addLeftWidget(gui.GroupBox('Support options'))
        self.manualButton = optionsBox.addWidget(gui.Button("Manual"))
        self.reportBugButton = optionsBox.addWidget(gui.Button("Report bug"))
        self.requestFeatureButton = optionsBox.addWidget(gui.Button("Request feature"))
        self.donateButton = optionsBox.addWidget(gui.Button("Donate"))
        
        @self.manualButton.mhEvent
        def onClicked(event):
            webbrowser.open('http://download.tuxfamily.org/makehuman/makehuman_a_manual.pdf');
        
        @self.reportBugButton.mhEvent
        def onClicked(event):
            webbrowser.open('http://code.google.com/p/makehuman/issues/entry');
          
        @self.requestFeatureButton.mhEvent
        def onClicked(event):
            webbrowser.open('http://code.google.com/p/makehuman/issues/entry?template=Request%20feature');
            
        @self.donateButton.mhEvent
        def onClicked(event):
            webbrowser.open('https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=34KYQRLBE2K3N');
            
    def onShow(self, event):
    
        gui3d.TaskView.onShow(self, event)
        self.manualButton.setFocus()

def load(app):
    category = app.getCategory('Help')
    taskview = category.addTask(HelpTaskView(category))

def unload(app):
    pass



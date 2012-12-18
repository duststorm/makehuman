#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import webbrowser

class HelpTaskView(gui3d.TaskView):

    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Help')

        optionsBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Support options', gui3d.GroupBoxStyle._replace(height=25+24*4+6)))
        self.manualButton = optionsBox.addView(gui3d.Button("Manual"))
        self.reportBugButton = optionsBox.addView(gui3d.Button("Report bug"))
        self.requestFeatureButton = optionsBox.addView(gui3d.Button("Request feature"))
        self.donateButton = optionsBox.addView(gui3d.Button("Donate"))
        
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
    taskview = category.addView(HelpTaskView(category))
    print 'Help imported'

def unload(app):
    pass



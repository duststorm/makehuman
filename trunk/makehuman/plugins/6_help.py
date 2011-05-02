#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import webbrowser

class HelpTaskView(gui3d.TaskView):

    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Help')

        optionsBox = gui3d.GroupBox(self, [10, 80, 9.0], 'Support options', gui3d.GroupBoxStyle._replace(height=25+24*4+6))
        self.manualButton = gui3d.Button(optionsBox, "Manual")
        self.reportBugButton = gui3d.Button(optionsBox, "Report bug")
        self.requestFeatureButton = gui3d.Button(optionsBox, "Request feature")
        self.donateButton = gui3d.Button(optionsBox, "Donate")
        
        @self.manualButton.event
        def onClicked(event):
            webbrowser.open('http://download.tuxfamily.org/makehuman/makehuman_a_manual.pdf');
        
        @self.reportBugButton.event
        def onClicked(event):
            webbrowser.open('http://code.google.com/p/makehuman/issues/entry');
          
        @self.requestFeatureButton.event
        def onClicked(event):
            webbrowser.open('http://code.google.com/p/makehuman/issues/entry?template=Request%20feature');
            
        @self.donateButton.event
        def onClicked(event):
            webbrowser.open('https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=34KYQRLBE2K3N');

def load(app):
    category = app.getCategory('Help')
    taskview = HelpTaskView(category)
    print 'Help imported'

def unload(app):
    pass



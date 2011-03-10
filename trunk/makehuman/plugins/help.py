#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import webbrowser

class HelpTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Help')

        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Support options', gui3d.GroupBoxStyle._replace(height=25+24*3+6));y+=25
        self.manualButton = gui3d.Button(self, [18, y, 9.5], "Manual");y+=24
        self.reportBugButton = gui3d.Button(self, [18, y, 9.5], "Report bug");y+=24
        self.requestFeatureButton = gui3d.Button(self, [18, y, 9.5], "Request feature");y+=24
        
        @self.manualButton.event
        def onClicked(event):
            webbrowser.open('http://download.tuxfamily.org/makehuman/makehuman_a_manual.pdf');
        
        @self.reportBugButton.event
        def onClicked(event):
            webbrowser.open('http://code.google.com/p/makehuman/issues/entry');
          
        @self.requestFeatureButton.event
        def onClicked(event):
            webbrowser.open('http://code.google.com/p/makehuman/issues/entry?template=Request%20feature');

def load(app):
    category = app.getCategory('Help')
    taskview = HelpTaskView(category)
    print 'Help imported'

def unload(app):
    pass



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

import gui3d, mh, os
import files3d
import mh2proxy
import export_config

class ProxyTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Proxies')
        self.filechooser = self.addView(gui3d.FileChooser('data/proxymeshes', 'proxy', 'png', 'notfound.png'))

        @self.filechooser.event
        def onFileSelected(filename):
            
            self.setProxy(gui3d.app.selectedHuman, filename)

            gui3d.app.switchCategory('Modelling')
        
    def setProxy(self, human, proxy):

        human.setProxy(mh2proxy.readProxyFile(human.getSeedMesh(), proxy, False))

    def onShow(self, event):
        # When the task gets shown, set the focus to the file chooser
        gui3d.app.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.app.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)
        
    def onResized(self, event):
        self.filechooser.onResized(event)

    def onHumanChanging(self, event):
        
        human = event.human
        if event.change == 'reset':
            human.setProxy(None)
            
    def onHumanChanged(self, event):
        
        human = event.human

    def loadHandler(self, human, values):
        
	(fname, ext) = os.path.splitext(values[1])
        path = export_config.findExistingProxyFile("proxymeshes", None, "%s.proxy" % fname)        	
        self.setProxy(human, path)
        
    def saveHandler(self, human, file):
        
        if human.proxy:
            file.write('proxy %s\n' % human.proxy.name.lower())

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addView(ProxyTaskView(category))

    app.addLoadHandler('proxy', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


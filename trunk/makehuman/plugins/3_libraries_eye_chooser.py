"""
B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2011

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

TO DO

"""

import gui3d, mh, os, module3d

class EyesTaskView(gui3d.TaskView):
    
    def __init__(self, category):
        
        gui3d.TaskView.__init__(self, category, 'Eyes')
        self.filechooser = self.addView(gui3d.FileChooser('data/eyes', 'mhstx', 'png', 'data/eyes/notfound.png'))

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            
            self.setEyes(gui3d.app.selectedHuman, filename)

            gui3d.app.switchCategory('Modelling')
        
    def setEyes(self, human, mhstx):
        
        f = open(mhstx, 'rU')
        try:
            subTextures = eval(f.read(), {"__builtins__":None}, {'True':True, 'False':False})
        except:
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
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
        #texture.loadImage(img)

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
            pass

    def onHumanChanged(self, event):
        
        human = event.human
        pass

    def loadHandler(self, human, values):
        pass
        #self.setEyes(human, os.path.join('data/eyes', values[1].replace('.obj', ''), values[1].replace('.obj', '.mhclo')))
        
    def saveHandler(self, human, file):
        pass
        #for clo in human.clothesObjs.values():
        #    if clo:
        #        file.write('clothes %s\n' % clo.mesh.name)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Library')
    taskview = category.addView(EyesTaskView(category))

    app.addLoadHandler('eyes', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass


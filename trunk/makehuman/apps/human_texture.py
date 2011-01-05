#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2010

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

TO DO

"""

__docformat__ = 'restructuredtext'

import gui3d
import events3d
import mh


class HumanTextureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Human texture', label='Texture')
        self.filechooser = gui3d.FileChooser(self, 'data/textures', ['bmp', 'png', 'tif', 'tiff', 'jpg', 'jpeg'], None)

        @self.filechooser.event
        def onFileSelected(filename):
            print 'Loading %s' % filename
            self.app.scene3d.selectedHuman.setTexture('data/textures/' + filename)
            
            self.app.categories['Modelling'].tasksByName['Macro modelling'].backgroundImageToggle.setSelected(True)
            self.app.switchCategory('Modelling')
            self.app.scene3d.redraw(1)

    def onShow(self, event):

    # When the task gets shown, set the focus to the file chooser

        self.app.scene3d.selectedHuman.hide()
        gui3d.TaskView.onShow(self, event)
        self.filechooser.setFocus()

    # HACK: otherwise the toolbar background disappears for some weird reason

        self.app.scene3d.redraw(0)

    def onHide(self, event):
        self.app.scene3d.selectedHuman.show()
        gui3d.TaskView.onHide(self, event)



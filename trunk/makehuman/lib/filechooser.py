#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Qt filechooser widget.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

A Qt based filechooser widget.
"""

import os

from PyQt4 import QtCore, QtGui

import qtgui as gui
import mh
import log

class ThumbnailCache(object):
    aspect_mode = QtCore.Qt.KeepAspectRatioByExpanding
    scale_mode = QtCore.Qt.SmoothTransformation

    def __init__(self, size):
        self.cache = {}
        self.size = size

    def __getitem__(self, name):
        nstat = os.stat(name)
        if name in self.cache:
            stat, pixmap = self.cache[name]
            if stat.st_size == nstat.st_size and stat.st_mtime == nstat.st_mtime:
                return pixmap
            else:
                del self.cache[name]
        pixmap = self.loadImage(name)
        self.cache[name] = (nstat, pixmap)
        return pixmap

    def loadImage(self, path):
        pixmap = QtGui.QPixmap(path)
        width, height = self.size
        pixmap = pixmap.scaled(width, height, self.aspect_mode, self.scale_mode)
        pwidth = pixmap.width()
        pheight = pixmap.height()
        if pwidth > width or pheight > height:
            x0 = max(0, (pwidth - width) / 2)
            y0 = max(0, (pheight - height) / 2)
            pixmap = pixmap.copy(x0, y0, width, height)
        return pixmap

class FileChooserRectangle(gui.Button):
    _size = (128, 128)
    _imageCache = ThumbnailCache(_size)

    def __init__(self, owner, file, label, imagePath):
        super(FileChooserRectangle, self).__init__()
        gui.Widget.__init__(self)
        self.owner = owner
        self.file = file

        self.layout = QtGui.QGridLayout(self)
        self.layout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)

        image = self._imageCache[imagePath]
        self.preview = QtGui.QLabel()
        self.preview.setPixmap(image)
        self.layout.addWidget(self.preview, 0, 0)
        self.layout.setRowStretch(0, 1)
        self.layout.setColumnMinimumWidth(0, self._size[0])
        self.layout.setRowMinimumHeight(0, self._size[1])

        self.label = QtGui.QLabel()
        self.label.setText(label)
        self.label.setMinimumWidth(1)
        self.layout.addWidget(self.label, 1, 0)
        self.layout.setRowStretch(1, 0)

    def onClicked(self, event):
        self.owner.selection = self.file
        self.owner.callEvent('onFileSelected', self.file)

class FlowLayout(QtGui.QLayout):
    def __init__(self, parent = None):
        super(FlowLayout, self).__init__(parent)
        self._children = []

    def addItem(self, item):
        self._children.append(item)

    def count(self):
        return len(self._children)

    def itemAt(self, index):
        if index < 0 or index >= self.count():
            return None
        return self._children[index]

    def takeAt(self, index):
        child = self.itemAt(index)
        if child is not None:
            del self._children[index]
        return child

    def hasHeightForWidth(self):
        return True

    def _doLayout(self, width, real=False):
        x = 0
        y = 0
        rowHeight = 0
        for child in self._children:
            size = child.sizeHint()
            w = size.width()
            h = size.height()
            if x + w > width:
                x = 0
                y += rowHeight
                rowHeight = 0
            rowHeight = max(rowHeight, h)
            if real:
                child.setGeometry(QtCore.QRect(x, y, w, h))
            x += w
        return y + rowHeight

    def heightForWidth(self, width):
        return self._doLayout(width, False)

    def sizeHint(self):
        width = 0
        height = 0
        for child in self._children:
            size = child.sizeHint()
            w = size.width()
            h = size.height()
            width += w
            height = max(height, h)
        return QtCore.QSize(width, height)

    def setGeometry(self, rect):
        self._doLayout(rect.width(), True)

    def expandingDirections(self):
        return QtCore.Qt.Vertical

    def minimumSize(self):
        if not self._children:
            return QtCore.QSize(0, 0)
        return self._children[0].sizeHint()

class FileSort(object):
    """
    The default file sorting class. Can sort files on name, creation and modification date and size.
    """
    def __init__(self):
        pass
        
    def fields(self):
        """
        Returns the names of the fields on which this FileSort can sort. For each field it is assumed that the method called sortField exists.
        
        :return: The names of the fields on which this FileSort can sort.
        :rtype: list or tuple
        """
        return ("name", "created", "modified", "size")

    def sort(self, by, filenames):
        method = getattr(self, "sort%s" % by.capitalize())
        return method(filenames)
        
    def sortName(self, filenames):
        return sorted(filenames)
    def sortModified(self, filenames):
        decorated = [(os.path.getmtime(filename), i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for modified, i, filename in decorated]
        
    def sortCreated(self, filenames):
        decorated = [(os.path.getctime(filename), i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for created, i, filename in decorated]
    
    def sortSize(self, filenames):
        decorated = [(os.path.getsize(filename), i, filename) for i, filename in enumerate(filenames)]
        decorated.sort()
        return [filename for size, i, filename in decorated]

class FileSortRadioButton(gui.RadioButton):
    def __init__(self, chooser, group, selected, field):
        gui.RadioButton.__init__(self, group, "By %s" % field, selected)
        self.field = field
        self.chooser = chooser
        
    def onClicked(self, event):
        self.chooser.sortBy = self.field
        self.chooser.refresh()

class FileChooser(QtGui.QWidget, gui.Widget):
    """
    A FileChooser widget. This widget can be used to let the user choose an existing file.
    
    :param path: The path from which the recursive search is started.
    :type path: str
    :param extension: The extension(s) of the files to display.
    :type extension: str or list
    :param previewExtension: The extension of the preview for the files. None if the file itself is to be used.
    :type previewExtension: str or None
    :param notFoundImage: The full filepath of the image to be used in case the preview is not found.
    :type notFoundImage: str or None
    :param sort: A file sorting instance which will be used to provide sorting of the found files.
    :type sort: FileSort
    """
    
    def __init__(self, path, extension, previewExtensions='bmp', notFoundImage=None, sort=FileSort()):
        super(FileChooser, self).__init__()
        gui.Widget.__init__(self)

        self.paths = None
        self.extension = extension
        self.setPreviewExtensions(previewExtensions)

        self.sort = sort
        self.selection = ''
        self.childY = {}
        self.notFoundImage = notFoundImage
        self.sortBy = self.sort.fields()[0]
        self.sortgroup = []

        self.layout = QtGui.QGridLayout(self)

        self.sortBox = gui.GroupBox('Sort')
        self.layout.addWidget(self.sortBox, 0, 0)
        self.layout.setRowStretch(0, 0)
        self.layout.setColumnStretch(0, 0)

        self.layout.addWidget(QtGui.QWidget(), 1, 0)

        self.files_sc = QtGui.QScrollArea()
        self.files_sc.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.files_sc.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.layout.addWidget(self.files_sc, 0, 1, 2, -1)
        self.layout.setRowStretch(1, 1)
        self.layout.setColumnStretch(1, 1)

        self.files = QtGui.QWidget()
        self.files_sc.installEventFilter(self)
        self.files_sc.setWidget(self.files)
        self.files_sc.setWidgetResizable(True)
        self.children = FlowLayout(self.files)
        self.children.setSizeConstraint(QtGui.QLayout.SetMinimumSize)

        self.location = gui.TextView('')
        self.layout.addWidget(self.location, 2, 0, 1, -1)
        self.layout.setRowStretch(2, 0)

        self.refreshButton = self.sortBox.addWidget(gui.Button('Refresh'))
        for i, field in enumerate(self.sort.fields()):
            self.sortBox.addWidget(FileSortRadioButton(self, self.sortgroup, i == 0, field))

        self.setPaths(path)

        @self.refreshButton.mhEvent
        def onClicked(value):
            self.refresh()

    def setPaths(self, value):
        self.paths = value if isinstance(value, list) else [value]
        locationLbl = "  |  ".join(self.paths)
        self.location.setText(os.path.abspath(locationLbl))

    def setPreviewExtensions(self, value):
        if not value:
            self.previewExtensions = None
        elif isinstance(value, list):
            self.previewExtensions = value
        else:
            self.previewExtensions = [value]

    def _updateScrollBar(self):
        pass

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Resize:
            mh.callAsync(self._updateScrollBar)
        return False
        
    def getPreview(self, filename):
        preview = filename
        
        if self.previewExtensions:
            log.debug('%s, %s', self.extension, self.previewExtensions)
            preview = filename.replace('.' + self.extension, '.' + self.previewExtensions[0])
            i = 1
            while not os.path.exists(preview) and i < len(self.previewExtensions):
                preview = filename.replace('.' + self.extension, '.' + self.previewExtensions[i])
                i = i + 1
        else:
            preview = filename
            
        if not os.path.exists(preview) and self.notFoundImage:
            # preview = os.path.join(self.path, self.notFoundImage)
            # TL: full filepath needed, so we don't look into user dir.
            preview = self.notFoundImage

        return preview

    def search(self):
        if isinstance(self.extension, str):
            extensions = [self.extension]
        else:
            extensions = self.extension

        for path in self.paths:
            for root, dirs, files in os.walk(path):
                for f in files:
                    ext = os.path.splitext(f)[1][1:].lower()
                    if ext in self.extension:
                        if f.lower().endswith('.' + ext):
                            yield os.path.join(root, f)

    def refresh(self):
        for i in xrange(self.children.count()):
            child = self.children.itemAt(0)
            self.children.removeItem(child)
            child.widget().hide()
            child.widget().destroy()

        # Create icons
        for file in self.sort.sort(self.sortBy, list(self.search())):
            label = os.path.basename(file)
            if isinstance(self.extension, str):
                label = os.path.splitext(label)[0]
            self.children.addWidget(FileChooserRectangle(self, file, label, self.getPreview(file)))

        mh.redraw()

    def onShow(self, event):
        self.refresh()

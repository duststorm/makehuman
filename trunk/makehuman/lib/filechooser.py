
import os

from PyQt4 import QtCore, QtGui

import gui3d
from qtgui import *
import qtui

class FileChooserRectangle(Button):
    _imageCache = {}

    @classmethod
    def _getImage(cls, path):
        if path not in cls._imageCache:
            cls._imageCache[path] = QtGui.QImage(path)
        return cls._imageCache[path]

    def __init__(self, owner, file, label, imagePath, size = (128, 128)):
        super(FileChooserRectangle, self).__init__()
        Widget.__init__(self)
        self.owner = owner
        self.file = file

        self.setMinimumSize(*size)
        self.layout = QtGui.QGridLayout(self)

        image = self._getImage(imagePath)
        self.preview = QtGui.QLabel()
        self.preview.setPixmap(QtGui.QPixmap.fromImage(image))
        self.layout.addWidget(self.preview, 0, 0)
        self.layout.setRowStretch(0, 1)

        self.label = QtGui.QLabel()
        self.label.setText(label)
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

class FileSortRadioButton(RadioButton):
    def __init__(self, group, selected, field):
        RadioButton.__init__(self, group, "By %s" % field, selected)
        self.field = field
        
    def onClicked(self, event):
        parent = self.parentWidget().parentWidget()
        parent.sortBy = self.field
        parent.refresh()

class FileChooser(QtGui.QWidget, Widget):
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
    
    def __init__(self, path, extension, previewExtension='bmp', notFoundImage=None, sort=FileSort()):
        super(FileChooser, self).__init__()
        Widget.__init__(self)

        self.path = path if isinstance(path, basestring) else path[0]
        self.paths = path if isinstance(path, list) else [path]
        self.extension = extension
        self.previewExtension = previewExtension

        self.sort = sort
        self.selection = ''
        self.childY = {}
        self.notFoundImage = notFoundImage
        self.sortBy = self.sort.fields()[0]
        self.sortgroup = []

        self.layout = QtGui.QGridLayout(self)

        self.sortBox = GroupBox('Sort')
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

        self.location = TextView(os.path.abspath(self.path))
        self.layout.addWidget(self.location, 2, 0, 1, -1)
        self.layout.setRowStretch(2, 0)

        self.refreshButton = self.sortBox.addWidget(Button('Refresh'))
        for i, field in enumerate(self.sort.fields()):
            self.sortBox.addWidget(FileSortRadioButton(self.sortgroup, i == 0, field))
        
        @self.refreshButton.mhEvent
        def onClicked(value):
            self.refresh()

    def _updateScrollBar(self):
        pass

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Resize:
            qtui.callAsync(self._updateScrollBar)
        return False
        
    def getPreview(self, filename):
        preview = filename
        
        if self.previewExtension:
            preview = filename.replace('.' + self.extension, '.' + self.previewExtension)
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

        gui3d.app.redraw()

    def onShow(self, event):
        self.refresh()

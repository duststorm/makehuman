#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from PyQt4 import QtCore, QtGui

from core import G
import events3d
import language

def getLanguageString(text):
    if not text:
        return text
    return language.language.getLanguageString(text)

class Tab(events3d.EventHandler):
    def __init__(self, parent, name, label):
        super(Tab, self).__init__()
        self.parent = parent
        self.name = name
        self.label = label

    def setSelected(self, state):
        pass

class Widget(events3d.EventHandler):
    def __init__(self):
        events3d.EventHandler.__init__(self)

    def callEvent(self, eventType, event):
        super(Widget, self).callEvent(eventType, event)
        if G.app and G.app.mainwin and G.app.mainwin.canvas:
            G.app.mainwin.canvas.update()

    def showEvent(self, event):
        self.callEvent('onShow', self)

    def hideEvent(self, event):
        self.callEvent('onHide', self)

class TabsBase(Widget):
    def __init__(self):
        super(TabsBase, self).__init__()
        self.tabBar().setExpanding(False)
        self.connect(self, QtCore.SIGNAL('currentChanged(int)'), self.tabChanged)
        self._tabs_by_idx = {}
        self._tabs_by_name = {}

    def _addTab(self, name, label):
        label = getLanguageString(label)
        tab = Tab(self, name, label)
        tab.idx = self._makeTab(tab)
        self._tabs_by_idx[tab.idx] = tab
        self._tabs_by_name[tab.name] = tab
        return tab

    def tabChanged(self, idx):
        tab = self._tabs_by_idx.get(idx)
        if tab:
            self.callEvent('onTabSelected', tab)
            tab.callEvent('onClicked', tab)

    def findTab(self, name):
        return self._tabs_by_name.get(name)

    def changeTab(self, name):
        self.setCurrentIndex(self.findTab(name).idx)

class Tabs(QtGui.QTabWidget, TabsBase):
    def __init__(self, parent = None):
        QtGui.QTabWidget.__init__(self, parent)
        TabsBase.__init__(self)

    def _makeTab(self, tab):
        tab.child = TabBar(self)
        return super(Tabs, self).addTab(tab.child, tab.label)

    def addTab(self, name, label):
        return super(Tabs, self)._addTab(name, label)

    def tabChanged(self, idx):
        super(Tabs, self).tabChanged(idx)
        tab = self._tabs_by_idx.get(idx)
        if tab:
            tab.child.tabChanged(tab.child.currentIndex())

class TabBar(QtGui.QTabBar, TabsBase):
    def __init__(self, parent = None):
        QtGui.QTabBar.__init__(self, parent)
        TabsBase.__init__(self)

    def tabBar(self):
        return self

    def _makeTab(self, tab):
        return super(TabBar, self).addTab(tab.label)

    def addTab(self, name, label):
        return super(TabBar, self)._addTab(name, label)

class GroupBox(QtGui.QGroupBox, Widget):
    def __init__(self, label = ''):
        label = getLanguageString(label) if label else ''
        QtGui.QGroupBox.__init__(self, label)
        Widget.__init__(self)
        self.layout = QtGui.QGridLayout(self)

    def __str__(self):
        return "%s - %s" % (type(self), unicode(self.title()))

    def addWidget(self, widget, row = None, column = 0, rowSpan = 1, columnSpan = 1, alignment = QtCore.Qt.Alignment(0)):
        # widget.setParent(self)
        if row is None:
            row = self.layout.count()
        self.layout.addWidget(widget, row, column, rowSpan, columnSpan, alignment)
        widget.show()
        return widget

    def removeWidget(self, widget):
        self.layout.removeWidget(widget)
        # widget.setParent(None)

    @property
    def children(self):
        return list(self.layout.itemAt(i).widget() for i in xrange(self.layout.count()))

class Slider(QtGui.QWidget, Widget):
    _imageCache = {}
    _show_images = False
    _instances = set()

    @classmethod
    def _getImage(cls, path):
        if path not in cls._imageCache:
            cls._imageCache[path] = QtGui.QPixmap(path)
        return cls._imageCache[path]

    def __init__(self, value=0.0, min=0.0, max=1.0, label=None, vertical=False, valueConverter=None, image=None):
        super(Slider, self).__init__()
        Widget.__init__(self)
        self.text = getLanguageString(label) or ''

        orient = (QtCore.Qt.Vertical if vertical else QtCore.Qt.Horizontal)
        self.slider = QtGui.QSlider(orient)
        self.min = min
        self.max = max
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)
        self.slider.setValue(self._f2i(value))
        self.slider.setTracking(False)
        self.hold_events = False
        self.connect(self.slider, QtCore.SIGNAL('sliderMoved(int)'), self._changing)
        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self._changed)

        label = (self.text % value) if '%' in self.text else self.text
        self.label = QtGui.QLabel(label)
        self.layout = QtGui.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label, 1, 0)
        self.layout.setColumnStretch(0, 0)
        self.layout.addWidget(self.slider, 1, 1)
        self.layout.setColumnStretch(1, 1)

        if image is not None:
            self.image = QtGui.QLabel()
            self.image.setPixmap(self._getImage(image))
            self.layout.addWidget(self.image, 0, 1)
        else:
            self.image = None

        self._update_image()

        type(self)._instances.add(self)

    def __del__(self):
        type(self)._instances.remove(self)

    def _update_image(self):
        if self.image is None:
            return
        if type(self)._show_images:
            self.image.show()
        else:
            self.image.hide()

    @classmethod
    def imagesShown(cls):
        return cls._show_images

    @classmethod
    def showImages(cls, state):
        cls._show_images = state
        for w in cls._instances:
            w._update_image()

    def _changing(self, value):
        if self.hold_events:
            return
        value = self._i2f(value)
        if '%' in self.text:
            self.label.setText(self.text % value)
        self.callEvent('onChanging', value)

    def _changed(self, value):
        if self.hold_events:
            return
        value = self._i2f(value)
        if '%' in self.text:
            self.label.setText(self.text % value)
        self.callEvent('onChange', value)

    def _f2i(self, x):
        return int(round(1000 * (x - self.min) / (self.max - self.min)))

    def _i2f(self, x):
        return self.min + (x / 1000.0) * (self.max - self.min)

    def setValue(self, value):
        self.hold_events = True
        self.slider.setValue(self._f2i(value))
        self.hold_events = False

    def getValue(self):
        return self._i2f(self.slider.value())
        
    def setMin(self, min):
        value = self.getValue()
        self.min = min
        self.setValue(value)
        
    def setMax(self, max):
        value = self.getValue()
        self.max = max
        self.setValue(value)

class ButtonBase(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.connect(self, QtCore.SIGNAL('clicked(bool)'), self._clicked)

    def getLabel(self):
        return unicode(self.text())

    def setLabel(self, label):
        label = getLanguageString(label)
        self.setText(label)

    def _clicked(self, state):
        self.callEvent('onClicked', None)

    @property
    def selected(self):
        return self.isChecked()

    def setSelected(self, value):
        self.setChecked(value)

class Button(QtGui.QPushButton, ButtonBase):
    def __init__(self, label=None, selected=False):
        label = getLanguageString(label)
        super(Button, self).__init__(label)
        ButtonBase.__init__(self)

class CheckBox(QtGui.QCheckBox, ButtonBase):
    def __init__(self, label=None, selected=False):
        label = getLanguageString(label)
        super(CheckBox, self).__init__(label)
        ButtonBase.__init__(self)
        self.setChecked(selected)

ToggleButton = CheckBox

class RadioButton(QtGui.QRadioButton, ButtonBase):
    groups = {}

    def __init__(self, group, label=None, selected=False):
        label = getLanguageString(label)
        super(RadioButton, self).__init__(label)
        ButtonBase.__init__(self)
        self.group = group
        self.group.append(self)
        self.setChecked(selected)
        self._addToGroup(group)

    def __del__(self):
        self._removeFromGroup(self.group)

    def _addToGroup(self, group):
        if id(group) in type(self).groups:
            rbgroup = type(self).groups[id(group)]
        else:
            rbgroup = QtGui.QButtonGroup()
            rbgroup.setExclusive(True)
            type(self).groups[id(group)] = rbgroup
        rbgroup.addButton(self)

    def _removeFromGroup(self, group):
        if id(group) not in type(self).groups:
            return
        rbgroup = type(self).groups[id(group)]
        rbgroup.removeButton(self)
        if len(rbgroup.buttons()) == 0:
            del type(self).groups[id(group)]

    @property
    def selected(self):
        return self.isChecked()

    def getSelection(self):
        for radio in self.group:
            if radio.selected:
                return radio

class TextView(QtGui.QLabel, Widget):
    def __init__(self, label = ''):
        label = getLanguageString(label)
        super(TextView, self).__init__(label)
        Widget.__init__(self)

    def setText(self, text):
        text = getLanguageString(text) if text else ''
        super(TextView,self).setText(text)
        
    def setTextFormat(self, text, *values):
        text = getLanguageString(text) if text else ''
        super(TextView,self).setText(text % values)

class SliderBox(GroupBox):
    def __init__(self, label = ''):
        super(SliderBox, self).__init__(label)
        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 1)
        self.row = 0

    def addWidget(self, widget, row = None, column = 0, rowSpan = 1, columnSpan = -1, alignment = QtCore.Qt.Alignment(0)):
        if row is None:
            row = self.row
        else:
            self.row = row
        self.row += 1

        if not isinstance(widget, Slider):
            return super(SliderBox, self).addWidget(widget, row, column, rowSpan, columnSpan, alignment)

        label = widget.label
        widget.layout.removeWidget(label)
        super(SliderBox, self).addWidget(label, row, 0, 1, 1)
        super(SliderBox, self).addWidget(widget, row, 1, 1, -1)

        return widget

def intValidator(text):
    return not text or text.isdigit() or (text[0] == '-' and (len(text) == 1 or text[1:].isdigit()))
    
def floatValidator(text):
    return not text or (text.replace('.', '').isdigit() and text.count('.') <= 1) or (text[0] == '-' and (len(text) == 1 or text[1:].replace('.', '').isdigit()) and text.count('.') <= 1) # Negative sign and optionally digits with optionally 1 decimal point

def filenameValidator(text):
    return not text or len(set(text) & set('\\/:*?"<>|')) == 0

class TextEdit(QtGui.QLineEdit, Widget):
    def __init__(self, text='', validator = None):
        super(TextEdit, self).__init__(text)
        Widget.__init__(self)
        self.setValidator(validator)
        self.connect(self, QtCore.SIGNAL('textEdited(QString)'), self._textChanged)

    @property
    def text(self):
        return self.getText()

    def _textChanged(self, string):
        self.callEvent('onChange', string)

    def setText(self, text):
        self.setText(text)
        self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

    def getText(self):
        return super(TextEdit, self).text()

    def validateText(self, text):
        if self.__validator:
            return self.__validator(text)
        else:
            return True

    def setValidator(self, validator):
        self.__validator = validator
        if validator == intValidator:
            qvalidator = QtGui.QIntValidator()
        elif validator == floatValidator:
            qvalidator = QtGui.QDoubleValidator()
        elif validator == filenameValidator:
            qvalidator = QtGui.QRegExpValidator(QRegExp(r'[^\/:*?"<>|]*'))
        else:
            qvalidator = None
        super(TextEdit, self).setValidator(qvalidator)

class ProgressBar(QtGui.QProgressBar, Widget):
    def __init__(self, visible=True):
        super(ProgressBar, self).__init__()
        Widget.__init__(self)
        self.setVisible(visible)

    def setProgress(self, progress, redraw=True):
        min = self.minimum()
        max = self.maximum()
        self.setValue(min + progress * (max - min))

class ShortcutEdit(QtGui.QLabel, Widget):
    def __init__(self, shortcut):
        modifiers, key = shortcut
        text = self.shortcutToLabel(modifiers, key)
        super(ShortcutEdit, self).__init__(text)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def setShortcut(self, shortcut):
        modifiers, key = shortcut
        self.setText(self.shortcutToLabel(modifiers, key))

    def keyPressEvent(self, event):
        key = event.key()
        mod = int(event.modifiers()) & ~QtCore.Qt.ShiftModifier
        if key in (QtCore.Qt.Key_Shift, QtCore.Qt.Key_Control, QtCore.Qt.Key_Alt, QtCore.Qt.Key_Meta):
            return
        self.setText(self.shortcutToLabel(mod, key))
        self.callEvent('onChanged', (mod, key))

    def shortcutToLabel(self, mod, key):
        seq = QtGui.QKeySequence(key + mod)
        return seq.toString()

    def onChanged(self, shortcut):
        pass

class MouseActionEdit(QtGui.QLabel, Widget):
    def __init__(self, shortcut):
        modifiers, button = shortcut
        text = self.shortcutToLabel(modifiers, button)
        super(MouseActionEdit, self).__init__(text)

    def setShortcut(self, shortcut):
        modifiers, button = shortcut
        self.setText(self.shortcutToLabel(modifiers, button))

    def mousePressEvent(self, event):
        button = event.button()
        modifiers = int(event.modifiers())
        self.setText(self.shortcutToLabel(modifiers, button))
        self.callEvent('onChanged', (modifiers, button))

    def shortcutToLabel(self, modifiers, button):
        labels = []
        
        if modifiers & QtCore.Qt.ControlModifier:
            labels.append('Ctrl')
        if modifiers & QtCore.Qt.AltModifier:
            labels.append('Alt')
        if modifiers & QtCore.Qt.MetaModifier:
            labels.append('Meta')
        if modifiers & QtCore.Qt.ShiftModifier:
            labels.append('Shift')
            
        if button & QtCore.Qt.LeftButton:
            labels.append('Left')
        elif button & QtCore.Qt.MidButton:
            labels.append('Middle')
        elif button & QtCore.Qt.RightButton:
            labels.append('Right')
        else:
            labels.append('[Unknown]')
            
        return '+'.join(labels)
        
    def onChanged(self, shortcut):
        pass

class StackedBox(QtGui.QStackedWidget, Widget):
    def __init__(self):
        super(StackedBox, self).__init__()
        Widget.__init__(self)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

    def addWidget(self, widget):
        w = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(w)
        layout.addWidget(widget)
        layout.addStretch()
        super(StackedBox, self).addWidget(w)
        return widget

    def showWidget(self, widget):
        self.setCurrentWidget(widget.parentWidget())

class Dialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(Dialog, self).__init__(parent)
        self.setModal(True)

        self.helpIds = set()

        icon = self.style().standardIcon(QtGui.QStyle.SP_MessageBoxWarning)

        self.layout = QtGui.QGridLayout(self)
        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 0)
        self.layout.setColumnStretch(3, 0)

        self.icon = QtGui.QLabel()
        self.icon.setPixmap(icon.pixmap(64))
        self.layout.addWidget(self.icon, 0, 0, 2, 1)

        self.text = QtGui.QLabel()
        self.layout.addWidget(self.text, 0, 1, 1, -1)

        self.check = QtGui.QCheckBox("Don't show this again")
        self.layout.addWidget(self.check, 1, 1, 1, -1)

        self.button1 = QtGui.QPushButton()
        self.layout.addWidget(self.button1, 2, 2)

        self.button2 = QtGui.QPushButton()
        self.layout.addWidget(self.button2, 2, 3)

        self.connect(self.button1, QtCore.SIGNAL('clicked(bool)'), self.accept)
        self.connect(self.button2, QtCore.SIGNAL('clicked(bool)'), self.reject)

    def prompt(self, title, text, button1Label, button2Label=None, button1Action=None, button2Action=None, helpId=None):
        if helpId in self.helpIds:
            return

        button1Label = getLanguageString(button1Label)
        button2Label = getLanguageString(button2Label)

        self.setWindowTitle(title)
        self.text.setText(text)
        self.button1.setText(button1Label)

        if button2Label is not None:
            self.button2.setText(button2Label)
            self.button2.show()
        else:
            self.button2.hide()

        if helpId:
            self.check.show()
            self.check.setChecked(False)
        else:
            self.check.hide()

        which = self.exec_()

        if which == QtGui.QDialog.Accepted and button1Action:
            button1Action()
        elif which == QtGui.QDialog.Rejected and button2Action:
            button2Action()

        if helpId and self.check.isChecked():
            self.helpIds.add(helpId)

class FileEntryView(QtGui.QWidget, Widget):
    def __init__(self, buttonLabel):
        super(FileEntryView, self).__init__()
        Widget.__init__(self)

        buttonLabel = getLanguageString(buttonLabel)

        self.directory = os.getcwd()
        self.filter = ''

        self.layout = QtGui.QGridLayout(self)

        self.browse = QtGui.QPushButton("...")
        self.layout.addWidget(self.browse, 0, 0)
        self.layout.setColumnStretch(0, 0)

        self.edit = QtGui.QLineEdit()
        self.edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[^\/:*?"<>|]*')))
        self.layout.addWidget(self.edit, 0, 1)
        self.layout.setColumnStretch(1, 1)

        self.confirm = QtGui.QPushButton(buttonLabel)
        self.layout.addWidget(self.confirm, 0, 2)
        self.layout.setColumnStretch(2, 0)

        self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)

        self.connect(self.browse, QtCore.SIGNAL('clicked(bool)'), self._browse)
        self.connect(self.confirm, QtCore.SIGNAL('clicked(bool)'), self._confirm)
        self.connect(self.edit, QtCore.SIGNAL(' returnPressed()'), self._confirm)

    def setDirectory(self, directory):
        self.directory = directory

    def setFilter(self, filter):
        self.filter = filter
        if '(*.*)' not in self.filter:
            self.filter = ';;'.join([self.filter, 'All Files (*.*)'])

    def _browse(self, state = None):
        path = QtGui.QFileDialog.getSaveFileName(G.app.mainwin, "Save File", self.directory, self.filter)
        self.edit.setText(path)

    def _confirm(self, state = None):
        if len(self.edit.text()):
            self.callEvent('onFileSelected', unicode(self.edit.text()))
                
    def onFocus(self, event):
        self.edit.setFocus()

class SplashScreen(QtGui.QSplashScreen):
    def __init__(self, image):
        super(SplashScreen, self).__init__(G.app.mainwin, QtGui.QPixmap(image))
        self._text = ''
        self._format = '%s'
        self._stdout = sys.stdout

    def setFormat(self, fmt):
        self._format = fmt

    def write(self, text):
        if self._stdout:
            self._stdout.write(text)
        self._text += text
        while '\n' in self._text:
            line, self._text = self._text.split('\n', 1)
            line = line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            line = self._format % line
            self.showMessage(line, alignment = QtCore.Qt.AlignHCenter)
            G.app.processEvents()

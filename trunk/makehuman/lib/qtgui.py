#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import sys
import os

from PyQt4 import QtCore, QtGui

from core import G
import events3d
import language
import log

def getLanguageString(text):
    if not text:
        return text
    return language.language.getLanguageString(text)

class Widget(events3d.EventHandler):
    def __init__(self):
        events3d.EventHandler.__init__(self)

    def callEvent(self, eventType, event):
        super(Widget, self).callEvent(eventType, event)

    def focusInEvent(self, event):
        self.callEvent('onFocus', self)
        super(type(self), self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.callEvent('onBlur', self)
        super(type(self), self).focusOutEvent(event)

    def showEvent(self, event):
        self.callEvent('onShow', self)
        super(type(self), self).showEvent(event)

    def hideEvent(self, event):
        self.callEvent('onHide', self)
        super(type(self), self).hideEvent(event)

    def onFocus(self, event):
        pass

    def onBlur(self, event):
        pass

    def onShow(self, event):
        pass

    def onHide(self, event):
        pass

class Tab(Widget):
    def __init__(self, parent, name, label):
        super(Tab, self).__init__()
        self.parent = parent
        self.name = name
        self.label = label

    def onClicked(self, event):
        pass

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
        tab = self.findTab(name)
        if tab is None:
            return
        self.setCurrentIndex(tab.idx)

    def onTabSelected(self, event):
        pass

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
        self.setDrawBase(False)

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

# PyQt doesn't implement QProxyStyle so we have to do all this ...

class SliderStyle(QtGui.QCommonStyle):
    def __init__(self, parent):
        self.__parent = parent
        super(SliderStyle, self).__init__()

    def drawComplexControl(self, control, option, painter, widget = None):
        return self.__parent.drawComplexControl(control, option, painter, widget)

    def drawControl(self, element, option, painter, widget = None):
        return self.__parent.drawControl(element, option, painter, widget)

    def drawItemPixmap(self, painter, rectangle, alignment, pixmap):
        return self.__parent.drawItemPixmap(painter, rectangle, alignment, pixmap)

    def drawItemText(self, painter, rectangle, alignment, palette, enabled, text, textRole = QtGui.QPalette.NoRole):
        return self.__parent.drawItemText(painter, rectangle, alignment, palette, enabled, text, textRole)

    def drawPrimitive(self, element, option, painter, widget = None):
        return self.__parent.drawPrimitive(element, option, painter, widget)

    def generatedIconPixmap(self, iconMode, pixmap, option):
        return self.__parent.generatedIconPixmap(iconMode, pixmap, option)

    def hitTestComplexControl(self, control, option, position, widget = None):
        return self.__parent.hitTestComplexControl(control, option, position, widget)

    def itemPixmapRect(self, rectangle, alignment, pixmap):
        return self.__parent.itemPixmapRect(rectangle, alignment, pixmap)

    def itemTextRect(self, metrics, rectangle, alignment, enabled, text):
        return self.__parent.itemTextRect(metrics, rectangle, alignment, enabled, text)

    def pixelMetric(self, metric, option = None, widget = None):
        return self.__parent.pixelMetric(metric, option, widget)

    def polish(self, *args, **kwargs):
        return self.__parent.polish(*args, **kwargs)

    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QtGui.QStyle.SH_Slider_AbsoluteSetButtons:
            return QtCore.Qt.LeftButton | QtCore.Qt.MidButton | QtCore.Qt.RightButton
        return self.__parent.styleHint(hint, option, widget, returnData)

    def subControlRect(self, control, option, subControl, widget = None):
        return self.__parent.subControlRect(control, option, subControl, widget)

    def subElementRect(self, element, option, widget = None):
        return self.__parent.subElementRect(element, option, widget)

    def unpolish(self, *args, **kwargs):
        return self.__parent.unpolish(*args, **kwargs)

    def sizeFromContents(self, ct, opt, contentsSize, widget = None):
        return self.__parent.sizeFromContents(ct, opt, contentsSize, widget)

class Slider(QtGui.QWidget, Widget):
    _imageCache = {}
    _show_images = False
    _instances = set()
    _style = None

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
        if Slider._style is None:
            Slider._style = SliderStyle(self.slider.style())
        self.slider.setStyle(Slider._style)

        self.min = min
        self.max = max
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)
        self.slider.setValue(self._f2i(value))
        self.slider.setTracking(False)
        self.connect(self.slider, QtCore.SIGNAL('sliderMoved(int)'), self._changing)
        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self._changed)
        self.slider.installEventFilter(self)

        label = (self.text % value) if '%' in self.text else self.text
        self.label = QtGui.QLabel(label)
        # Decrease vertical gap between label and slider
        #self.label.setContentsMargins(0, 0, 0, -1)
        self.layout = QtGui.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label, 1, 0)
        self.layout.addWidget(self.slider, 2, 0)
        if not self.text:
            self.label.hide()

        if image is not None:
            self.image = QtGui.QLabel()
            self.image.setPixmap(self._getImage(image))
            self.layout.addWidget(self.image, 0, 0)
        else:
            self.image = None

        self._update_image()

        type(self)._instances.add(self)

    def __del__(self):
        type(self)._instances.remove(self)

    def eventFilter(self, object, event):
        if object != self.slider:
            return
        if event.type() == QtCore.QEvent.FocusIn:
            self.callEvent('onFocus', self)
        elif event.type() == QtCore.QEvent.FocusOut:
            self.callEvent('onBlur', self)
        return False

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
        value = self._i2f(value)
        if '%' in self.text:
            self.label.setText(self.text % value)
        self.callEvent('onChanging', value)

    def _changed(self, value):
        value = self._i2f(value)
        if '%' in self.text:
            self.label.setText(self.text % value)
        self.callEvent('onChange', value)

    def _f2i(self, x):
        return int(round(1000 * (x - self.min) / (self.max - self.min)))

    def _i2f(self, x):
        return self.min + (x / 1000.0) * (self.max - self.min)

    def setValue(self, value):
        if self._f2i(value) == self.slider.value():
            return
        self.slider.blockSignals(True)
        self.slider.setValue(self._f2i(value))
        self.slider.blockSignals(False)

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

    def onChanging(self, event):
        pass

    def onChange(self, event):
        pass

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

    def onClicked(self, event):
        pass

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

class ListView(QtGui.QListWidget, Widget):
    def __init__(self):
        super(ListView, self).__init__()
        Widget.__init__(self)

    def setData(self, items):
        self.clear()
        self.addItems(items)

    _brushes = {}
    @classmethod
    def getBrush(cls, color):
        if color not in cls._brushes:
            cls._brushes[color] = QtGui.QBrush(QtGui.QColor(color))
        return cls._brushes[color]

    def addItem(self, text, color = None, data = None):
        item = QtGui.QListWidgetItem(self)
        item.setText(text)
        if color is not None:
            item.setForeground(self.getBrush(color))
        if data is not None:
            item.setData(QtCore.Qt.UserRole, data)
        super(ListView, self).addItem(item)

    def getSelectedItem(self):
        items = self.selectedItems()
        if len(items) > 0:
            return str(items[0].text())
        return None

    def getItemData(self, row):
        return self.item(row).data(QtCore.Qt.UserRole).toPyObject()

    def showItem(self, row, state):
        self.item(row).setHidden(not state)

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
    pass

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
        self.connect(self, QtCore.SIGNAL('returnPressed()'), self._enter)
        key_up = QtGui.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Up), self,
            context = QtCore.Qt.WidgetShortcut)
        key_down = QtGui.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Down), self,
            context = QtCore.Qt.WidgetShortcut)
        self.connect(key_up, QtCore.SIGNAL("activated()"), self._key_up)
        self.connect(key_down, QtCore.SIGNAL("activated()"), self._key_down)

    @property
    def text(self):
        return self.getText()

    def _textChanged(self, string):
        self.callEvent('onChange', string)

    def _enter(self):
        self.callEvent('onActivate', self.getText())

    def setText(self, text):
        super(TextEdit, self).setText(text)
        self.setCursorPosition(len(text))

    def getText(self):
        return unicode(super(TextEdit, self).text())

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

    def onChange(self, event):
        pass

    def _key_up(self):
        self.callEvent('onUpArrow', None)

    def _key_down(self):
        self.callEvent('onDownArrow', None)

class DocumentEdit(QtGui.QTextEdit, Widget):
    NoWrap		= QtGui.QTextEdit.NoWrap
    WidgetWidth		= QtGui.QTextEdit.WidgetWidth
    FixedPixelWidth	= QtGui.QTextEdit.FixedPixelWidth
    FixedColumnWidth	= QtGui.QTextEdit.FixedColumnWidth

    def __init__(self, text=''):
        super(DocumentEdit, self).__init__(text)
        Widget.__init__(self)
        self.setAcceptRichText(False)

    @property
    def text(self):
        return self.getText()

    def setText(self, text):
        self.setPlainText(text)

    def addText(self, text):
        self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        self.insertPlainText(text)

    def getText(self):
        return unicode(super(DocumentEdit, self).toPlainText())

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
        if shortcut is not None:
            modifiers, key = shortcut
            text = self.shortcutToLabel(modifiers, key)
        else:
            text = ''
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
        event.accept()

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

        self.check = QtGui.QCheckBox(getLanguageString("Don't show this again"))
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
        text = getLanguageString(text)
        title = getLanguageString(title)

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
        self.filter = getLanguageString(filter)
        if '(*.*)' not in self.filter:
            self.filter = ';;'.join([self.filter, getLanguageString('All Files')+' (*.*)'])

    def _browse(self, state = None):
        path = QtGui.QFileDialog.getSaveFileName(G.app.mainwin, getLanguageString("Save File"), self.directory, self.filter)
        self.edit.setText(path)

    def _confirm(self, state = None):
        if len(self.edit.text()):
            self.callEvent('onFileSelected', unicode(self.edit.text()))
                
    def onFocus(self, event):
        self.edit.setFocus()

    def onFileSelected(self, shortcut):
        pass

class SplashScreen(QtGui.QSplashScreen):
    def __init__(self, image):
        super(SplashScreen, self).__init__(G.app.mainwin, QtGui.QPixmap(image))
        self._text = ''
        self._format = '%s'
        self._stdout = sys.stdout

    def setFormat(self, fmt):
        self._format = fmt

    def escape(self, text):
        return text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

    def logMessage(self, text):
        text = self._format % self.escape(text)
        self.showMessage(text, alignment = QtCore.Qt.AlignHCenter)

class StatusBar(QtGui.QStatusBar, Widget):
    def __init__(self):
        super(StatusBar, self).__init__()
        Widget.__init__(self)
        self._perm = QtGui.QLabel()
        self.addWidget(self._perm, 1)
        self.duration = 2000

    def showMessage(self, text, *args):
        text = getLanguageString(text) % args
        super(StatusBar, self).showMessage(text, self.duration)

    def setMessage(self, text, *args):
        text = getLanguageString(text) % args
        self._perm.setText(text)

class VScrollLayout(QtGui.QLayout):
    def __init__(self, parent = None):
        super(VScrollLayout, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self._child = None
        self._position = 0

    def addItem(self, item):
        if self._child is not None:
            raise RuntimeError('layout already has a child')
        self._child = item
        self._update()

    def count(self):
        return int(self._child is not None)

    def itemAt(self, index):
        if index != 0:
            return None
        if self._child is None:
            return None
        return self._child

    def takeAt(self, index):
        if self.child is None:
            return None
        child = self._child
        self._child = None
        self._update()
        return child

    def minimumSize(self):
        if self._child is None:
            return super(VScrollLayout, self).minimumSize()
        # log.debug('VScrollLayout.minimumSize(child): %d %d', self._child.sizeHint().width(), self._child.sizeHint().height())
        left, top, right, bottom = self.getContentsMargins()
        return QtCore.QSize(self._child.minimumSize().width() + left + right, 0)

    def maximumSize(self):
        if self._child is None:
            return super(VScrollLayout, self).maximumSize()
        # log.debug('VScrollLayout.maximumSize(child): %d %d', self._child.sizeHint().width(), self._child.sizeHint().height())
        left, top, right, bottom = self.getContentsMargins()
        return self._child.maximumSize() + QtCore.QSize(left + right, top + bottom)

    def sizeHint(self):
        if self._child is None:
            return super(VScrollLayout, self).sizeHint()
        # log.debug('VScrollLayout.sizeHint(child): %d %d', self._child.sizeHint().width(), self._child.sizeHint().height())
        left, top, right, bottom = self.getContentsMargins()
        return self._child.sizeHint() + QtCore.QSize(left + right, top + bottom)

    def setGeometry(self, rect):
        super(VScrollLayout, self).setGeometry(rect)
        self._position
        # log.debug('VScrollLayout.setGeometry: position: %d', self._position)
        # log.debug('VScrollLayout.setGeometry: %d %d %d %d', rect.x(), rect.y(), rect.width(), rect.height())
        if self._child is None:
            return
        size = self._child.sizeHint()
        left, top, right, bottom = self.getContentsMargins()
        # log.debug('VScrollLayout.getContentsMargins: %d %d %d %d', left, top, right, bottom)

        rect = rect.adjusted(left, top, -right, -bottom)
        rect.adjust(0, -self._position, 0, -self._position)
        # log.debug("%x", int(self._child.widget().sizePolicy().horizontalPolicy()))
        if not self._child.widget().sizePolicy().horizontalPolicy() & QtGui.QSizePolicy.ExpandFlag:
            rect.setWidth(size.width())
        if not self._child.widget().sizePolicy().verticalPolicy() & QtGui.QSizePolicy.ExpandFlag:
            rect.setHeight(size.height())
        else:
            rect.setHeight(max(rect.height(), size.height()))

        # log.debug('VScrollLayout.setGeometry(child): %d %d %d %d', rect.x(), rect.y(), rect.width(), rect.height())
        self._child.setGeometry(rect)

    def expandingDirections(self):
        if self._child is None:
            return 0
        return self._child.expandingDirections()

    def hasHeightForWidth(self):
        if self._child is None:
            return super(VScrollLayout, self).hasHeightForWidth()
        return self._child.hasHeightForWidth()

    def heightForWidth(self, width):
        if self._child is None:
            return super(VScrollLayout, self).heightForWidth(width)
        return self._child.heightForWidth(width)

    def setPosition(self, value):
        self._position = value
        self._update()

    def _update(self):
        self.update()

    def childHeight(self):
        if self._child is None:
            return 0
        left, top, right, bottom = self.getContentsMargins()
        return self._child.sizeHint().height() + top + bottom

class Viewport(QtGui.QWidget):
    def __init__(self):
        super(Viewport, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self._layout = VScrollLayout(self)
        self._layout.setContentsMargins(1, 20, 1, 20)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._child = None

    def setWidget(self, widget):
        if widget is None:
            self._layout.removeWidget(self._child)
        else:
            self._layout.addWidget(widget)
        self._child = widget
        self.updateGeometry()

    def childHeight(self):
        return self._layout.childHeight()

    def setPosition(self, value):
        self._layout.setPosition(value)

class VScrollArea(QtGui.QWidget, Widget):
    def __init__(self):
        super(VScrollArea, self).__init__()
        Widget.__init__(self)

        self._viewport = Viewport()
        self._scrollbar = QtGui.QScrollBar(QtCore.Qt.Vertical)
        self._scrollbar.setRange(0, 0)
        self._scrollbar.setMinimumHeight(0)
        self._scrollbar.setSingleStep(10)
        self._layout = QtGui.QBoxLayout(QtGui.QBoxLayout.RightToLeft, self)
        self._layout.addWidget(self._scrollbar, 0)
        self._layout.addWidget(self._viewport, 1)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._scrollbar.setTracking(True)
        self._widget = None
        self.connect(self._scrollbar, QtCore.SIGNAL('valueChanged(int)'), self._changed)

    def setWidget(self, widget):
        if self._widget is not None:
            self._widget.removeEventFilter(self)
        self._widget = widget
        self._viewport.setWidget(self._widget)
        self.updateGeometry()
        self._updateScrollSize()
        if self._widget is not None:
            self._widget.installEventFilter(self)

    def resizeEvent(self, event):
        # log.debug('resizeEvent: %d, %d', event.size().width(), event.size().height())
        super(VScrollArea, self).resizeEvent(event)
        self._updateScrollSize()
        self._updateScrollPosition()

    def _updateScrollSize(self):
        cheight = self._viewport.childHeight()
        vheight = self._viewport.size().height()
        # log.debug('_updateScrollSize: %d, %d', cheight, vheight)
        self._scrollbar.setRange(0, cheight - vheight)
        self._scrollbar.setPageStep(vheight)

    def _changed(self, value):
        # log.debug('VScrollArea_changed: %d', value)
        self._updateScrollPosition()

    def _updateScrollPosition(self):
        value = self._scrollbar.value()
        # log.debug('_updateScrollPosition: %d', value)
        self._viewport.setPosition(value)

    def eventFilter(self, object, event):
        if object == self._widget and event.type() != QtCore.QEvent.Resize:
            # log.debug('Viewport child resize: %d,%d -> %d,%d',
            #           event.oldSize().width(), event.oldSize().height(),
            #           event.size().width(), event.size().height())
            self._updateScrollSize()
        return False

    def getClassName(self):
        """
        Classname for this widet, useful for styling using qss.
        """
        return str(self.metaObject().className())

class TreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, text, parent=None, isDir=False):
        super(TreeItem, self).__init__([text])
        self.text = text
        self.parent = parent
        self.isDir = isDir
        if self.isDir:
            self.setIcon(0, TreeView._dirIcon)
            self.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        else:
            self.setIcon(0, TreeView._fileIcon)
            self.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.DontShowIndicator)

    def addChild(self, text, isDir=False):
        item = TreeItem(text, self, isDir)
        super(TreeItem, self).addChild(item)
        return item

    def addChildren(self, strings):
        items = [TreeItem(text, self) for text in strings]
        super(TreeItem, self).addChildren(items)
        return items

class TreeView(QtGui.QTreeWidget, Widget):
    _dirIcon = None
    _fileIcon = None

    def __init__(self, parent = None):
        super(TreeView, self).__init__(parent)
        Widget.__init__(self)
        self.connect(self, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem *,int)'), self._activate)
        self.connect(self, QtCore.SIGNAL('itemExpanded(QTreeWidgetItem *)'), self._expand)
        if TreeView._dirIcon is None:
            TreeView._dirIcon = self.style().standardIcon(QtGui.QStyle.SP_DirIcon)
        if TreeView._fileIcon is None:
            TreeView._fileIcon = self.style().standardIcon(QtGui.QStyle.SP_FileIcon)

    def addTopLevel(self, text, isDir=True):
        item = TreeItem(text, None, isDir)
        self.addTopLevelItem(item)
        return item

    def _activate(self, item, column):
        if not item.isDir:
            self.callEvent('onActivate', item)

    def _expand(self, item):
        if item.isDir:
            self.callEvent('onExpand', item)

class SpinBox(QtGui.QSpinBox, Widget):
    def __init__(self, value, parent = None):
        super(SpinBox, self).__init__(parent)
        Widget.__init__(self)
        self.setRange(0, 99999)
        self.setValue(value)
        self.connect(self, QtCore.SIGNAL('valueChanged(int)'), self._changed)

    def _changed(self, value):
        self.callEvent('onChange', value)

    def setValue(self, value):
        self.blockSignals(True)
        super(SpinBox, self).setValue(value)
        self.blockSignals(False)

class BrowseButton(Button):
    def __init__(self, mode = 'open'):
        mode = mode.lower()
        if mode not in ('open', 'save', 'dir'):
            raise RuntimeError("mode '%s' not recognised; must be 'open', 'save', or 'dir'")
        super(BrowseButton, self).__init__("...")
        self._path = ''
        self._filter = ''
        self._mode = mode

    def setPath(self, path):
        self._path = path

    def setFilter(self, filter):
        self._filter = filter

    def _clicked(self, state):
        log.debug('clicked')
        if not os.path.isfile(self._path):
            self._path = os.path.split(self._path)[0]
            if not os.path.isdir(self._path):
                self._path = os.getcwd()
        if self._mode == 'open':
            self._path = str(QtGui.QFileDialog.getOpenFileName(G.app.mainwin, directory=self._path, filter=self._filter))
        elif self._mode == 'save':
            self._path = str(QtGui.QFileDialog.getSaveFileName(G.app.mainwin, directory=self._path, filter=self._filter))
        elif self._mode == 'dir':
            self._path = str(QtGui.QFileDialog.getExistingDirectory(G.app.mainwin, directory=self._path))
        self.callEvent('onClicked', self._path)

class Action(QtGui.QAction, Widget):
    _groups = {}

    @classmethod
    def getIcon(cls, name):
        # icon = G.app.mainwin.style().standardIcon(QtGui.QStyle.SP_MessageBoxWarning)
        path = os.path.join('data', 'icons', name + '.png')
        if G.app.theme:
            themePath = os.path.join('data', 'themes', G.app.theme, 'icons', name + '.png')
            if os.path.isfile(themePath):
                path = themePath
        if not os.path.isfile(path):
            path = os.path.join('data', 'icons', 'notfound.png')
        return QtGui.QIcon(path)

    @classmethod
    def getGroup(cls, name):
        if name not in cls._groups:
            cls._groups[name] = ActionGroup()
        return cls._groups[name]

    def __init__(self, name, text, method, tooltip = None, group = None, toggle = False):
        super(Action, self).__init__(self.getIcon(name), text, G.app.mainwin)
        self.name = name
        self.method = method
        if tooltip is not None:
            self.setToolTip(tooltip)
        if group is not None:
            self.setActionGroup(self.getGroup(group))
        if toggle:
            self.setCheckable(True)
        self.connect(self, QtCore.SIGNAL('triggered(bool)'), self._activate)

    @property
    def text(self):
        return str(super(Action, self).text())

    def setActionGroup(self, group):
        self.setCheckable(True)
        super(Action, self).setActionGroup(group)

    def _activate(self, checked):
        self.method()

class ActionGroup(QtGui.QActionGroup):
    def __init__(self):
        super(ActionGroup, self).__init__(G.app.mainwin)

class Actions(object):
    def __init__(self):
        self._order = []

    def __setattr__(self, name, value):
        if name[0] != '_':
            self._order.append(value)
        object.__setattr__(self, name, value)

    def __iter__(self):
        return iter(self._order)

class SizePolicy(object):
    Fixed               = QtGui.QSizePolicy.Fixed
    Minimum             = QtGui.QSizePolicy.Minimum
    Maximum             = QtGui.QSizePolicy.Maximum
    Preferred           = QtGui.QSizePolicy.Preferred
    Expanding           = QtGui.QSizePolicy.Expanding
    MinimumExpanding    = QtGui.QSizePolicy.MinimumExpanding
    Ignored             = QtGui.QSizePolicy.Ignored

class TableView(QtGui.QTableWidget, Widget):
    def __init__(self):
        super(TableView, self).__init__()
        Widget.__init__(self)

    def setItem(self, row, col, text, data = None):
        item = QtGui.QTableWidgetItem(text)
        if data is not None:
            item.setData(QtCore.Qt.UserRole, data)
        super(TableView, self).setItem(row, col, item)

    def getItemData(self, row, col):
        return self.item(row, col).data(QtCore.Qt.UserRole).toPyObject()

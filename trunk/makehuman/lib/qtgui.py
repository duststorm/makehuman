#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from core import G
import events3d

class Tab(events3d.EventHandler):
    def __init__(self, parent, label):
        super(Tab, self).__init__()
        self.parent = parent
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

    @staticmethod
    def getLanguageString(text):
        return text

    def setPosition(self, position):
        pass

    def getPosition(self):
        return (0, 0, 0)

class TabsBase(Widget):
    def __init__(self):
        super(TabsBase, self).__init__()
        self.tabBar().setExpanding(False)
        self.connect(self, QtCore.SIGNAL('currentChanged(int)'), self.tabChanged)
        self._tabs = {}

    def _addTab(self, label):
        tab = Tab(self, label)
        tab.idx = self._makeTab(tab)
        self._tabs[tab.idx] = tab
        return tab

    def tabChanged(self, idx):
        tab = self._tabs.get(idx)
        if tab:
            self.callEvent('onTabSelected', tab)
            tab.callEvent('onClicked', tab)

class Tabs(QtGui.QTabWidget, TabsBase):
    def __init__(self, parent = None):
        QtGui.QTabWidget.__init__(self, parent)
        TabsBase.__init__(self)

    def _makeTab(self, tab):
        tab.child = TabBar(self)
        return super(Tabs, self).addTab(tab.child, tab.label)

    def addTab(self, label):
        return super(Tabs, self)._addTab(label)

    def tabChanged(self, idx):
        super(Tabs, self).tabChanged(idx)
        tab = self._tabs.get(idx)
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

    def addTab(self, label):
        return super(TabBar, self)._addTab(label)

class GroupBox(QtGui.QGroupBox, Widget):
    def __init__(self, label = ''):
        label = self.getLanguageString(label) if label else ''
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
    def __init__(self, value=0.0, min=0.0, max=1.0, label=None, vertical=False, valueConverter=None):
        super(Slider, self).__init__()
        Widget.__init__(self)
        orient = (QtCore.Qt.Vertical if vertical else QtCore.Qt.Horizontal)
        self.slider = QtGui.QSlider(orient)
        self.min = min
        self.max = max
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)
        self.slider.setValue(value)
        self.slider.setTracking(False)
        self.hold_events = False
        self.connect(self.slider, QtCore.SIGNAL('sliderMoved(int)'), self._changing)
        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self._changed)

        self.label = QtGui.QLabel(label or '')
        self.layout = QtGui.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label, 0, 0)
        self.layout.setColumnStretch(0, 0)
        self.layout.addWidget(self.slider, 0, 1)
        self.layout.setColumnStretch(1, 1)

    def _changing(self, value):
        if self.hold_events:
            return
        self.callEvent('onChanging', self._i2f(value))

    def _changed(self, value):
        if self.hold_events:
            return
        self.callEvent('onChange', self._i2f(value))

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
        self.setText(label)

    def _clicked(self, state):
        self.callEvent('onClicked', None)

    @property
    def selected(self):
        return self.isChecked()

    def setSelected(self, value):
        self.setChecked(value)

class Button(QtGui.QPushButton, ButtonBase):
    def __init__(self, label=None, selected=False, style=None):
        super(Button, self).__init__(label)
        ButtonBase.__init__(self)

class CheckBox(QtGui.QCheckBox, ButtonBase):
    def __init__(self, label=None, selected=False, style=None):
        super(CheckBox, self).__init__(label)
        ButtonBase.__init__(self)
        self.setChecked(selected)

ToggleButton = CheckBox

class RadioButton(QtGui.QRadioButton, ButtonBase):
    groups = {}

    def __init__(self, group, label=None, selected=False, style=None):
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
    def __init__(self, label = '', style=None):
        label = self.getLanguageString(label) if label else ''
        super(TextView, self).__init__(label)
        Widget.__init__(self)

    def setText(self, text):
        text = self.getLanguageString(text) if text else ''
        super(TextView,self).setText(text)
        
    def setTextFormat(self, text, *values):
        text = self.getLanguageString(text) if text else ''
        super(TextView,self).setText(text % values)

def intValidator(text):
    return not text or text.isdigit() or (text[0] == '-' and (len(text) == 1 or text[1:].isdigit()))
    
def floatValidator(text):
    return not text or (text.replace('.', '').isdigit() and text.count('.') <= 1) or (text[0] == '-' and (len(text) == 1 or text[1:].replace('.', '').isdigit()) and text.count('.') <= 1) # Negative sign and optionally digits with optionally 1 decimal point

def filenameValidator(text):
    return not text or len(set(text) & set('\\/:*?"<>|')) == 0

class TextEdit(QtGui.QLineEdit, Widget):
    def __init__(self, text='', style=None, validator = None):
        super(TextEdit, self).__init__(text)
        Widget.__init__(self)
        self.setValidator(validator)
        self.connect(self, QtCore.SIGNAL('textEdited(QString)'), self._textChanged)

    @property
    def text(self):
        return self.toPlainText()

    def _textChanged(self, string):
        self.callEvent('onChange', string)

    def setText(self, text):
        self.setPlainText(text)
        self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

    def getText(self):
        return self.toPlainText()

    def validateText(self, text):
        if self.__validator:
            return self.__validator(text)
        else:
            return True

    def setValidator(self, validator):
        self.__validator = validator
        if validator == intValidator:
            qvalidator = QIntValidator()
        elif validator == floatValidator:
            qvalidator = QDoubleValidator()
        elif validator == filenameValidator:
            qvalidator = QRegExpValidator(QRegExp(r'[\/:*?"<>|]*'))
        else:
            qvalidator = None
        super(TextEdit, self).setValidator(qvalidator)

class ProgressBar(QtGui.QProgressBar, Widget):
    def __init__(self, style=None, barStyle=None, visible=True):
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

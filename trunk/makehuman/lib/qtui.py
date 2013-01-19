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
import atexit
import log

from PyQt4 import QtCore, QtGui, QtOpenGL

from core import G
import glmodule as gl
import events3d
import qtgui

class Modifiers:
    SHIFT = int(QtCore.Qt.ShiftModifier)
    CTRL  = int(QtCore.Qt.ControlModifier)
    ALT   = int(QtCore.Qt.AltModifier)
    META  = int(QtCore.Qt.MetaModifier)

class Keys:
    a = QtCore.Qt.Key_A
    b = QtCore.Qt.Key_B
    c = QtCore.Qt.Key_C
    d = QtCore.Qt.Key_D
    e = QtCore.Qt.Key_E
    f = QtCore.Qt.Key_F
    g = QtCore.Qt.Key_G
    h = QtCore.Qt.Key_H
    i = QtCore.Qt.Key_I
    j = QtCore.Qt.Key_J
    k = QtCore.Qt.Key_K
    l = QtCore.Qt.Key_L
    m = QtCore.Qt.Key_M
    n = QtCore.Qt.Key_N
    o = QtCore.Qt.Key_O
    p = QtCore.Qt.Key_P
    q = QtCore.Qt.Key_Q
    r = QtCore.Qt.Key_R
    s = QtCore.Qt.Key_S
    t = QtCore.Qt.Key_T
    u = QtCore.Qt.Key_U
    v = QtCore.Qt.Key_V
    w = QtCore.Qt.Key_W
    x = QtCore.Qt.Key_X
    y = QtCore.Qt.Key_Y
    z = QtCore.Qt.Key_Z

    N0 = QtCore.Qt.Key_0
    N1 = QtCore.Qt.Key_1
    N2 = QtCore.Qt.Key_2
    N3 = QtCore.Qt.Key_3
    N4 = QtCore.Qt.Key_4
    N5 = QtCore.Qt.Key_5
    N6 = QtCore.Qt.Key_6
    N7 = QtCore.Qt.Key_7
    N8 = QtCore.Qt.Key_8
    N9 = QtCore.Qt.Key_9

    F1  = QtCore.Qt.Key_F1
    F2  = QtCore.Qt.Key_F2
    F3  = QtCore.Qt.Key_F3
    F4  = QtCore.Qt.Key_F4
    F5  = QtCore.Qt.Key_F5
    F6  = QtCore.Qt.Key_F6
    F7  = QtCore.Qt.Key_F7
    F8  = QtCore.Qt.Key_F8
    F9  = QtCore.Qt.Key_F9
    F10 = QtCore.Qt.Key_F10
    F11 = QtCore.Qt.Key_F11
    F12 = QtCore.Qt.Key_F12
    F13 = QtCore.Qt.Key_F13
    F14 = QtCore.Qt.Key_F14
    F15 = QtCore.Qt.Key_F15

    UP        = QtCore.Qt.Key_Up
    DOWN      = QtCore.Qt.Key_Down
    LEFT      = QtCore.Qt.Key_Left
    RIGHT     = QtCore.Qt.Key_Right

    PAGEUP    = QtCore.Qt.Key_PageUp
    PAGEDOWN  = QtCore.Qt.Key_PageDown
    HOME      = QtCore.Qt.Key_Home
    END       = QtCore.Qt.Key_End
    INSERT    = QtCore.Qt.Key_Insert
    DELETE    = QtCore.Qt.Key_Delete
    PAUSE     = QtCore.Qt.Key_Pause

    RETURN    = QtCore.Qt.Key_Return
    BACKSPACE = QtCore.Qt.Key_Backspace
    ESCAPE    = QtCore.Qt.Key_Escape
    TAB       = QtCore.Qt.Key_Tab

    PLUS      = QtCore.Qt.Key_Plus
    MINUS     = QtCore.Qt.Key_Minus
    PERIOD    = QtCore.Qt.Key_Period

    SHIFT     = QtCore.Qt.Key_Shift
    CTRL      = QtCore.Qt.Key_Control
    ALT       = QtCore.Qt.Key_Alt
    META      = QtCore.Qt.Key_Meta

Keys._all = set(getattr(Keys, k)
                for k in dir(Keys)
                if k[0] != '_')

class Buttons:
    LEFT = QtCore.Qt.LeftButton
    MIDDLE = QtCore.Qt.MidButton
    RIGHT = QtCore.Qt.RightButton

    LEFT_MASK = LEFT
    MIDDLE_MASK = MIDDLE
    RIGHT_MASK = RIGHT

g_mouse_pos = None
gg_mouse_pos = None

class Canvas(QtOpenGL.QGLWidget):
    def __init__(self, parent):
        format = QtOpenGL.QGLFormat()
        format.setAlpha(True)
        format.setDepthBufferSize(24)
        format.setSampleBuffers(True)
        format.setSamples(4)
        super(Canvas, self).__init__(format, parent)
        self.create()

    def create(self):
        G.swapBuffers = self.swapBuffers
        self.setFocusPolicy(QtCore.Qt.TabFocus)
        self.setFocus()
        self.setAutoBufferSwap(False)
        self.setAutoFillBackground(False)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setAttribute(QtCore.Qt.WA_KeyCompression, False)
        self.setMouseTracking(True)
        self.setMinimumHeight(5)
        self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)

    def callback(self, name, *args, **kwargs):
        accum = kwargs.get('accum', False)
        name = 'on%sCallback' % name
        app = self.parentWidget().app
        if not hasattr(app, name):
            return
        func = getattr(app, name)
        if G.profile:
            if accum:
                profiler.accum('func(*args)' % name, globals(), locals())
            else:
                profiler.flush()
                profiler.run('func(*args)' % name, globals(), locals())
        else:
            func(*args)

    def mousePressEvent(self, ev):
        self.mouseUpDownEvent(ev, "MouseDown")

    def mouseReleaseEvent(self, ev):
        self.mouseUpDownEvent(ev, "MouseUp")

    def mouseUpDownEvent(self, ev, direction):
        global gg_mouse_pos

        x = ev.x()
        y = ev.y()
        b = ev.button()

        gg_mouse_pos = x, y

        gl.getPickedColor(x, y)

        self.callback(direction, b, x, y)

        # Update screen
        self.update()

        gl.updatePickingBuffer()

    def wheelEvent(self, ev):
        global gg_mouse_pos

        x = ev.x()
        y = ev.y()
        d = ev.delta()

        gg_mouse_pos = x, y

        b = 1 if d > 0 else -1

        self.callback('MouseWheel', b, x, y)

    def mouseMoveEvent(self, ev):
        global gg_mouse_pos, g_mouse_pos

        x = ev.x()
        y = ev.y()

        if gg_mouse_pos is None:
            gg_mouse_pos = x, y

        if g_mouse_pos is None:
            callAsync(self.handleMouse)

        g_mouse_pos = (x, y)

    def handleMouse(self):
        global gg_mouse_pos, g_mouse_pos

        if g_mouse_pos is None:
            return

        ox, oy = gg_mouse_pos
        (x, y) = g_mouse_pos
        g_mouse_pos = None
        xrel = x - ox
        yrel = y - oy
        gg_mouse_pos = x, y

        buttons = int(G.app.mouseButtons())

        if not buttons:
            gl.getPickedColor(x, y)

        self.callback('MouseMoved', buttons, x, y, xrel, yrel, accum = True)

        if buttons:
            self.update()

    def initializeGL(self):
        gl.OnInit()

    def paintGL(self):
        gl.draw()

    def resizeGL(self, w, h):
        G.windowHeight = h
        G.windowWidth = w
        gl.reshape(w, h)
        self.callback('Resized', w, h, False)

    def timerEvent(self, ev):
        handleTimer(ev.timerId())

class VLayout(QtGui.QLayout):
    def __init__(self, parent = None):
        super(VLayout, self).__init__(parent)
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

    def _doLayout(self, x, y, width, height, real=False):
        last = None
        for i, child in enumerate(self._children):
            widget = child.widget()
            if widget and not widget.isVisible():
                continue
            last = i

        x1 = x + width
        y1 = y + height

        for i, child in enumerate(self._children):
            widget = child.widget()
            if not widget or widget.isHidden():
                w = 0
                h = 0
            else:
                size = child.maximumSize()
                w = size.width()
                h = size.height()
            if real:
                child.setGeometry(QtCore.QRect(x, y, min(w, x1 - x), min(h, y1 - y)))
            width = max(width, w)
            y += h
        return width, y

    def sizeHint(self):
        width, height = self._doLayout(0, 0, 1e9, 1e9, False)
        return QtCore.QSize(width, height)

    def maximumSize(self):
        return self.sizeHint()

    def setGeometry(self, rect):
        self._doLayout(rect.x(), rect.y(), rect.width(), rect.height(), True)

    def expandingDirections(self):
        return QtCore.Qt.Vertical

class TaskPanel(qtgui.VScrollArea):
    def __init__(self):
        super(TaskPanel, self).__init__()
        self.setMinimumHeight(250)
        self.child = QtGui.QWidget()
        self.child.setContentsMargins(0, 0, 0, 0)
        self.child.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        self.setWidget(self.child)
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self.child)

    def addWidget(self, widget, *args, **kwargs):
        self.layout.addWidget(widget, *args, **kwargs)
        return widget

    def removeWidget(self, widget):
        self.layout.removeWidget(widget)

class CategoryPanel(QtGui.QWidget, qtgui.Widget):
    def __init__(self):
        super(CategoryPanel, self).__init__()
        qtgui.Widget.__init__(self)
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.BottomToTop, self)

    def addWidget(self, widget, *args, **kwargs):
        self.layout.addWidget(widget, *args, **kwargs)
        return widget

    def removeWidget(self, widget):
        self.layout.removeWidget(widget)

def getQtVersion():
    return [ int(versionNb) for versionNb in str(QtCore.qVersion()).split(".") ]

class Frame(QtGui.QWidget):
    title = "MakeHuman"

    def __init__(self, app, size):
        self.app = app
        super(Frame, self).__init__()

        self.shortcuts = {}

        self.setWindowTitle(self.title)
        qtVersion = getQtVersion()
        if qtVersion[0] >= 4 and qtVersion[1] >= 2:
            self.setWindowIcon(QtGui.QIcon("icons/makehuman_bg.svg"))
        else:
            self.setWindowIcon(QtGui.QIcon("icons/makehuman.bmp"))
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setAttribute(QtCore.Qt.WA_KeyCompression, False)
        self.resize(*size)
        self.create()

    def panel(self):
        widget = QtGui.QWidget()
        widget.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, False)
        widget.setAutoFillBackground(True)
        widget.setContentsMargins(0, 0, 0, 0)
        return widget

    def create(self):
        self.v_layout = QtGui.QGridLayout(self)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.setSpacing(0)

        self.tab_panel = self.panel()
        self.v_layout.addWidget(self.tab_panel, 0, 0)
        self.v_layout.setRowStretch(0, 0)

        self.tab_layout = QtGui.QGridLayout(self.tab_panel)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs = qtgui.Tabs()
        self.tab_layout.addWidget(self.tabs)

        self.h_layout = QtGui.QGridLayout()
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.setSpacing(0)
        self.v_layout.addLayout(self.h_layout, 1, 0)
        self.v_layout.setRowStretch(1, 1)

        self.b_panel = self.panel()
        self.bottom = QtGui.QBoxLayout(QtGui.QBoxLayout.BottomToTop, self.b_panel)
        self.v_layout.addWidget(self.b_panel, 2, 0)
        self.v_layout.setRowStretch(2, 0)

        self.l_panel = self.panel()
        self.l_layout = QtGui.QGridLayout(self.l_panel)
        self.l_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addWidget(self.l_panel, 0, 0)
        self.h_layout.setColumnStretch(0, 0)

        self.t_layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.h_layout.addLayout(self.t_layout, 0, 1)
        self.h_layout.setColumnStretch(1, 1)

        self.t_panel = self.panel()
        self.top = VLayout(self.t_panel)
        self.top.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.t_layout.addWidget(self.t_panel)
        self.t_panel.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Maximum)

        self.canvas = Canvas(self)
        self.t_layout.addWidget(self.canvas)

        self.r_panel = self.panel()
        self.r_layout = QtGui.QGridLayout(self.r_panel)
        self.r_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addWidget(self.r_panel, 0, 2)
        self.h_layout.setColumnStretch(2, 0)

        self.left_top    = QtGui.QStackedLayout()
        self.l_layout.addLayout(self.left_top, 0, 0)
        self.l_layout.setRowStretch(0, 1)

        self.left_bottom  = QtGui.QBoxLayout(QtGui.QBoxLayout.BottomToTop)
        self.l_layout.addLayout(self.left_bottom, 2, 0)
        self.l_layout.setRowStretch(2, 0)

        self.right_top    = QtGui.QStackedLayout()
        self.r_layout.addLayout(self.right_top, 0, 0)
        self.r_layout.setRowStretch(0, 1)

        self.right_bottom = CategoryPanel()
        self.r_layout.addWidget(self.right_bottom, 2, 0)
        self.r_layout.setRowStretch(2, 0)

        self.statusBar = qtgui.StatusBar()
        self.bottom.addWidget(self.statusBar)
        self.progressBar = qtgui.ProgressBar()
        self.bottom.addWidget(self.progressBar)

    def addPanels(self):
        left = TaskPanel()
        right = TaskPanel()
        left.setObjectName("LeftTaskPanel")
        right.setObjectName("RightTaskPanel")
        self.left_top.addWidget(left)
        self.right_top.addWidget(right)
        return left, right

    def showPanels(self, left, right):
        self.left_top.setCurrentWidget(left)
        self.right_top.setCurrentWidget(right)

    def addPanelBottomLeft(self):
        panel = CategoryPanel()
        self.left_bottom.addWidget(panel)
        return panel

    def showPanelBottomLeft(self, panel):
        for widget in [self.left_bottom.itemAt(i).widget()
                       for i in xrange(self.left_bottom.count())]:
            if widget is not panel:
                widget.hide()
        if panel is not None:
            panel.show()

    def getPanelBottomRight(self):
        return self.right_bottom

    def addTopWidget(self, widget, *args, **kwargs):
        self.top.addWidget(widget, *args, **kwargs)
        return widget

    def removeTopWidget(self, widget):
        self.top.removeWidget(widget)

    def update(self):
        super(Frame, self).update()
        self.canvas.update()

    def closeEvent(self, ev):
        ev.ignore()
        self.app.onQuitCallback()

    def refreshLayout(self, widget=None):
        if widget is None:
            widget = self
        widget.updateGeometry()
        for child in QtGui.QWidget.children(widget):
            if child.isWidgetType():
                self.refreshLayout(child)

    def setShortcut(self, modifier, key, method):
        sequence = QtGui.QKeySequence(modifier + key)

        if method in self.shortcuts:
            self.shortcuts[method].setKey(sequence)
            return
                
        shortcut = QtGui.QShortcut(sequence, self)
        shortcut.setContext(QtCore.Qt.ApplicationShortcut)
        self.connect(shortcut, QtCore.SIGNAL("activated()"), method)
        self.shortcuts[method] = shortcut

class Application(QtGui.QApplication, events3d.EventHandler):
    def __init__(self):
        super(Application, self).__init__(sys.argv)
        self.mainwin = None
        self.log_window = None
        self.statusBar = None
        self.progressBar = None
        self.splash = None

    def OnInit(self):
        self.mainwin = Frame(self, (G.windowWidth, G.windowHeight))
        self.statusBar = self.mainwin.statusBar
        self.progressBar = self.mainwin.progressBar
        self.mainwin.show()
        self.log_window = qtgui.DocumentEdit()
        
    def started(self):
        self.callEvent('onStart', None)

    def start(self):
        self.OnInit()
        callAsync(self.started)
        self.exec_()
        gl.OnExit()

    def stop(self):
        self.callEvent('onStop', None)
        sys.exit()
        
    def redraw(self):
        self.mainwin.update()
        
    def getWindowSize(self):
        return G.windowWidth, G.windowHeight

    def addLogMessage(self, text):
        if self.log_window is None:
            return
        self.log_window.addText(text)

    def processEvents(self, flags = QtCore.QEventLoop.ExcludeUserInputEvents):
        super(Application, self).processEvents(flags)

    def event(self, event):
        if event.type() == QtCore.QEvent.User:
            event.callback()
            return True
        return super(Application, self).event(event)

g_timers = {}

def getKeyModifiers():
    return int(QtGui.QApplication.keyboardModifiers())

def addTimer(milliseconds, callback):
    timer_id = G.app.mainwin.canvas.startTimer(milliseconds)
    g_timers[timer_id] = callback
    return timer_id

def removeTimer(id):
    G.app.mainwin.canvas.killTimer(id)
    del g_timers[id]

def handleTimer(id):
    if id not in g_timers:
        return
    callback = g_timers[id]
    callback()

class AsyncEvent(QtCore.QEvent):
    def __init__(self, callback):
        super(AsyncEvent, self).__init__(QtCore.QEvent.User)
        self.callback = callback

def callAsync(callback):
    if G.app is None:
        log.notice('callAsync with no application')
        return
    G.app.postEvent(G.app, AsyncEvent(callback))

def getSaveFileName(directory, filter = "All files (*.*)"):
    return str(QtGui.QFileDialog.getSaveFileName(
        G.app.mainwin, qtgui.getLanguageString("Save File"), directory, filter))

def getOpenFileName(directory, filter = "All files (*.*)"):
    return str(QtGui.QFileDialog.getOpenFileName(
        G.app.mainwin, qtgui.getLanguageString("Open File"), directory, filter))

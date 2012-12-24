import sys
import atexit

from PyQt4 import QtCore, QtGui, QtOpenGL

from core import G
import glmodule as gl
import events3d
import qtgui

import traceback
def catching(func):
    def wrapper(*args, **kwargs):
        # if func.func_name != 'idleFunc':
        #     print func
        try:
            return func(*args, **kwargs)
        except StandardError, e:
            traceback.print_exc()

    # def wrapper(*args, **kwargs):
    #     return func(*args, **kwargs)

    return wrapper

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
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()
        self.setAutoBufferSwap(False)
        self.setAutoFillBackground(False)
        # self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
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

    def mouseButtonDown(self, b, x, y):
        # Check which object/group was hit
        if b in (1,2,3):
            gl.getPickedColor(x, y)

        # Notify python
        self.callback('MouseDown', b, x, y)

        # Update screen
        self.update()

        if b in (1,2,3):
            gl.updatePickingBuffer()

    def mouseButtonUp(self, b, x, y):
        # Check which object/group was hit
        if b in (1,2,3):
            gl.getPickedColor(x, y)

        # Notify python
        self.callback('MouseUp', b, x, y)

        # Update screen
        self.update()

        gl.updatePickingBuffer()

    def mouseMotion(self, s, x, y, xrel, yrel):
        # Check which object/group was hit
        if not s:
            gl.getPickedColor(x, y)

        # Notify python
        self.callback('MouseMoved', s, x, y, xrel, yrel, accum = True)

        # Update screen
        if s:
            self.update()

    def mousePressEvent(self, ev):
        global gg_mouse_pos

        x = ev.x()
        y = ev.y()
        b = ev.button()

        gg_mouse_pos = x, y

        self.mouseButtonDown(b, x, y)

    def mouseReleaseEvent(self, ev):
        global gg_mouse_pos

        x = ev.x()
        y = ev.y()
        b = ev.button()

        gg_mouse_pos = x, y

        self.mouseButtonUp(b, x, y)

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
            QtCore.QTimer.singleShot(0, self.idle)

        g_mouse_pos = (x, y)

    def keyDown(self, key, character, modifiers):
        self.callback('KeyDown', key, character, modifiers)

    def keyUp(self, key, character, modifiers):
        self.callback('KeyUp', key, character, modifiers)
        gl.updatePickingBuffer()

    def keyPressEvent(self, ev):
        key = ev.key()
        characters = ev.text()

        if key in Keys._all:
            self.keyDown(key, unicode(characters[:1]), getKeyModifiers())
        elif characters:
            for character in characters:
                # ev.text() may hold multiple characters regardless of
                #  WA_KeyCompression setting
                character = unicode(character)
                key = ord(character)
                self.keyDown(key, character, getKeyModifiers())
        else:
            super(Canvas, self).keyPressEvent(ev)

    def keyReleaseEvent(self, ev):
        key = ev.key()
        characters = ev.text()

        if key in Keys._all:
            self.keyUp(key, unicode(characters[:1]), getKeyModifiers())
        elif characters:
            character = characters[0]
            character = unicode(character)
            key = ord(character)
            self.keyUp(key, character, getKeyModifiers())
        else:
            super(Canvas, self).keyReleaseEvent(ev)

    def initializeGL(self):
        gl.OnInit()

    def paintGL(self):
        gl.draw()

    def resizeGL(self, w, h):
        G.windowHeight = h
        G.windowWidth = w
        gl.reshape(w, h)
        self.callback('Resized', w, h, False)

    def handleMouse(self):
        global gg_mouse_pos, g_mouse_pos

        if g_mouse_pos is not None:
            # print 'mouse motion'
            ox, oy = gg_mouse_pos
            (x, y) = g_mouse_pos
            g_mouse_pos = None
            xrel = x - ox
            yrel = y - oy
            gg_mouse_pos = x, y

            buttons = int(G.app.mouseButtons())

            self.mouseMotion(buttons, x, y, xrel, yrel)

    def idle(self, *args):
        self.handleMouse()

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

        first = True
        x1 = x + width
        y1 = y + height

        for i, child in enumerate(self._children):
            widget = child.widget()
            if not widget or widget.isHidden():
                w = 0
                h = 0
            elif first or i == last:
                first = False
                size = child.maximumSize()
                w = size.width()
                h = size.height()
            else:
                size = child.sizeHint()
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

class Frame(QtGui.QWidget):
    Bottom      = 0
    Top         = 1
    LeftTop     = 2
    LeftBottom  = 3
    RightTop    = 4
    RightBottom = 5
    Center      = 6

    title = "MakeHuman"

    def __init__(self, app, size):
        self.app = app
        super(Frame, self).__init__()
        self.setWindowTitle(self.title)
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setAttribute(QtCore.Qt.WA_KeyCompression, False)
        self.resize(*size)
        self.create()

    def panel(self):
        widget = QtGui.QWidget()
        # widget.setAttribute(QtCore.Qt.WA_PaintOnScreen, False)
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

        self.left_top = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.l_layout.addLayout(self.left_top, 0, 0)
        self.l_layout.setRowStretch(0, 0)

        self.l_layout.setRowStretch(1, 1)

        self.left_bottom  = QtGui.QBoxLayout(QtGui.QBoxLayout.BottomToTop)
        self.l_layout.addLayout(self.left_bottom, 2, 0)
        self.l_layout.setRowStretch(2, 0)

        self.right_top    = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.r_layout.addLayout(self.right_top, 0, 0)
        self.r_layout.setRowStretch(0, 0)

        self.r_layout.setRowStretch(1, 1)

        self.right_bottom = QtGui.QBoxLayout(QtGui.QBoxLayout.BottomToTop)
        self.r_layout.addLayout(self.right_bottom, 2, 0)
        self.r_layout.setRowStretch(2, 0)

        self.sides = {
            self.Bottom:      self.bottom,
            self.Top:         self.top,
            self.LeftTop:     self.left_top,
            self.LeftBottom:  self.left_bottom,
            self.RightTop:    self.right_top,
            self.RightBottom: self.right_bottom,
            }

    def addWidget(self, edge, widget, *args, **kwargs):
        self.sides[edge].addWidget(widget, *args, **kwargs)
        return widget

    def removeWidget(self, edge, widget):
        self.sides[edge].removeWidget(widget)

    def update(self):
        super(Frame, self).update()
        self.canvas.update()

    def closeEvent(self, ev):
        ev.ignore()
        self.app.onQuitCallback()

class Application(QtGui.QApplication, events3d.EventHandler):
    def __init__(self):
        super(Application, self).__init__(sys.argv)

    def OnInit(self):
        self.mainwin = Frame(self, (G.windowWidth, G.windowHeight))
        self.mainwin.show()
        
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
        
    def redrawNow(self):
        gl.draw()
        
    def getWindowSize(self):
        return G.windowWidth, G.windowHeight
        
g_timers = {}

def getKeyModifiers():
    return int(QtGui.QApplication.keyboardModifiers())

def setCaption(caption):
    G.app.mainwin.setWindowTitle(caption)

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

def callAsync(callback):
    QtCore.QTimer.singleShot(0, callback)

def addWidget(edge, widget, *args, **kwargs):
    return G.app.mainwin.addWidget(edge, widget, *args, **kwargs)

def removeWidget(edge, widget):
    return G.app.mainwin.removeWidget(edge, widget)

def changeCategory(category):
    G.app.mainwin.tabs.changeTab(category)

def changeTask(category, task):
    G.app.mainwin.tabs.findTab(category).child.changeTab(task)

def refreshLayout(widget=None):
    if widget is None:
        widget = G.app.mainwin
    widget.updateGeometry()
    for child in QtGui.QWidget.children(widget):
        if child.isWidgetType():
            refreshLayout(child)

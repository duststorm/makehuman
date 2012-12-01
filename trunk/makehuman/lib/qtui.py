import sys
import atexit

from PyQt4 import QtCore, QtGui, QtOpenGL

from core import *
from glmodule import updatePickingBuffer, getPickedColor, OnInit, OnExit, reshape, draw

def keyDown(key, character, modifiers):
    callKeyDown(key, unichr(character), modifiers)

def keyUp(key, character, modifiers):
    callKeyUp(key, unichr(character), modifiers)
    updatePickingBuffer()

def mouseButtonDown(b, x, y):
    # Check which object/group was hit
    if b in (1,2,3):
        getPickedColor(x, y)

    # Notify python
    callMouseButtonDown(b, x, y)

    # Update screen
    queueUpdate()

    if b in (1,2,3):
        updatePickingBuffer()

def mouseButtonUp(b, x, y):
    # Check which object/group was hit
    if b in (1,2,3):
        getPickedColor(x, y)

    # Notify python
    callMouseButtonUp(b, x, y)

    # Update screen
    queueUpdate()

    updatePickingBuffer()

def mouseMotion(s, x, y, xrel, yrel):
    # Check which object/group was hit
    if not s:
        getPickedColor(x, y)

    # Notify python
    callMouseMotion(s, x, y, xrel, yrel)

    # Update screen
    if s:
        queueUpdate()

def quit():
    callQuit()

def shutDown():
    sys.exit()

def queueUpdate():
    g_app.mainwin.update()

def setFullscreen(fullscreen):
    pass

def setCaption(caption):
    g_app.mainwin.setWindowTitle(caption)

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

KMOD_LSHIFT = 0x0001
KMOD_RSHIFT = 0x0002
KMOD_LCTRL = 0x0040
KMOD_RCTRL = 0x0080
KMOD_LALT = 0x0100
KMOD_RALT = 0x0200
KMOD_LMETA = 0x0400
KMOD_RMETA = 0x0800

def getKeyModifiers():
    state = g_app.keyboardModifiers()
    mod = 0
    if state & QtCore.Qt.AltModifier:
        mod |= KMOD_LALT
    if state & QtCore.Qt.ControlModifier:
        mod |= KMOD_LCTRL
    if state & QtCore.Qt.ShiftModifier:
        mod |= KMOD_LSHIFT
    if state & QtCore.Qt.MetaModifier:
        mod |= KMOD_META
    return mod

SDLK_F1 = 282
SDLK_F2 = 283
SDLK_F3 = 284
SDLK_F4 = 285
SDLK_F5 = 286
SDLK_F6 = 287
SDLK_F7 = 288
SDLK_F8 = 289
SDLK_F9 = 290
SDLK_F10 = 291
SDLK_F11 = 292
SDLK_F12 = 293

SDLK_UP = 273
SDLK_DOWN = 274
SDLK_RIGHT = 275
SDLK_LEFT = 276
SDLK_INSERT = 277
SDLK_HOME = 278
SDLK_END = 279
SDLK_PAGEUP = 280
SDLK_PAGEDOWN = 281

key_mapping = {
    QtCore.Qt.Key_F1:        SDLK_F1,
    QtCore.Qt.Key_F2:        SDLK_F2,
    QtCore.Qt.Key_F3:        SDLK_F3,
    QtCore.Qt.Key_F4:        SDLK_F4,
    QtCore.Qt.Key_F5:        SDLK_F5,
    QtCore.Qt.Key_F6:        SDLK_F6,
    QtCore.Qt.Key_F7:        SDLK_F7,
    QtCore.Qt.Key_F8:        SDLK_F8,
    QtCore.Qt.Key_F9:        SDLK_F9,
    QtCore.Qt.Key_F10:       SDLK_F10,
    QtCore.Qt.Key_F11:       SDLK_F11,
    QtCore.Qt.Key_F12:       SDLK_F12,
    QtCore.Qt.Key_Left:      SDLK_LEFT,
    QtCore.Qt.Key_Up:        SDLK_UP,
    QtCore.Qt.Key_Right:     SDLK_RIGHT,
    QtCore.Qt.Key_Down:      SDLK_DOWN,
    QtCore.Qt.Key_PageUp:    SDLK_PAGEUP,
    QtCore.Qt.Key_PageDown:  SDLK_PAGEDOWN,
    QtCore.Qt.Key_Home:      SDLK_HOME,
    QtCore.Qt.Key_End:       SDLK_END,
    QtCore.Qt.Key_Insert:    SDLK_INSERT
    }

SDL_BUTTON_LEFT = 1
SDL_BUTTON_MIDDLE = 2
SDL_BUTTON_RIGHT = 3

SDL_BUTTON_LEFT_MASK = 1
SDL_BUTTON_MIDDLE_MASK = 2
SDL_BUTTON_RIGHT_MASK = 4

button_mapping = {
    QtCore.Qt.LeftButton: (SDL_BUTTON_LEFT, SDL_BUTTON_LEFT_MASK),
    QtCore.Qt.MidButton: (SDL_BUTTON_MIDDLE, SDL_BUTTON_MIDDLE_MASK),
    QtCore.Qt.RightButton: (SDL_BUTTON_RIGHT, SDL_BUTTON_RIGHT_MASK)
    }

g_mouse_pos = None

def handleMouse():
    global g_mouse_pos
    if g_mouse_pos is not None:
        # print 'mouse motion'
        ox, oy = G.mouse_pos
        (x, y) = g_mouse_pos
        g_mouse_pos = None
        xrel = x - ox
        yrel = y - oy
        G.mouse_pos = x, y

        mouse_state = g_app.mouseButtons()
        buttons = 0
        if mouse_state & QtCore.Qt.LeftButton:
            buttons |= SDL_BUTTON_LEFT_MASK
        if mouse_state & QtCore.Qt.MidButton:
            buttons |= SDL_BUTTON_MIDDLE_MASK
        if mouse_state & QtCore.Qt.RightButton:
            buttons |= SDL_BUTTON_RIGHT_MASK

        mouseMotion(buttons, x, y, xrel, yrel)

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
        # self.setAutoFillBackground(False)
        # self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def mousePressEvent(self, ev):
        x = ev.x()
        y = ev.y()

        G.mouse_pos = x, y

        b = ev.button()
        b, mask = button_mapping.get(b, (0, 0))

        mouseButtonDown(b, x, y)

    def mouseReleaseEvent(self, ev):
        x = ev.x()
        y = ev.y()

        G.mouse_pos = x, y

        b = ev.button()
        b, mask = button_mapping.get(b, (0, 0))

        mouseButtonUp(b, x, y)

    def mouseMoveEvent(self, ev):
        global g_mouse_pos

        x = ev.x()
        y = ev.y()

        if G.mouse_pos is None:
            G.mouse_pos = x, y

        if g_mouse_pos is None:
            QtCore.QTimer.singleShot(0, self.idle)

        g_mouse_pos = (x, y)

    def keyPressEvent(self, ev):
        key = ev.nativeVirtualKey()
        character = ev.text()

        if key in key_mapping:
            key = key_mapping[key]
        else:
            super(Canvas, self).keyPressEvent(ev)
            return

        keyDown(key, character, getKeyModifiers())

        ev.accept()

    def keyReleaseEvent(self, ev):
        key = ev.nativeVirtualKey()
        character = ev.text()

        if key in key_mapping:
            key = key_mapping[key]
        else:
            super(Canvas, self).keyReleaseEvent(ev)
            return

        keyUp(key, character, getKeyModifiers())

        ev.accept()

    def initializeGL(self):
        OnInit()

    def paintGL(self):
        draw()

    def resizeGL(self, w, h):
        reshape(w, h)

    def idle(self, *args):
        handleMouse()

    def timerEvent(self, ev):
        handleTimer(ev.timerId())

class Frame(QtGui.QWidget):
    title = "MakeHuman"

    def __init__(self, app, size):
        self.app = app
        super(Frame, self).__init__()
        self.setWindowTitle(self.title)
        self.resize(*size)
        self.canvas = Canvas(self)
        self.layout = QtGui.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.canvas)
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def update(self):
        super(Frame, self).update()
        self.canvas.update()

    def closeEvent(self, ev):
        ev.ignore()
        quit()

class Application(QtGui.QApplication):
    def __init__(self):
        super(Application, self).__init__(sys.argv)

    def OnInit(self):
        self.mainwin = Frame(self, (G.windowWidth, G.windowHeight))
        self.mainwin.show()

g_app = None

def createWindow(useTimer = None):
    global g_app
    g_app = Application()
    g_app.OnInit()

def eventLoop():
    g_app.exec_()
    OnExit()

g_timers = {}

def addTimer(milliseconds, callback):
    timer_id = g_app.mainwin.canvas.startTimer(milliseconds)
    g_timers[timer_id] = callback
    return timer_id

def removeTimer(id):
    g_app.mainwin.canvas.killTimer(id)
    del g_timers[id]

def handleTimer(id):
    if id not in g_timers:
        return
    callback = g_timers[id]
    callback()

def callAsync(callback):
    QtCore.QTimer.singleShot(0, callback)

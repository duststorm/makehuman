import sys
import atexit

from OpenGL.GLUT import *

from core import *
from glmodule import updatePickingBuffer, getPickedColor, OnInit, OnExit, reshape, draw

def swapBuffers():
    glutSwapBuffers()

def keyDown(key, character, modifiers):
    callKeyDown(key, character, modifiers)

def keyUp(key, character, modifiers):
    callKeyUp(key, character, modifiers)
    updatePickingBuffer()

def mouseButtonDown(b, x, y):
    # Check which object/group was hit
    if b in (1,2,3):
        getPickedColor(x, y)

    # Notify python
    callMouseButtonDown(b, x, y)

    # Update screen
    queueUpdate()

    if b in (0,1,2):
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
    if bool(glutLeaveMainLoop):
        glutLeaveMainLoop()
    else:
        sys.exit()

def queueUpdate():
    glutPostRedisplay()

def setFullscreen(fullscreen):
    pass

def setCaption(caption):
    glutSetWindowTitle(caption)

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

g_modifiers = 0

def getKeyModifiers():
    return g_modifiers

KMOD_LSHIFT = 0x0001
KMOD_RSHIFT = 0x0002
KMOD_LCTRL = 0x0040
KMOD_RCTRL = 0x0080
KMOD_LALT = 0x0100
KMOD_RALT = 0x0200
KMOD_LMETA = 0x0400
KMOD_RMETA = 0x0800

modifier_mapping = [
    (GLUT_ACTIVE_SHIFT, KMOD_LSHIFT),
    (GLUT_ACTIVE_CTRL, KMOD_LCTRL),
    (GLUT_ACTIVE_ALT, KMOD_LALT)
    ]

def getModifiers():
    global g_modifiers
    gmod = glutGetModifiers()
    smod = 0
    for gmask, smask in modifier_mapping:
        if gmod & gmask:
            smod |= smask
    g_modifiers = smod

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
    GLUT_KEY_F1:        SDLK_F1,
    GLUT_KEY_F2:        SDLK_F2,
    GLUT_KEY_F3:        SDLK_F3,
    GLUT_KEY_F4:        SDLK_F4,
    GLUT_KEY_F5:        SDLK_F5,
    GLUT_KEY_F6:        SDLK_F6,
    GLUT_KEY_F7:        SDLK_F7,
    GLUT_KEY_F8:        SDLK_F8,
    GLUT_KEY_F9:        SDLK_F9,
    GLUT_KEY_F10:       SDLK_F10,
    GLUT_KEY_F11:       SDLK_F11,
    GLUT_KEY_F12:       SDLK_F12,
    GLUT_KEY_LEFT:      SDLK_LEFT,
    GLUT_KEY_UP:        SDLK_UP,
    GLUT_KEY_RIGHT:     SDLK_RIGHT,
    GLUT_KEY_DOWN:      SDLK_DOWN,
    GLUT_KEY_PAGE_UP:   SDLK_PAGEUP,
    GLUT_KEY_PAGE_DOWN: SDLK_PAGEDOWN,
    GLUT_KEY_HOME:      SDLK_HOME,
    GLUT_KEY_END:       SDLK_END,
    GLUT_KEY_INSERT:    SDLK_INSERT
    }

@catching
def keyDownFunc(key, x, y):
    getModifiers()
    character = key
    key = ord(key)
    keyDown(key, character, g_modifiers)

@catching
def keyUpFunc(key, x, y):
    getModifiers()
    character = key
    key = ord(key)
    callKeyUp(key, character, g_modifiers)

@catching
def specialDownFunc(key, x, y):
    if not (key >= 0x70 and key <= 0x75):
        getModifiers()
    key = key_mapping.get(key, key)
    keyDown(key, "", g_modifiers)

@catching
def specialUpFunc(key, x, y):
    if not (key >= 0x70 and key <= 0x75):
        getModifiers()
    key = key_mapping.get(key, key)
    keyUp(key, "", g_modifiers)

SDL_BUTTON_LEFT = 1
SDL_BUTTON_MIDDLE = 2
SDL_BUTTON_RIGHT = 3

SDL_BUTTON_LEFT_MASK = 1
SDL_BUTTON_MIDDLE_MASK = 2
SDL_BUTTON_RIGHT_MASK = 4

button_mapping = {
    GLUT_LEFT_BUTTON: (SDL_BUTTON_LEFT, SDL_BUTTON_LEFT_MASK),
    GLUT_MIDDLE_BUTTON: (SDL_BUTTON_MIDDLE, SDL_BUTTON_MIDDLE_MASK),
    GLUT_RIGHT_BUTTON: (SDL_BUTTON_RIGHT, SDL_BUTTON_RIGHT_MASK)
    }

g_mouse_pos = None
g_mouse_state = 0

@catching
def mouseButtonFunc(b, s, x, y):
    getModifiers()
    G.mouse_pos = x, y

    global g_mouse_state
    b, mask = button_mapping.get(b, (b+1,1<<b))
    if s == GLUT_DOWN:
        g_mouse_state |= mask
    else:
        g_mouse_state &= ~mask

    if s == GLUT_DOWN:
        mouseButtonDown(b, x, y)
    else:
        mouseButtonUp(b, x, y)

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
        mouseMotion(g_mouse_state, x, y, xrel, yrel)

def mouseMotionFunc(s, x, y):
    getModifiers()
    if G.mouse_pos is None:
        G.mouse_pos = x, y
    global g_mouse_pos
    g_mouse_pos = (x, y)
    glutIdleFunc(idleFunc)

@catching
def mouseMotionActiveFunc(x, y):
    mouseMotionFunc(True, x, y)

@catching
def mouseMotionPassiveFunc(x, y):
    global g_mouse_state
    g_mouse_state = 0
    mouseMotionFunc(False, x, y)

@catching
def drawFunc():
    draw()

@catching
def reshapeFunc(w, h):
    reshape(w, h)

@catching
def idleFunc():
    glutIdleFunc(None)
    handleMouse()
    Async.process()

def createWindow(useTimer = None):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    # glutInitDisplayString("rgb=8 samples")
    glutInitWindowSize(G.windowWidth, G.windowHeight)

    G.swapBuffers = glutSwapBuffers

    # Load and set window icon
    # TODO
    # image = SDL_LoadBMP("mh_icon.bmp");

    glutCreateWindow("MakeHuman")
    glutSetKeyRepeat(GLUT_KEY_REPEAT_DEFAULT)

    glutKeyboardFunc(keyDownFunc)
    glutKeyboardUpFunc(keyUpFunc)
    glutSpecialFunc(specialDownFunc)
    glutSpecialUpFunc(specialUpFunc)
    glutMotionFunc(mouseMotionActiveFunc)
    glutPassiveMotionFunc(mouseMotionPassiveFunc)
    glutMouseFunc(mouseButtonFunc)
    glutDisplayFunc(drawFunc)
    glutReshapeFunc(reshapeFunc)
    glutIdleFunc(idleFunc)

    # if bool(glutCloseFunc):
    if HAVE_FREEGLUT:
        glutCloseFunc(quit)
    else:
        atexit.register(quit)
    atexit.register(quit)

    OnInit()

def eventLoop():
    glutMainLoop()
    OnExit()

class Timer(object):
    timers = {}
    nextid = 0

    def __init__(self, id, interval, callback):
        self.id = id
        self.interval = interval
        self.callback = callback

    @staticmethod
    def timerCallback(id):
        self = Timer.timers.get(id)
        if self is None:
            return
        callAsync(self.callback)
        glutTimerFunc(self.interval, self.timerCallback, self.id)

    @classmethod
    def new(cls, milliseconds, callback):
        cls.nextid += 1
        t = cls(cls.nextid, milliseconds, callback)
        cls.timers[t.id] = t
        glutTimerFunc(t.interval, cls.timerCallback, t.id)
        return t.id

    @classmethod
    def remove(cls, id):
        if t.id in cls.timers:
            del cls.timers[t.id]

def addTimer(milliseconds, callback):
    return Timer.new(milliseconds, callback)

def removeTimer(id):
    Timer.remove(id)

class Async(object):
    queue = []

    @classmethod
    def add(cls, callback):
        cls.queue.append(callback)
        glutIdleFunc(idleFunc)

    @classmethod
    def process(cls):
        queue = cls.queue
        cls.queue = []
        for callback in queue:
            # print 'async callback: %r' % callback
            callback()

def callAsync(callback):
    Async.add(callback)

import sys
import atexit

import wx
import wx.glcanvas as gl

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
    sys.exit()

def queueUpdate():
    g_app.mainwin.Refresh()

def setFullscreen(fullscreen):
    pass

def setCaption(caption):
    g_app.mainwin.SetTitle(caption)

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
    state = wx.GetMouseState()
    mod = 0
    if state.AltDown():
        mod |= KMOD_LALT
    if state.ControlDown():
        mod |= KMOD_LCTRL
    if state.ShiftDown():
        mod |= KMOD_LSHIFT
    if state.MetaDown():
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
    wx.WXK_F1:        SDLK_F1,
    wx.WXK_F2:        SDLK_F2,
    wx.WXK_F3:        SDLK_F3,
    wx.WXK_F4:        SDLK_F4,
    wx.WXK_F5:        SDLK_F5,
    wx.WXK_F6:        SDLK_F6,
    wx.WXK_F7:        SDLK_F7,
    wx.WXK_F8:        SDLK_F8,
    wx.WXK_F9:        SDLK_F9,
    wx.WXK_F10:       SDLK_F10,
    wx.WXK_F11:       SDLK_F11,
    wx.WXK_F12:       SDLK_F12,
    wx.WXK_LEFT:      SDLK_LEFT,
    wx.WXK_UP:        SDLK_UP,
    wx.WXK_RIGHT:     SDLK_RIGHT,
    wx.WXK_DOWN:      SDLK_DOWN,
    wx.WXK_PAGEUP:    SDLK_PAGEUP,
    wx.WXK_PAGEDOWN:  SDLK_PAGEDOWN,
    wx.WXK_PRIOR:     SDLK_PAGEUP,
    wx.WXK_NEXT:      SDLK_PAGEDOWN,
    wx.WXK_HOME:      SDLK_HOME,
    wx.WXK_END:       SDLK_END,
    wx.WXK_INSERT:    SDLK_INSERT
    }

SDL_BUTTON_LEFT = 1
SDL_BUTTON_MIDDLE = 2
SDL_BUTTON_RIGHT = 3

SDL_BUTTON_LEFT_MASK = 1
SDL_BUTTON_MIDDLE_MASK = 2
SDL_BUTTON_RIGHT_MASK = 4

button_mapping = {
    wx.MOUSE_BTN_LEFT: (SDL_BUTTON_LEFT, SDL_BUTTON_LEFT_MASK),
    wx.MOUSE_BTN_MIDDLE: (SDL_BUTTON_MIDDLE, SDL_BUTTON_MIDDLE_MASK),
    wx.MOUSE_BTN_RIGHT: (SDL_BUTTON_RIGHT, SDL_BUTTON_RIGHT_MASK)
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

        mouse_state = wx.GetMouseState()
        buttons = 0
        if mouse_state.LeftDown():
            buttons |= SDL_BUTTON_LEFT_MASK
        if mouse_state.MiddleDown():
            buttons |= SDL_BUTTON_MIDDLE_MASK
        if mouse_state.RightDown():
            buttons |= SDL_BUTTON_RIGHT_MASK

        mouseMotion(buttons, x, y, xrel, yrel)

class Canvas(gl.GLCanvas):
    _attribs = [gl.WX_GL_RGBA, gl.WX_GL_DOUBLEBUFFER, gl.WX_GL_DEPTH_SIZE, 24]

    def __init__(self, parent):
        super(Canvas, self).__init__(
            parent,
            style = wx.WANTS_CHARS | wx.FULL_REPAINT_ON_RESIZE,
            attribList = self._attribs)
	self.Create()

    def Create(self):
	self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase)
	self.Bind(wx.EVT_PAINT, self.draw)
        self.Bind(wx.EVT_LEFT_DOWN, self.mouse)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.mouse)
        self.Bind(wx.EVT_RIGHT_DOWN, self.mouse)
        self.Bind(wx.EVT_LEFT_UP, self.mouse)
        self.Bind(wx.EVT_MIDDLE_UP, self.mouse)
        self.Bind(wx.EVT_RIGHT_UP, self.mouse)
        self.Bind(wx.EVT_MOTION, self.motion)
        self.Bind(wx.EVT_CHAR, self.char)
        self.Bind(wx.EVT_KEY_DOWN, self.key)
        self.Bind(wx.EVT_KEY_UP, self.key)
        self.Bind(wx.EVT_SIZE, self.resize)
        self.Bind(wx.EVT_IDLE, self.idle)
        self.Bind(wx.EVT_TIMER, self.timer)
        G.swapBuffers = self.SwapBuffers
        self.SetFocus()

    def erase(self, ev):
        if ev.GetDC() is None:
            wx.ClientDC(self)

    def mouse(self, ev):
        x = ev.GetX()
        y = ev.GetY()

        G.mouse_pos = x, y

        b = ev.GetButton() - 1
        b, mask = button_mapping.get(b, (b+1,1<<b))
        if ev.ButtonDown():
            mouseButtonDown(b, x, y)
        else:
            mouseButtonUp(b, x, y)

    def motion(self, ev):
        global g_mouse_pos

        x = ev.GetX()
        y = ev.GetY()

        if G.mouse_pos is None:
            G.mouse_pos = x, y

        g_mouse_pos = (x, y)

    def char(self, ev):
        key = ev.GetKeyCode()
        character = ev.GetUniChar()
        keyDown(key, character, getKeyModifiers())

    def key(self, ev):
        key = ev.GetKeyCode()
        character = ev.GetUniChar()
        etype = ev.GetEventType()

        if key in key_mapping:
            key = key_mapping[key]
        elif etype == wx.wxEVT_KEY_DOWN:
            ev.Skip()
            return

        if etype == wx.wxEVT_KEY_DOWN:
            keyDown(key, character, getKeyModifiers())
        else:
            keyUp(key, character, getKeyModifiers())

    def draw(self, ev):
	dc = wx.PaintDC(self)
        self.SetCurrent()
        draw()

    def resize(self, ev):
        size = ev.GetSize()
        w, h = size.Get()
        self.SetCurrent()
        reshape(w, h)

    def idle(self, ev):
        handleMouse()

    def timer(self, ev):
        handleTimer(ev.id)

class Frame(wx.Frame):
    title = "MakeHuman"

    def __init__(self, app, size):
	self.app = app
	wx.Frame.__init__(self, None, title = Frame.title, size = size)
        self.canvas = Canvas(self)
        self.Bind(wx.EVT_ACTIVATE, self.activate)
        self.Bind(wx.EVT_CLOSE, self.close)

    def activate(self, ev):
        self.canvas.SetFocus()
        ev.Skip()

    def close(self, ev):
        if ev.CanVeto():
            ev.Veto()
            quit()
        else:
            self.Destroy()

class Application(wx.App):
    def OnInit(self):
	size = wx.Size(G.windowWidth, G.windowHeight)
	self.mainwin = Frame(self, size)
	self.mainwin.Show()
	self.SetTopWindow(self.mainwin)
	return True

g_app = None

def createWindow(useTimer = None):
    global g_app
    g_app = Application()
    OnInit()

def eventLoop():
    g_app.MainLoop()
    OnExit()

g_timers = {}
g_timer_id = 0

def addTimer(milliseconds, callback):
    id = g_timer_id
    g_timer_id += 1
    timer = wx.Timer(g_app.mainwin.canvas, g_timer_id)
    g_timers[g_timer_id] = (timer, callback)
    timer.start(milliseconds, False)
    return g_timer_id

def removeTimer(id):
    timer, _ = g_timers[id]
    timer.Stop()
    del g_timers[id]

def handleTimer(id):
    if id not in g_timers:
        return
    timer, callback = g_timers[id]
    callback()

def callAsync(callback):
    wx.CallAfter(callback)

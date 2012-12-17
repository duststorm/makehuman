import traceback
import profiler

class Globals(object):
    def __init__(self):
        self.world = []
        self.cameras = []
        self.windowHeight = 600
        self.windowWidth = 800
        self.color_picked = (0, 0, 0)
        self.millisecTimer = False
        self.pendingUpdate = False
        self.pendingTimer = False
        self.loop = True
        self.fullscreen = False
        self.clearColor = (0.0, 0.0, 0.0, 0.0)
        self.mouse_pos = None

        self.swapBuffers = None
        self.resizeCallback = None
        self.mouseDownCallback = None
        self.mouseUpCallback = None
        self.mouseWheelCallback = None
        self.mouseMovedCallback = None
        self.keyDownCallback = None
        self.keyUpCallback = None
        self.quitCallback = None

        self.profile = False

G = Globals()

def callMouseButtonDown(b, x, y):
    profiler.flush()
    if G.mouseDownCallback:
        if G.profile:
            profiler.run('G.mouseDownCallback(b, x, y)', globals(), locals())
        else:
            G.mouseDownCallback(b, x, y)

def callMouseButtonUp(b, x, y):
    profiler.flush()
    if G.mouseUpCallback:
        if G.profile:
            profiler.run('G.mouseUpCallback(b, x, y)', globals(), locals())
        else:
            G.mouseUpCallback(b, x, y)

def callMouseWheel(b, x, y):
    profiler.flush()
    if G.mouseWheelCallback:
        if G.profile:
            profiler.run('G.mouseWheelCallback(b, x, y)', globals(), locals())
        else:
            G.mouseWheelCallback(b, x, y)

def callMouseMotion(s, x, y, xrel, yrel):
    if G.mouseMovedCallback:
        if G.profile:
            profiler.accum('G.mouseMovedCallback(s, x, y, xrel, yrel)', globals(), locals())
        else:
            G.mouseMovedCallback(s, x, y, xrel, yrel)

def callKeyDown(key, character, modifiers):
    if G.keyDownCallback:
        G.keyDownCallback(key, character, modifiers)

def callKeyUp(key, character, modifiers):
    if G.keyUpCallback:
        G.keyUpCallback(key, character, modifiers)

def callResize(w, h, fullscreen):
    if G.resizeCallback:
        try:
            G.resizeCallback(w, h, fullscreen)
        except StandardError, e:
            traceback.print_exc()

def callQuit():
    if G.quitCallback:
        G.quitCallback()

def setClearColor(r, g, b, a):
    G.clearColor = (r, g, b, a)

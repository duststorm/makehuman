import traceback
import profiler

class Globals(object):
    def __init__(self):
        self.app = None
        self.world = []
        self.cameras = []
        self.windowHeight = 600
        self.windowWidth = 800
        self.color_picked = (0, 0, 0)
        self.clearColor = (0.0, 0.0, 0.0, 0.0)
        self.swapBuffers = None
        self.profile = False

G = Globals()

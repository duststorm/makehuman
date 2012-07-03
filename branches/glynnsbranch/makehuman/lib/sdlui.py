
import sys
import atexit

from sdl import *
from core import *
from glmodule import updatePickingBuffer, getPickedColor, OnInit, OnExit, reshape, draw
from ctypes import *

g_savedx = 0 # saved x mouse position
g_savedy = 0 # saved y mouse position
g_desktopWidth = 0
g_desktopHeight = 0
g_windowWidth = 800
g_windowHeight = 600
g_screen = None # SDL_Surface *

def keyDown(key, character, modifiers):
    if sys.platform == 'win32':
        callKeyDown(key, unichr(character), modifiers)
    else:
        callKeyDown(key, chr(key if key < 256 else 0), modifiers)

def keyUp(key, character, modifiers):
    if sys.platform == 'win32':
        callKeyUp(key, unichr(character), modifiers)
    else:
        callKeyUp(key, chr(key if key < 256 else 0), modifiers)
    updatePickingBuffer()

def timerFunc(interval, param):
    """
    \brief Pass a timer callback event up to Python.
    \param interval an unsigned int, not used here.
    \param param a pointer, not used here.

    If the useTimer parameter is set when mhCreateWindow is called during the MakeHuman
    initiation sequence then this function is registered as the SDL timer event handler.

    This function processes timer events. It creates a new event that it pushes into the
    event queue, it resets the timer and returns. This timer function is called in a
    separate thread, but the newly registered event is handled by the standard thread
    in mhEventLoop, where it calls callTimerFunct, which calls mainScene.timerFunc in
    the Python module.

    Any Python functions registered to use this event perform their tasks before
    returning control to the event loop.

    """
    event = SDL_Event()

    event.type = SDL_USEREVENT
    event.user.code = 0
    event.user.data1 = param
    event.user.data2 = None

    SDL_PushEvent(byref(event))

    # reset the timer to recall the function again, after interval milliseconds
    return interval

def mouseButtonDown(b, x, y):
    """
    \brief Pass a mouse button down event up to Python.
    \param b an int indicating which button this event relates to.
    \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
    \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).

    This function processes mouse clicks (mouse button down events).
    This function writes the current mouse position and keyboard modifier
    states (Shift, Ctl etc.) into globals.
    Then it calls one of a set of mouse click event handling functions that
    will be bubbled up to the corresponding Python event handler.

    The Python Scene3D object holds separate attributes
    (sceneLMousePressedCallBack and
    sceneRMousePressedCallBack) to point to the
    different mouse button event handling functions.
    """

    # Since the mouse cursor doesn't move when a button is down, we
    # save the mouse position and restore it later to avoid jumping.
    # We also grab the input so we can move the (invisible) mouse outside the screen.
    
    g_savedx=x
    g_savedy=y
    if sys.platform == 'win32':
        SDL_WM_GrabInput(SDL_GRAB_ON)

    # Check which object/group was hit
    if b != 4 and b != 5:
        getPickedColor(x, y)

    # Notify python
    callMouseButtonDown(b, x, y)

    # Update screen
    queueUpdate()

    if b != 4 and b != 5:
        updatePickingBuffer()

def mouseButtonUp(b, x, y):
    """
    \brief Pass a mouse button up event up to Python.
    \param b an int indicating which button this event relates to.
    \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
    \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).

    This function processes mouse clicks (mouse button up events).
    This function writes the current mouse position and keyboard modifier
    states (Shift, Ctl etc.) into globals.
    Then it calls one of a set of mouse click event handling functions that
    will be bubbled up to the corresponding Python event handler.

    The Python Scene3D object holds separate attributes
    (sceneLMouseReleasedCallBack and
    sceneRMouseReleasedCallBack) to point to the
    different mouse button event handling functions.
    """

    # Since the mouse cursor doesn't move when a button is down, we
    # save the mouse position and restore it later to avoid jumping.
    # We also ungrab the previously grabbed input

    if sys.platform == 'win32':
        SDL_WM_GrabInput(SDL_GRAB_OFF)

    # Check which object/group was hit
    if b != 4 and b != 5:
        getPickedColor(x, y)

    # Notify python
    callMouseButtonUp(b, x, y)

    # Update screen
    queueUpdate()

    updatePickingBuffer()

def mouseMotion(s, x, y, xrel, yrel):
    """
    \brief Pass a mouse motion event up to Python and adjust current camera view.
    \param s an int indicating the mouse.motion.state of the event (1=Mouse moved, 0=Mouse click).
    \param x an int specifying the horizontal mouse pointer position in the GUI window (in pixels).
    \param y an int specifying the vertical mouse pointer position in the GUI window (in pixels).
    \param xrel an int specifying the difference between the previously recorded horizontal mouse
           pointer position in the GUI window and the current position (in pixels).
    \param yrel an int specifying the difference between the previously recorded vertical mouse
           pointer position in the GUI window and the current position (in pixels).

    This function processes mouse movement events, calling a corresponding Python event handler.

    This function writes the difference between the last recorded mouse position and the current
    mouse position, along with the current mouse position and keyboard modifier states
    (Shift, Ctl etc.) into globals.
    Then it calls a mouse click motion handling function that will be bubbled up to
    the Python function assigned to the sceneMouseMotionCallback attribute
    on the Scene3D object. That function processes the event and control is
    returned to the event loop to await the next event.
    """

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
    G.loop = 0

def queueUpdate():
    """
    \brief Queue an update.

    This function places an update event into the event queue if there
    isn't one pending already. This makes sure we don't create a "traffic
    jam" in the event queue when the system is slow in redrawing
    """

    if G.pendingUpdate:
        return

    G.pendingUpdate = 1

    ev = SDL_Event()
    ev.type = SDL_VIDEOEXPOSE
    SDL_PushEvent(byref(ev))

def setFullscreen(fullscreen):
    """
    \brief Set fullscreen mode.
    \param fullscreen an int indicating whether to use a window or full screen mode.

    This function controls whether the MakeHuman GUI is displayed in a window
    or in full screen mode:
      0 for windowed
      1 for fullscreen
    """

    if G.fullscreen == fullscreen:
        return

    G.fullscreen = fullscreen

    if fullscreen:
        G.windowWidth  = g_desktopWidth
        G.windowHeight = g_desktopHeight
    else:
        G.windowWidth  = g_windowWidth
        G.windowHeight = g_windowHeight

    if not g_screen:
        return

    g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (SDL_FULLSCREEN if G.fullscreen else 0) | SDL_RESIZABLE)
    OnInit()
    reshape(G.windowWidth, G.windowHeight)
    callResize(G.windowWidth, G.windowHeight, G.fullscreen)
    draw()

def setCaption(caption):
    SDL_WM_SetCaption(caption, caption)

def createWindow(useTimer):
    """
    \brief Create SDL window.
    \param useTimer an int controlling whether timer based processing is to be used (1=yes, 0=no).

    This function implements one of the first parts of the MakeHuman initiation sequence.
    It sets up the environment that the SDL module will use to manage the GUI window.
    """

    atexit.register(SDL_Quit)

    if SDL_Init(SDL_INIT_VIDEO) < 0:
        printf("Unable to init SDL: %s" % SDL_GetError())
        sys.exit(1)

    SDL_GL_SetAttribute(SDL_GL_RED_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_GREEN_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_BLUE_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)

    #if defined(SDL_GL_SWAP_CONTROL) #  SDL_GL_SWAP_CONTROL is deprecated in SDL 1.3! 
    #SDL_GL_SetAttribute(SDL_GL_SWAP_CONTROL, 1) # This fixes flickering in compiz
    #endif

    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 4)

    info = SDL_GetVideoInfo()
    g_desktopWidth = info.contents.current_w
    g_desktopHeight = info.contents.current_h

    # Load and set window icon
    image = SDL_LoadBMP("mh_icon.bmp")
    if image:
        colorkey = SDL_MapRGB(image.contents.format, 255, 255, 255)
        SDL_SetColorKey(image, SDL_SRCCOLORKEY, colorkey)
        SDL_WM_SetIcon(image, None)

    if G.fullscreen:
        G.windowWidth = g_desktopWidth
        G.windowHeight = g_desktopHeight
    else:
        G.windowWidth = g_windowWidth
        G.windowHeight = g_windowHeight

    g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (SDL_FULLSCREEN if G.fullscreen else 0) | SDL_RESIZABLE)
    if not g_screen:
        print("No antialiasing available, turning off antialiasing.")
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 0)
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 0)
        g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (SDL_FULLSCREEN if G.fullscreen else 0) | SDL_RESIZABLE)
        if not g_screen:
            print("No 24 bit z buffer available, switching to 16 bit.")
            SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 16)
            g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (SDL_FULLSCREEN if G.fullscreen else 0) | SDL_RESIZABLE)
            if not g_screen:
                print("No 16 bit z buffer available, exiting.")
                print SDL_GetError()
                print G.windowWidth, G.windowHeight, 24, G.fullscreen, hex(SDL_OPENGL | (SDL_FULLSCREEN if G.fullscreen else 0) | SDL_RESIZABLE)
                sys.exit(1)

    SDL_WM_SetCaption("MakeHuman", "")
    SDL_EnableKeyRepeat(SDL_DEFAULT_REPEAT_DELAY, SDL_DEFAULT_REPEAT_INTERVAL)

    if sys.platform == 'win32':
        SDL_EnableUNICODE(1)

    if useTimer:
        SDL_InitSubSystem(SDL_INIT_TIMER)

    G.swapBuffers = SDL_GL_SwapBuffers

    OnInit()
    reshape(G.windowWidth, G.windowHeight)
    draw()

def eventLoop():
    """
    \brief Start the event loop to manage the MakeHuman GUI.

    This function implements the event loop which manages all user interaction,
    determining which functions to call to handle events etc.
    """

    # SDL_ShowCursor(SDL_DISABLE)

    while G.loop:
        event = SDL_Event()

        SDL_WaitEvent(byref(event))

        # On OS-X SDL continuously posts events even when a native dialog or
        # Window is opened. So if the ActiveWindow (focused Window) is not
        # the main window then cancel the SDL Event.

        if event.type == SDL_ACTIVEEVENT:
            if event.active.state & SDL_APPINPUTFOCUS:
                if event.active.gain:
                    # SDL_ShowCursor(SDL_DISABLE)
                    pass
                else:
                    # SDL_ShowCursor(SDL_ENABLE)
                    if sys.platform == 'win32':
                        SDL_WM_GrabInput(SDL_GRAB_OFF)

        elif event.type == SDL_KEYDOWN:
            keyDown(event.key.keysym.sym, event.key.keysym.unicode, event.key.keysym.mod)

        elif event.type == SDL_KEYUP:
            if event.key.keysym.sym == SDLK_F11 or (event.key.keysym.sym == SDLK_RETURN and event.key.keysym.mod & KMOD_ALT):
                setFullscreen(G.fullscreen) # Switch fullscreen
            else:
                keyUp(event.key.keysym.sym, event.key.keysym.unicode, event.key.keysym.mod)

        elif event.type == SDL_MOUSEMOTION:
            if True: # sys.platform in ('win32', 'darwin'):
                mouseMotion(event.motion.state, event.motion.x, event.motion.y, event.motion.xrel, event.motion.yrel)
            else:
                x = c_int()
                y = c_int()
                SDL_GetMouseState(byref(x), byref(y))
                if x.value == event.motion.x and y.value == event.motion.y:
                    mouseMotion(event.motion.state, event.motion.x, event.motion.y, event.motion.xrel, event.motion.yrel)

        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouseButtonDown(event.button.button, event.button.x, event.button.y)

        elif event.type == SDL_MOUSEBUTTONUP:
            mouseButtonUp(event.button.button, event.button.x, event.button.y)

        elif event.type == SDL_USEREVENT:
            cast(event.user.data1, CFUNCTYPE(None))()

        elif event.type == SDL_VIDEORESIZE:
            G.windowWidth = g_windowWidth = event.resize.w
            G.windowHeight = g_windowHeight = event.resize.h
            g_screen = SDL_SetVideoMode(G.windowWidth, G.windowHeight, 24, SDL_OPENGL | (SDL_FULLSCREEN if G.fullscreen else 0) | SDL_RESIZABLE)
            OnInit()

            #  hdusel: On some systems a SDL_SetVideoMode causes that the OpenGL context will be reinitialzed.
            # (see http://forums.libsdl.org/viewtopic.php?t=5503&sid=bb2bd59aff7710bbb3dc3ecd5e9b79cf)
            # This leads not only to loose the OpenGL Context which will be resumed by OnInit() but in
            # a lost of all loaded textures also.
            # 
            # OS X is concerned of this phenomen :-/ So we'll need to restore all loaded textures after
            # SDL_SetVideoMode() has been called. The Restore of the textures needs some additional effort
            # which is actually done in a texture cache which is relized as a C++ class within the os-x code
            # folder. If any other platform has problems to restore its textures because of an OpenGL context
            # loss caused of SDL_SetVideoMode() we should consider to move this Cache to the common code
            # area.
            # 
            # This issue fixes the ticket "Issue 118: Interface is not redrawn when the window is maximized on OSX"
            # (http://code.google.com/p/makehuman/issues/detail?id=118).

            if sys.platform == 'darwin':
                textureCacheRestoreTextures()

            reshape(event.resize.w, event.resize.h)
            callResize(event.resize.w, event.resize.h, G.fullscreen)
            draw()

        elif event.type == SDL_VIDEOEXPOSE:
            draw()
            G.pendingUpdate = 0

        elif event.type == SDL_QUIT:
            quit()

    OnExit()

_timers = {}

def addTimer(milliseconds, callback):
    callback = SDL_NewTimerCallback(callback)
    id = SDL_AddTimer(milliseconds, cb, "")
    _timers[id] = callback
    return id

def removeTimer(id):
    del _timers[id]
    return SDL_RemoveTimer(id)

_callbacks = {}

def callAsync(callback):
    if callback not in _callbacks:
        _callbacks[callback] = CFUNCTYPE(None)(callback)
    callback = _callbacks[callback]

    event = SDL_Event()

    event.type = SDL_USEREVENT
    event.user.code = 1
    event.user.data1 = cast(callback, c_void_p)
    event.user.data2 = c_void_p(0)

    SDL_PushEvent(byref(event))

def getKeyModifiers():
    return SDL_GetModState()

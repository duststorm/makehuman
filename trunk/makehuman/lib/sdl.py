import sys
from ctypes import *

if sys.platform == 'win32':
    try:
        _sdl = cdll.SDL
    except:
        _sdl = CDLL('bin/win/SDL.dll')
elif sys.platform == 'darwin':
    _sdl = CDLL('/opt/local/lib/libSDL.dylib')
else:
    _sdl = CDLL('libSDL.so')

### Constants

SDL_INIT_TIMER		= 0x00000001
SDL_INIT_AUDIO		= 0x00000010
SDL_INIT_VIDEO		= 0x00000020
SDL_INIT_CDROM		= 0x00000100
SDL_INIT_JOYSTICK	= 0x00000200
SDL_INIT_NOPARACHUTE	= 0x00100000
SDL_INIT_EVENTTHREAD	= 0x01000000
SDL_INIT_EVERYTHING	= 0x0000FFFF

SDL_APPMOUSEFOCUS	= 0x01
SDL_APPINPUTFOCUS	= 0x02
SDL_APPACTIVE		= 0x04

SDL_ANYFORMAT		= 0x10000000
SDL_HWPALETTE		= 0x20000000
SDL_DOUBLEBUF		= 0x40000000
SDL_FULLSCREEN		= 0x80000000
SDL_OPENGL      	= 0x00000002
SDL_OPENGLBLIT		= 0x0000000A
SDL_RESIZABLE		= 0x00000010
SDL_NOFRAME		= 0x00000020

SDL_HWACCEL		= 0x00000100
SDL_SRCCOLORKEY		= 0x00001000
SDL_RLEACCELOK		= 0x00002000
SDL_RLEACCEL		= 0x00004000
SDL_SRCALPHA		= 0x00010000
SDL_PREALLOC		= 0x01000000

SDL_SWSURFACE		= 0x00000000
SDL_HWSURFACE		= 0x00000001
SDL_ASYNCBLIT		= 0x00000004

SDL_QUERY		= -1
SDL_IGNORE		= 0
SDL_DISABLE		= 0
SDL_ENABLE		= 1

SDL_DEFAULT_REPEAT_DELAY	= 500
SDL_DEFAULT_REPEAT_INTERVAL	= 30

### Enumerations

# SDL_GrabMode
SDL_GrabMode = c_int

SDL_GRAB_QUERY		= -1
SDL_GRAB_OFF		= 0
SDL_GRAB_ON		= 1
SDL_GRAB_FULLSCREEN	= 2

# SDL_EventType
SDL_EventType = c_int

SDL_NOEVENT		= 0
SDL_ACTIVEEVENT		= 1
SDL_KEYDOWN		= 2
SDL_KEYUP		= 3
SDL_MOUSEMOTION		= 4
SDL_MOUSEBUTTONDOWN	= 5
SDL_MOUSEBUTTONUP	= 6
SDL_JOYAXISMOTION	= 7
SDL_JOYBALLMOTION	= 8
SDL_JOYHATMOTION	= 9
SDL_JOYBUTTONDOWN	= 10
SDL_JOYBUTTONUP		= 11
SDL_QUIT		= 12
SDL_SYSWMEVENT		= 13
SDL_EVENT_RESERVEDA	= 14
SDL_EVENT_RESERVEDB	= 15
SDL_VIDEORESIZE		= 16
SDL_VIDEOEXPOSE		= 17
SDL_EVENT_RESERVED2	= 18
SDL_EVENT_RESERVED3	= 19
SDL_EVENT_RESERVED4	= 20
SDL_EVENT_RESERVED5	= 21
SDL_EVENT_RESERVED6	= 22
SDL_EVENT_RESERVED7	= 23
SDL_USEREVENT		= 24

# SDL_GLattr
SDL_GLattr = c_int

SDL_GL_RED_SIZE			= 0
SDL_GL_GREEN_SIZE		= 1
SDL_GL_BLUE_SIZE		= 2
SDL_GL_ALPHA_SIZE		= 3
SDL_GL_BUFFER_SIZE		= 4
SDL_GL_DOUBLEBUFFER		= 5
SDL_GL_DEPTH_SIZE		= 6
SDL_GL_STENCIL_SIZE		= 7
SDL_GL_ACCUM_RED_SIZE		= 8
SDL_GL_ACCUM_GREEN_SIZE		= 9
SDL_GL_ACCUM_BLUE_SIZE		= 10
SDL_GL_ACCUM_ALPHA_SIZE		= 11
SDL_GL_STEREO			= 12
SDL_GL_MULTISAMPLEBUFFERS	= 13
SDL_GL_MULTISAMPLESAMPLES	= 14
SDL_GL_ACCELERATED_VISUAL	= 15
SDL_GL_SWAP_CONTROL		= 16

# SDLMod
SDLMod = c_int

KMOD_NONE	= 0x0000
KMOD_LSHIFT	= 0x0001
KMOD_RSHIFT	= 0x0002
KMOD_LCTRL	= 0x0040
KMOD_RCTRL	= 0x0080
KMOD_LALT	= 0x0100
KMOD_RALT	= 0x0200
KMOD_LMETA	= 0x0400
KMOD_RMETA	= 0x0800
KMOD_NUM	= 0x1000
KMOD_CAPS	= 0x2000
KMOD_MODE	= 0x4000
KMOD_RESERVED	= 0x8000

KMOD_CTRL	= KMOD_LCTRL  | KMOD_RCTRL
KMOD_SHIFT	= KMOD_LSHIFT | KMOD_RSHIFT
KMOD_ALT	= KMOD_LALT   | KMOD_RALT
KMOD_META	= KMOD_LMETA  | KMOD_RMETA

# SDLKey
SDLKey = c_int

SDLK_RETURN	= 13
SDLK_F11	= 292

# Simple types

# SDL_TimerID
SDL_TimerID = c_void_p

# SDL_NewTimerCallback
# typedef Uint32 (SDLCALL *SDL_NewTimerCallback)(Uint32 interval, void *param);
SDL_NewTimerCallback = CFUNCTYPE(c_uint, c_uint, c_void_p)

# SDL_bool
def SDL_bool(x):
    return bool(x)

### Structure and union types

class SDL_PixelFormat(Structure):
    _fields_ = [
	('palette',	c_void_p),
	('BitsPerPixel',c_ubyte),
	('BytesPerPixel',c_ubyte),
	('Rloss',	c_ubyte),
	('Gloss',	c_ubyte),
	('Bloss',	c_ubyte),
	('Aloss',	c_ubyte),
	('Rshift',	c_ubyte),
	('Gshift',	c_ubyte),
	('Bshift',	c_ubyte),
	('Ashift',	c_ubyte),
	('Rmask',	c_uint),
	('Gmask',	c_uint),
	('Bmask',	c_uint),
	('Amask',	c_uint),
	('colorkey',	c_uint),
	('alpha',	c_ubyte)
        ]

class SDL_Rect(Structure):
    _fields_ = [
        ('x',		c_short),
        ('y',		c_short),
        ('w',		c_ushort),
        ('h',		c_ushort)
        ]

class SDL_Surface(Structure):
    _fields_ = [
	('flags',	c_uint),
	('format',	POINTER(SDL_PixelFormat)),
	('w',		c_int),
	('h',		c_int),
	('pitch',	c_ushort),
	('pixels',	c_void_p),
	('offset',	c_int),
	('hwdata',	c_void_p),
	('clip_rect',	SDL_Rect),
	('unused1',	c_uint),
	('locked',	c_uint),
	('map',		c_void_p),
	('format_version',c_uint),
	('refcount',	c_int)
        ]

class SDL_VideoInfo(Structure):
    _fields_ = [
        ('flags',	c_uint),
        ('video_mem',	c_uint),
	('vfmt',	POINTER(SDL_PixelFormat)),
	('current_w',	c_int),
	('current_h',	c_int)
        ]

class SDL_keysym(Structure):
    _fields_ = [
	('scancode',	c_ubyte),
	('sym',		SDLKey),
	('mod',		SDLMod),
	('unicode',	c_ushort)
        ]

class SDL_ActiveEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('gain',        c_ubyte),
        ('state',       c_ubyte)
        ]

class SDL_KeyboardEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('which',       c_ubyte),
        ('state',       c_ubyte),
        ('keysym',      SDL_keysym)
        ]

class SDL_MouseMotionEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('which',       c_ubyte),
        ('state',       c_ubyte),
        ('x',           c_ushort),
        ('y',           c_ushort),
        ('xrel',        c_short),
        ('yrel',        c_short)
        ]

class SDL_MouseButtonEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('which',       c_ubyte),
        ('button',      c_ubyte),
        ('state',       c_ubyte),
        ('x',           c_ushort),
        ('y',           c_ushort)
        ]

class SDL_JoyAxisEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('which',       c_ubyte),
        ('axis',        c_ubyte),
        ('value',       c_short)
        ]

class SDL_JoyBallEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('which',       c_ubyte),
        ('ball',        c_ubyte),
        ('xrel',        c_short),
        ('yrel',        c_short)
        ]

class SDL_JoyHatEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('which',       c_ubyte),
        ('hat',         c_ubyte),
        ('value',       c_ubyte)
        ]

class SDL_JoyButtonEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('which',       c_ubyte),
        ('button',      c_ubyte),
        ('state',       c_ubyte)
        ]

class SDL_ResizeEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('w',           c_int),
        ('h',           c_int)
        ]

class SDL_ExposeEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte)
        ]

class SDL_QuitEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte)
        ]

class SDL_UserEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('code',        c_int),
        ('data1',       c_void_p),
        ('data2',       c_void_p)
        ]

class SDL_SysWMEvent(Structure):
    _fields_ = [
        ('type',        c_ubyte),
        ('msg',         c_void_p)
        ]

class SDL_Event(Union):
    _fields_ = [
	('type',	c_ubyte),
	('active',	SDL_ActiveEvent),
	('key',		SDL_KeyboardEvent),
	('motion',	SDL_MouseMotionEvent),
	('button',	SDL_MouseButtonEvent),
	('jaxis',	SDL_JoyAxisEvent),
	('jball',	SDL_JoyBallEvent),
	('jhat',	SDL_JoyHatEvent),
	('jbutton',	SDL_JoyButtonEvent),
	('resize',	SDL_ResizeEvent),
	('expose',	SDL_ExposeEvent),
	('quit',	SDL_QuitEvent),
	('user',	SDL_UserEvent),
	('syswm',	SDL_SysWMEvent)
        ]

### Functions

# int SDL_EnableKeyRepeat(int delay, int interval);
SDL_EnableKeyRepeat = _sdl.SDL_EnableKeyRepeat
SDL_EnableKeyRepeat.argtypes = [c_int, c_int]
SDL_EnableKeyRepeat.restype = c_int

# int SDL_EnableUNICODE(int enable);
SDL_EnableUNICODE = _sdl.SDL_EnableUNICODE
SDL_EnableUNICODE.argtypes = [c_int]
SDL_EnableUNICODE.restype = c_int

# SDLMod SDL_GetModState(void);
SDL_GetModState = _sdl.SDL_GetModState
SDL_GetModState.argtypes = []
SDL_GetModState.restype = SDLMod

# Uint8 SDL_GetMouseState(int *x, int *y);
SDL_GetMouseState = _sdl.SDL_GetMouseState
SDL_GetMouseState.argtypes = [POINTER(c_int), POINTER(c_int)]
SDL_GetMouseState.restype = c_ubyte

# int SDL_ShowCursor(int toggle);
SDL_ShowCursor = _sdl.SDL_ShowCursor
SDL_ShowCursor.argtypes = [c_int]
SDL_ShowCursor.restyp = c_int

# SDL_GrabMode SDL_WM_GrabInput(SDL_GrabMode mode);
SDL_WM_GrabInput = _sdl.SDL_WM_GrabInput
SDL_WM_GrabInput.argtypes = [SDL_GrabMode]
SDL_WM_GrabInput.restype = SDL_GrabMode

# void SDL_WM_SetCaption(const char *title, const char *icon);
SDL_WM_SetCaption = _sdl.SDL_WM_SetCaption
SDL_WM_SetCaption.argtypes = [c_char_p, c_char_p]
SDL_WM_SetCaption.restype = None

# void SDL_WM_SetIcon(SDL_Surface *icon, Uint8 *mask);
SDL_WM_SetIcon = _sdl.SDL_WM_SetIcon
SDL_WM_SetIcon.argtypes = [POINTER(SDL_Surface), POINTER(c_ubyte)]
SDL_WM_SetIcon.restype = None

# SDL_Surface * SDL_SetVideoMode(int width, int height, int bpp, Uint32 flags);
SDL_SetVideoMode = _sdl.SDL_SetVideoMode
SDL_SetVideoMode.argtypes = [c_int, c_int, c_int, c_uint]
SDL_SetVideoMode.restype = POINTER(SDL_Surface)

# int SDL_SetColorKey(SDL_Surface *surface, Uint32 flag, Uint32 key);
SDL_SetColorKey = _sdl.SDL_SetColorKey
SDL_SetColorKey.argtypes = [POINTER(SDL_Surface), c_uint, c_uint]
SDL_SetColorKey.restype = c_int

# const SDL_VideoInfo * SDL_GetVideoInfo(void);
SDL_GetVideoInfo = _sdl.SDL_GetVideoInfo
SDL_GetVideoInfo.argtypes = []
SDL_GetVideoInfo.restype = POINTER(SDL_VideoInfo)

# Uint32 SDL_MapRGB(const SDL_PixelFormat * const format, const Uint8 r, const Uint8 g, const Uint8 b);
SDL_MapRGB = _sdl.SDL_MapRGB
SDL_MapRGB.argtypes = [POINTER(SDL_PixelFormat), c_ubyte, c_ubyte, c_ubyte]
SDL_MapRGB.restype = c_uint

# int SDL_GL_SetAttribute(SDL_GLattr attr, int value);
SDL_GL_SetAttribute = _sdl.SDL_GL_SetAttribute
SDL_GL_SetAttribute.argtypes = [SDL_GLattr, c_int]
SDL_GL_SetAttribute.restype = c_int

# void SDL_GL_SwapBuffers(void)
SDL_GL_SwapBuffers = _sdl.SDL_GL_SwapBuffers
SDL_GL_SwapBuffers.argtypes = []
SDL_GL_SwapBuffers.restype = None

# SDL_Surface * SDL_LoadBMP_RW(SDL_RWops *src, int freesrc);
SDL_LoadBMP_RW = _sdl.SDL_LoadBMP_RW
SDL_LoadBMP_RW.argtypes = [c_void_p, c_int]
SDL_LoadBMP_RW.restype = POINTER(SDL_Surface)

# SDL_RWops * SDL_RWFromFile(const char *file, const char *mode);
SDL_RWFromFile = _sdl.SDL_RWFromFile
SDL_RWFromFile.argtypes = [c_char_p, c_char_p]
SDL_RWFromFile.restype = c_void_p

# int SDL_PushEvent(SDL_Event *event);
SDL_PushEvent = _sdl.SDL_PushEvent
SDL_PushEvent.argtypes = [POINTER(SDL_Event)]
SDL_PushEvent.restyle = c_int

# int SDL_WaitEvent(SDL_Event *event);
SDL_WaitEvent = _sdl.SDL_WaitEvent
SDL_WaitEvent.argtypes = [POINTER(SDL_Event)]
SDL_WaitEvent.restyle = c_int

# SDL_TimerID SDL_AddTimer(Uint32 interval, SDL_NewTimerCallback callback, void *param);
SDL_AddTimer = _sdl.SDL_AddTimer
SDL_AddTimer.argtypes = [c_uint, SDL_NewTimerCallback, c_void_p]
SDL_AddTimer.restype = SDL_TimerID

# SDL_bool SDL_RemoveTimer(SDL_TimerID t);
SDL_RemoveTimer = _sdl.SDL_RemoveTimer
SDL_RemoveTimer.argtypes = [SDL_TimerID]
SDL_RemoveTimer.restype = SDL_bool

# int SDL_Init(Uint32 flags);
SDL_Init = _sdl.SDL_Init
SDL_Init.argtypes = [c_uint]
SDL_Init.restype = c_int

# int SDL_InitSubSystem(Uint32 flags);
SDL_InitSubSystem = _sdl.SDL_InitSubSystem
SDL_InitSubSystem.argtypes = [c_uint]
SDL_InitSubSystem.restype = c_int

# void SDL_Quit(void);
SDL_Quit = _sdl.SDL_Quit
SDL_Quit.argtypes = []
SDL_Quit.restype = None

# char * SDL_GetError(void);
SDL_GetError = _sdl.SDL_GetError
SDL_GetError.argtypes = []
SDL_GetError.restype = c_char_p

# SDL_Surface* SDL_ConvertSurface(SDL_Surface *src, SDL_PixelFormat *fmt, Uint32 flags);
SDL_ConvertSurface = _sdl.SDL_ConvertSurface
SDL_ConvertSurface.argtypes = [POINTER(SDL_Surface), POINTER(SDL_PixelFormat), c_uint]
SDL_ConvertSurface.restype = POINTER(SDL_Surface)

# void SDL_FreeSurface(SDL_Surface *surface);
SDL_FreeSurface = _sdl.SDL_FreeSurface
SDL_FreeSurface.argtypes = [POINTER(SDL_Surface)]
SDL_FreeSurface.restype = None

# int SDL_LockSurface(SDL_Surface *surface);
SDL_LockSurface = _sdl.SDL_LockSurface
SDL_LockSurface.argtypes = [POINTER(SDL_Surface)]
SDL_LockSurface.restype = c_int

# void SDL_UnlockSurface(SDL_Surface *surface);
SDL_UnlockSurface = _sdl.SDL_UnlockSurface
SDL_UnlockSurface.argtypes = [POINTER(SDL_Surface)]
SDL_UnlockSurface.restype = None

### Macros

def SDL_LoadBMP(file):
    return SDL_LoadBMP_RW(SDL_RWFromFile(file, "rb"), 1)


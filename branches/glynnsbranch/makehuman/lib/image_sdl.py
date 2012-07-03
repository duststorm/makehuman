import sys
from ctypes import *
import numpy as np
from sdl import *

if sys.platform == 'win32':
    try:
        _sdlimg = cdll.SDL_image
    except:
        _sdlimg = CDLL('bin/win/SDL_image.dll')
else:
    _sdlimg = CDLL('libSDL_image.so')

# SDL_Surface * IMG_Load(const char *file);
IMG_Load = _sdlimg.IMG_Load
IMG_Load.argtypes = [c_char_p]
IMG_Load.restype = POINTER(SDL_Surface)

def load(path):
    surface = IMG_Load(path)
    if not cast(surface, c_void_p).value:
        raise RuntimeError("Could not load %s, %s" % (path, SDL_GetError()))

    if SDL_LockSurface(surface) != 0:
        raise RuntimeError("Could not lock surface")

    surf = surface.contents

    d = surf.format.contents.BytesPerPixel
    w = surf.w
    h = surf.h
    pixels = cast(surf.pixels, POINTER(c_char))
    nbytes = w * h * d
    data = np.fromstring(pixels[:nbytes], dtype=np.uint8).reshape((h, w, d))

    SDL_UnlockSurface(surface)
    SDL_FreeSurface(surface)

    return data

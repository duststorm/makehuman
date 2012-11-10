import os
import numpy as np

from core import G
if G.use_wximage:
    import image_wx
elif G.use_pil:
    import image_pil
elif G.use_sdlimage:
    import image_sdl
    import image_bmp
    import image_png
else:
    import image_png
    import image_bmp

_all = ['new', 'open', 'fromstring', 'fromdata']

def new(mode, size):
    return Image(mode, size)

def open(path):
    if G.use_wximage:
        return load_wx(path)
    if G.use_sdlimage:
        return load_sdl(path)
    if G.use_pil:
        return load_pil(path)
    return load_png(path)

def fromstring(mode, size, data):
    im = Image(mode, size)
    im._data = np.fromstring(data, dtype=np.uint8).reshape(im._data.shape)
    return im

def fromdata(data):
    return Image(data = data)

class Image(object):
    def __init__(self, mode = None, size = None, data = None):
        if data is not None:
            self._data = data
        else:
            width, height = size
            components = {'L': 1, 'LA': 2, 'RGB': 3, 'RGBA': 4}[mode]
            self._data = np.empty((height, width, components), dtype=np.uint8)

    @property
    def size(self):
        h, w, c = self._data.shape
        return (w, h)

    @property
    def mode(self):
        h, w, c = self._data.shape
        return {1: 'L', 2: 'LA', 3: 'RGB', 4: 'RGBA'}[c]

    def save(self, path):
        if G.use_wximage:
            image_wx.save(path, self._data)
        elif G.use_pil:
            image_pil.save(path, self._data)
        else:
            base, ext = os.path.splitext(path)
            ext = ext.lower()
            if ext == '.bmp':
                image_bmp.save(path, self._data)
            elif ext == '.png':
                image_png.save(path, self._data)
            else:
                raise NotImplementedError()

    def resize(self, size, filter):
        dw, dh = size
        sh, sw, _ = self._data.shape
        xmap = np.floor((np.arange(dw) + 0.5) * sw / dw).astype(int)
        ymap = np.floor((np.arange(dh) + 0.5) * sh / dh).astype(int)
        return Image(data = self._data[ymap, xmap])

    def getpixel(self, xy):
        x, y = xy
        return self._data[y,x,:]

    def putpixel(self, xy, color):
        x, y = xy
        self._data[y,x,:] = color

    def paste(self, other, xy):
        x, y = xy
        dh, dw, dc = self._data.shape
        sh, sw, sc = other._data.shape
        if sc != dc:
            raise ValueError("source image has incorrect format")
        sw = min(sw, dw - x)
        sh = min(sh, dh - y)
        self._data[y:y+sh,x:x+sw,:] = other._data

    def convert(self, mode):
        if self.mode == mode:
            return self
        other = Image(mode, self.size)
        _, _, sc = self._data.shape
        _, _, dc = other._data.shape
        if sc == 1:
            other._data[...] = self._data
        elif sc == 3 and dc == 4:
            other._data[...,:3] = self._data
            other._data[...,3] = 255
        elif dc == 3:
            other._data[...] = self._data[...,:3]
        elif dc == 1:
            other._data[...] = np.sum(self._data[...,:3], axis=-1) / 3
        else:
            raise RuntimeError()

    def flip_vertical(self):
        other = Image(self.mode, self.size)
        other._data[...] = self._data[::-1,:,:]
        return other

    def flip_horizontal(self):
        other = Image(self.mode, self.size)
        other._data[...] = self._data[:,::-1,:]
        return other

    def data(self):
        self._data = np.ascontiguousarray(self._data)
        return self._data

def load_png(path):
    return Image(data = image_png.load(path))

def load_sdl(path):
    return Image(data = image_sdl.load(path))

def load_wx(path):
    return Image(data = image_wx.load(path))

def load_pil(path):
    return Image(data = image_pil.load(path))


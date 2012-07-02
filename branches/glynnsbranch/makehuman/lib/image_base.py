import os
import struct
from ctypes import *
import numpy as np

from core import G
if G.use_wximage:
    import wx
else:
    try:
        import png
    except StandardError, e:
        print e

_all = ['new', 'open', 'fromstring']

def new(mode, size):
    return Image(mode, size)

def open(path):
    if G.use_wximage:
        return load_wx(path)
    base, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext == '.png':
        return load_png(path)

def fromstring(mode, size, data):
    im = Image(mode, size)
    im._data = np.fromstring(data, dtype=np.uint8).reshape(im._data.shape)
    return im

# resampling filters
NONE = 0
NEAREST = 0
ANTIALIAS = 1 # 3-lobed lanczos
LINEAR = BILINEAR = 2
CUBIC = BICUBIC = 3

# transpose
FLIP_LEFT_RIGHT = 0
FLIP_TOP_BOTTOM = 1
ROTATE_90 = 2
ROTATE_180 = 3
ROTATE_270 = 4

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
        base, ext = os.path.splitext(path)
        ext = ext.lower()
        if G.use_wximage:
            save_wx(path, ext, self._data)
            return
        if ext == '.bmp':
            return save_bmp(path, self._data)
        else:
            raise NotImplementedError()

    def resize(self, size, filter):
        # todo: interpolation methods
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

    def transpose(self, op):
        if op == FLIP_TOP_BOTTOM:
            other = Image(self.mode, self.size)
            other._data[...] = self._data[::-1,:,:]
            return other
        elif op == FLIP_LEFT_RIGHT:
            other = Image(self.mode, self.size)
            other._data[...] = self._data[:,::-1,:]
            return other
        else:
            raise NotImplementedError()

    def tostring(self, fmt, mode):
        if fmt != 'raw':
            raise NotImplementedError()
        im = self.convert(mode)
        return im._data.tostring()

def load_wx(path):
    im = wx.Image(path)
    w, h = im.GetSize().Get()
    data = np.fromstring(im.GetData(), dtype=np.uint8).reshape((h, w, 3))
    dir, file = os.path.split(path)
    base, last = os.path.split(dir)
    if last.lower() == 'fonts' and np.all(data[...,0] == data[...,1]) and np.all(data[...,1] == data[...,2]):
        data = data[...,:1]
    elif im.HasAlpha():
        a = np.fromstring(im.GetAlphaData(), dtype=np.uint8).reshape((h, w, 1))
        data = np.dstack((data, a))
    del im
    return Image(data = data)

def save_wx(path, ext, data):
    _types = {
        '.bmp':  wx.BITMAP_TYPE_BMP,
        '.jpg':  wx.BITMAP_TYPE_JPEG,
        '.jpeg': wx.BITMAP_TYPE_JPEG,
        '.png':  wx.BITMAP_TYPE_PNG,
        '.pcx':  wx.BITMAP_TYPE_PCX,
        '.ppm':  wx.BITMAP_TYPE_PNM,
        '.tif':  wx.BITMAP_TYPE_TIF,
        '.tiff': wx.BITMAP_TYPE_TIF,
        '.xpm':  wx.BITMAP_TYPE_XPM
        }

    h, w, d = data.shape
    if d == 1:
        data = np.dstack((data, data, data))
        d =3
    elif d == 2:
        l = data[...,0]
        a = data[...,1]
        data = np.dstack((l, l, l, a))
        d = 4
    im = wx.EmptyImage()
    im.Create(w, h, False)
    im.SetData(data[...,:3].tostring())
    if d > 3:
        im.SetAlphaData(data[...,3].tostring())
    im.SaveFile(path, _types[ext])

def _read_data(png_ptr, data, length):
    userp = png.get_io_ptr(png_ptr)
    userp = cast(userp, POINTER(c_void_p))
    bufp = userp.contents
    memmove(data, bufp, length)
    bufp.value += length

_version = None

def load_png(path):
    global _version
    if _version is None:
        _version = png.get_header_ver(c_void_p(0))

    with file(path, 'rb') as f:
        buffer = f.read()

    pixels = None

    png_ptr = png.create_read_struct(_version, None, None, None)
    png_ptr = c_void_p(png_ptr)
    if not png_ptr:
        raise RuntimeError("Couldn't allocate PNG structure")

    info_ptr = png.create_info_struct(png_ptr)
    info_ptr = c_void_p(info_ptr)
    if not info_ptr:
        raise RuntimeError("Couldn't allocate PNG info structure")

    bufp = cast(c_char_p(buffer), c_void_p)
    read_data = png.rw_func(_read_data)
    png.set_read_fn(png_ptr, byref(bufp), read_data)

    png.read_info(png_ptr, info_ptr)

    w = c_uint()
    h = c_uint()
    bit_depth = c_int()
    color_type = c_int()

    png.get_IHDR(png_ptr, info_ptr, byref(w), byref(h),
                 byref(bit_depth), byref(color_type),
                 None, None, None)

    w = w.value
    h = h.value
    bit_depth = bit_depth.value
    color_type = color_type.value

    if color_type == png.COLOR_TYPE_PALETTE:
        if png.get_valid(png_ptr, info_ptr, png.INFO_tRNS):
            png.set_tRNS_to_alpha(png_ptr)
            mode = 'RGBA'
        else:
            mode = 'RGB'
        png.set_palette_to_rgb(png_ptr)
    elif color_type == png.COLOR_TYPE_GRAY:
        if bit_depth < 8:
            png.set_expand_gray_1_2_4_to_8(png_ptr)
        mode = 'L'
    elif color_type == png.COLOR_TYPE_GRAY_ALPHA:
        if bit_depth < 8:
            png.set_expand_gray_1_2_4_to_8(png_ptr)
        mode = 'LA'
    elif color_type == png.COLOR_TYPE_RGB:
        mode = 'RGB'
    elif color_type == png.COLOR_TYPE_RGB_ALPHA:
        mode = 'RGBA'
    else:
        raise RuntimeError('color_type = %r' % color_type)

    if bit_depth < 8:
        png.set_packing(png_ptr)
    elif bit_depth == 16:
        png.set_strip_16(png_ptr)

    png.read_update_info(png_ptr, info_ptr)

    image = Image(mode, (w, h))
    pixels = image._data

    for y in xrange(h):
        ptr = c_void_p(pixels[y].__array_interface__['data'][0])
        png.read_row(png_ptr, ptr, None)

    png.read_end(png_ptr, None)

    png.destroy_read_struct(byref(png_ptr), byref(info_ptr), None)

    return image

def save_bmp(path, data):
    h, w, c = data.shape

    # BITMAPFILEHEADER structure
    #
    #  0 2      signature: 'B','M'
    #  2 4      file size
    #  6 2      reserved
    #  8 2      reserved
    # 10 4      offset to bitmap data

    file_header = struct.pack(
        '<2cI2hI',
        'B','M',
        14 + 40 + h * w * c,
        0, 0,
        54)

    # BITMAPINFOHEADER structure
    #
    # 0     4       BITMAPINFOHEADER size
    # 4     4       width
    # 8     4       height (+ve => bottom-up, -ve => top-down)
    # 12    2       number of planes (must be 1)
    # 14    2       bits per pixel
    # 16    4       compression
    # 20    4       image size
    # 24    4       X pixels per meter
    # 28    4       Y pixels per meter
    # 32    4       number of palette colors used
    # 36    4       number of important palette colors
    # 40 ... palette

    info_header = struct.pack(
        '<IIIHHIIIIII',
        40,
        w, h,
        1,
        c * 8,
        0,
        w * h,
        2953, 2953,
        0, 0)

    data = data[:,:,::-1]       # RGB->BGR
    data = data[::-1,:,:]       # vertical flip

    rowsize = w * c
    if rowsize % 4 != 0:
        padsize = (rowsize + 3) / 4 * 4
        data2 = np.zeros((h, padsize), dtype=np.uint8)
        data2[:,:rowsize] = data.reshape((h, rowsize))
        data = data2

    with file(path, 'wb') as f:
        f.write(file_header)
        f.write(info_header)
        f.write(np.ascontiguousarray(data).tostring())

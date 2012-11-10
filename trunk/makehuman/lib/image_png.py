import os
from ctypes import *
import numpy as np
import png

_version = None

def _read_data(png_ptr, data, length):
    userp = png.get_io_ptr(png_ptr)
    userp = cast(userp, POINTER(c_void_p))
    bufp = userp.contents
    memmove(data, bufp, length)
    bufp.value += length

def load(path):
    base, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext != '.png':
        raise NotImplementedError('Invalid image format: %s' % ext)

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
        depth = 1
    elif color_type == png.COLOR_TYPE_GRAY_ALPHA:
        if bit_depth < 8:
            png.set_expand_gray_1_2_4_to_8(png_ptr)
        depth = 2
    elif color_type == png.COLOR_TYPE_RGB:
        depth = 3
    elif color_type == png.COLOR_TYPE_RGB_ALPHA:
        depth = 4
    else:
        raise RuntimeError('color_type = %r' % color_type)

    if bit_depth < 8:
        png.set_packing(png_ptr)
    elif bit_depth == 16:
        png.set_strip_16(png_ptr)

    png.read_update_info(png_ptr, info_ptr)

    pixels = np.empty((h, w, depth), dtype = np.uint8)

    for y in xrange(h):
        ptr = c_void_p(pixels[y].__array_interface__['data'][0])
        png.read_row(png_ptr, ptr, None)

    png.read_end(png_ptr, None)

    png.destroy_read_struct(byref(png_ptr), byref(info_ptr), None)

    return pixels

def _write_data(png_ptr, data, length):
    userp = png.get_io_ptr(png_ptr)
    userp = cast(userp, POINTER(py_object))
    outf = userp.contents.value
    outf.write(cast(data, POINTER(c_char))[:length])

def _flush_data(png_ptr):
    userp = png.get_io_ptr(png_ptr)
    userp = cast(userp, POINTER(py_object))
    outf = userp.contents.value
    outf.flush()

_color_types = [
    None, 
    png.COLOR_TYPE_GRAY,
    png.COLOR_TYPE_GRAY_ALPHA,
    png.COLOR_TYPE_RGB,
    png.COLOR_TYPE_RGB_ALPHA
    ]

def save(path, data):
    base, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext != '.png':
        raise NotImplementedError()

    global _version
    if _version is None:
        _version = png.get_header_ver(c_void_p(0))

    png_ptr = png.create_write_struct(_version, None, None, None)
    png_ptr = c_void_p(png_ptr)
    if not png_ptr:
        raise RuntimeError("Couldn't allocate PNG structure")

    info_ptr = png.create_info_struct(png_ptr)
    info_ptr = c_void_p(info_ptr)
    if not info_ptr:
        raise RuntimeError("Couldn't allocate PNG info structure")

    outf = open(path, 'wb')
    outfp = pointer(py_object(outf))

    write_data = png.rw_func(_write_data)
    flush_data = png.flush_func(_flush_data)
    png.set_write_fn(png_ptr, cast(outfp, c_void_p), write_data, flush_data)

    h, w, c = data.shape

    color_type = _color_types[c]

    png.set_IHDR(png_ptr, info_ptr, w, h, 8, color_type,
                 png.INTERLACE_NONE,
                 png.COMPRESSION_TYPE_DEFAULT,
                 png.FILTER_TYPE_DEFAULT)

    buf = data.tostring()
    buf = cast(c_char_p(buf), c_void_p)
    row_pointers = (c_void_p * h)()
    for i in xrange(h):
        row_pointers[i] = c_void_p(buf.value + i * w * c)

    png.set_rows(png_ptr, info_ptr, cast(row_pointers, POINTER(c_void_p)))

    png.write_png(png_ptr, info_ptr, 0, None)

    png.destroy_write_struct(byref(png_ptr), byref(info_ptr))

    del outfp
    outf.close()

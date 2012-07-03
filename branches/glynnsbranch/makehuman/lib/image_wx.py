import os
import numpy as np
import wx

def load(path):
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
    return data

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

def save(path, ext, data):
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


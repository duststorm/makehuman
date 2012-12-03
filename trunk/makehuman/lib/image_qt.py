import os
import numpy as np

from PyQt4 import QtCore, QtGui

def load(path):
    im = QtGui.QImage(path)
    if im.isNull():
        raise RuntimeError("unable to load image '%s'" % path)
    w, h = im.width(), im.height()
    alpha = im.hasAlphaChannel()
    im = im.convertToFormat(QtGui.QImage.Format_ARGB32)
    data = im.bits().asstring(h * w * 4)
    data = np.fromstring(data, dtype=np.uint8).reshape((h, w, 4))
    del im

    # BGRA -> RGBA
    data = data[...,[2,1,0,3]]

    if not alpha:
        data = data[...,:3]

    dir, file = os.path.split(path)
    base, last = os.path.split(dir)
    if last.lower() == 'fonts' and np.all(data[...,1:] - data[...,:1] == 0):
        data = data[...,:1]

    data = np.ascontiguousarray(data)

    return data

def save(path, data):
    h, w, d = data.shape
    if d == 1:
        data = np.dstack((data, data, data))
        d = 3
    elif d == 2:
        l = data[...,0]
        a = data[...,1]
        data = np.dstack((l, l, l, a))
        d = 4

    if d == 3:
        fmt = QtGui.QImage.Format_RGB32
    elif d == 4:
        fmt = QtGui.QImage.Format_ARGB32

    im = QtGui.QImage(data.tostring(), w, h, w * d, fmt)
    im.save(path)

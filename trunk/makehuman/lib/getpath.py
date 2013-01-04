#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers, Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Utility module for finding the user home path.
"""

import sys
import os

if sys.platform == 'win32':
    import _winreg

def getPath(type):
    if isinstance(type, (str, unicode)):
        typeStr = str(type)
    elif type is None:
        typeStr = ""
    else:
        raise TypeError("String expected")

    if sys.platform == 'win32':
        keyname = r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
        name = 'Personal'
        k = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyname)
        value, type = _winreg.QueryValueEx(k, 'Personal')
        if type == _winreg.REG_EXPAND_SZ:
            path = _winreg.ExpandEnvironmentStrings(value)
        elif type == _winreg.REG_SZ:
            path = value
        else:
            raise RuntimeError("Couldn't determine user folder")

        if typeStr == "exports":
            path += u"\\makehuman\\exports\\"
        elif typeStr == "models":
            path += u"\\makehuman\\models\\"
        elif typeStr == "grab":
            path += u"\\makehuman\\grab\\"
        elif typeStr == "render":
            path += u"\\makehuman\\render\\"
        elif typeStr == "":
            path += u"\\makehuman\\"
        else:
            raise ValueError("Unknown value '%s' for getPath()!" % typeStr)
    else:
        path = os.path.expanduser('~')
        if sys.platform.startswith("darwin"): 
            path = os.path.join(path,"Documents")
            path = os.path.join(path,"MakeHuman")
        else:
            path = os.path.join(path,"makehuman")

        if typeStr == "exports":
            path += "/exports/"
        elif typeStr == "models":
            path += "/models/"
        elif typeStr == "grab":
            path += "/grab/"
        elif typeStr == "render":
            path += "/render/"
        elif typeStr == "":
            path += "/"
        else:
            raise ValueError("Unknown property '%s' for getPath()!" % typeStr)

    return path


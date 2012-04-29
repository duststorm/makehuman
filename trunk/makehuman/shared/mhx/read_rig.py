#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**     MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:** http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**     MakeHuman Team 2001-2011

**Licensing:**       GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TO DO

"""

import aljabr
from aljabr import *
import mhxbones
import os

#
#   setupRigJoint (words, obj, verts, locations):
#
def setupRigJoint (words, obj, verts, locations):
    key = words[0]
    typ = words[1]
    if typ == 'joint':
        loc = mhxbones.calcJointPos(obj, words[2])
        locations[key] = loc
    elif typ == 'vertex':
        v = int(words[2])
        locations[key] = verts[v].co
    elif typ == 'position':
        x = locations[words[2]]
        y = locations[words[3]]
        z = locations[words[4]]
        locations[key] = [x[0],y[1],z[2]]
    elif typ == 'line':
        k1 = float(words[2])
        k2 = float(words[4])
        locations[key] = vadd(vmul(locations[words[3]], k1), vmul(locations[words[5]], k2))
    elif typ == 'offset':
        x = float(words[3])
        y = float(words[4])
        z = float(words[5])
        locations[key] = vadd(locations[words[2]], [x,y,z])
    elif typ == 'voffset':
        v = int(words[2])
        x = float(words[3])
        y = float(words[4])
        z = float(words[5])
        try:
            loc = verts[v].co
        except:
            loc = verts[v]         
        locations[key] = vadd(loc, [x,y,z])
    elif typ == 'front':
        raw = locations[words[2]]
        head = locations[words[3]]
        tail = locations[words[4]]
        offs = eval(words[5])
        vec = aljabr.vsub(tail, head)
        vec2 = aljabr.vdot(vec, vec)
        vraw = aljabr.vsub(raw, head)
        x = aljabr.vdot(vec, vraw) / vec2
        rvec = aljabr.vmul(vec, x)
        nloc = aljabr.vadd(head, rvec, offs)
        locations[key] = nloc
    else:
        raise NameError("Unknown %s" % typ)

#
#   readRigFile(filename, obj, verts=obj.verts):
#

def readRigFile(filename, obj, verts=None):
    if type(filename) == tuple:
        (folder, fname) = filename
        filename = os.path.join(folder, fname)
    path = os.path.realpath(os.path.expanduser(filename))
    try:
        fp = open(path, "rU")
    except:
        print("*** Cannot open %s" % path)
        return

    doLocations = 1
    doBones = 2
    doWeights = 3
    status = 0

    locations = {}
    armature = []
    weights = {}

    if not verts:
        verts = obj.verts
    for line in fp: 
        words = line.split()
        if len(words) == 0:
            pass
        elif words[0] == '#':
            if words[1] == 'locations':
                status = doLocations
            elif words[1] == 'bones':
                status = doBones
            elif words[1] == 'weights':
                status = doWeights
                wts = []
                weights[words[2]] = wts
        elif status == doWeights:
            wts.append((int(words[0]), float(words[1])))
        elif status == doLocations:
            setupRigJoint (words, obj, verts, locations)
        elif status == doBones:
            bone = words[0]
            head = locations[words[1]]
            tail = locations[words[2]]
            roll = float(words[3])
            parent = words[4]
            options = {}
            for word in words[5:]:
                try:
                    float(word)
                    values.append(word)
                    continue
                except:
                    pass
                if word[0] == '-':
                    values = []
                    options[word] = values
                else:
                    values.append(word)
            armature.append((bone, head, tail, roll, parent, options))
        else:
            raise NameError("Unknown status %d" % status)

    fp.close()
    return (locations, armature, weights)


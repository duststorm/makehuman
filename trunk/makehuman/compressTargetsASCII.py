#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Convert ASCII .target files to use minimal space.
This script is useful to run everytime before new targets or modifications are
committed.
"""

import fnmatch
import os

def getTargets(rootPath):
    targetFiles = []
    for root, dirnames, filenames in os.walk(rootPath):
        for filename in fnmatch.filter(filenames, '*.target'):
            targetFiles.append(os.path.join(root, filename))
    return targetFiles

def formatFloat(f):
    f = round(f, 2)
    if f == 0:
        # Make sure -0.0 becomes 0
        return 0
    return "%.3f" % f

allTargets = getTargets('data/targets')
for (i, targetPath) in enumerate(allTargets):
    f = open(targetPath, 'rb')
    target = f.readlines()
    f.close()
    newTarget = []
    for line in target:
        fields = line.split()
        idx = int(fields[0])
        dx = formatFloat( float(fields[1]) )
        dy = formatFloat( float(fields[2]) )
        dz = formatFloat( float(fields[3]) )
        newLine = "%d %s %s %s" % (idx, dx, dy, dz)
        newTarget.append(newLine)
    f = open(targetPath, 'wb')  # write binary to enforce unix line-endings on windows
    newTarget = "\n".join(newTarget)
    f.write(newTarget)
    f.close()
    print "[%.0f%% done] Updated file %s" % (100*(float(i)/float(len(allTargets))), targetPath)

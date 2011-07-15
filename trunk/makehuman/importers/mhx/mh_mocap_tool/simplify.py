# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2011
# Coding Standards:    See http://sites.google.com/site/makehumandocs/developers-guide

import bpy, math
from . import load

#
#    simplifyFCurves(context, rig, useVisible, useMarkers):
#

def simplifyFCurves(context, rig, useVisible, useMarkers):
    scn = context.scene
    if not scn.MhxDoSimplify:
        return
    try:
        act = rig.animation_data.action
    except:
        act = None
    if not act:
        print("No action to simplify")
        return

    if useVisible:
        fcurves = []
        for fcu in act.fcurves:
            if not fcu.hide:
                fcurves.append(fcu)
                #print(fcu.data_path, fcu.array_index)
    else:
        fcurves = act.fcurves

    if useMarkers:
        (minTime, maxTime) = getMarkedTime(scn)        
        if minTime == None:    
            print("Need two selected markers")
            return
    else:
        (minTime, maxTime) = ('All', 0)

    for fcu in fcurves:
        simplifyFCurve(fcu, act, scn.MhxErrorLoc, scn.MhxErrorRot, minTime, maxTime)
    load.setInterpolation(rig)
    print("Curves simplified")
    return

#
#    simplifyFCurve(fcu, act, maxErrLoc, maxErrRot, minTime, maxTime):
#

def simplifyFCurve(fcu, act, maxErrLoc, maxErrRot, minTime, maxTime):
    #print("WARNING: F-curve simplification turned off")
    #return
    words = fcu.data_path.split('.')
    if words[-1] == 'location':
        maxErr = maxErrLoc
    elif words[-1] == 'rotation_quaternion':
        maxErr = maxErrRot * math.pi/180
    elif words[-1] == 'rotation_euler':
        maxErr = maxErrRot * math.pi/180
    else:
        raise NameError("Unknown FCurve type %s" % words[-1])

    if minTime == 'All':
        points = fcu.keyframe_points
        before = []
        after = []
    else:
        points = []
        before = []
        after = []
        for pt in fcu.keyframe_points:
            t = pt.co[0]
            if t < minTime:
                before.append(pt.co)
            elif t > maxTime:
                after.append(pt.co)
            else:
                points.append(pt)

    nPoints = len(points)
    if nPoints <= 2:
        return
    keeps = []
    new = [0, nPoints-1]
    while new:
        keeps += new
        keeps.sort()
        new = iterateFCurves(points, keeps, maxErr)
    newVerts = before
    for n in keeps:
        newVerts.append(points[n].co)
    newVerts += after
    
    path = fcu.data_path
    index = fcu.array_index
    grp = fcu.group.name
    act.fcurves.remove(fcu)
    nfcu = act.fcurves.new(path, index, grp)
    for co in newVerts:
        t = co[0]
        try:
            dt = t - int(t)
        except:
            dt = 0.5
        if abs(dt) > 1e-5:
            pass
            # print(path, co, dt)
        else:
            nfcu.keyframe_points.insert(frame=co[0], value=co[1])

    return

#
#    iterateFCurves(points, keeps, maxErr):
#

def iterateFCurves(points, keeps, maxErr):
    new = []
    for edge in range(len(keeps)-1):
        n0 = keeps[edge]
        n1 = keeps[edge+1]
        (x0, y0) = points[n0].co
        (x1, y1) = points[n1].co
        if x1 > x0:
            dxdn = (x1-x0)/(n1-n0)
            dydx = (y1-y0)/(x1-x0)
            err = 0
            for n in range(n0+1, n1):
                (x, y) = points[n].co
                xn = n0 + dxdn*(n-n0)
                yn = y0 + dydx*(xn-x0)
                if abs(y-yn) > err:
                    err = abs(y-yn)
                    worst = n
            if err > maxErr:
                new.append(worst)
    return new

#
#    getMarkedTime(scn):
#

def getMarkedTime(scn):
    markers = []
    for mrk in scn.timeline_markers:
        if mrk.select:
            markers.append(mrk.frame)
    markers.sort()
    if len(markers) >= 2:
        return (markers[0], markers[-1])
    else:
        return (None, None)



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

"""
Abstract
Tool for making animations loop seamlessly
Version 0.3

Place the script in the .blender/scripts/addons dir
Activate the script in the "Add-Ons" tab (user preferences).
Access from the File > Import menu.

Alternatively, run the script in the script editor (Alt-P), and access from the File > Import menu
"""

bl_info = {
    "name": "MHX Fourier",
    "author": "Thomas Larsson",
    "version": "0.4",
    "blender": (2, 5, 6),
    "api": 35774,
    "location": "View3D > Properties > MHX Fourier",
    "description": "Fourier tool",
    "warning": "",
    'wiki_url': 'http://sites.google.com/site/makehumandocs/blender-export-and-mhx',
    "category": "3D View"}

"""
Run from text window. 
Access from UI panel (N-key) when rig is active.

"""

DEBUG = True

import bpy, cmath, math, mathutils
from bpy.props import *

#
#    ditfft2(f, N, z):
#
#    Y_0,...,N?1 ? ditfft2(X, N, s):             DFT of (X0, Xs, X2s, ..., X(N-1)s):
#    if N = 1 then
#        Y_0 ? X_0                                      trivial size-1 DFT base case
#    else
#        Y_0,...,N/2?1 ? ditfft2(X, N/2, 2s)             DFT of (X_0, X_2s, X_4s, ...)
#        Y_N/2,...,N?1 ? ditfft2(X+s, N/2, 2s)           DFT of (X_s, X_s+2s, X_s+4s, ...)
#        for k = 0 to N/2?1                           combine DFTs of two halves into full DFT:
#            t ? Y_k
#            Y_k ? t + exp(?2?i k/N) * Y_k+N/2
#            Y_k+N/2 ? t ? exp(?2?i k/N) * Y_k+N/2
#        endfor
#    endif
    
def ditfft2(f, N, z):
    if N == 1:
        return f
    else:
        N2 = int(N/2)
        f_even = ditfft2(f[::2], N2, z*z)
        f_odd = ditfft2(f[1::2], N2, z*z)
        e = 1
        y_even = []
        y_odd = []
        for k in range(N2):
            t0 = f_even[k]
            t1 = f_odd[k]
            y_even.append( t0 + e*t1 )
            y_odd.append( t0 - e*t1 )
            e *= z
        return y_even + y_odd

#
#    fourierFCurves(context):
#

def fourierFCurves(context):
    rig = context.object
    try:
        act = rig.animation_data.action
    except:
        act = None
    if not act:
        print("No FCurves to Fourier")
        return

    scn = context.scene
    t0 = scn.frame_start
    tn = scn.frame_end
    if scn.MhxRemoveRoot:
        modifyFcurves(act, rig, -1, scn, t0, tn)

    for fcu in act.fcurves:
        fourierFCurve(fcu, act, scn, t0, tn)
    
    for fcu in act.fcurves:
        f0 = fcu.evaluate(t0)
        fcu.keyframe_points.insert(frame=tn+1, value=f0)

    setInterpolation(rig)
    return
    
#
#    class CAnimation:
#

class CAnimation:
    def __init__(self, name):
        self.name = name
        self.fcurves = {}
        self.locals = {}
        self.globals = {}
        self.matrix = None
        self.inverse = None
        self.head = None

#
#    modifyFcurves(act, rig, factor, scn, t0, tn):
#

def modifyFcurves(act, rig, factor, scn, t0, tn):
    animations = {}
    for fcu in act.fcurves:
        addAnimation(fcu, animations, rig.data.bones)
    for anim in animations.values():
        setLocations(anim, t0, tn)
    rootAnim = animations['Root']    
    for anim in animations.values():
        if anim.name != 'Root':
            addRoot(anim, factor, rootAnim.globals, scn, t0, tn)
            removeLinearTerm(anim, t0, tn)
    addRoot(rootAnim, factor, rootAnim.globals, scn, t0, tn)
    return rootAnim

#
#    removeLinearTerm(anim, t0, tn):
#

def removeLinearTerm(anim, t0, tn):
    for index in range(3):
        try:
            fcu = anim.fcurves[index]
        except:
            fcu = None
        if fcu:
            f0 = fcu.evaluate(t0)
            fn = fcu.evaluate(tn)
            df = (fn-f0)/(tn-t0)
            n = tn-t0
            df0 = df*n/2.0
            for pt in fcu.keyframe_points:
                t = pt.co[0]
                pt.co[1] += df0 - df*(t-t0)
    return                    

#
#    addAnimation(fcu, animations, bones):
#

def addAnimation(fcu, animations, bones):
    words = fcu.data_path.split('.')
    if words[2] != 'location':
        return
    index = fcu.array_index
    words2 = words[1].split('"')
    name = words2[1]
    try:
        anim = animations[name]
        first = False
    except:
        anim = CAnimation(name)
        animations[name] = anim
        first = True        
    if first:
        b = bones[name]    
        (loc,rot,scale) = b.matrix_local.decompose()
        anim.matrix = rot.to_matrix()
        anim.inverse = anim.matrix.copy()
        anim.inverse.invert()
        anim.head = b.head_local.copy()
    anim.fcurves[index] = fcu
    return

#
#    setLocations(anim, t0, t1):
#

def setLocations(anim, t0, t1):
    if anim.fcurves:
        xvec = anim.fcurves[0]
        yvec = anim.fcurves[1]
        zvec = anim.fcurves[2]
        for t in range(t0, t1+1):
            x = xvec.evaluate(t)
            y = yvec.evaluate(t)
            z = zvec.evaluate(t)
            anim.locals[t] = mathutils.Vector((x,y,z))
            anim.globals[t] = anim.head + anim.locals[t]*anim.matrix
    return

#
#    addRoot(anim, factor, rootGlobals, scn, t0, t1):
#

def addRoot(anim, factor, rootGlobals, scn, t0, t1):
    if anim.fcurves:
        for t in range(t0, t1+1):
            anim.globals[t] += factor*rootGlobals[t]
            anim.locals[t] = (anim.globals[t] - anim.head)*anim.inverse
        for index in range(3):
            if (index == 2 or not scn.MhxRemoveZOnly):
                pts = anim.fcurves[index].keyframe_points
                vec0 = anim.locals[t0]
                vec1 = anim.locals[t1]
                for pt in pts:
                    t = int(pt.co[0])
                    if t < t0:
                        pt.co[1] = vec0[index]
                    elif t > t1:
                        pt.co[1] = vec1[index]
                    else:
                        vec = anim.locals[t]
                        pt.co[1] = vec[index]
        
    return

#
#    fourierFCurve(fcu, act, scn, t0, tn):
#

def fourierFCurve(fcu, act, scn, t0, tn):
    path = fcu.data_path
    index = fcu.array_index
    grp = fcu.group.name
    words = path.split('.')

    isLoc = False
    if words[-1] == 'location':
        doFourier = False     # scn.MhxFourierLoc
    elif words[-1] == 'rotation_quaternion':
        doFourier = True    # scn.MhxFourierRot
    else:
        doFourier = False
    if not doFourier:
        return

    N = int(2**scn.MhxFourierLevels)
    points = fcu.keyframe_points
    T = (tn-t0+1)
    dt = T/N
    f0 = fcu.evaluate(t0)
    fn = fcu.evaluate(tn)
    df = (fn-f0)/(N-1)
    df = 0
    fcu.keyframe_points.insert(frame=tn+1, value=f0)    
    
    f = []
    for i in range(N):
        fi = fcu.evaluate(t0 + i*dt)
        f.append( fi - i*df)

    if DEBUG and isLoc and index == 2:
        print(path, index)
        printList(f)
    
    w = complex( 0, -2*cmath.pi/N )
    z = cmath.exp(w)
    fhat = ditfft2(f, N, z)
    
    if DEBUG and isLoc and index == 2:
        print("   ***")
        printList(fhat)

    act.fcurves.remove(fcu)
    nfcu = act.fcurves.new(path, index, grp)
    w = complex( 0, 2*cmath.pi/T )
    z = cmath.exp(w)
    e = 1
    kmax = int(2**scn.MhxFourierTerms)
    if kmax > N/2:
        kmax = N/2
    for ti in range(t0, tn+2):
        yi = evalFourier(fhat, kmax, e)/N
        e *= z
        nfcu.keyframe_points.insert(frame=ti, value=yi)
    return

#
#    evalFourier(fhat, kmax, z):
#

def evalFourier(fhat, kmax, z):
    e = 1
    f = 0
    k = 0
    for fn in fhat:
        f += fn*e
        e *= z
        k += 1
        if k >= kmax:
            break
    y = f + f.conjugate()
    if abs(y.imag) > 1e-3:
        raise NameError("Not real", f)
    return y.real

#
#    printList(arr):
#

def printList(arr):
    for elt in arr:
        if type(elt) == float:
            print("%.3f" % elt)
        elif type(elt) == complex:
            if abs(elt.imag) < 1e-4:
                print("%.3f" % elt.real)
            elif abs(elt.real) < 1e-4:
                print("%.3fj" % elt.imag)
            else:
                print("%.3f+%.3fj" % (elt.real, elt.imag))
        else:
            print(elt)

#
#    makeTestCurve(context)
#    class VIEW3D_OT_MhxMakeTestCurve(bpy.types.Operator):
#

def makeTestCurve(context):
    scn = context.scene
    t0 = scn.frame_start
    tn = scn.frame_end
    N = tn-t0+1
    rig = context.object
    act = rig.animation_data.action
    fcu = act.fcurves[0]
    path = fcu.data_path
    index = fcu.array_index
    grp = fcu.group.name
    act.fcurves.remove(fcu)
    nfcu = act.fcurves.new(path, index, grp)
    w = 2*cmath.pi/N
    for k in range(N+1):
        t = k+t0
        y = 2*math.sin(w*k) + math.sin(2*w*k)
        nfcu.keyframe_points.add(frame=t, value=y)
    setInterpolation(rig)
    return

class VIEW3D_OT_MhxMakeTestCurveButton(bpy.types.Operator):
    bl_idname = "view3d.mhx_make_test_curve"
    bl_label = "Make test curve"

    def execute(self, context):
        makeTestCurve(context)
        print("Made curve")
        return{'FINISHED'}    

#
#    setInterpolation(rig):
#

def setInterpolation(rig):
    if not rig.animation_data:
        return
    act = rig.animation_data.action
    if not act:
        return
    for fcu in act.fcurves:
        for pt in fcu.keyframe_points:
            pt.interpolation = 'LINEAR'
        fcu.extrapolation = 'CONSTANT'
    return

#
#    toggleIkConstraints(rig):
#    class VIEW3D_OT_MhxToggleIkConstraintsButton(bpy.types.Operator):
#

def toggleIkConstraints(rig):
    pbones = rig.pose.bones
    first = True
    for pb in pbones:
        for cns in pb.constraints:
            if (cns.type == 'IK'):
                if first:
                    first = False
                    if cns.influence > 0.5:
                        inf = 0.0
                        res = 'OFF'
                    else:
                        inf = 1.0
                        res = 'ON'
                cns.influence = inf
    if first:
        return 'NOT FOUND'
    return res

class VIEW3D_OT_MhxToggleIkConstraintsButton(bpy.types.Operator):
    bl_idname = "view3d.mhx_toggle_ik_constraints"
    bl_label = "Toggle IK constraints"

    def execute(self, context):
        res = toggleIkConstraints(context.object)
        print("IK constraints toggled", res)
        return{'FINISHED'}    

#
#    class VIEW3D_OT_MhxFourierButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxFourierButton(bpy.types.Operator):
    bl_idname = "view3d.mhx_fourier"
    bl_label = "Fourier"

    def execute(self, context):
        import bpy
        fourierFCurves(context)
        print("Curves Fouriered")
        return{'FINISHED'}    


#
#    class MhxFourierPanel(bpy.types.Panel):
#

class Bvh2MhxFourierPanel(bpy.types.Panel):
    bl_label = "Mhx Fourier"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        if context.object and context.object.type == 'ARMATURE':
            return True

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.operator("view3d.mhx_init_interface")
        #layout.operator("view3d.mhx_make_test_curve")
        layout.operator("view3d.mhx_toggle_ik_constraints")
        layout.separator()
        layout.prop(scn, "MhxRemoveRoot")
        layout.prop(scn, "MhxRemoveZOnly")
        layout.prop(scn, "MhxFourierLevels")
        layout.prop(scn, "MhxFourierTerms")
        layout.operator("view3d.mhx_fourier")

        return

#
#    class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
#

def initInterface(context):
    bpy.types.Scene.MhxRemoveRoot = BoolProperty(
        name="Remove root animation",
        description="Remove root animation",
        default=True)

    bpy.types.Scene.MhxRemoveZOnly = BoolProperty(
        name="Only Z component",
        description="Remove only Z-component of root animation",
        default=True)

    bpy.types.Scene.MhxFourierLoc = BoolProperty(
        name="Location",
        description="Fourier transform location F-curves",
        default=True)

    bpy.types.Scene.MhxFourierRot = BoolProperty(
        name="Rotation",
        description="Fourier transform rotation F-curves",
        default=True)

    bpy.types.Scene.MhxFourierLevels = IntProperty(
        name="Fourier levels", 
        description="Fourier levels",
        min = 1, max = 6,
        default=3)

    bpy.types.Scene.MhxFourierTerms = IntProperty(
        name="Fourier terms", 
        description="Fourier terms",
        min = 1, max = 12,
        default=4)

class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
    bl_idname = "view3d.mhx_init_interface"
    bl_label = "Initialize"

    def execute(self, context):
        import bpy
        initInterface(context)
        print("Interface initialized")
        return{'FINISHED'}    

initInterface(bpy.context)

#
#    register
#

def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass

if __name__ == "__main__":
    register()


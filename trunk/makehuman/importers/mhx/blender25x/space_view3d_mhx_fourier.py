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

bl_addon_info = {
	"name": "MHX Fourier",
	"author": "Thomas Larsson",
	"version": "0.1",
	"blender": (2, 5, 5),
	"api": 33590,
	"location": "View3D > Properties > MHX Fourier",
	"description": "Fourier tool",
	"warning": "",
	"category": "3D View"}

"""
Run from text window. 
Access from UI panel (N-key) when rig is active.

"""

MAJOR_VERSION = 0
MINOR_VERSION = 2
BLENDER_VERSION = (2, 55, 5)

import bpy, cmath
from bpy.props import *

#
#	ditfft2(f, n, s, z):
#
#	Y0,...,N−1 ← ditfft2(X, N, s):             DFT of (X0, Xs, X2s, ..., X(N-1)s):
#    if N = 1 then
#        Y0 ← X0                                      trivial size-1 DFT base case
#    else
#        Y0,...,N/2−1 ← ditfft2(X, N/2, 2s)             DFT of (X0, X2s, X4s, ...)
#        YN/2,...,N−1 ← ditfft2(X+s, N/2, 2s)           DFT of (Xs, Xs+2s, Xs+4s, ...)
#        for k = 0 to N/2−1                           combine DFTs of two halves into full DFT:
#            t ← Yk
#            Yk ← t + exp(−2πi k/N) Yk+N/2
#            Yk+N/2 ← t − exp(−2πi k/N) Yk+N/2
#        endfor
#    endif
	
def ditfft2(f, n, s, z):
	if n == 1:
		return f
	else:
		n2 = int(n/2)
		f_even = ditfft2(f[::2], n2, 2*s, z)
		f_odd = ditfft2(f[1::2], n2, 2*s, z)
		e = 1
		y_even = []
		y_odd = []
		for k in range(n2):
			t0 = f_even[k]
			t1 = f_odd[k]
			y_even.append( t0 + e*t1 )
			y_odd.append( t0 - e*t1 )
			e *= z
		return y_even + y_odd

#
#	fourierFCurves(context):
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

	for fcu in act.fcurves:
		fourierFCurve(fcu, act, context.scene)
	setInterpolation(rig)
	return

#
#	fourierFCurve(fcu, act, scn):
#

def fourierFCurve(fcu, act, scn):
	words = fcu.data_path.split('.')
	if words[-1] == 'location':
		doFourier = scn.MhxFourierLoc
	elif words[-1] == 'rotation_quaternion':
		doFourier = scn.MhxFourierRot
	else:
		doFourier = False
	if not doFourier:
		return

	n = int(2**scn.MhxFourierLevels)
	points = fcu.keyframe_points
	if len(points) <= 2:
		return
	t0 = scn.frame_start
	tn = scn.frame_end
	dt = (tn-t0+1)/n
	f0 = fcu.evaluate(t0)
	fn = fcu.evaluate(tn)
	df = (fn-f0)/(n-1)

	f = []
	for i in range(n):
		fi = fcu.evaluate(t0 + i*dt)
		f.append( fi - i*df )
	w = complex( 0, 2*cmath.pi/n )
	z = cmath.exp(w)
	fhat = ditfft2(f, n, 1, z)
	print(fhat)
	
	path = fcu.data_path
	index = fcu.array_index
	grp = fcu.group.name
	act.fcurves.remove(fcu)
	nfcu = act.fcurves.new(path, index, grp)
	w = complex( 0, -2*cmath.pi/n )
	z = 1
	for t in range(t0, tn+1):
		y = evalFourier(fhat, 3, z)
		z *= w
		nfcu.keyframe_points.add(frame=t, value=y)
	print(path, index, t, y)
	return

def evalFourier(fhat, kmax, z):
	e = 1
	f = 0
	for k in range(kmax):
		fn = fhat[k]
		f += fn*e
		e *= z
	return f.real

#
#	setInterpolation(rig):
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
#	class OBJECT_OT_FourierButton(bpy.types.Operator):
#

class OBJECT_OT_FourierButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_FourierButton"
	bl_label = "Fourier"

	def execute(self, context):
		import bpy
		fourierFCurves(context)
		print("Curves Fouriered")
		return{'FINISHED'}	


#
#	class MhxFourierPanel(bpy.types.Panel):
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
		layout.operator("object.InitInterfaceButton")

		layout.label('Fourier')
		row = layout.row()
		row.prop(scn, "MhxFourierLoc")
		row.prop(scn, "MhxFourierRot")
		layout.prop(scn, "MhxFourierLevels")
		layout.operator("object.FourierButton")

		return

#
#	class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

def initInterface(context):
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

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
	bl_idname = "OBJECT_OT_InitInterfaceButton"
	bl_label = "Initialize"

	def execute(self, context):
		import bpy
		initInterface(context)
		print("Interface initialized")
		return{'FINISHED'}	

initInterface(bpy.context)

#
#	register
#

def register():
	pass

def unregister():
	pass

if __name__ == "__main__":
	register()


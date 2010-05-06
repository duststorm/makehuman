import bpy

def printVertNums():
	ob = bpy.context.object
	print("Verts in ", ob)
	#bpy.ops.object.mode_set('OBJECT')
	me = ob.data
	for v in me.verts:
		if v.selected:
			print(v.index)
	print("End")
	#bpy.ops.object.mode_set('EDIT')

#printVertNums()




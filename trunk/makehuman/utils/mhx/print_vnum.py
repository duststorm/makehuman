import bpy
 
def printVertNums():
	ob = bpy.context.object
	print("Verts in ", ob)
	#bpy.ops.object.mode_set('OBJECT')
	me = ob.data
	for v in me.vertices:
		if v.select:
			print(v.index)
	print("End")
	#bpy.ops.object.mode_set('EDIT')

def selectQuads():
	ob = bpy.context.object
	me = ob.data
	for f in me.faces:
		if len(f.verts) == 4:
			f.select = True
		else:
			f.select = False
	return
	
printVertNums()
#selectQuads()





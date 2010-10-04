
import bpy

def unVertexDiamonds():
	ob = bpy.context.object
	print("Unvertex diamonds in %s" % ob)
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.mode_set(mode='OBJECT')
	me = ob.data
	for f in me.faces:		
		if len(f.vertices) < 4:
			for vn in f.vertices:
				me.vertices[vn].select = True
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.object.vertex_group_remove_from(all=True)
	bpy.ops.object.mode_set(mode='OBJECT')
	return

unVertexDiamonds()



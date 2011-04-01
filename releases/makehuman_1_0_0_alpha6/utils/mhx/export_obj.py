#----------------------------------------------------------
# File export_obj.py
# Simple obj exporter which writes only verts, faces, and texture verts
# Better uv coords than standard exporter
#----------------------------------------------------------
import bpy, os

def export_simple_obj(filepath, ob, rot90, scale):
	name = os.path.basename(filepath)
	realpath = os.path.realpath(os.path.expanduser(filepath))
	fp = open(realpath, 'w')	
	print('Exporting %s' % realpath)

	if not ob or ob.type != 'MESH':
		raise NameError('Cannot export: active object %s is not a mesh.' % ob)
	me = ob.data

	for v in me.vertices:
		x = scale*v.co
		if rot90:
			fp.write("v %.5f %.5f %.5f\n" % (x[0], x[2], -x[1]))
		else:
			fp.write("v %.5f %.5f %.5f\n" % (x[0], x[1], x[2]))

	if len(me.uv_textures) > 0:
		(ntexvert, ntexvertco) = sort_uvs(me)
		for (x,y) in ntexvertco:
			fp.write("vt %.5f %.5f\n" % (x,y))
		
		vt = 0
		for f in me.faces:
			verts = f.vertices
			fp.write("f ")
			for k in range(len(verts)):
				fp.write("%d/%d " % (verts[k]+1, ntexvert[vt]+1))
				vt += 1
			fp.write("\n")
	else:
		for f in me.faces:
			verts = f.vertices
			fp.write("f ")
			for k in range(len(verts)):
				fp.write("%d " % (verts[k]+1))
			fp.write("\n")
	
	print('%s successfully exported' % realpath)
	fp.close()
	return

def sort_uvs(me):
	uvtex = me.uv_textures[0]
	vt = 0
	texverts = []
	for f in me.faces:
		uv = uvtex.data[f.index].uv_raw
		texface = []
		for k in range(len(f.vertices)):
			texverts.append((uv[2*k], uv[2*k+1], vt))
			vt += 1
	texverts.sort()

	x0 = 1e10
	y0 = 1e10
	eps = 1e-4
	nvt = -1
	ntexvert = {}
	ntexvertco = []
	for (x,y,vt) in texverts:
		if abs(x-x0) < eps and abs(y-y0) < eps:
			ntexvert[vt] = nvt
		else:
			nvt += 1
			ntexvert[vt] = nvt
			ntexvertco.append( (x,y) )
			x0 = x
			y0 = y
	return (ntexvert, ntexvertco)

	

#
#	User interface
#

class export_OT_simple_obj(bpy.types.Operator):
	bl_idname = "io_export_scene.simple_obj"
	bl_description = 'Export from simple OBJ file format (.obj)'
	bl_label = "Export simple OBJ"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"

	filepath = bpy.props.StringProperty(
		name="File Path", 
		description="File path used for exporting the simple OBJ file", 
		maxlen= 1024, default= "")

	rot90 = bpy.props.BoolProperty(
		name = "Rotate 90 degrees",
		description="Rotate mesh to Y up",
		default = True)

	scale = bpy.props.FloatProperty(
		name = "Scale", 
		description="Scale mesh", 
		default = 1.0, min = 0.001, max = 1000.0)

	def execute(self, context):
		print("Load", self.properties.filepath)
		export_simple_obj(self.properties.filepath, 
			context.object, self.rot90, 1.0/self.scale)
		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

#
#	Add simple exporter to the File > Export menu
#

def menu_func(self, context):
	self.layout.operator(export_OT_simple_obj.bl_idname, text="Simple OBJ (.obj)...")

def register():
	bpy.types.INFO_MT_file_export.append(menu_func)

def unregister():
	bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
	register()


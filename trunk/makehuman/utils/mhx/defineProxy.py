import bpy
import os

def findProxy():
	bob = bpy.data.objects['Human']
	pob = bpy.data.objects['Proxy']
	base = bob.data
	proxy = pob.data
	
	bestVerts = []
	for pv in proxy.verts:
		pindex = pv.groups[0].group
		name = pob.vertex_groups[pindex].name
		bindex = None
		for bvg in bob.vertex_groups:
			if bvg.name == name:
				bindex = bvg.index

		print(pv.index, name, pindex, bindex)

		mv = 0
		mindist = 1e6
		for bv in base.verts:
			if len(bv.groups) > 0 and bv.groups[0].group == bindex:
				vec = pv.co - bv.co
				if vec.length < mindist:
					mv = bv
					mindist = vec.length
		if mindist > 0.9e6:
			raise NameError("Failed to match vertex %s" % pv)
		bestVerts.append((pv, mv, mindist))
	return bestVerts

def printProxy(path, verts):	
	file = os.path.expanduser(path)
	fp= open(file, "w")

	fp.write("Verts\n")
	for (pv,bv,dist) in verts:
		fp.write("%3d\n" % (bv.index))
	proxy =  bpy.data.objects['Proxy'].data

	fp.write("Faces\n")
	for f in proxy.faces:
		for v in f.verts:
			fp.write("%d " % (v+1))
		fp.write("\n")

	fp.close()
	return

path = '~/myproxy.proxy'
print("Doing %s" % path)
verts = findProxy()
printProxy(path, verts)
print("%s done" % path)


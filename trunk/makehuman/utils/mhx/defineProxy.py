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
		bestVerts.append((pv, mv, []))

	print("Setting up face table")
	vfaces = {}
	for f in base.faces:
		for v in f.verts:
			try:
				vfaces[v].append(f)
			except:
				vfaces[v] = [f]
	
	print("Finding weights")
	for (pv, bv, fcs) in bestVerts:
		print(pv.index)
		for f in vfaces[bv.index]:
			verts = []
			for v in f.verts:
				verts.append(base.verts[v].co)
			wts = cornerWeights(pv.co, verts)
			fcs.append((f.verts, wts))

	print("Finding best weights")
	bestFaces = []
	for (pv, bv, fcs) in bestVerts:
		print(pv.index)
		minmax = -1e6
		for (fverts, wts) in fcs:
			w = minWeight(wts)
			if w > minmax:
				minmax = w
				bWts = wts
				bVerts = fverts
		if minmax > -0.15:
			bestFaces.append((pv, bVerts, bWts))	
		else:
			bestFaces.append((pv, [bv.index,0,1], [1,0,0]))
				
	print("Done")
	return bestFaces

#
#	minWeight(wts)
#

def minWeight(wts):
	best = 1e6
	for w in wts:
		if w < best:
			best = w
	return best

#
#	cornerWeights(pv, verts):
#
#	px = w0*x0 + w1*x1 + w2*x2
#	py = w0*y0 + w1*y1 + w2*y2
#	pz = w0*z0 + w1*z1 + w2*z2
#
#	w2 = 1-w0-w1
#
#	w0*(x0-x2) + w1*(x1-x2) = px-x2
#	w0*(y0-y2) + w1*(y1-y2) = py-y2
#
#	a00*w0 + a01*w1 = b0
#	a10*w0 + a11*w1 = b1
#
#	det = a00*a11 - a01*a10
#
#	det*w0 = a11*b0 - a01*b1
#	det*w1 = -a10*b0 + a00*b1
#

def cornerWeights(pv, verts):
	r0 = verts[0]
	r1 = verts[1]
	r2 = verts[2]

	u01 = r1-r0
	u02 = r2-r0
	n = u01.cross(u02)
	n.normalize()

	u = pv-r0
	r = r0 + u - n*u.dot(n)

	'''
	print(list(pv))
	print(" r  ", list(r))
	print(" r0 ", list(r0))
	print(" r1 ", list(r1))
	print(" r2 ", list(r2))
	print(" n  ", list(n))
	'''

	a00 = r0[0]-r2[0]
	a01 = r1[0]-r2[0]
	a10 = r0[1]-r2[1]
	a11 = r1[1]-r2[1]
	b0 = r[0]-r2[0]
	b1 = r[1]-r2[1]
	
	det = a00*a11 - a01*a10

	w0 = (a11*b0 - a01*b1)/det
	w1 = (-a10*b0 + a00*b1)/det
	
	return (w0, w1, 1-w0-w1)

#
#	printProxy(path, faces):	
#
		
def printProxy(path, faces):	
	file = os.path.expanduser(path)
	fp= open(file, "w")

	fp.write("Verts\n")
	for (pv, verts, wts) in faces:
		fp.write("%5d %5d %5d %.5f %.5f %.5f\n" % (verts[0], verts[1], verts[2], wts[0], wts[1], wts[2]))
	proxy =  bpy.data.objects['Proxy'].data

	fp.write("Faces\n")
	for f in proxy.faces:
		for v in f.verts:
			fp.write("%d " % (v+1))
		fp.write("\n")

	fp.close()
	return

path = '~/makehuman/myproxy.proxy'
print("Doing %s" % path)
verts = findProxy()
printProxy(path, verts)
print("%s done" % path)


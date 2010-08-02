import bpy
import os

threshold = -0.2
mListLength = 2


def printMverts(stuff, mverts):
	for n in range(mListLength):
		(v,dist) = mverts[n]
		if v:
			print(stuff, v.index, dist)

def selectVert(vn, ob):
	bpy.context.scene.objects.active = ob
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.mode_set(mode='OBJECT')
	ob.data.verts[vn].selected = True
	return	

def findProxy(log):
	bob = bpy.data.objects['Human']
	pob = bpy.data.objects['Proxy']
	base = bob.data
	proxy = pob.data
	
	bestVerts = []
	for pv in proxy.verts:
		try:
			pindex = pv.groups[0].group
		except:
			pindex = -1
		if pindex < 0:
			vn = pv.index
			selectVert(vn, pob)
			raise NameError("Proxy vert %d not member of any group" % vn)

		name = pob.vertex_groups[pindex].name
		bindex = None
		for bvg in bob.vertex_groups:
			if bvg.name == name:
				bindex = bvg.index
		if bindex == None:
			raise NameError("Did not find vertex group %s in base mesh" % name)

		mverts = []
		for n in range(mListLength):
			mverts.append((None, 1e6))

		for bv in base.verts:
			if len(bv.groups) > 0 and bv.groups[0].group == bindex:
				vec = pv.co - bv.co
				n = 0
				for (mv,mdist) in mverts:
					if vec.length < mdist:
						for k in range(n+1, mListLength):
							j = mListLength-k+n
							mverts[j] = mverts[j-1]
						mverts[n] = (bv, vec.length)
						#print(bv.index)
						#printMverts(bv.index, mverts)
						break
					n += 1

		(mv, mindist) = mverts[0]
		if mv:
			print(pv.index, mv.index, mindist, name, pindex, bindex)
			log.write("%d %d %.5f %s %d %d\n" % (pv.index, mv.index, mindist, name, pindex, bindex))
			#printMverts("  ", mverts)
		else:
			raise NameError("Failed to find vert %d in group %s %s" % (pv.index, pindex, bindex))
		if mindist > 5:
			raise NameError("Minimal distance %f > 5.0. Check base and proxy scales." % mindist)

		bestVerts.append((pv, mverts, []))

	print("Setting up face table")
	vfaces = {}
	for f in base.faces:
		for v in f.verts:
			try:
				vfaces[v].append(f)
			except:
				vfaces[v] = [f]
	
	print("Finding weights")
	for (pv, mverts, fcs) in bestVerts:
		print(pv.index)
		for (bv,mdist) in mverts:
			if bv:
				for f in vfaces[bv.index]:
					verts = []
					for v in f.verts:
						verts.append(base.verts[v].co)
					wts = cornerWeights(pv, verts)
					fcs.append((f.verts, wts))

	print("Finding best weights")
	bestFaces = []
	for (pv, mverts, fcs) in bestVerts:
		print(pv.index)
		minmax = -1e6
		for (fverts, wts) in fcs:
			w = minWeight(wts)
			if w > minmax:
				minmax = w
				bWts = wts
				bVerts = fverts
		if minmax > threshold:
			bestFaces.append((pv, bVerts, bWts))	
		else:
			(mv, mdist) = mverts[0]
			bestFaces.append((pv, [mv.index,0,1], [1,0,0]))
				
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

	u = pv.co-r0
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
	if abs(det) < 1e-20:
		print("Proxy vert %d mapped to degenerate triangle (det = %g) with corners" % (pv.index, det))
		print("r0", r0[0], r0[1], r0[2])
		print("r1", r1[0], r1[1], r1[2])
		print("r2", r2[0], r2[1], r2[2])
		highlight(pv, 'Proxy')
		raise NameError("Singular matrix in cornerWeights")

	w0 = (a11*b0 - a01*b1)/det
	w1 = (-a10*b0 + a00*b1)/det
	
	return (w0, w1, 1-w0-w1)

#
#	highlight(pv, obname):
#

def highlight(pv, obname):
	ob = bpy.data.objects[obname]
	me = ob.data
	for v in me.verts:
		v.selected = False
	pv.selected = True
	return
	
#
#	printProxy(path, faces):	
#
		
def printProxy(path, faces):	
	file = os.path.expanduser(path)
	fp= open(file, "w")

	fp.write("Verts\n")
	for (pv, verts, wts) in faces:
		print(pv.index,verts,wts)
		fp.write("%5d %5d %5d %.5f %.5f %.5f\n" % (verts[0], verts[1], verts[2], wts[0], wts[1], wts[2]))

	'''
	proxy =  bpy.data.objects['Proxy'].data
	fp.write("Faces\n")
	for f in proxy.faces:
		for v in f.verts:
			fp.write("%d " % (v+1))
		fp.write("\n")
	'''
	fp.close()
	return

#
#
#

def printAll():
	path = '~/makehuman/myproxy.proxy'
	path = '/home/thomas/myproxy.proxy'
	print("Doing %s" % path)
	logfile = os.path.expanduser('~/makehuman/proxy.log')
	log = open(logfile, "w")
	verts = findProxy(log)
	log.close()
	printProxy(path, verts)
	print("%s done" % path)


printAll()	


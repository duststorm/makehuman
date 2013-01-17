#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Mesh Subdivision Plugin.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers, Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

__docformat__ = 'restructuredtext'

import time
import numpy as np

from module3d import Object3D
import log

class SubdivisionObject(Object3D):
    def __init__(self, object):
        name = object.name + '.sub'
        super(SubdivisionObject, self).__init__(name, 4)

        self.loc = object.loc.copy()
        self.rot = object.rot.copy()
        self.scale = object.scale.copy()
        self.cameraMode = object.cameraMode
        self.visibility = object.visibility
        self.pickable = object.pickable
        self.texture = object.texture
        self.shadeless = object.shadeless
        self.solid = object.solid
        self.transparentPrimitives = object.transparentPrimitives * 4
        self.object = object.object
        self.parent = object
        self.priority = object.priority

    def create(self, progressCallback):
        total = 19
        now = [time.time()]
        def progress(x):
            last = now[0]
            now[0] = time.time()
            log.debug('%d: %f', x, now[0] - last)
            if progressCallback:
                progressCallback(float(x)/total)

        progress(0)
        
        parent = self.parent
        nverts = len(parent.coord)
        ntexco = len(parent.texco)
        nfaces = len(parent.fvert)

        group_mask = np.ones(len(parent._faceGroups), dtype=bool)

        for g in parent._faceGroups:
            fg = self.createFaceGroup(g.name)
            if ('joint' in fg.name or 'helper' in g.name):
                group_mask[fg.idx] = False

        progress(1)

        face_mask = group_mask[parent.group]
        self.face_map = np.argwhere(face_mask)[...,0]
        self.face_rmap = np.zeros(nfaces, dtype=int) - 1
        nfaces = len(self.face_map)
        self.face_rmap[self.face_map] = np.arange(nfaces)

        progress(2)

        verts = parent.fvert[face_mask]
        vert_mask = np.zeros(nverts, dtype = bool)
        vert_mask[verts] = True
        self.vtx_map = np.argwhere(vert_mask)[...,0]
        vtx_rmap = np.zeros(nverts, dtype=int) - 1
        nverts = len(self.vtx_map)
        vtx_rmap[self.vtx_map] = np.arange(nverts)

        progress(3)

        uvs = parent.fuvs[face_mask]
        uv_mask = np.zeros(ntexco, dtype = bool)
        uv_mask[uvs] = True
        self.uv_map = np.argwhere(uv_mask)[...,0]
        uv_rmap = np.zeros(ntexco, dtype=int) - 1
        ntexco = len(self.uv_map)
        uv_rmap[self.uv_map] = np.arange(ntexco)

        progress(4)

        vedgelist = []
        vedgemap = {}
        fvert = vtx_rmap[parent.fvert[self.face_map]]
        vedges = np.dstack((fvert,np.roll(fvert,-1,axis=1)))
        fverts = []

        tedgelist = []
        tedgemap = {}
        fuv = uv_rmap[parent.fuvs[self.face_map]]
        tedges = np.dstack((fuv,np.roll(fuv,-1,axis=1)))
        fuvs = []

        groups = []

        self.cbase = nverts
        self.ebase = nverts + nfaces

        self.tcbase = ntexco
        self.tebase = ntexco + nfaces

        progress(5)

        fvedges2 = []
        ftedges2 = []

        for i, fi in enumerate(self.face_map):
            group = parent.group[fi]

            fvedges = []
            ftedges = []

            for (va,vb) in vedges[i]:
                if va > vb:
                    va,vb = vb,va
                p = va,vb

                vi = vedgemap.get(p)
                if vi is None:
                    vi = len(vedgelist)
                    vedgelist.append((p,(i,i)))
                    vedgemap[p] = vi
                else:
                    p,(j,_) = vedgelist[vi]
                    vedgelist[vi] = (p,(j,i))

                fvedges.append(vi)

            for j, (ta,tb) in enumerate(tedges[i]):
                if ta > tb:
                    ta,tb = tb,ta
                q = ta,tb

                ti = tedgemap.get(q)
                if ti is None:
                    ti = len(tedgelist)
                    tedgelist.append(q)
                    tedgemap[q] = ti

                ftedges.append(ti)

            fvedges2.append(fvedges)
            ftedges2.append(ftedges)

        progress(6)

        nfaces = len(self.face_map)

        self.fvert = np.empty((nfaces,4,4), dtype=np.uint32)
        self.fuvs  = np.empty((nfaces,4,4), dtype=np.uint32)
        self.group = np.empty((nfaces,4), dtype=np.uint32)

        # Create faces
        # v0  e0  v1
        # 
        # e3  c   e1
        #
        # v3  e2  v2

        self.fvert[:,:,0] = fvert
        self.fvert[:,:,2] = np.arange(nfaces)[:,None] + self.cbase

        self.fuvs[:,:,0] = fuv
        self.fuvs[:,:,2] = np.arange(nfaces)[:,None] + self.tcbase

        self.group[...] = parent.group[self.face_map][:,None]

        progress(7)

        fvedges2 = np.asarray(fvedges2, dtype=np.uint32) + self.ebase

        self.fvert[:,:,1] = fvedges2
        self.fvert[:,:,3] = np.roll(fvedges2,1,axis=-1)

        ftedges2 = np.asarray(ftedges2, dtype=np.uint32) + self.tebase

        self.fuvs[:,:,1] = ftedges2
        self.fuvs[:,:,3] = np.roll(ftedges2,1,axis=-1)

        progress(8)

        self.evert = np.asarray(vedgelist, dtype = np.uint32)
        self.etexc = np.asarray(tedgelist, dtype = np.uint32)

        self.vedge = np.zeros((nverts, self.MAX_FACES), dtype=np.uint32)
        self.nedges = np.zeros(nverts, dtype=np.uint8)

        progress(9)

        for i, (vab,_) in enumerate(self.evert):
            for v in vab:
                self.vedge[v, self.nedges[v]] = i
                self.nedges[v] += 1

        progress(10)

        nverts = self.ebase + len(vedgelist)

        self.coord = np.zeros((nverts, 3), dtype=np.float32)
        self.vnorm = np.zeros((nverts, 3), dtype=np.float32)
        self.color = np.zeros((nverts, 4), dtype=np.uint8) + 255
        self.vface = np.zeros((nverts, self.MAX_FACES), dtype=np.uint32)
        self.nfaces = np.zeros(nverts, dtype=np.uint8)

        self.ucoor = False
        self.unorm = False
        self.ucolr = False

        progress(11)

        ntexco = self.tebase + len(tedgelist)

        self.texco = np.zeros((ntexco, 2), dtype=np.float32)

        self.utexc = False

        progress(12)

        nfaces *= 4

        self.fvert = self.fvert.reshape((nfaces,4))
        self.fuvs  = self.fuvs.reshape((nfaces,4))
        self.group = self.group.reshape(nfaces)
        self.fnorm = np.zeros((nfaces,3))

        # nfaces = len(fverts)
        # 
        # self.fvert = np.asarray(fverts, dtype=np.uint32)
        # self.fnorm = np.zeros((nfaces, 3), dtype=np.float32)
        # self.fuvs  = np.asarray(fuvs, dtype=np.uint32)
        # self.group = np.asarray(groups, dtype=np.uint16)

        progress(13)

        self._update_faces()

        progress(14)

        self.updateIndexBuffer()

        progress(15)

        self.update_uvs()

        progress(16)

        self.update_coords()

        progress(17)

        self.calcNormals()

        progress(18)

        self.sync_all()

        progress(19)

    def dump(self):
        for k in dir(self):
            v = getattr(self, k)
            if isinstance(v, type(self.fvert)):
                fmt = '%.6f' if v.dtype in (np.float32, float) else '%d'
                if len(v.shape) > 2:
                    v = v.reshape((-1,v.shape[-1]))
                np.savetxt('dump/%s.txt' % k, v, fmt=fmt)

    def update_uvs(self):
        parent = self.parent

        btexc = self.texco[:self.tcbase]
        ctexc = self.texco[self.tcbase:self.tebase]
        etexc = self.texco[self.tebase:]

        ctexc[...] = np.sum(parent.texco[parent.fuvs[self.face_map]], axis=1) / 4

        iva = self.etexc[:,0]
        ivb = self.etexc[:,1]

        ptexco = parent.texco[self.uv_map]

        ta = ptexco[iva]
        tb = ptexco[ivb]
        etexc[...] = (ta + tb) / 2
        del iva, ivb, ta, tb

        btexc[...] = ptexco

        self.markUVs()

    def update_coords(self):
        parent = self.parent

        bvert = self.coord[:self.cbase]
        cvert = self.coord[self.cbase:self.ebase]
        evert = self.coord[self.ebase:]

        cvert[...] = np.sum(parent.coord[parent.fvert[self.face_map]], axis=1) / 4

        pcoord = parent.coord[self.vtx_map]

        iva = self.evert[:,0,0]
        ivb = self.evert[:,0,1]
        ic1 = self.evert[:,1,0]
        ic2 = self.evert[:,1,1]

        va = pcoord[iva]
        vb = pcoord[ivb]
        mvert = va + vb
        del iva, ivb, va, vb

        vc1 = cvert[ic1]
        vc2 = cvert[ic2]
        vc = vc1 + vc2
        del vc1, vc2

        inedge = (ic1 == ic2)

        evert[...] = np.where(inedge[:,None], mvert / 2, (mvert + vc) / 4)
        del ic1, ic2, vc

        nvface = parent.nfaces[self.vtx_map]

        # comment: this code could really do with some comments
        edgewt = np.arange(self.MAX_FACES)[None,:,None] < self.nedges[:,None,None]
        edgewt2 = edgewt * inedge[self.vedge][:,:,None]
        edgewt = edgewt / self.nedges.astype(np.float32)[:,None,None]
        nvedge = np.sum(edgewt2, axis=1)
        oevert = np.sum(mvert[self.vedge] * edgewt / 2, axis=1)
        oevert2 = np.sum(mvert[self.vedge] * edgewt2 / 2, axis=1)
        facewt = np.arange(self.MAX_FACES)[None,:,None] < nvface[:,None,None]
        facewt = facewt / nvface.astype(np.float32)[:,None,None]
        ofvert = np.sum(cvert[self.face_rmap[parent.vface[self.vtx_map]]] * facewt, axis=1)
        opvert = pcoord

        valid = nvface >= 3

        bvert[...] = np.where(valid[:,None],
                              np.where((self.nedges == nvface)[:,None],
                                       (ofvert + 2 * oevert + (nvface[:,None] - 3) * opvert) / nvface[:,None],
                                       (oevert2 + opvert) / (nvedge + 1)),
                              (3 * oevert - ofvert) / 2)

        self.markCoords(coor=True)

    def update(self):
        self.update_coords()
        super(SubdivisionObject, self).update()

def createSubdivisionObject(object, progressCallback=None):
    obj = SubdivisionObject(object)
    obj.create(progressCallback)
    # obj.dump()
    return obj

def updateSubdivisionObject(object, progressCallback=None):
    object.update()
    object.calcNormals()
    object.sync_all()

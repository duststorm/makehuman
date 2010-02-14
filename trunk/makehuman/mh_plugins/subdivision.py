#!/usr/bin/python
# -*- coding: utf-8 -*-
# You may use, modify and redistribute this module under the terms of the GNU GPL.

""" 
Mesh Subdivision Plugin.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements a plugin to subdivide a mesh object. This enables a 
considerable degree of smoothing to be performed on the mesh before it is 
exported to external rendering engines.

The subdivided mesh object is created as a new object that is separate 
and distinct from the original object upon which it is based. New vertices 
are created both at the locations of the original vertices and at the 
midpoints along the edges of ajoining vertices.
 
The positions of all of the vertices in the new object are adjusted and 
recalculated in order to create a smoothed copy of the original mesh.

Requires:

- base modules

"""

__docformat__ = 'restructuredtext'

import time
import module3d


def newSubVert1(v, object):
    """
    This function adds a new subdivision vertex into the list of vertices.
    It calls the constructor on the Vert class to initialize a new vertex
    based upon settings copied from an existing vertex. It adds attributes 
    to identify that the new vertex is a sub-division vertex.
    It calls the *calcSubCoord1* function to adjust the position and normal
    of the new vertex based upon the surrounding vertices 
    (effectively rounding off the corners and smoothing the mesh). 
     
    The new vertex is returned to the calling function.
    
    Parameters
    ----------
   
    v:     
      *Vert*.  An existing vertex.
    objIdx:     
      *integer*.  The index of the new Object3D object that will end up containing a copy of this vertex.
    """

    loopVertices = v.vertsShared()
    vSubd = module3d.Vert(v.co, v.idx, object)
    vSubd.sub_type = 1
    n = len(loopVertices)

    if n == 3:
        b = 0.1875
        a = 1 - n * b
    elif n > 3:
        b = 3.0 / (8 * n)
        a = 1.0 - n * b
    else:
        a = 0.75  # 3/4
        b = 0.125  # 1/8
    vSubd.sub_data = [v, a, b, loopVertices]

    calcSubCoord1(vSubd)
    return vSubd


def calcSubCoord1(vSubd):
    """
    This function calculates or re-calculates the new position and normal for a sub-division 
    vertex that is based upon an existing (non-subdivided) vertex position. It does this 
    by considering the original positions and normals of all of the 
    surrounding vertices from the original object.
    
    A vertex based on a position occupied by a vertex in the original object before it was 
    sub-divided is known as a sub_type 1 vertex.
    
    Parameters
    ----------
   
    vSubd:     
      *Vert*.  A vertex with some additional attributes added to identify it as a sub-division vertex.
    """

    v = vSubd.sub_data[0]
    a = vSubd.sub_data[1]
    b = vSubd.sub_data[2]
    loopVertices = vSubd.sub_data[3]
    subdX = a * v.co[0]
    subdY = a * v.co[1]
    subdZ = a * v.co[2]
    noX = a * v.no[0]
    noY = a * v.no[1]
    noZ = a * v.no[2]

    # texU = a*v.uv[0]
    # texV = a*v.uv[1]

    for lv in loopVertices:
        subdX += b * lv.co[0]
        subdY += b * lv.co[1]
        subdZ += b * lv.co[2]
        noX += b * lv.no[0]
        noY += b * lv.no[1]
        noZ += b * lv.no[2]

        # texU += b*lv.uv[0]
        # texV += b*lv.uv[1]

    vSubd.co = [subdX, subdY, subdZ]
    vSubd.no = [noX, noY, noZ]


    # vSubd.uv = [texU,texV]
    # vSubd.color = v.color


def calcSubCoord2(vSubd):
    """
    This function calculates or re-calculates the new position 
    and normal for a sub-division vertex that is positioned in 
    the middle of an edge on the original object (second instance).
     
    Each 'edge' vertex can potentially be shared by two faces, so can 
    potentially be encountered twice during the calculation sequence.
    The sub_type is used to differentiate between two occurrences of 
    the same 'edge' vertex. This function handles a sub_type 2 vertex 
    which means that it was the second instance encountered in the 
    original calculation sequence.
        
    Parameters
    ----------
   
    vSubd:     
      *Vert*.  A vertex with some additional attributes added to identify it as a sub-division vertex.
    """

    v1 = vSubd.sub_data[0]
    v2 = vSubd.sub_data[1]
    v3 = vSubd.sub_data[2]
    v4 = vSubd.sub_data[3]
    subdX = 0.375 * (v1.co[0] + v2.co[0]) + 0.125 * (v3.co[0] + v4.co[0])
    subdY = 0.375 * (v1.co[1] + v2.co[1]) + 0.125 * (v3.co[1] + v4.co[1])
    subdZ = 0.375 * (v1.co[2] + v2.co[2]) + 0.125 * (v3.co[2] + v4.co[2])
    noX = 0.375 * (v1.no[0] + v2.no[0]) + 0.125 * (v3.no[0] + v4.no[0])
    noY = 0.375 * (v1.no[1] + v2.no[1]) + 0.125 * (v3.no[1] + v4.no[1])
    noZ = 0.375 * (v1.no[2] + v2.no[2]) + 0.125 * (v3.no[2] + v4.no[2])

    # texU = 0.375*(v1.uv[0] + v2.uv[0]) + 0.125*(v3.uv[0] + v4.uv[0])
    # texV = 0.375*(v1.uv[1] + v2.uv[1]) + 0.125*(v3.uv[1] + v4.uv[1])
    # r = (v1.color[0] + v2.color[0])/2
    # g = (v1.color[1] + v2.color[1])/2
    # b = (v1.color[2] + v2.color[2])/2
    # a = (v1.color[3] + v2.color[3])/2

    vSubd.co = [subdX, subdY, subdZ]
    vSubd.no = [noX, noY, noZ]


    # vSubd.uv = [texU,texV]
    # vSubd.color = [r,g,b,a]


def calcSubCoord3(vSubd):
    """
    This function calculates or re-calculates the new position 
    and normal for a sub-division vertex that is positioned in 
    the middle of an edge on the original object (second instance).
     
    Each 'edge' vertex can potentially be shared by two faces, so can 
    potentially be encountered twice during the calculation sequence.
    The sub_type is used to differentiate between two occurrences of 
    the same 'edge' vertex. This function handles a sub_type 3 vertex 
    which means that it was the first instance encountered in the 
    original calculation sequence.
        
    Parameters
    ----------
   
    vSubd:     
      *Vert*.  A vertex with some additional attributes added to identify it as a sub-division vertex.
    """

    v1 = vSubd.sub_data[0]
    v2 = vSubd.sub_data[1]

    subdX = 0.5 * (v1.co[0] + v2.co[0])
    subdY = 0.5 * (v1.co[1] + v2.co[1])
    subdZ = 0.5 * (v1.co[2] + v2.co[2])
    noX = 0.5 * (v1.no[0] + v2.no[0])
    noY = 0.5 * (v1.no[1] + v2.no[1])
    noZ = 0.5 * (v1.no[2] + v2.no[2])

    # texU = 0.5*(v1.uv[0] + v2.uv[0])
    # texV = 0.5*(v1.uv[1] + v2.uv[1])
    # r = (v1.color[0] + v2.color[0])/2
    # g = (v1.color[1] + v2.color[1])/2
    # b = (v1.color[2] + v2.color[2])/2
    # a = (v1.color[3] + v2.color[3])/2

    vSubd.co = [subdX, subdY, subdZ]
    vSubd.no = [noX, noY, noZ]


    # vSubd.uv = [texU,texV]
    # vSubd.color = [r,g,b,a]


def subdivide(ob, scene):
    """
    This function checks for the existence of a subdivided version of the 
    Object3D object specified (within the specified Scene3D object) and, 
    if found, updates the sub-division vertex information (otherwise it 
    creates a new subdivided version of the Object3D object).
     
    The subdivided object is identified by appending the string \".sub\" to 
    the end of the name of the original object. 
    
    Parameters
    ----------
   
    ob:     
      *Object3D*.  The object to subdivide.
    scene:     
      *Scene3D*.  The scene object containing the object to subdivide.
    """

    t = time.time()
    subdividedObj = scene.getObject(ob.name + '.sub')
    if subdividedObj:
        print 'Sub data present'
        for v in subdividedObj.verts:
            if v.sub_type == 1:
                calcSubCoord1(v)
            if v.sub_type == 2:
                calcSubCoord2(v)
            if v.sub_type == 3:
                calcSubCoord3(v)
            v.update()
    else:

        print 'Calculating sub data'
        calcSubData(ob, scene)
    print 'time for subdivision: %s' % (time.time() - t)


def addEdgeVert(v0, v1, v2, face, edges, object):
    """
    This function adds a sub-division vertex in the middle of an edge. 
    It is called from the calcSubData function which loops through every edge of 
    every face.
    
    As a consequence, each sub-division vertex can be encountered twice because 
    two adjoining faces share an edge and therefore share the corresponding 
    sub-division vertex.

    This function therefore defines a sub_type for each copy of the vertex where:
    
      - *sub_type 2* signifies that this vertex has already been calculated
      - *sub_type 3* signifies that this is the first encounter with this vertex
    
    
    
    Parameters
    ----------
   
    v0:     
      *Vert*.  The first vertex of the face.
    v1:     
      *Vert*.  The second vertex of the face.
    v2:     
      *Vert*.  The third vertex of the face.
    face:     
      *Face*.  The face on which this edge sits.
    edges:     
      *list of edge names*.  The edges processed so far in this cycle (used to establish whether this edge has already been processed).
    object:     
      *Object3D*.  The object containing the face to be subdivided.
    """

    # Just make an unique key

    if v0.idx > v1.idx:
        key = str(v0.idx) + '-' + str(v1.idx)
        edge = [v0, v1]
    else:
        key = str(v1.idx) + '-' + str(v0.idx)
        edge = [v1, v0]

    if not edges.has_key(key):
        vSubd = module3d.Vert([0, 0, 0], -1, object)
        vSubd.sub_data = edge + [v2]
        vSubd.sub_type = 3
        edges[key] = vSubd
    else:
        vSubd = edges[key]
        vSubd.sub_type = 2
        vSubd.sub_data.append(v2)

    face.sub_verts.append(vSubd)


def calcSubData(ob, scene):
    """
    This function creates a new Object3D object which is a sub-divided 
    copy of an existing object, adding it into the Scene3D object that 
    is a parent of the original object. 

    First it creates new vertices based upon the vertices from the original
    object, but with positions and normals that have been adjusted (smoothed).
    Next it loops through the faces in the original object adding an additional 
    vertex in the middle of each edge.
    
    Finally it fills in all of the remaining information necessary to complete 
    the new object (including generating four new faces to sub-divide each of 
    the triangular faces from the original object), makes the subdivided 
    object the currently selected object in the scene and redraws the scene.
    
    Parameters
    ----------
   
    ob:     
      *Object3D*.  The original object to be copied and subdivided.
    scene:     
      *Scene3D*.  The scene object containing the original Object3D object and new, sub-divided Object3D object.
    """

    t1 = time.time()
    subObjName = ob.name + '.sub'

    t3 = time.time()
    subdividedObj = scene.newObj(subObjName)
    subdividedObj.x = ob.x
    subdividedObj.y = ob.y
    subdividedObj.z = ob.z
    subdividedObj.rx = ob.rx
    subdividedObj.ry = ob.ry
    subdividedObj.rz = ob.rz
    subdividedObj.sx = ob.sx
    subdividedObj.sy = ob.sy
    subdividedObj.sz = ob.sz
    subdividedObj.visibility = ob.visibility
    subdividedObj.shadeless = ob.shadeless
    subdividedObj.pickable = ob.pickable
    subdividedObj.cameraMode = ob.cameraMode
    subdividedObj.text = ob.text
    subdividedObj.uvValues = ob.uvValues[:]
    subdividedObj.indexBuffer = []
    for v in ob.verts:
        vSubd = newSubVert1(v, subdividedObj)
        subdividedObj.verts.append(vSubd)

        # subdividedObj.colors.append([v.color[0],v.color[1], v.color[2], v.color[3]])

    print 'time to create new obj and map verts: ', time.time() - t3

    t4 = time.time()
    edgeVerts = {}
    for f in ob.faces:
        f.sub_verts = []
        v0 = f.verts[0]
        v1 = f.verts[1]
        v2 = f.verts[2]
        addEdgeVert(v0, v1, v2, f, edgeVerts, subdividedObj)
        addEdgeVert(v1, v2, v0, f, edgeVerts, subdividedObj)
        addEdgeVert(v2, v0, v1, f, edgeVerts, subdividedObj)

    for ev in edgeVerts.values():
        if ev.sub_type == 3:
            calcSubCoord3(ev)
        if ev.sub_type == 2:
            calcSubCoord2(ev)
        ev.idx = len(subdividedObj.verts)
        subdividedObj.verts.append(ev)

            # subdividedObj.colors.append([ev.color[0],ev.color[1], ev.color[2], ev.color[3]])

    print 'time to add edge verts: ', time.time() - t4

    fg = module3d.FaceGroup('subobj')
    fg.parent = subdividedObj
    subdividedObj.facesGroups.append(fg)
    fullArrayIndex = 0
    groupVerts = {}
    for f in ob.faces:
        v0 = subdividedObj.verts[f.verts[0].idx]
        v2 = subdividedObj.verts[f.verts[1].idx]
        v4 = subdividedObj.verts[f.verts[2].idx]
        v1 = f.sub_verts[0]
        v3 = f.sub_verts[1]
        v5 = f.sub_verts[2]

        f1 = module3d.Face(v0, v1, v5)
        f2 = module3d.Face(v1, v2, v3)
        f3 = module3d.Face(v1, v3, v5)
        f4 = module3d.Face(v5, v3, v4)

        # Simple UV linear interpolation: uv are not subdivided

        if f.uv:
            uv0 = subdividedObj.uvValues[f.uv[0]]
            uv2 = subdividedObj.uvValues[f.uv[1]]
            uv4 = subdividedObj.uvValues[f.uv[2]]
            uv1 = len(subdividedObj.uvValues)
            subdividedObj.uvValues.append([uv0[0] + (uv2[0] - uv0[0]) * 0.5, uv0[1] + (uv2[1] - uv0[1]) * 0.5])
            uv3 = len(subdividedObj.uvValues)
            subdividedObj.uvValues.append([uv2[0] + (uv4[0] - uv2[0]) * 0.5, uv2[1] + (uv4[1] - uv2[1]) * 0.5])
            uv5 = len(subdividedObj.uvValues)
            subdividedObj.uvValues.append([uv4[0] + (uv0[0] - uv4[0]) * 0.5, uv4[1] + (uv0[1] - uv4[1]) * 0.5])
            uv0 = f.uv[0]
            uv2 = f.uv[1]
            uv4 = f.uv[2]

            f1.uv = [uv0, uv1, uv5]
            f2.uv = [uv1, uv2, uv3]
            f3.uv = [uv1, uv3, uv5]
            f4.uv = [uv5, uv3, uv4]

        faces = [f1, f2, f3, f4]

        for f in faces:
            for (i, v) in enumerate(f.verts):
                t = f.uv[i]
                if v.idx not in groupVerts:
                    v.indicesInFullVertArray.append(fullArrayIndex)
                    groupVerts[v.idx] = {}
                    groupVerts[v.idx][t] = fullArrayIndex
                    subdividedObj.indexBuffer.append(fullArrayIndex)
                    fullArrayIndex += 1
                elif t not in groupVerts[v.idx]:
                    v.indicesInFullVertArray.append(fullArrayIndex)
                    groupVerts[v.idx][t] = fullArrayIndex
                    subdividedObj.indexBuffer.append(fullArrayIndex)
                    fullArrayIndex += 1
                else:
                    subdividedObj.indexBuffer.append(groupVerts[v.idx][t])

            f.group = fg
            fg.faces.append(f)
            subdividedObj.faces.append(f)

    subdividedObj.vertexBufferSize = fullArrayIndex
    subdividedObj.texture = ob.texture

    scene.update()
    print 'Time to calc and send subdata: ', time.time() - t1



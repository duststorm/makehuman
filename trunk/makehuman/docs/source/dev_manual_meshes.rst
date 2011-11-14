
.. highlight:: python
   :linenothreshold: 5

.. _meshes:

Meshes
======


When writing exporters, subdivision or polygon reducing algorithms it can be useful
to know how the mesh is stored in Python (the C side has a different compact but
less convenient representation). An Object3D has three important lists: object.verts,
object.faces and object.faceGroups. The first two lists contain instances of Vertex and
Face. The facesGroups contain FaceGroup objects. A FaceGroup specifies the name
of the group and the faces that make up the group. A Face references 3 vertices in
face.verts. A Vert or vertex holds its coordinates in vert.co and normal in vert.no. If we
put all this together, we can write a simple Wavefront object exporter now

::


    f = open(filename,'w')
    for v in obj.verts:
        f.write("v %f %f %f\n" %tuple(v.co))

    for uv in obj.uvValues:
        f.write("vt %f %f\n" %tuple(uv))

    for g in obj.faceGroups:
        f.write("g %s\n" %(g.name))
        for fc in g.faces:
            f.write("f")
            for v in fc.verts:
                f.write(" %i/%i/%i " %(v.idx + 1, fc.uv[i] + 1, v.idx + 1))
    f.close()



As you can see, we take the uv values from obj.uvValues. The uv values are referenced
in two places, obj.uvValues holds all the uv values of each vertex by index.
Face.uv is a list with the uv values of each vertex of the face. The reason is that while
normals are per vertex, uv values are per facevertex, because a vertex can have a different
uv depending on which face is drawn.

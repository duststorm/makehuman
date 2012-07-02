import Blender
from Blender import Scene, Curve, Object #, Mesh, Effect
scn= Scene.GetCurrent()
for object in scn.objects.selected:
    #1: Get c.p. of each edge
    mesh=object.getData()
    cu = Curve.New(mesh.name)
    point = mesh.verts[0].co
    cu.appendNurb([point[0],point[1],point[2],1])
    #endpoints are added twice to attach curves to the surface
    for v in mesh.verts:
        cu[0].append([v.co[0],v.co[1],v.co[2],1])
    N = len(mesh.verts)
    point = mesh.verts[N-1].co
    cu[0].append([point[0],point[1],point[2],1])
    scn.objects.unlink(object)
    scn.objects.new(cu)
Blender.Redraw()

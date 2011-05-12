import Blender
from Blender import Mesh, Scene

def drawBox(scn, bounds, name="Cube"):
  x = bounds[1][0]-bounds[0][0]
  mesh = Mesh.Primitives.Cube(x)
  verts = mesh.verts
  for v in verts:
    v.co[1] = v.co[1]*(bounds[1][1]-bounds[0][1])/x
    v.co[2] = v.co[2]*(bounds[1][2]-bounds[0][2])/x
    
  center = [0.5*(bounds[0][0]+bounds[1][0]),0.5*(bounds[0][1]+bounds[1][1]),0.5*(bounds[0][2]+bounds[1][2])]
  obj = scn.objects.new(mesh,name)
  obj.setLocation(*center)

  
scn = Scene.GetCurrent() #get current scene

bboxj =[[1.3661949999999998, 4.5287560000000004, -1.1008855], [1.891527, 5.988215499999999, 0.31737949999999998]]

drawBox(scn, bboxj)

bboxl = [[1.891527, 4.5287560000000004, -1.1008855], [4.0522844999999998, 5.988215499999999, 0.31737949999999998]]

drawBox(scn, bboxl)

Blender.Redraw()
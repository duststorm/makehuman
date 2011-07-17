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

bboxj1 = [[1.2894580000000002, 4.6063499999999999, -0.69851099999999999], [1.51987275, 5.9755405000000001, 0.62123800000000007]]
bboxj2 = [[1.51987275, 4.6063499999999999, -0.69851099999999999], [2.4649654999999999, 5.9755405000000001, 0.62123800000000007]]

drawBox(scn, bboxj1)
drawBox(scn, bboxj2)

Blender.Redraw()

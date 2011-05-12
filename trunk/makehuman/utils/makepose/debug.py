import Blender
from Blender import Mesh, Scene

def drawCube(scn, bounds, name="Cube"):
	mesh = Mesh.Primitives.Cube(bounds[0][0]-bounds[1][0])
	center = [0.5*(bounds[0][0]+bounds[1][0]),0.5*(bounds[0][1]+bounds[1][1]),0.5*(bounds[0][2]+bounds[1][2])]
	obj = scn.objects.new(mesh,name)
	obj.setLocation(*center)

  
scn = Scene.GetCurrent() #get current scene

bboxj =[[1.3661949999999998, 4.5387560000000002, -1.0908855], [1.9384319999999999, 5.9782154999999992, 0.30737949999999997]]

drawCube(scn, bboxj)

bboxl = [[1.844622, 4.9297319999999996, -0.94940899999999995], [4.0522844999999998, 5.8845669999999997, 0.151307]]

drawCube(scn, bboxl)

Blender.Redraw()
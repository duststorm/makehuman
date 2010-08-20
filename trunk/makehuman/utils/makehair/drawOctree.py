import Blender, math, sys, random
#from datetime import datetime
from Blender import Window, Scene, Curve, Object, Mesh
mainPath = Blender.sys.dirname(Blender.Get('filename'))
sys.path.append(mainPath)
import simpleoctree

def world2Local(vec, matrix):
    x, y, z = vec
    xloc, yloc, zloc = matrix[3][0], matrix[3][1], matrix[3][2]
    return  [x*matrix[0][0] + y*matrix[0][1] + z*matrix[0][2] - xloc,\
            x*matrix[1][0] + y*matrix[1][1] + z*matrix[1][2] - yloc,\
            x*matrix[2][0] + y*matrix[2][1] + z*matrix[2][2] - zloc]

def drawCube(scn, bounds, name):
    mesh = Mesh.Primitives.Cube(bounds[0][0]-bounds[1][0])
    center = [0.5*(bounds[0][0]+bounds[1][0]),0.5*(bounds[0][1]+bounds[1][1]),0.5*(bounds[0][2]+bounds[1][2])]
    obj = scn.objects.new(mesh,name)
    obj.setLocation(*center)

def drawOctree(root,mat,scn):
    point1 = world2Local(root.bounds[0],mat)
    point2 = world2Local(root.bounds[6],mat)
    if len(root.children)==0 and not len(root.verts)==0: drawCube(scn,[point1,point2],"")
    for i in range(0,len(root.children)):
        drawOctree(root.children[i],mat,scn)

base = Blender.Object.Get("Base")
octree = simpleoctree.SimpleOctree(base.getData().verts,0.08)
scn = Scene.GetCurrent() #get current scene
drawOctree(octree.root,base.getMatrix(),scn)
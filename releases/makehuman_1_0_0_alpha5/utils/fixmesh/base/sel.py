import Blender
from Blender import *

editmode = Window.EditMode()    # are we in edit mode?  If so ...
if editmode: Window.EditMode(0) # leave edit mode before getting the mesh

scn = Scene.GetCurrent()
ob = scn.objects.active
me = ob.getData(0, 1)
for v in me.verts:
	if v.sel:
		print v.index


 
 

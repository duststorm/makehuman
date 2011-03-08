import Blender
from Blender import Object

def getSelectedVertices():
    selectedVertices = []
	ob = Object.Get("Human")
    for i,v in enumerate(obj.verts):
        if v.sel == 1:
            selectedVertices.append(i)
    return selectedVertices
	
def getVertGroups():
    vertGroups = {}
	obj = Object.Get("Human").getData(mesh=True)
    vertGroupNames = obj.getVertGroupNames()
    for n in vertGroupNames:
        vertGroups[n] = obj.getVertsFromGroup(n)
    return vertGroups
	
def getSelectedGroup(verts, vertGroups)
	selectedGroups=[]
	for v in verts:
		for key in vertGroups.keys():
			if (v in vertGroups[k]):
				if (k not in selectedGroups): v.append(k)
				break
	return selectedGroups
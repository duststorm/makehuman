from Blender import Object

def getSelectedVertices():
    selectedVertices = []
    ob = Object.Get("HumanMesh").getData()
    for i,v in enumerate(ob.verts):
        if v.sel == 1:
            selectedVertices.append(i)
    return selectedVertices
	
def getVertGroups():
    vertGroups = {}
    obj = Object.Get("HumanMesh").getData(mesh=True)
    vertGroupNames = obj.getVertGroupNames()
    for n in vertGroupNames:
        vertGroups[n] = obj.getVertsFromGroup(n)
    return vertGroups
	
def getSelectedGroup(verts, vertGroups):
	selectedGroups=[]
	for v in verts:
		for key in vertGroups.keys():
			if (v in vertGroups[key]):
				if (key not in selectedGroups): selectedGroups.append(key)
				break
	return selectedGroups

vertGroups = getVertGroups();
verts = getSelectedVertices();
print getSelectedGroup(verts, vertGroups)
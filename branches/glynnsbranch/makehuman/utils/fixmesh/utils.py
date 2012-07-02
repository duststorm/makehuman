import Blender
from Blender import *

def wipeVertGroups():
	Window.EditMode(1)
	Window.EditMode(0)
	ob = Object.Get("Human")
	me = ob.getData(mesh=1)
	vlist = []
	for v in me.verts:
		if v.sel:
			vlist.append(v.index)
	if vlist == []:
		Window.EditMode(1)
		return
	grps = me.getVertGroupNames()
	for g in grps:
		me.removeVertsFromGroup(g, vlist)
	Window.EditMode(1)
	return

def removeAllVertGroups():
	Window.EditMode(0)
	ob = Object.Get("Human")
	me = ob.getData(mesh=1)
	grps = me.getVertGroupNames()
	for g in grps:
		me.removeVertGroup(g)
	Window.EditMode(1)
	return

def cleanGroup(g):
	Window.EditMode(0)
	ob = Object.Get("Human")
	me = ob.getData(mesh=1)
	me.removeVertGroup(g)
	Window.EditMode(1)
	return


def findSelected():
	Window.EditMode(0)
	me = Mesh.Get("Human")
  print "Selected"
	for v in me.verts:
		if v.sel:
			print v.index
	print "end"
	Window.EditMode(1)
	return

def selectVertex(n):
	Window.EditMode(0)
	me = Mesh.Get("new")
	print "Selected"
	for v in me.verts:
		v.sel = 0
		if v.index == n:
			v.sel = 1
	print "end"
	Window.EditMode(1)
	return

def assignWeighted(w, g1, g2):
	Window.EditMode(0)
	ob = Object.Get("Human")
	me = ob.getData(mesh=1)
	vlist = []
	for v in me.verts:
		if v.sel:
			vlist.append(v.index)
	if vlist == []:
		Window.EditMode(1)
		return
	print vlist
	me.assignVertsToGroup(g1, vlist, w, Mesh.AssignModes.REPLACE)
	me.assignVertsToGroup(g2, vlist, 1-w, Mesh.AssignModes.REPLACE)
	Window.EditMode(1)
	
		
	
#assignWeighted(1.0, 'Hips', 'UpLegTwist_L')
#cleanGroup('Genitalia')
#wipeVertGroups()
#removeAllVertGroups()			
findSelected()

#selectVertex(6668)
from Blender import Object, Window, Draw, BGL
from Blender.BGL import *

def getSelectedVertices():
    selectedVertices = []
    ob = Object.GetSelected()[0].getData()
    for v in ob.verts:
        if (v.sel):
            selectedVertices.append(v.index)
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

def saveSelVerts(path):
    """
    This function saves the indices of selected verts

    Parameters
    ----------

    filePath:
        *string*. A string containing the operating system path to the
        file to be written.

    """
    try:
        fileDescriptor = open(path, "w")
    except:
        print "Unable to open %s"%(path)
        return  None
    selectVerts = getSelectedVertices()
    for v in selectVerts:
        fileDescriptor.write("%d\n"%(v))
    fileDescriptor.close()

def loadSelVerts(path):
    """
    This function load the indices of selected verts

    Parameters
    ----------

    filePath:
        *string*. A string containing the operating system path to the
        file to be written.

    """
    selectedIndices = []
    try:
        fileDescriptor = open(path)
    except:
        print "Unable to open %s"%(path)
        return  None
    for vData in fileDescriptor:
        i = int(vData.split()[0])
        selectedIndices.append(i)
    fileDescriptor.close()
    return selectedIndices

    
def event(event, value):
    """
    This function handles keyboard events when the escape key or the 's' key
    is pressed to exit or save the morph target file.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed
    value:
        *int*. A value **EDITORIAL NOTE: Need to find out what this is used for**

    """
    if event == Draw.ESCKEY and not value: Draw.Exit()
    elif event == Draw.SKEY:
        Window.FileSelector (saveSelVerts, "Save index of selected vertices")
    elif event == Draw.LKEY:
        Window.FileSelector (loadSelVerts, "Load index of verts to select")
    Draw.Draw()

def buttonEvents(event):
    """
    This function handles events when the morph target is being processed.

    Parameters
    ----------

    event:
        *int*. An indicator of the event to be processed

    """
    if event == 0: pass
    Draw.Draw()

    
def draw():
    """
    This function draws the morph target on the screen and adds buttons to
    enable utility functions to be called to process the target.

    **Parameters:** This method has no parameters.

    """
    glClearColor(0.5, 0.5, 0.5, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2i(10, 300)
    Draw.Text("Utilities")

    glColor3f(0.5, 0.0, 0.0)
    glRasterPos2i(10, 250)

Draw.Register(draw, event, buttonEvents)

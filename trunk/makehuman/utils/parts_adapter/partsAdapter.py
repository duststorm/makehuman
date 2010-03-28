import sys
import os
import math

dir_input = ""                      #input directory
dir_output = ""                     #output directory
vertgroups = "data.vertgroups"      #filename for vertsgroup
max_vert = 0;                       #max num of verts
external_group = []                 #verts of the skin
g_transf = []                       #verts group to adapt
vpairs = []                         #array of pairs for near verts
originalVerts = []                  #original base mesh coords

mesh_actual   = None                #class mesh for the working mesh
mesh_original = None                #class mesh for the original mesh

stringGroup = ["eye_left","eye_right","mouth","el_lt1","el_lt2","el_lt3","el_lt4","el_lt5","el_lt6","el_lt7","el_lt8","el_lt9","el_lt10","el_lt11","el_lt12","el_lt13","el_lb1","el_lb2","el_lb3","el_lb4","el_lb5","el_lb6","el_lb7","el_lb8","el_lb9","el_lb10","el_lb11","el_lb12","el_rt1","el_rt2","el_rt3","el_rt4","el_rt5","el_rt6","el_rt7","el_rt8","el_rt9","el_rt10","el_rt11","el_rt12","el_rt13","el_rb1","el_rb2","el_rb3","el_rb4","el_rb5","el_rb6","el_rb7","el_rb8","el_rb9","el_rb10","el_rb11","el_rb12","joint-head","joint-mouth","joint-neck","joint-l-finger-1-1","joint-l-finger-1-2","joint-l-finger-1-3","joint-l-finger-2-1","joint-l-finger-2-2","joint-l-finger-2-3","joint-l-finger-3-1","joint-l-finger-3-2","joint-l-finger-3-3","joint-l-finger-4-1","joint-l-finger-4-2","joint-l-finger-4-3","joint-l-finger-5-1","joint-l-finger-5-2","joint-l-finger-5-3","joint-l-hand","joint-l-knee","joint-l-shoulder","joint-l-toe-1-1","joint-l-toe-1-2","joint-l-toe-2-1","joint-l-toe-2-2","joint-l-toe-2-3","joint-l-toe-3-1","joint-l-toe-3-2","joint-l-toe-3-3","joint-l-toe-4-1","joint-l-toe-4-2","joint-l-toe-4-3","joint-l-toe-5-1","joint-l-toe-5-2","joint-l-toe-5-3","joint-l-ankle","joint-l-clavicle","joint-l-elbow","joint-l-upper-leg","joint-pelvis","joint-r-ankle","joint-r-clavicle","joint-r-elbow","joint-r-finger-1-1","joint-r-finger-1-2","joint-r-finger-1-3","joint-r-finger-2-1","joint-r-finger-2-2","joint-r-finger-2-3","joint-r-finger-3-1","joint-r-finger-3-2","joint-r-finger-3-3","joint-r-finger-4-1","joint-r-finger-4-2","joint-r-finger-4-3","joint-r-finger-5-1","joint-r-finger-5-2","joint-r-finger-5-3","joint-r-hand","joint-r-knee","joint-r-shoulder","joint-r-upper-leg","joint-spine1","joint-spine2","joint-spine3","joint-r-toe-1-1","joint-r-toe-1-2","joint-r-toe-2-1","joint-r-toe-2-2","joint-r-toe-2-3","joint-r-toe-3-1","joint-r-toe-3-2","joint-r-toe-3-3","joint-r-toe-4-1","joint-r-toe-4-2","joint-r-toe-4-3","joint-r-toe-5-1","joint-r-toe-5-2","joint-r-toe-5-3","joint-l-eye","joint-r-eye"]                    #Namegroups to adapt

class vert:
    """
    Class that represents the vertex, with coordinates in coo and index in index
    """
    co = []
    index = 0

    def __init__(self, co, index):
        self.co = co
        self.index = index

class mesh:
    """
    Class that represents the mesh, manages the coordinate transformation from base to target
    """
    coor_base = []
    coor_targ = []

    def add(self, targ):
        """
        Add vertex entry in mesh class
        """
        index = targ.index;
        x = targ.co[0] + originalVerts[index][0]
        y = targ.co[1] + originalVerts[index][1]
        z = targ.co[2] + originalVerts[index][2]
        v = vert([x, y, z], index)
        self.coor_base.append(v)
        self.coor_targ.append(targ)

    def setElement(self, v):
        """
        Set vertex entry in mesh class
        """
        index = v.index;
        x = v.co[0] + originalVerts[index][0]
        y = v.co[1] + originalVerts[index][1]
        z = v.co[2] + originalVerts[index][2]
        vrt = vert([x, y, z], index)
        self.coor_base[index] = vrt
        self.coor_targ[index] = v

    def getBaseAt(self, index):
        """
        Return base coords in index position
        """
        return self.coor_base[index]

    def getBase(self):
        """
        Return base coords
        """
        return self.coor_base

    def getTargAt(self, index):
        """
        Return target coords in index position
        """
        return self.coor_targ[index]

    def getTarg(self):
        """
        Return target coords
        """
        return self.coor_targ

    def __init__(self):
        self.coor_base = []
        self.coor_targ = []

def readGroups():
    """
    This function loads the verts of group from vertsgroup file
    """
    try:
        #open file vertgroups
        confDescriptor = open(vertgroups, "r")
    except:
        print "Errore apertura file %s",(vertgroups)
        return  None

    linesConf   = confDescriptor.readlines()
    gName = "" #name of working group
    for l in linesConf:
        if l.startswith("#"):
            #the group is found
            gName  = ((l.split("#")[1]).split("\n"))[0]
        else:
            words = l.split(",")
            tmp = []
            for i in words:
                if gName == "external_body":
                    #add index for skin
                    external_group.append(int(i))
                else:
                    #add index for gName group
                    tmp.append(int(i))
            try:
                g_transf[stringGroup.index(gName)] = tmp
            except:
                "Not found " + gName


def calcPairs():
    global g_transf, originalVerts, external_group, vpairs
    """
    This function calculate the pairs of a vert of group and his near vert in the skin
    """
    for g in g_transf:
        #temporary structure for base coords of g
        refTarget = []
        for i in range(0, max_vert):
            refTarget.append(None);
        for i in g:
            refTarget[i] = vert([originalVerts[i][0], originalVerts[i][1], originalVerts[i][2]], i)

        #search near vertex
        v = originalVerts[external_group[0]]
        dist =  math.sqrt(math.pow(v[0] - refTarget[g[0]].co[0], 2) + math.pow(v[1] - refTarget[g[0]].co[1], 2) + math.pow(v[2] - refTarget[g[0]].co[2], 2))
        #bbV is the boundingbox of g
        bbV = calcBuondingBoxV(g, refTarget)
        for e in external_group:
            for f in bbV:
                i = originalVerts[e]
                distTemp = math.sqrt(math.pow(i[0] - refTarget[f.index].co[0], 2) + math.pow(i[1] - refTarget[f.index].co[1], 2) + math.pow(i[2] - refTarget[f.index].co[2], 2))
                if distTemp < dist:
                    dist = distTemp
                    nearV = i
                    nearIndex = e
                    ref = refTarget[f.index]
        #add pair
        pair = [nearV, ref]
        vpairs.append(pair)

def createTarget(file):
    """
    This function creates target structure from target file
    """
    global max_vert, mesh_actual, mesh_original

    mesh_actual   = mesh()
    mesh_original = mesh()

    #open file target
    try:
        fileDescriptor = open(dir_input+file, "r")
    except:
        print "Errore apertura file %s",(file)

    #add max_vert entries
    for i in range (0, max_vert):
        v = vert([0.0, 0.0, 0.0], i)
        mesh_actual.add(v)
        mesh_original.add(v)

    linesTarget = fileDescriptor.readlines()
    #preparing target structures
    index = -1
    for l in linesTarget:
        words = l.split(" ")
        if len(words) == 0 or words[0].startswith('#'):
            pass
        else:
            index = int(words[0])
            v = vert([float(words[1]), float(words[2]), float(words[3])], index)
            mesh_actual.setElement(v)       #set vert
            mesh_original.setElement(v)     #set vert
    fileDescriptor.close()


def calcCenter(listIndex, refTarget):
    """
    This function calculates the center
    """
    bb = calcBuondingBox(listIndex, refTarget)
    return [(bb[0] + (bb[1] - bb[0])/2), (bb[2] + (bb[3] - bb[2])/2), (bb[4] + (bb[5] - bb[4])/2)]

def calcBuondingBoxV(listIndex, refTarget):
    """
    This function calculates the boundingbox and returns the verts in the bound
    """
    offset = listIndex[0]

    maxx = refTarget[offset]
    minx = refTarget[offset]
    maxy = refTarget[offset]
    miny = refTarget[offset]
    maxz = refTarget[offset]
    minz = refTarget[offset]

    for v in listIndex:
        offset = v
        if refTarget[offset].co[0] > maxx.co[0]:
            maxx = refTarget[offset]
        if refTarget[offset].co[0] < minx.co[0]:
            minx = refTarget[offset]
        if refTarget[offset].co[1] > maxy.co[1]:
            maxy = refTarget[offset]
        if refTarget[offset].co[1] < miny.co[1]:
            miny = refTarget[offset]
        if refTarget[offset].co[2] > maxz.co[2]:
            maxz = refTarget[offset]
        if refTarget[offset].co[2] < minz.co[2]:
            minz = refTarget[offset]

    return [minx, maxx, miny, maxy, minz, maxz]

def calcBuondingBox(listIndex, refTarget):
    """
    This function calculates the boundingbox and returns the coords in the bound
    """
    offset = listIndex[0]

    maxx = refTarget[offset].co[0]
    minx = refTarget[offset].co[0]
    maxy = refTarget[offset].co[1]
    miny = refTarget[offset].co[1]
    maxz = refTarget[offset].co[2]
    minz = refTarget[offset].co[2]

    for v in listIndex:
        offset = v
        if refTarget[offset].co[0] > maxx:
            maxx = refTarget[offset].co[0]
        if refTarget[offset].co[0] < minx:
            minx = refTarget[offset].co[0]
        if refTarget[offset].co[1] > maxy:
            maxy = refTarget[offset].co[1]
        if refTarget[offset].co[1] < miny:
            miny = refTarget[offset].co[1]
        if refTarget[offset].co[2] > maxz:
            maxz = refTarget[offset].co[2]
        if refTarget[offset].co[2] < minz:
            minz = refTarget[offset].co[2]

    return [minx, maxx, miny, maxy, minz, maxz]

def adapter():
    """
    Adapting the parts
    """
    for g in g_transf:
        #restore mesh
        restore(g)
        #scale mesh
        fact = scale(g)
        #positioning mesh
        positioning(g, fact)

def positioning(g, fact):
    global mesh_actual, mesh_original, originalVerts, vpairs
    """
    Reposition the group in the right position
    """
    offset = g_transf.index(g)
    ref = vpairs[offset][1]     #reference vert in group
    nearV = vpairs[offset][0]   #reference vert in skin
    nearIndex = originalVerts.index(nearV)

    #the distance dist* (from ref to near in base coors) must be multiplied by the scaling factor
    distx = (ref.co[0] - nearV[0]) * fact
    disty = (ref.co[1] - nearV[1]) * fact
    distz = (ref.co[2] - nearV[2]) * fact

    nearT = mesh_actual.getBaseAt(nearIndex)
    #the distance distT* (from ref to near in target coors)
    distTx = mesh_actual.getBaseAt(ref.index).co[0] - nearT.co[0]
    distTy = mesh_actual.getBaseAt(ref.index).co[1] - nearT.co[1]
    distTz = mesh_actual.getBaseAt(ref.index).co[2] - nearT.co[2]
    #put group in near vert
    for v in g:
        x = (mesh_actual.getTargAt(v).co[0] - distTx)
        y = (mesh_actual.getTargAt(v).co[1] - distTy)
        z = (mesh_actual.getTargAt(v).co[2] - distTz)
        vrt = vert([x, y, z], v)
        mesh_actual.setElement(vrt)

    #put group in a right position
    for v in g:
        x = (mesh_actual.getTargAt(v).co[0] + distx)
        y = (mesh_actual.getTargAt(v).co[1] + disty)
        z = (mesh_actual.getTargAt(v).co[2] + distz)
        vrt = vert([x, y, z], v)
        mesh_actual.setElement(vrt)




def scale(g):
    """
    Scale the group
    """
    global mesh_actual, mesh_original
    centerActual = calcBuondingBox(g, mesh_actual.getBase())
    centerRestore = calcBuondingBox(g, mesh_original.getBase())

    #calculate scaling factor
    distx = math.sqrt(math.pow(centerActual[1] - centerActual[0], 2))
    disty = math.sqrt(math.pow(centerActual[3] - centerActual[2], 2))
    distz = math.sqrt(math.pow(centerActual[5] - centerActual[4], 2))
    distxt = math.sqrt(math.pow(centerRestore[1] - centerRestore[0], 2))
    distyt = math.sqrt(math.pow(centerRestore[3] - centerRestore[2], 2))
    distzt = math.sqrt(math.pow(centerRestore[5] - centerRestore[4], 2))
    fact = min((distxt/distx),(distyt/disty),(distzt/distz))

    #scaling mesh
    for v in g:
        x = ((mesh_actual.getTargAt(v).co[0] + mesh_actual.getBaseAt(v).co[0]) * fact) - mesh_actual.getBaseAt(v).co[0]
        y = ((mesh_actual.getTargAt(v).co[1] + mesh_actual.getBaseAt(v).co[1]) * fact) - mesh_actual.getBaseAt(v).co[1]
        z = ((mesh_actual.getTargAt(v).co[2] + mesh_actual.getBaseAt(v).co[2]) * fact) - mesh_actual.getBaseAt(v).co[2]
        vrt = vert([x, y, z], v)
        mesh_actual.setElement(vrt)
    return fact

def restore(g):
    """
    Restore the group
    """
    global mesh_actual
    for v in g:
        mesh_actual.setElement(vert([0,0,0], v))

def saveTarget(file):
    """
    This fuction saves the file target
    """
    global mesh_actual
    #open file target
    try:
        fileDescriptor = open(dir_output+file, "w")
    except:
        print "Error opening file %s",(file)
        return  None
    #save file target reading target struct
    for i in mesh_actual.getTarg():
        if math.fabs(i.co[0]) == 0.0 and math.fabs(i.co[1]) == 0.0 and math.fabs(i.co[2]) == 0.0:
            pass
        else:
            fileDescriptor.write("%d %f %f %f\n" % (i.index, i.co[0], i.co[1], i.co[2]))
    fileDescriptor.close()




def loadInitialBaseCoords(path):
    global max_vert
    """
    This function is a little utility function to load only the vertex data
    from a wavefront obj file.

    Parameters
    ----------

    path:
        *string*. A string containing the operating system path to the
        file that contains the wavefront obj.

    """
    try:
        fileDescriptor = open(path)
    except:
        print "Error opening %s file"%(path)
        return
    data = fileDescriptor.readline()
    vertsCoo = []
    max_vert = 0
    gName = ""
    while data:
        dataList = data.split()
        if dataList[0] == "v":
            max_vert += 1
            co = (float(dataList[1]),\
                    float(dataList[2]),\
                    float(dataList[3]))
            vertsCoo.append(co)
        if dataList[0] == "g":
            try:
                #check if the group must be adapt 
                stringGroup.index(dataList[1])
                gName  = dataList[1]
            except:
                gName = ""
        if dataList[0] == "f" and gName != "":
            for faceData in dataList[1:]:
                vInfo = faceData.split('/')
                vIdx = int(vInfo[0]) - 1  # -1 because obj is 1 based list
                #add index
                try:
                    g_transf[stringGroup.index(gName)].index(vIdx)
                except:
                    g_transf[stringGroup.index(gName)].append(vIdx)
        data = fileDescriptor.readline()
    fileDescriptor.close()
    return vertsCoo

if __name__ == '__main__' :
    """
    Main function
    """
    if len(sys.argv) < 3:
        print "Usage: " + sys.argv[0] + " input_dir output_dir" #Usage
        sys.exit()

    dir_input = sys.argv[1]
    dir_output = sys.argv[2]

    #check slashes for directories
    if dir_input.endswith("/") == False:
        dir_input += "/"

    if dir_output.endswith("/") == False:
        dir_output += "/"

    for i in stringGroup:
        g_transf.append([])

    #fill groups and load initial base coords
    readGroups()
    originalVerts = loadInitialBaseCoords("base.obj")
    
    #open directory
    try:
        file_list = os.listdir(dir_input)
    except:
        print "No such input directory %s" % (dir_input)
        sys.exit()
    try:
        os.listdir(dir_output)
    except:
        print "No such output directory %s" % (dir_output)
        sys.exit()
        
    print "Preparing structures..."
    #calculate pairs of verts
    calcPairs()

    cnt = 1
    total = 0
    for f in file_list:
        try:
            f.index(".target") #check if is a target
            total += 1
        except:
            pass

    for f in file_list:
        try:
            f.index(".target") #check if is a target
            print
            print "Processing file %s [%d/%d]" % (f, cnt, total)
            createTarget(f) #ceate target struct
            adapter()       #adapt groups
            saveTarget(f)   #save target
            cnt += 1
        except:
            pass


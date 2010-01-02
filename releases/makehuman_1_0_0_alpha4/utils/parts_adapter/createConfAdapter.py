import sys
import math


neighbor = []
mhverts = []
distances = []
#gruppo occhi
#gruppo sopracciglia
#gruppo ciglia
#gruppi joints
#gruppo lingua
#gruppo denti

originalVerts = [] #Original base mesh coords
path = "base.obj"


class vert:
	co = []
	index = 0
	
	def __init__(self, co, index):
		self.co = co
		self.index = index
	
def loadInitialBaseCoords(path):
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
        
    try:
        listDescriptor = open("list.txt", "r")
    except:
        print "Error opening %s file"%("list.txt")
        return
    dataList = listDescriptor.readlines()
    for l in dataList:
		data = l.split(" ");
		if len(data) == 0 or data[0].startswith('#'):
			pass
		else:
			mhverts.append(int(data[0]))
			neighbor.append(int(data[1]))
    listDescriptor.close()
       
    data = fileDescriptor.readline()
    vertsCoo = []
    count = 0
    while data:
        dataList = data.split()
        if dataList[0] == "v":
            co = (float(dataList[1]),\
                    float(dataList[2]),\
                    float(dataList[3]))
            index = count
            originalVerts.append(vert(co, index))
            count += 1
        data = fileDescriptor.readline()
    fileDescriptor.close()
    return vertsCoo
    
    
def calc_conf():

	for v in range(0, len(mhverts)):
		vtargetIndex = 0
		x = (originalVerts[mhverts[v]].co[0] - originalVerts[neighbor[v]].co[0])
		y = (originalVerts[mhverts[v]].co[1] - originalVerts[neighbor[v]].co[1])
		z = (originalVerts[mhverts[v]].co[2] - originalVerts[neighbor[v]].co[2])
		distances.append([x, y, z])
	#per ogni gruppo
		#per ogni v del gruppo
			#trovo il vicino e memorizzo distanza

def write_conf(output_file):
	try:
		fileDescriptor = open(output_file, "w")
 	except:
		print "Errore apertura file %s",(output_file)
		return  None		
	
	for i in range (0, len(mhverts)):
		fileDescriptor.write("%d %d %f %f %f\n" % (mhverts[i], neighbor[i], distances[i][0], distances[i][1], distances[i][2]))
  	fileDescriptor.close()
#scrivo file

if __name__ == '__main__' :
	try :
		output_file = sys.argv[1]
	except IndexError :
		print "Usage: python ", sys.argv[0], " <output_file>"
		sys.exit(-1)
		
	faceVerts = loadInitialBaseCoords(path)
	calc_conf()	
	write_conf(output_file)

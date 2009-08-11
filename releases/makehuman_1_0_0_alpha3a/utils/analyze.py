import re
import sys

def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    if len(sys.argv) < 2:
        print("specify the file to analyze")
        return;
    
    vertices = 0
    texcoords = 0
    faces = 0
    groups = 0
    groupname = None
    groupfaces = 0
    groupverticeset = set()
    groupvertices = 0
    nogroupvertices = 0
    triangles = 0
    quads = 0
    
    faceparser = re.compile(r"(\d+)/")
    
    print("analyzing " + sys.argv[1])

    with open(sys.argv[1]) as f:
        for line in f:
            if line[0] == 'v':
                if line[1] == 't':
                    texcoords += 1
                else:
                    vertices += 1
            elif line[0] == 'f':
                faces += 1
                groupfaces += 1
                verts = faceparser.findall(line)
                if len(verts) == 3:
                    triangles += 1
                else:
                    quads += 1
                for vert in verts:
                    groupverticeset.add(int(vert))
                    nogroupvertices += 1;
            elif line[0] == 'g':
                groups += 1
                if groupname != None:
                    print("group " + str(groups -1) + " named " + groupname + ": " + str(groupfaces) + " faces " + str(len(groupverticeset)) + " vertices")
                    groupfaces = 0
                    groupvertices += len(groupverticeset)
                    groupverticeset.clear()
                groupname = line[2:-1]
        if groupname != None:
            print("group " + str(groups) + " named " + groupname + ": " + str(groupfaces) + " faces " + str(len(groupverticeset)) + " vertices")

    print("vertices: %s" %(vertices))
    print("Texture coordinates: %s"%(texcoords))
    print("Faces: %s"%(faces))
    print("Groups: %s"%(groups))
    print("Quads: %i"%(quads))
    print("Triangles: %i"%(triangles))

    print("Vertices created by duplicating everything:" + str(nogroupvertices) + " (" + str((nogroupvertices - vertices) * 100 / vertices) + "% overhead)")
    print("Vertices created by duplicating only outside groups:" + str(groupvertices) + " (" + str((groupvertices - vertices) * 100 / vertices) + "% overhead)")
    
if __name__ == "__main__":
    main()

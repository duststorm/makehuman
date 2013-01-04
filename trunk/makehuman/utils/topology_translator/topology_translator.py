# You may use, modify and redistribute this module under the terms of the GNU AGPL3.0.
"""
Translate a  morph target from a mesh with topology 1 to a mesh with topology 2
The shape of old and new objs must be similar. We assume the new mesh is done using a retopology tool.

===========================  ==================================================================
Project Name:                **MakeHuman**
Module File Location:        utils/topology_translator/topology_translator.py
Product Home Page:           http://www.makehuman.org/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2013
Licensing:                   AGPL3 (see also: http://www.makehuman.org/node/318)
Coding Standards:            See http://www.makehuman.org/node/165#TOC-Coding-Style
===========================  ==================================================================


"""
from topologylib import *
import getopt
import sys

def usage():
    print""
    print"NAME"
    print"    %s: a program to translate a  morph target from"%(sys.argv[0])
    print"    a mesh with topology 1 to a mesh with topology 2"
    print"    In order to have a correct conversion, the diff.data "
    print"    must be build using a base mesh1 and base mesh2 very "
    print"    similar in shape (not in topology)"
    print"    For this reason we assume the base mesh1 is done "
    print"    using a retopology tool, upon base mesh2."
    print""
    print"SYNOPSIS"
    print"    %s [options]"%(sys.argv[0])
    print""
    print"OPTIONS:"
    print"    --build; build the database of differences to be used in conversion"
    print"    --target path; to specify the target file to convert"
    print"    --targetbase path; to specify the obj to be used as reference to save targets"
    print"    --folder path; to specify the folder with all targets to convert"
    print"    --mold path; to specify the mesh obj to be fitted to"
    print"    --tofit path; to specify the obj to fit to the mold"
    print"    --help; what you're looking at right now."
    print"    --testObj: path; Save a subdivided version of the obj passes as argument"
    print""
    print"AUTHOR:"
    print"    Manuel Bastioni (info@makehuman.org)"
    print""
    print"SEE ALSO:"
    print"    MakeHuman web page:"
    print"    http://www.makehuman.org"
    print""
    exit()


def main(argv):

    target = None
    mesh2 = "mesh2.obj"
    mesh1 = "mesh1.obj"
    datafile = "diff.data"
    targetbase = None
    buildit = None
    testobj = None
    folder = None
    simil = None

    #handle options
    try:
        opts, args = getopt.getopt(argv, "h", ["help","build","simil=","target=","targetbase=","tofit=","mold=","datafile=","testobj=","folder="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("--target"):
            target = arg
        elif opt in ("--targetbase"):
            targetbase = arg
        elif opt in ("--tofit"):
            mesh1 = arg
        elif opt in ("--mold"):
            mesh2 = arg
        elif opt in ("--datafile"):
            datafile = arg
        elif opt in ("--build"):
            buildit = 1
        elif opt in ("--testobj"):
            testobj = arg
        elif opt in ("--folder"):
            folder = arg
        elif opt in ("--simil"):            
            simil = arg

    if buildit:        
        vertsList1 = loadVertsCoo(mesh1)
        vertsList2 = loadVertsCoo(mesh2)
        faces2 = loadFacesIndices(mesh2)
        saveData(vertsList1, vertsList2, faces2, datafile, epsilon = 0.2)
    elif testobj:
        vertices = loadVertsCoo(testobj)
        faces = loadFacesIndices(testobj)
        tess = subdivideObj(faces, vertices, 2)
        saveTestObj(tess[0], tess[1], testobj+".subdivided.obj")
    elif simil:        
        vertsList1 = loadVertsCoo(mesh1)
        vertsList2 = loadVertsCoo(mesh2)
        faces2 = loadFacesIndices(mesh2)
        meshComparison(vertsList1, vertsList2, faces2, simil)       
    else:
        vertsList1 = loadVertsCoo(mesh1)
        if not targetbase:
            targetbase = mesh1
        originalVerts = loadVertsCoo(targetbase)            
        if folder:
            fileList = os.listdir(folder)
            for fileName in fileList:
                mesh2 = os.path.join(folder,fileName)
                if target:
                    convertedName = target
                else:
                    convertedName = os.path.basename(mesh2)+"target"
                if os.path.isfile(mesh2):                    
                    vertsList2 = loadVertsCoo(mesh2)
                    faces2 = loadFacesIndices(mesh2)                    
                    convertFile(vertsList1, vertsList2, faces2, datafile, originalVerts, convertedName, targetbase, target)
        else:            
            vertsList2 = loadVertsCoo(mesh2)
            faces2 = loadFacesIndices(mesh2) 
            if target:
                convertedName = target
            else:
                convertedName = os.path.basename(mesh2)+"target"
            convertFile(vertsList1, vertsList2, faces2, datafile, originalVerts, convertedName, targetbase, target)


if __name__ == "__main__":
    main(sys.argv[1:])


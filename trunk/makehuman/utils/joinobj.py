# You may use, modify and redistribute this module under the terms of the GNU GPL.
"""
Join 2 wavefront objs

===========================  ==================================================================
Project Name:                **MakeHuman**
Module File Location:        utils/joinobj.py
Product Home Page:           http://www.makehuman.org/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2013
Licensing:                   AGPL3 (see also: http://www.makehuman.org/node/318)
Coding Standards:            See http://www.makehuman.org/node/165#TOC-Coding-Style
===========================  ==================================================================

This module implements a utility function to join to wavefront obj, without alter the vert order of them.

"""

__docformat__ = 'restructuredtext'


import sys
import getopt
import os


def readFile(objFile):
    fp= open(objFile, "r")

    fileVerts = []
    fileVt = []
    fileFacesAndGroups = []

    for line in fp:
        lineSplit= line.split()
        if len(lineSplit) == 0:
            pass
        elif lineSplit[0] == 'v':
            fileVerts.append(line)
        elif lineSplit[0] == 'vt':
            fileVt.append(line)
        elif lineSplit[0] == 'g':
            fileFacesAndGroups.append(line)
        elif lineSplit[0] == 'f':
            fileFacesAndGroups.append(line)
    fp.close()
    return fileVerts,fileVt,fileFacesAndGroups


def writeFile(file1, file2, outfile):

    data = concatenateFile(file1, file2)
    outfp = open(outfile, "w")
    for v in data[0]:
        outfp.write(v)
    for vt in data[1]:
        outfp.write(vt)
    for f in data[2]:
        outfp.write(f)
    outfp.close()



def concatenateFile(file1, file2):
    file1Data = readFile(file1)
    file2Data = readFile(file2)

    outputVerts =  file1Data[0]
    file2Verts =  file2Data[0]

    outputVt =  file1Data[1]
    file2Vt =  file2Data[1]

    outputFacesAndGroups =  file1Data[2]
    file2FacesAndGroups =  file2Data[2]

    nVert = len(outputVerts)
    nVt = len(outputVt)

    for vert in file2Verts:
        outputVerts.append(vert)

    for vt in file2Vt:
        outputVt.append(vt)

    #TODO: handle the case with group already present in file1
    for facesAndGroups in file2FacesAndGroups:
        if facesAndGroups[0] == "f":
            facesData = facesAndGroups[1:].split()
            newFacesData = "f "
            for data in facesData:
                vertData = data.split("/")

                #case1: face contains only index of vert
                if len(vertData) == 1:
                    n1 = int(vertData[0]) + nVert
                    newVertData = str(n1)

                #case2: face contains index of vert and index of UV
                if len(vertData) => 2:
                    n1 = int(vertData[0]) + nVert
                    n2 = int(vertData[1]) + nVt
                    newVertData = str(n1)+"/"+str(n2)+" "
                newFacesData += newVertData
            newFacesData += "\n"
            outputFacesAndGroups.append(newFacesData)
    return outputVerts,outputVt,outputFacesAndGroups


def usage():
    print "Usage: " + sys.argv[0] + " [options] inputfile1 inputfile2 outputfile"


def main(argv):

    #handle options
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
    file1 = sys.argv[-3]
    file2 = sys.argv[-2]
    outfile = sys.argv[-1]

    #Check files arguments
    if len(sys.argv) < 4:
        usage()
        sys.exit()
    try:
        file_list = os.path.isfile(file1)
    except:
        print "No such file %s" % (file1)
        sys.exit(2)
    try:
        file_list = os.path.isfile(file2)
    except:
        print "No such file %s" % (file2)
        sys.exit(2)

    #processing files
    writeFile(file1, file2, outfile)


if __name__ == "__main__":
    main(sys.argv[1:])








#!/usr/bin/env python
import sys
sys.path = ["./core", "./lib"] + sys.path
import algos3d
import os
import zipfile
import fnmatch

def getFiles(rootPath, filterStr):
    foundFiles = []
    for root, dirnames, filenames in os.walk(rootPath):
        for filename in fnmatch.filter(filenames, filterStr):
            foundFiles.append(os.path.join(root, filename))
    return foundFiles


if __name__ == '__main__':
    obj = algos3d.Target(None, None)
    with zipfile.ZipFile('data/targets.npz', mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        allTargets = getFiles('data', '*.target')
        for (i, path) in enumerate(allTargets):
            try:
                obj._load_text(path)
                iname, vname = obj._save_binary(path)
                zip.write(iname)
                zip.write(vname)
                os.remove(iname)
                os.remove(vname)
                print "[%.0f%% done] converted target %s" % (100*(float(i)/float(len(allTargets))), path)
            except StandardError, e:
                print 'error converting target %s' % path

    with open('data/images.list', 'w') as f:
        for (i, path) in getFiles('data', '*.target'):
            path = path.replace('\\','/')
            f.write(path + '\n')

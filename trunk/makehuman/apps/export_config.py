""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

"""

import os
import mh
import shutil

#
#    safePrint( string, filename ):
#    Utility for evading encoding errors
#

"""
def safePrint( string, filename ):
    try:
        print("%s %s" % (string, filename))
        return
    except:
        pass
    return
    ascii = ""
    space = ord(' ')
    z = ord('z')
    for c in filename:
        d = ord(c)
        if d < space or d > z:
            ascii += "\\x%x " % d
        else:
            ascii += chr(d)
    print("%s %s" % (string, ascii))
"""
#
#
#

def truthValue(word):
    if word.lower() in ["false", "no", "0"]:
        return False
    return True

#
#    proxyFilePtr(name):
#

def proxyFilePtr(name):
    head = os.path.normpath(mh.getPath(''))
    for path in [head, './']:
        filename = os.path.realpath( os.path.join(path, name) )
        try:
            fp = open(filename, "r")
            print("    Using config file", filename )
            return fp
        except:
            print("*** Cannot open",  filename )
    return None
    
#
#    class CExportConfig:
#

class CExportConfig:
    def __init__(self):
        self.mainmesh = ['obj', 'mhx', 'dae']
        self.rigtype = 'mhx'
        self.daerig = 'game'
        self.mhxversion = ['25']
        self.exporting = True
        self.separatefolder = False
        self.feetonground = True
        self.outFolder = None
        self.texFolder = None
        self.proxyList = []
        self.hidden = True
        #self.expressions = False
        self.expressionunits = False
        #self.faceshapes = True
        self.bodyshapes = True
        #self.facepanel = True
        self.cage = False
        self.advancedspine = False
        self.breastrig = False
        self.malerig = False
        self.skirtrig = "inh"
        self.clothesrig = True
        self.clothesvisibilitydrivers = True
        self.customshapes = False
        self.copiedFiles = {}
        self.warpField = {}
        
        # Used by mhx exporter
        self.mhx25 = True
        self.vertexWeights = []
        self.customShapes = {}
        self.poseInfo = {}
        self.boneGroups = []
        self.recalcRoll = []              
        self.vertexGroupFiles = []
        self.gizmoFiles = []
        self.headName = "Head"
        self.objectProps = []
        self.armatureProps = []
        self.customProps = []
        self.customShapeFiles = []
        

    def __repr__(self):
        return (
"<CExportConfig use:%s mhx:%s daz:%s version%s\n" % (self.mainmesh, self.rigtype, self.daerig, self.mhxversion) +
"  expr:%s body:%s cage:%s\n" % (self.expressionunits, self.bodyshapes, self.cage) +
"  breastrig:%s gen:%s vis:%s>" % (self.breastrig, self.malerig, self.clothesvisibilitydrivers))

#
#   class CProxyFile:
#

class CProxyFile:
    def __init__(self):
        self.type = 'Clothes'
        self.layer = 0
        self.useMhx = True
        self.useObj = True
        self.useDae = True
        self.file = ""
        self.name = None
        
    def set(self, type, layer, mhx, obj, dae):
        self.type = type
        self.layer = layer
        self.useMhx = mhx
        self.useObj = obj
        self.useDae = dae
        
    def __repr__(self):
        return (
"<CProxyFile type %s layer %d\n" % (self.type, self.layer) +
"    mhx %s obj %s dae %s\n" % (self.useMhx, self.useObj, self.useDae) + 
"    name %s file \"%s\">" % (self.name, self.file))
        
#
#
#
        
def getExistingProxyFile(words, category):
    path = words[1]  
    if len(words) <= 2:
        if not os.path.exists(os.path.realpath(path)):
            return None
        print ("Found", path)
        return path
    else:
        file = os.path.basename(path)
        uuid = words[2]
        paths = []
        folder = os.path.join(mh.getPath(''), 'data', category)
        addProxyFiles(file, folder, paths, 6)
        folder = os.path.join('data', category)
        addProxyFiles(file, folder, paths, 6)
        for path in paths:        
            uuid1 = scanFileForUuid(path)
            if uuid1 == uuid:
                print("Found", path, uuid)
                return path
        return None                


def addProxyFiles(file, folder, paths, depth):
    if depth < 0:
        return None
    try:
        files = os.listdir(folder)        
    except OSError:
        return None
    for pname in files:
        path = os.path.join(folder, pname)
        if pname == file:
            paths.append(path)
        elif os.path.isdir(path):
            addProxyFiles(file, path, paths, depth-1)
    return            


def scanFileForUuid(path):           
    fp = open(path)
    for line in fp:
        words = line.split()
        if len(words) == 0:
            break
        elif words[0] == '#':
            if words[1] == "uuid":
                fp.close()
                return words[2]
        else:
            break
    fp.close()
    return None
            

def exportConfig(human, useHair, options=None):
    cfg = CExportConfig()
    type = 'Proxy'
    layer = 2
    useMhx = True
    useObj = True
    useDae = True

    if options:
        print(options)
        cfg.mhxversion = options['mhxversion']
        cfg.hidden = options['hidden']
        #cfg.expressions = options['expressions']
        cfg.expressionunits = options['expressionunits']
        #cfg.faceshapes = options['faceshapes']
        cfg.bodyshapes = options['bodyshapes']
        cfg.customshapes = options['customshapes']
        #cfg.facepanel = options['facepanel']
        cfg.separatefolder = options['separatefolder']
        cfg.feetonground = options['feetonground']
        cfg.cage = options['cage']
        cfg.clothesrig = options['clothesrig']
        cfg.advancedspine = options['advancedspine']
        cfg.malerig = options['malerig']
        if options['skirtrig']:
            cfg.skirtrig = "own"
        else:
            cfg.skirtrig = "inh"
        cfg.rigtype = options['mhxrig']

    if useHair and human.hairProxy:
        words = human.hairObj.mesh.name.split('.')
        pfile = CProxyFile()
        pfile.set('Clothes', 2, useMhx, useObj, useDae)
        name = goodName(words[0])
        #pfile.file = findExistingProxyFile("hairstyles", None, "%s.mhclo" % name)
        pfile.file = human.hairProxy.file
        cfg.proxyList.append(pfile)

    for (key,clo) in human.clothesObjs.items():
        if clo:
            name = goodName(key)
            pfile = CProxyFile()
            pfile.set('Clothes', 3, useMhx, useObj, useDae)            
            #pfile.file = findExistingProxyFile("clothes", name, "%s.mhclo" % name)
            proxy = human.clothesProxies[key]
            pfile.file = proxy.file
            cfg.proxyList.append(pfile)
            
    if human.proxy:
        name = goodName(human.proxy.name)
        pfile = CProxyFile()
        pfile.set('Proxy', 4, useMhx, useObj, useDae)
        #pfile.file = findExistingProxyFile("proxymeshes", name, "%s.proxy" % name)
        pfile.file = human.proxy.file
        cfg.proxyList.append(pfile)    

    if cfg.cage:
        pfile = getCageFile("./data/cages/cage/cage.mhclo", 4, useMhx, useObj, useDae)
        cfg.proxyList.append(pfile)    
        
    return cfg

    """
    status = None
    for line in fp:
        words = line.split()
        if len(words) == 0 or words[0][0] == '#':
            pass
        elif words[0] == '@':
            status = None
            key = words[1].lower()
            if key in ['mainmesh', 'mhxversion']:
                try:
                    exec("cfg.%s = words[2:]" % key)
                except:
                    pass
            elif key in [
                'separatefolder', 'feetonground', "hidden",
                #'expressions', 'faceshapes', 
                'expressionunits', 'bodyshapes', 'customshapes', 'facepanel',
                'advancedspine', 'malerig', 
                'clothesrig', 'clothesvisibilitydrivers'
                ]:
                try:
                    exec("cfg.%s = %s" % (key, truthValue(words[2])))
                except:
                    pass
            elif key in ['skirtrig']:   
                value = words[2][0:3].lower()
                exec("cfg.%s = value" % key)
            elif key == 'mhxrig':
                try:
                    cfg.rigtype = words[2].lower()
                except:
                    pass
            elif key == 'daerig':
                try:
                    cfg.daerig = words[2].lower()
                except:
                    pass
            elif key == 'obj':
                try:
                    useObj = eval(words[2])
                except:
                    pass
            elif key == 'mhx':
                try:
                    useMhx = eval(words[2])
                except:
                    pass
            elif key == 'dae':
                try:
                    useDae = eval(words[2])
                except:
                    pass
            elif key == 'proxy':
                typ = 'Proxy'
                layer = int(words[2])
            elif key == 'cage':
                typ = 'Cage'
                layer = int(words[2])
            elif key == 'clothes':
                typ = 'Clothes'
                layer = int(words[2])
            else:
                print('Ignored unrecognized command %s in mh_export.config' % words[1])
        elif typ == 'Cage':
            if len(words) > 0:
                name = words[0]
            else:
                name = "./data/cages/cage/cage.mhclo"
            pfile = getCageFile(name, layer, useMhx, useObj, useDae)
            cfg.cage = True
            cfg.proxyList.append(pfile)
    fp.close()
    print "Proxy configuration: Use %s" % cfg.mainmesh
    for elt in cfg.proxyList:
        print "  ", elt
    return cfg
    """
    
    
def getCageFile(name, layer, useMhx, useObj, useDae):
    pfile = CProxyFile()
    pfile.set('Cage', layer, useMhx, useObj, useDae)
    name = goodName(name)
    pfile.file = os.path.realpath(os.path.expanduser(name))
    return pfile

#
#   goodName(name):
#   getSubFolder(path, name):
#   getOutFileName(filePath, fromDir, isTexture, human, config):
#

def getOutFileFolder(filename, config):
    (fname, ext) = os.path.splitext(filename)
    fname = goodName(os.path.basename(fname))
    if config.separatefolder:
        config.outFolder = getSubFolder(os.path.dirname(filename), fname)
        if config.outFolder:
            outfile = os.path.join(config.outFolder, "%s%s" % (fname, ext)) 
        config.texFolder = getSubFolder(config.outFolder, "textures")
        config.copiedFiles = {}
    if not config.texFolder:
        outfile = filename
    return outfile


def getSubFolder(path, name):
    folder = os.path.join(path, name)
    #print "Using folder", folder
    if not os.path.exists(folder):
        print "Creating folder"
        #print folder
        try:
            os.mkdir(folder)
        except:
            print "Unable to create separate folder:",
            #print folder
            return None
    return folder        
    

def getOutFileName(filePath, fromDir, isTexture, human, config):
    srcDir = os.path.realpath(os.path.expanduser(fromDir))
    filename = os.path.basename(filePath)
    if human and (filename == "texture.tif"):
        texname = human.getTexture()
        fromPath = texname.replace("png", "tif")
        fileDir = os.path.dirname(fromPath)         
        filename = os.path.basename(fromPath)
        #print(filePath, fromDir, fileDir, fromPath)
        if fileDir == fromDir:
            fromPath = os.path.join(srcDir, filename)
    else:
        fromPath = os.path.join(srcDir, filename)
    if config.separatefolder:
        if isTexture:
            toPath = os.path.join(config.texFolder, filename)
        else:
            toPath = os.path.join(config.outFolder, filename)
        try:
            config.copiedFiles[fromPath]
            done = True
        except:
            done = False
        if not done:
            if 0 and human:
                texture = module3d.getTexture(human.getTexture())
                print(dir(texture))
                img = mh.Image(human.getTexture())
                print(dir(img))
                img.save(toPath)
                halt
            try:
                shutil.copyfile(fromPath, toPath)
            except:
                pass    
            config.copiedFiles[fromPath] = True
        return toPath
    else:
        return fromPath
        
def goodName(name):
    return name.replace(" ", "_").replace("-","_").lower()
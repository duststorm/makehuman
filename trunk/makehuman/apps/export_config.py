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
Configure export options by reading mh_export.config.

"""

import os
import mh
import shutil

#
#    safePrint( string, filename ):
#    Utility for evading encoding errors
#

def safePrint( string, filename ):
    try:
        print("%s %s" % (string, filename))
        return
    except:
        success = False
    if not success:
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
            safePrint("    Using config file", filename )
            return fp
        except:
            safePrint("*** Cannot open",  filename )
    return None
    
#
#    class CExportConfig:
#

class CExportConfig:
    def __init__(self):
        self.mainmesh = ['obj', 'mhx', 'dae']
        self.mhxrig = 'mhx'
        self.daerig = 'game'
        self.mhxversion = ['25']
        self.separatefolder = False
        self.outFolder = None
        self.texFolder = None
        self.proxyList = []
        self.expressions = True
        self.faceshapes = True
        self.bodyshapes = True
        self.cage = False
        self.breastrig = False
        self.biceps = False
        self.malerig = False
        self.skirtrig = "inh"
        self.clothesvisibilitydrivers = False
        self.customrigs = []
        self.customshapes = []
        self.customvertexgroups = []
        self.copiedFiles = {}
        
    def __repr__(self):
        return (
"<CExportConfig use:%s mhx:%s daz:%s version%s\n" % (self.mainmesh, self.mhxrig, self.daerig, self.mhxversion) +
"  expr:%s face:%s body:%s cage:%s\n" % (self.expressions, self.faceshapes, self.bodyshapes, self.cage) +
"  breastrig:%s biceps:%s gen:%s vis:%s>" % (self.breastrig, self.biceps, self.malerig, self.clothesvisibilitydrivers))

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
#   exportConfig(human, useHair, options=None):
#

def exportConfig(human, useHair, options=None):
    cfg = CExportConfig()
    type = 'Proxy'
    layer = 2
    useMhx = True
    useObj = True
    useDae = True
    #useClothes = False
    useProxy = 'Rorkimaru'

    if options:
        print(options)
        cfg.mhxversion = options['mhxversion']
        cfg.expressions = options['expressions']
        cfg.faceshapes = options['faceshapes']
        cfg.bodyshapes = options['bodyshapes']
        cfg.separatefolder = options['separatefolder']
        cfg.cage = options['cage']
        cfg.breastrig = options['breastrig']
        cfg.malerig = options['malerig']
        if options['skirtrig']:
            cfg.skirtrig = "own"
        else:
            cfg.skirtrig = None
        cfg.mhxrig = options['mhxrig']
        fp = 0
    else:    
        fp = proxyFilePtr('mh_export.config')

    if useHair and human.hairObj:
        words = human.hairObj.mesh.name.split('.')
        pfile = CProxyFile()
        pfile.set('Clothes', 2, useMhx, useObj, useDae)
        name = goodName(words[0])
        pfile.file = os.path.expanduser("./data/hairstyles/%s.mhclo" % name)
        cfg.proxyList.append(pfile)

    for (name,clo) in human.clothesObjs.items():
        if clo:
            name = goodName(name)
            pfile = CProxyFile()
            pfile.set('Clothes', 3, useMhx, useObj, useDae)            
            pfile.file = os.path.expanduser("./data/clothes/%s/%s.mhclo" % (name, name))
            cfg.proxyList.append(pfile)
            
    if human.proxy:
        name = goodName(human.proxy.name)
        pfile = CProxyFile()
        pfile.set('Proxy', 4, useMhx, useObj, useDae)
        pfile.file = os.path.expanduser("./data/proxymeshes/%s/%s.proxy" % (name, name))
        cfg.proxyList.append(pfile)    

    if not fp: 
        if useProxy:
            pfile = CProxyFile()
            pfile.set('Proxy', 3, useMhx, useObj, useDae)
            pfile.file = os.path.expanduser("./data/templates/%s.proxy" % useProxy)
            cfg.proxyList.append(pfile)
        return cfg

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
                'separatefolder',
                'expressions', 'faceshapes', 'bodyshapes', 
                'breastrig', 'biceps', 'malerig',
                'clothesvisibilitydrivers'
                ]:
                try:
                    exec("cfg.%s = %s" % (key, truthValue(words[2])))
                except:
                    pass
            elif key in ['skirtrig']:   
                value = words[2][0:3].lower()
                exec("cfg.%s = value" % key)
            elif key in ['customrigs', 'customshapes', 'customvertexgroups']:
                status = key
            elif key == 'mhxrig':
                try:
                    cfg.mhxrig = words[2].lower()
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
                raise NameError('Unrecognized command %s in mh_export.config' % words[1])
        elif status:
            if status == 'customrigs':
                path = os.path.realpath(os.path.expanduser(words[0]))
                print(path)
                (dirname,fname) = os.path.split(path)
                print(fname)
                (modname,ext) = os.path.splitext(fname)
                print(modname, ext)
                if ext != ".py":
                    raise NameError("@CustomRig must be a .py file, not %s" % words[0])
                cfg.customrigs.append((dirname, modname))
            elif status == 'customshapes':
                path = os.path.realpath(os.path.expanduser(words[0]))
                cfg.customshapes.append(path)
            elif status == 'customvertexgroups':
                path = os.path.realpath(os.path.expanduser(words[0]))
                cfg.customvertexgroups.append(path)
        elif typ == 'Cage':
            pfile = CProxyFile()
            pfile.set(typ, layer, useMhx, useObj, useDae)
            name = goodName(words[0])
            pfile.file = os.path.realpath(os.path.expanduser(name))
            if len(words) > 1:
                pfile.name = words[1]
            if typ == 'Cage':
                cfg.cage = True
            cfg.proxyList.append(pfile)
    fp.close()
    print "Proxy configuration: Use %s" % cfg.mainmesh
    for elt in cfg.proxyList:
        print "  ", elt
    return cfg

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
    print(path, name)
    print("Using folder", folder)
    if not os.path.exists(folder):
        print("Creating folder", folder)
        try:
            os.mkdir(folder)
        except:
            print("Unable to create separate folder %s" % folder)
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
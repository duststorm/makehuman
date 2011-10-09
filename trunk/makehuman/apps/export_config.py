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
        self.useRig = 'mhx'
        self.mhxversion = ['24', '25']
        self.proxyList = []
        self.expressions = True
        self.faceshapes = True
        self.bodyshapes = True
        self.cage = False
        self.breasts = False
        self.biceps = False
        self.malegenitalia = False
        self.clothesvisibilitydrivers = False
        self.customrigs = []
        self.customshapes = []
        self.customvertexgroups = []
        
    def __repr__(self):
        return (
"<CExportConfig use:%s rig:%s version%s\n" % (self.mainmesh, self.useRig, self.mhxversion) +
"  expr:%s face:%s body:%s cage:%s\n" % (self.expressions, self.faceshapes, self.bodyshapes, self.cage) +
"  breasts:%s biceps:%s gen:%s vis:%s>" % (self.breasts, self.biceps, self.malegenitalia, self.clothesvisibilitydrivers))

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
#[('mhxversion', ['25']), ('expressions', True), ('useRig', 'mhx')]
#[('mhxversion', ['24', '25']), ('expressions', False), ('useRig', 'game')]

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
        cfg.cage = options['cage']
        cfg.useRig = options['useRig']
        #useClothes = options['clothes']
        useProxy = options['useProxy']
        fp = 0
    else:    
        fp = proxyFilePtr('mh_export.config')

    if useHair and human.hairObj:
        words = human.hairObj.meshName.split('.')
        pfile = CProxyFile()
        pfile.set('Clothes', 0, useMhx, useObj, useDae)
        pfile.file = os.path.expanduser("./data/hairstyles/%s.mhclo" % words[0])
        cfg.proxyList.append(pfile)

    for (name,clo) in human.clothesObjs.items():
        if clo:
            pfile = CProxyFile()
            pfile.set('Clothes', 0, useMhx, useObj, useDae)
            pfile.file = os.path.expanduser("./data/clothes/%s/%s.mhclo" % (name, name))
            cfg.proxyList.append(pfile)

    if not fp: 
        """
        if useClothes:
            for name in ['sweater', 'jeans']:
                pfile = CProxyFile()
                pfile.set('Clothes', 4, useMhx, useObj, useDae)
                pfile.file = os.path.expanduser("./data/clothes/%s/%s.mhclo" % (name,name))
                cfg.proxyList.append(pfile)
        """
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
                'expressions', 'faceshapes', 'bodyshapes', 
                'breasts', 'biceps', 'malegenitalia',
                'clothesvisibilitydrivers'
                ]:
                try:
                    exec("cfg.%s = %s" % (key, truthValue(words[2])))
                except:
                    pass
            elif key in ['customrigs', 'customshapes', 'customvertexgroups']:
                status = key
            elif key == 'rig':
                try:
                    cfg.useRig = words[2].lower()
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
        elif typ != 'Clothes':
            pfile = CProxyFile()
            pfile.set(typ, layer, useMhx, useObj, useDae)
            pfile.file = os.path.realpath(os.path.expanduser(words[0]))
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


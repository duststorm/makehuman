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
Interface to external rig

"""

import mhx_rig

ExternalRig = "Zepam"
#ExternalRig = None

if ExternalRig == "Zepam":
    import zepam_rig
    
    BoneGroups = [('GEN', 'THEME13'),
              ('IK', 'THEME05'),
              ('FK', 'THEME09'),
              ('FACIAL', 'THEME02')]
    RecalcRoll = []              
    GizmoFiles = ["./shared/mhx/templates/zepam_gizmos.mhx"]
        
    Joints = zepam_rig.ZepamJoints
    HeadsTails = zepam_rig.ZepamHeadsTails
    Armature = zepam_rig.ZepamArmature
    ObjectProps = zepam_rig.ZepamObjectProps
    ArmatureProps = zepam_rig.ZepamArmatureProps
    
    def writePoses(fp):
        zepam_rig.ZepamWritePoses(fp)
        return

    def getDrivers():
        return zepam_rig.getZepamDrivers()

elif ExternalRig == None:
    pass
else:
    raise NameError("Unknown external rig %s" % ExternalRig)
    

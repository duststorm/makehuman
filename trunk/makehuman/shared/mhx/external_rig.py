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

#ExternalRig = "Blenrig"
ExternalRig = None

if ExternalRig == "Blenrig":
    import blenrig_rig
    
    BoneGroups = [('GEN', 'THEME13'),
                  ('IK', 'THEME05'),
                  ('FK', 'THEME09'),
                  ('FACIAL', 'THEME02')]
    RecalcRoll = []              
    VertexGroupFiles = ["./shared/mhx/templates/blenrigmesh_weights.mhx"]
    GizmoFiles = ["./shared/mhx/templates/blenrig_gizmos.mhx"]
        
    Joints = blenrig_rig.BlenrigJoints
    HeadsTails = blenrig_rig.BlenrigHeadsTails
    Armature = blenrig_rig.BlenrigArmature
    ObjectProps = blenrig_rig.BlenrigObjectProps
    ArmatureProps = blenrig_rig.BlenrigArmatureProps
    
    def writePoses(fp):
        blenrig_rig.BlenrigWritePoses(fp)
        return

    def getDrivers():
        return blenrig_rig.getBlenrigDrivers()

elif ExternalRig == None:
    pass
else:
    raise NameError("Unknown external rig %s" % ExternalRig)
    

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://www.makehuman.org/node/319)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import Blender

pbones = Blender.Object.Get('Human').getPose().bones

def clamp(x, xmin, xmax):
	if x < xmin:
		return xmin
	elif x > xmax:
		return xmax
	else:
		return x

#
#	Rotations, including constraints
#	1 = 90 deg, -1 = -90 deg

def rotX(name):
	return 0
	return 1.414*pbones[name].quat.x

def rotZ(name):
	return 1.414*pbones[name].quat.z

#
#	Bones - used driven bones instead
#	Problems with py-drivers: 
#	quat not updated by constraints
#	posematrix in armature space, not bone space
#
'''
def ctrlBendElbowForward_L():
	r = rotX('LoArm_L')
	return clamp(r, 0, 1)

def ctrlBendElbowForward_R():
	r = rotX('LoArm_R')
	return clamp(r, 0, 1)

def ctrlBendHeadForward():
	r = rotX('Head')
	return clamp(3*r, 0, 1)

def ctrlBendKneeBack_L():
	r = rotX('LoLeg_L')
	return -clamp(r, -1, 0)

def ctrlBendKneeBack_R():
	r = rotX('LoLeg_R')
	return -clamp(r, -1, 0)

def ctrlBendLegBack_L():
	r = rotX('UpLeg_L')
	return -clamp(2*r, -1, 0)

def ctrlBendLegBack_R():
	r = rotX('UpLeg_R')
	return -clamp(2*r, -1, 0)

def ctrlBendLegForward_L():
	r = rotX('UpLeg_L')
	return clamp(r, 0, 1)

def ctrlBendLegForward_R():
	r = rotX('UpLeg_R')
	return clamp(r, 0, 1)

def ctrlShoulderDown_L():
	r = rotZ('UpArm_L')
	return -clamp(r, -1, 0)

def ctrlShoulderDown_R():
	r = rotZ('UpArm_R')
	return clamp(r, 0, 1)
'''
#
#	Face representation
#

fullScale = 0.25
factor = 1/fullScale

#
#	Brows
#

def ctrlBrowsMidDown():
	return factor*clamp(pbones['PBrows'].loc.z, 0, fullScale)

def ctrlBrowsMidUp():
	return -factor*clamp(pbones['PBrows'].loc.z, -fullScale, 0)

def ctrlBrowsSqueeze():
	return -factor*clamp(pbones['PBrows'].loc.x, -fullScale, 0)

def ctrlBrowsDown_L():
	return factor*clamp(pbones['PBrow_L'].loc.z, 0, fullScale)

def ctrlBrowsDown_R():
	return factor*clamp(pbones['PBrow_R'].loc.z, 0, fullScale)

def ctrlBrowsOutUp_L():
	return -factor*clamp(pbones['PBrow_L'].loc.z, -fullScale, 0)

def ctrlBrowsOutUp_R():
	return -factor*clamp(pbones['PBrow_R'].loc.z, -fullScale, 0)

#
#	Lids
#

def ctrlUpLidDown_L():
	z = clamp(pbones['PUpLid_L'].loc.z, -0.5*fullScale, fullScale)
	r = rotX('Eye_L')
	r = clamp(0.5*r, -0.5*fullScale, 0.5*fullScale)
	return factor*clamp(z-r, -0.5*fullScale, fullScale)

def ctrlUpLidDown_R():
	z = clamp(pbones['PUpLid_R'].loc.z, -0.5*fullScale, fullScale)
	r = rotX('Eye_R')
	r = clamp(0.5*r, -0.5*fullScale, 0.5*fullScale)
	return factor*clamp(z-r, -0.5*fullScale, fullScale)

def ctrlLoLidUp_L():
	z = clamp(pbones['PLoLid_L'].loc.z, -0.5*fullScale, fullScale)
	r = rotX('Eye_L')
	r = clamp(0.5*r, -0.5*fullScale, 0.5*fullScale)
	return factor*clamp(-z+r, -0.5*fullScale, fullScale)

def ctrlLoLidUp_R():
	z = clamp(pbones['PLoLid_R'].loc.z, -0.5*fullScale, fullScale)
	r = rotX('Eye_R')
	r = clamp(0.5*r, -0.5*fullScale, 0.5*fullScale)
	return factor*clamp(-z+r, -0.5*fullScale, fullScale)


#
#	Nose and jaw
#

def ctrlSneer_L():
	z = clamp(pbones['PNose'].loc.x, 0, fullScale) - clamp(pbones['PNose'].loc.z, -fullScale, 0)
	return factor*clamp(z, 0, fullScale)

def ctrlSneer_R():
	z = -clamp(pbones['PNose'].loc.x, -fullScale, 0) - clamp(pbones['PNose'].loc.z, -fullScale, 0)
	return factor*clamp(z, 0, fullScale)

def ctrlCheekUp_L():
	return -factor*clamp(pbones['PCheek_L'].loc.z, -fullScale, 0)

def ctrlCheekUp_R():
	return -factor*clamp(pbones['PCheek_R'].loc.z, -fullScale, 0)

def ctrlSquint_L():
	return factor*clamp(pbones['PCheek_L'].loc.x, 0, fullScale)

def ctrlSquint_R():
	return -factor*clamp(pbones['PCheek_R'].loc.x, -fullScale, 0)


#
#	Jaw and tounge
#

def ctrlMouthOpen():
	return factor*clamp(pbones['PJaw'].loc.z, 0, 1.5*fullScale)

def ctrlTongueOut():
	return factor*clamp(pbones['PJaw'].loc.x, -fullScale, 2*fullScale)

def ctrlTongueUp():
	return -factor*clamp(pbones['PTongue'].loc.z, -3*fullScale, 0)

def ctrlTongueLeft():
	return factor*clamp(pbones['PTongue'].loc.x, 0, 2*fullScale)

def ctrlTongueRight():
	return -factor*clamp(pbones['PTongue'].loc.x, -2*fullScale, 0)

#
#	Mouth expressions
#

def ctrlSmile_L():
	z = clamp(pbones['PMouth'].loc.x, 0, fullScale) + clamp(pbones['PMouth_L'].loc.x, 0, fullScale)
	return factor*clamp(z, 0, fullScale)

def ctrlSmile_R():
	z = clamp(pbones['PMouth'].loc.x, 0, fullScale) - clamp(pbones['PMouth_R'].loc.x, -fullScale, 0)
	return factor*clamp(z, 0, fullScale)

def ctrlFrown_L():
	z = clamp(pbones['PMouth'].loc.z, 0, fullScale) + clamp(pbones['PMouth_L'].loc.z, 0, fullScale)
	return factor*clamp(z, 0, fullScale)

def ctrlFrown_R():
	z = clamp(pbones['PMouth'].loc.z, 0, fullScale) + clamp(pbones['PMouth_R'].loc.z, 0, fullScale)
	return factor*clamp(z, 0, fullScale)

def ctrlNarrow_L():
	z = -clamp(pbones['PMouth'].loc.x, -fullScale, 0) - clamp(pbones['PMouth_L'].loc.x, -fullScale, 0)
	return factor*clamp(z, 0, fullScale)

def ctrlNarrow_R():
	z = -clamp(pbones['PMouth'].loc.x, -fullScale, 0) + clamp(pbones['PMouth_R'].loc.x, 0, fullScale)
	return factor*clamp(z, 0, fullScale)

#
#	Lips
#

def ctrlUpLipUp_L():
	z = -clamp(pbones['PUpLip'].loc.z, -fullScale, 0) - clamp(pbones['PUpLip_L'].loc.z, -fullScale, 0)
	return factor*clamp(z, 0, fullScale)

def ctrlUpLipUp_R():
	z = -clamp(pbones['PUpLip'].loc.z, -fullScale, 0) - clamp(pbones['PUpLip_R'].loc.z, -fullScale, 0)
	return factor*clamp(z, 0, fullScale)

def ctrlUpLipDown_L():
	z = clamp(pbones['PUpLip'].loc.z, 0, fullScale) + clamp(pbones['PUpLip_L'].loc.z, 0, fullScale)
	return factor*clamp(z, 0, fullScale)

def ctrlUpLipDown_R():
	z = clamp(pbones['PUpLip'].loc.z, 0, fullScale) + clamp(pbones['PUpLip_R'].loc.z, 0, fullScale)
	return factor*clamp(z, 0, fullScale)

def ctrlLoLipUp_L():
	z = -clamp(pbones['PLoLip'].loc.z, -fullScale, 0) - clamp(pbones['PLoLip_L'].loc.z, -fullScale, 0)
	return factor*clamp(z, 0, fullScale)

def ctrlLoLipUp_R():
	z = -clamp(pbones['PLoLip'].loc.z, -fullScale, 0) - clamp(pbones['PLoLip_R'].loc.z, -fullScale, 0)
	return factor*clamp(z, 0, fullScale)

def ctrlLoLipDown_L():
	z = clamp(pbones['PLoLip'].loc.z, 0, fullScale) + clamp(pbones['PLoLip_L'].loc.z, 0, fullScale)
	return factor*clamp(z, 0, fullScale)

def ctrlLoLipDown_R():
	z = clamp(pbones['PLoLip'].loc.z, 0, fullScale) + clamp(pbones['PLoLip_R'].loc.z, 0, fullScale)
	return factor*clamp(z, 0, fullScale)

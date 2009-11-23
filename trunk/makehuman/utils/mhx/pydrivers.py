import Blender

pbones = Blender.Object.Get('HumanRig').getPose().bones

def clamp(x, xmin, xmax):
	if x < xmin:
		return xmin
	elif x > xmax:
		return xmax
	else:
		return x

#
#	Bones
#

def ctrlBendElbowForward_L():
	return clamp(pbones['LoArm_L'].quat.x, 0, 1)

def ctrlBendElbowForward_R():
	return clamp(pbones['LoArm_R'].quat.x, 0, 1)

def ctrlBendHeadForward():
	return clamp(pbones['Head'].quat.x, 0, 1)

def ctrlBendKneeBack_L():
	return clamp(pbones['LoLeg_L'].quat.x, 0, 1)

def ctrlBendKneeBack_R():
	return clamp(pbones['LoLeg_R'].quat.x, 0, 1)

def ctrlBendLegBack_L():
	return -clamp(pbones['UpLeg_L'].quat.x, -1, 0)

def ctrlBendLegBack_R():
	return -clamp(pbones['UpLeg_R'].quat.x, -1, 0)

def ctrlBendLegForward_L():
	return clamp(pbones['UpLeg_L'].quat.x, 0, 1)

def ctrlBendLegForward_R():
	return clamp(pbones['UpLeg_R'].quat.x, 0, 1)

def ctrlShoulderDown_L():
	return- clamp(pbones['UpArm_L'].quat.z, -1, 0)

def ctrlShoulderDown_R():
	return clamp(pbones['UpArm_R'].quat.x, 0, 1)

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
#	Left = matrix[1][0]
#	Up = matrix[1][1]

def ctrlUpLidDown_L():
	z = clamp(pbones['PUpLid_L'].loc.z, -0.5*fullScale, fullScale)
	r = clamp(0.5*pbones['Eye_L'].poseMatrix[1][1], -0.5*fullScale, 0.5*fullScale)
	return factor*clamp(z-r, -0.5*fullScale, fullScale)

def ctrlUpLidDown_R():
	z = clamp(pbones['PUpLid_R'].loc.z, -0.5*fullScale, fullScale)
	r = clamp(0.5*pbones['Eye_R'].poseMatrix[1][1], -0.5*fullScale, 0.5*fullScale)
	return factor*clamp(z-r, -0.5*fullScale, fullScale)

def ctrlLoLidUp_L():
	z = clamp(pbones['PLoLid_L'].loc.z, -0.5*fullScale, fullScale)
	r = clamp(0.5*pbones['Eye_L'].poseMatrix[1][1], -0.5*fullScale, 0.5*fullScale)
	return factor*clamp(-z+r, -0.5*fullScale, fullScale)

def ctrlLoLidUp_R():
	z = clamp(pbones['PLoLid_R'].loc.z, -0.5*fullScale, fullScale)
	r = clamp(0.5*pbones['Eye_R'].poseMatrix[1][1], -0.5*fullScale, 0.5*fullScale)
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

def ctrlToungeUp():
	return -factor*clamp(pbones['PTounge'].loc.z, -3*fullScale, 0)

def ctrlToungeLeft():
	return factor*clamp(pbones['PTounge'].loc.x, 0, 2*fullScale)

def ctrlToungeRight():
	return -factor*clamp(pbones['PTounge'].loc.x, -2*fullScale, 0)

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







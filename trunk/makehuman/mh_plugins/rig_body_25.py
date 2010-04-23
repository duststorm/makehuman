#
#	Body bone definitions
#

import mhx_rig
from mhx_rig import *

BodyJoints = [
	('pelvis',			'j', 'pelvis'),
	('spine3',			'j', 'spine3'),
	('spine2',			'j', 'spine2'),
	('spine1',			'j', 'spine1'),
	('chest-front',			'v', 7292),
	('neck',			'j', 'neck'),
	('head',			'j', 'head'),

	('r-toe-1-1',			'j', 'r-toe-1-1'),
	('l-toe-1-1',			'j', 'l-toe-1-1'),
	('mid-feet',			'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
	('Root_head',			'o', ('mid-feet', [0,-0.3,0])),
	('Root_tail',			'o', ('Root_head', [0,0,-1])),
	#('Root_head',			'o', ('mid-feet', [0.0, 1.0, 0.0])),
	#('Root_tail',			'o', ('mid-feet', [0.0, -1.0, 0.0])),
	('Torso_head',			'o', ('pelvis', [0.0, 0.0, -3.0])),
	('Hips_tail',			'o', ('pelvis', [0.0, -1.5, 0.0])),
]

BodyHeadsTails = [

	('Root',			'Root_head', 'Root_tail'),
	('Torso',			'Hips_tail', 'pelvis'),
	('Hips',			'pelvis', 'Hips_tail'),
	#('Hips-inv',			'Hips-inv_head', 'pelvis'),
	('Pelvis',			'pelvis', 'spine3'),
	('Spine3',			'spine3', 'spine2'),
	('Spine2',			'spine2', 'spine1'),
	('Spine1',			'spine1', 'neck'),
	('Neck',			'neck', 'head'),
	('Head',			'head', 'head-end'),
	('Breathe',			'spine1', 'chest-front'),
	('Stomach',			'chest-front', 'pelvis'),

]

BodyArmature = [
	('Root', 'True',		0.0, None, F_WIR, L_MAIN, (1,1,1) ),
	('Torso', 'True',		0.0, 'Root', F_WIR, L_MAIN+L_SKEL, (1,1,1) ),
	('Hips', 'True',		-3.14159, 'Torso', F_DEF+F_CON+F_WIR, L_DEF, (1,1,1) ),

	('Pelvis', 'True',		0.0, 'Torso', F_CON, L_HELP, (1,1,1) ),
	('Spine3', 'True',		0.0, 'Pelvis', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_DEF, (1,1,1) ),
	('Spine2', 'True',		0.0, 'Spine3', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_DEF, (1,1,1) ),
	('Spine1', 'True',		0.0, 'Spine2', F_DEF+F_CON+F_WIR, L_DEF, (1,1,1) ),
	('Breathe', 'True',		0.0, 'Spine2', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Stomach', 'True',		-3.14159, 'Breathe', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Neck', 'True',		0.0, 'Spine1', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_HEAD+L_DEF, (1,1,1) ),
	('Head', 'True',		0.0, 'Neck', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_HEAD+L_DEF, (1,1,1) ),
]

def BodyWritePoses(fp):
	global boneGroups
	boneGroups = {}

	addPoseBone(fp, 'True', 'Root', 'GoboRoot', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Torso', 'GoboHips', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Hips', 'MHCircle10', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Hip_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Hip_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Spinal column
	addPoseBone(fp, 'True', 'Pelvis', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Spine3', 'MHCircle10', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Spine2', 'MHCircle15', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Spine1', 'MHCircle10', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Breathe', None, None, (0,0,0), (0,0,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Stomach', None, None, (0,0,0), (0,0,0), (1,0,1), (1,1,1), 0,
		[('LimitRot', C_OW_LOCAL+C_LTRA, ['Const', (0,0, 0,0, 0,0), (1,0,1)]),
		 ('StretchTo', 0, ['Const.001', 'Hips', 'PLANE_Z'])])

	addPoseBone(fp, 'True', 'Neck', 'GoboNeck', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'True', 'Head', 'GoboHead', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	return
	

#
#	Toe bone definitions
#

import mhx_rig
from mhx_rig import *

ToeJoints = [

	('r-toe-1-1',			'j', 'r-toe-1-1'),
	('r-toe-1-2',			'j', 'r-toe-1-2'),
	('r-toe-2-1',			'j', 'r-toe-2-1'),
	('r-toe-2-2',			'j', 'r-toe-2-2'),
	('r-toe-2-3',			'j', 'r-toe-2-3'),
	('r-toe-3-1',			'j', 'r-toe-3-1'),
	('r-toe-3-2',			'j', 'r-toe-3-2'),
	('r-toe-3-3',			'j', 'r-toe-3-3'),
	('r-toe-4-1',			'j', 'r-toe-4-1'),
	('r-toe-4-2',			'j', 'r-toe-4-2'),
	('r-toe-4-3',			'j', 'r-toe-4-3'),
	('r-toe-5-1',			'j', 'r-toe-5-1'),
	('r-toe-5-2',			'j', 'r-toe-5-2'),
	('r-toe-5-3',			'j', 'r-toe-5-3'),

	('l-toe-1-1',			'j', 'l-toe-1-1'),
	('l-toe-1-2',			'j', 'l-toe-1-2'),
	('l-toe-2-1',			'j', 'l-toe-2-1'),
	('l-toe-2-2',			'j', 'l-toe-2-2'),
	('l-toe-2-3',			'j', 'l-toe-2-3'),
	('l-toe-3-1',			'j', 'l-toe-3-1'),
	('l-toe-3-2',			'j', 'l-toe-3-2'),
	('l-toe-3-3',			'j', 'l-toe-3-3'),
	('l-toe-4-1',			'j', 'l-toe-4-1'),
	('l-toe-4-2',			'j', 'l-toe-4-2'),
	('l-toe-4-3',			'j', 'l-toe-4-3'),
	('l-toe-5-1',			'j', 'l-toe-5-1'),
	('l-toe-5-2',			'j', 'l-toe-5-2'),
	('l-toe-5-3',			'j', 'l-toe-5-3'),

	('l-toe-1-end',			'l', ((2.0, 'l-toe-1-2'), (-1.0, 'l-toe-1-1'))),
	('l-toe-2-end',			'l', ((2.0, 'l-toe-2-3'), (-1.0, 'l-toe-2-2'))),
	('l-toe-3-end',			'l', ((2.0, 'l-toe-3-3'), (-1.0, 'l-toe-3-2'))),
	('l-toe-4-end',			'l', ((2.0, 'l-toe-4-3'), (-1.0, 'l-toe-4-2'))),
	('l-toe-5-end',			'l', ((2.0, 'l-toe-5-3'), (-1.0, 'l-toe-5-2'))),
	('r-toe-1-end',			'l', ((2.0, 'r-toe-1-2'), (-1.0, 'r-toe-1-1'))),
	('r-toe-2-end',			'l', ((2.0, 'r-toe-2-3'), (-1.0, 'r-toe-2-2'))),
	('r-toe-3-end',			'l', ((2.0, 'r-toe-3-3'), (-1.0, 'r-toe-3-2'))),
	('r-toe-4-end',			'l', ((2.0, 'r-toe-4-3'), (-1.0, 'r-toe-4-2'))),
	('r-toe-5-end',			'l', ((2.0, 'r-toe-5-3'), (-1.0, 'r-toe-5-2'))),
	('r-toe-end',			'l', ((2.0, 'r-toe-3-3'), (-1.0, 'r-toe-3-1'))),
	('l-toe-end',			'l', ((2.0, 'l-toe-3-3'), (-1.0, 'l-toe-3-1'))),
]

ToeHeadsTails = [
	('Toe-1-1_L',			'r-toe-1-1', 'r-toe-1-2'),
	('Toe-1-2_L',			'r-toe-1-2', 'r-toe-1-end'),
	('Toe-2-1_L',			'r-toe-2-1', 'r-toe-2-2'),
	('Toe-2-2_L',			'r-toe-2-2', 'r-toe-2-3'),
	('Toe-2-3_L',			'r-toe-2-3', 'r-toe-2-end'),
	('Toe-3-1_L',			'r-toe-3-1', 'r-toe-3-2'),
	('Toe-3-2_L',			'r-toe-3-2', 'r-toe-3-3'),
	('Toe-3-3_L',			'r-toe-3-3', 'r-toe-3-end'),
	('Toe-4-1_L',			'r-toe-4-1', 'r-toe-4-2'),
	('Toe-4-2_L',			'r-toe-4-2', 'r-toe-4-3'),
	('Toe-4-3_L',			'r-toe-4-3', 'r-toe-4-end'),
	('Toe-5-1_L',			'r-toe-5-1', 'r-toe-5-2'),
	('Toe-5-2_L',			'r-toe-5-2', 'r-toe-5-3'),
	('Toe-5-3_L',			'r-toe-5-3', 'r-toe-5-end'),
	

	('Toe-1-1_R',			'l-toe-1-1', 'l-toe-1-2'),
	('Toe-1-2_R',			'l-toe-1-2', 'l-toe-1-end'),
	('Toe-2-1_R',			'l-toe-2-1', 'l-toe-2-2'),
	('Toe-2-2_R',			'l-toe-2-2', 'l-toe-2-3'),
	('Toe-2-3_R',			'l-toe-2-3', 'l-toe-2-end'),
	('Toe-3-1_R',			'l-toe-3-1', 'l-toe-3-2'),
	('Toe-3-2_R',			'l-toe-3-2', 'l-toe-3-3'),
	('Toe-3-3_R',			'l-toe-3-3', 'l-toe-3-end'),
	('Toe-4-1_R',			'l-toe-4-1', 'l-toe-4-2'),
	('Toe-4-2_R',			'l-toe-4-2', 'l-toe-4-3'),
	('Toe-4-3_R',			'l-toe-4-3', 'l-toe-4-end'),
	('Toe-5-1_R',			'l-toe-5-1', 'l-toe-5-2'),
	('Toe-5-2_R',			'l-toe-5-2', 'l-toe-5-3'),
	('Toe-5-3_R',			'l-toe-5-3', 'l-toe-5-end'),
]	

ToeArmature = [
	# Left toes
	('Toe-1-1_L', 'rigLeg&T_Toes',		2.42599, 'Toes_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-1-2_L', 'rigLeg&T_Toes',		2.42596, 'Toe-1-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-2-1_L', 'rigLeg&T_Toes',		1.79768, 'Toes_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-2-2_L', 'rigLeg&T_Toes',		-0.506141, 'Toe-2-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-2-3_L', 'rigLeg&T_Toes',		-0.506141, 'Toe-2-2_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-3-1_L', 'rigLeg&T_Toes',		2.77507, 'Toes_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-3-2_L', 'rigLeg&T_Toes',		3.05438, 'Toe-3-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-3-3_L', 'rigLeg&T_Toes',		3.05438, 'Toe-3-2_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-4-1_L', 'rigLeg&T_Toes',		-2.82743, 'Toes_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-4-2_L', 'rigLeg&T_Toes',		3.00198, 'Toe-4-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-4-3_L', 'rigLeg&T_Toes',		3.00198, 'Toe-4-2_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-5-1_L', 'rigLeg&T_Toes',		2.79252, 'Toes_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-5-2_L', 'rigLeg&T_Toes',		-2.9845, 'Toe-5-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-5-3_L', 'rigLeg&T_Toes',		-2.9845, 'Toe-5-2_L', F_DEF+F_CON, L_TOE, (1,1,1) ),

	# Right toes
	('Toe-1-1_R', 'rigLeg&T_Toes',		-2.42599, 'Toes_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-1-2_R', 'rigLeg&T_Toes',		-2.42598, 'Toe-1-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-2-1_R', 'rigLeg&T_Toes',		-1.79768, 'Toes_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-2-2_R', 'rigLeg&T_Toes',		0.506136, 'Toe-2-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-2-3_R', 'rigLeg&T_Toes',		0.506138, 'Toe-2-2_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-3-1_R', 'rigLeg&T_Toes',		-2.77507, 'Toes_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-3-2_R', 'rigLeg&T_Toes',		-3.05438, 'Toe-3-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-3-3_R', 'rigLeg&T_Toes',		-3.05439, 'Toe-3-2_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-4-1_R', 'rigLeg&T_Toes',		2.82743, 'Toes_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-4-2_R', 'rigLeg&T_Toes',		-3.00197, 'Toe-4-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-4-3_R', 'rigLeg&T_Toes',		-3.00197, 'Toe-4-2_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-5-1_R', 'rigLeg&T_Toes',		-2.79252, 'Toes_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-5-2_R', 'rigLeg&T_Toes',		2.98449, 'Toe-5-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-5-3_R', 'rigLeg&T_Toes',		2.98449, 'Toe-5-2_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
]

def ToeWritePoses(fp):
	global boneGroups
	boneGroups = {}

	# Left toes
	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-1-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-1-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-2-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-2-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-2-3_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-3-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-3-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-3-3_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-4-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-4-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-4-3_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-5-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-5-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-5-3_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	# Right toes
	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-1-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-1-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-2-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-2-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-2-3_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-3-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-3-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-3-3_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-4-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-4-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-4-3_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-5-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-5-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'rigLeg&T_Toes', 'Toe-5-3_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])
	return


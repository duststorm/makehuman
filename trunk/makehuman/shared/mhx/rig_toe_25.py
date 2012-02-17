#
#	Toe bone definitions
#

import mhx_globals as the
from mhx_globals import *
from mhx_rig import addPoseBone

ToeJoints = [
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
	('Toe-1-1_L',		2.42599, 'Toe_L', F_DEF, L_TOE, NoBB),
	('Toe-1-2_L',		2.42596, 'Toe-1-1_L', F_DEF, L_TOE, NoBB),
	('Toe-2-1_L',		1.79768, 'Toe_L', F_DEF, L_TOE, NoBB),
	('Toe-2-2_L',		-0.506141, 'Toe-2-1_L', F_DEF, L_TOE, NoBB),
	('Toe-2-3_L',		-0.506141, 'Toe-2-2_L', F_DEF, L_TOE, NoBB),
	('Toe-3-1_L',		2.77507, 'Toe_L', F_DEF, L_TOE, NoBB),
	('Toe-3-2_L',		3.05438, 'Toe-3-1_L', F_DEF, L_TOE, NoBB),
	('Toe-3-3_L',		3.05438, 'Toe-3-2_L', F_DEF, L_TOE, NoBB),
	('Toe-4-1_L',		-2.82743, 'Toe_L', F_DEF, L_TOE, NoBB),
	('Toe-4-2_L',		3.00198, 'Toe-4-1_L', F_DEF, L_TOE, NoBB),
	('Toe-4-3_L',		3.00198, 'Toe-4-2_L', F_DEF, L_TOE, NoBB),
	('Toe-5-1_L',		2.79252, 'Toe_L', F_DEF, L_TOE, NoBB),
	('Toe-5-2_L',		-2.9845, 'Toe-5-1_L', F_DEF, L_TOE, NoBB),
	('Toe-5-3_L',		-2.9845, 'Toe-5-2_L', F_DEF, L_TOE, NoBB),

	# Right toes
	('Toe-1-1_R',		-2.42599, 'Toe_R', F_DEF, L_TOE, NoBB),
	('Toe-1-2_R',		-2.42598, 'Toe-1-1_R', F_DEF, L_TOE, NoBB),
	('Toe-2-1_R',		-1.79768, 'Toe_R', F_DEF, L_TOE, NoBB),
	('Toe-2-2_R',		0.506136, 'Toe-2-1_R', F_DEF, L_TOE, NoBB),
	('Toe-2-3_R',		0.506138, 'Toe-2-2_R', F_DEF, L_TOE, NoBB),
	('Toe-3-1_R',		-2.77507, 'Toe_R', F_DEF, L_TOE, NoBB),
	('Toe-3-2_R',		-3.05438, 'Toe-3-1_R', F_DEF, L_TOE, NoBB),
	('Toe-3-3_R',		-3.05439, 'Toe-3-2_R', F_DEF, L_TOE, NoBB),
	('Toe-4-1_R',		2.82743, 'Toe_R', F_DEF, L_TOE, NoBB),
	('Toe-4-2_R',		-3.00197, 'Toe-4-1_R', F_DEF, L_TOE, NoBB),
	('Toe-4-3_R',		-3.00197, 'Toe-4-2_R', F_DEF, L_TOE, NoBB),
	('Toe-5-1_R',		-2.79252, 'Toe_R', F_DEF, L_TOE, NoBB),
	('Toe-5-2_R',		2.98449, 'Toe-5-1_R', F_DEF, L_TOE, NoBB),
	('Toe-5-3_R',		2.98449, 'Toe-5-2_R', F_DEF, L_TOE, NoBB),
]

#
#	addToePoses(fp):
#

def addToePoses(fp):
	# Left toes
	addPoseBone(fp, 'Toe-1-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-1-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-2-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-2-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-2-3_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-3-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-3-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-3-3_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-4-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-4-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-4-3_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-5-1_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-5-2_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-5-3_L', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	# Right toes
	addPoseBone(fp, 'Toe-1-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-1-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-2-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-2-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-2-3_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-3-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-3-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-3-3_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-4-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-4-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-4-3_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-5-1_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-5-2_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Toe-5-3_R', None, None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])
	return



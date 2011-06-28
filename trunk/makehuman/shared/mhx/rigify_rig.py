#
#  Bone definitions for Rigify rig
#
import mhx_rig
from mhx_rig import *
RigifyJoints = [
	('hips_head',				'vo', [7186, 0.000000, -0.144993, 0.144267]),
	('hips_tail',				'vo', [15318, 0.000000, -0.006407, 0.084869]),
	('spine_tail',				'vo', [14048, 0.000000, -0.001896, -0.093766]),
	('ribs_tail',				'vo', [14040, 0.000000, -0.131061, -0.095334]),
	('neck_tail',				'vo', [14033, -0.066200, 0.000875, 0.001135]),
	('head_tail',				'vo', [8225, 0.000000, -0.004809, -0.008947]),
	('shoulder.L_head',			'vo', [14251, -0.007489, -0.134305, 0.002279]),
	('shoulder.L_tail',			'vo', [2605, -0.002768, -0.187960, -0.172365]),
	('upper_arm.L_head',			'vo', [14162, 0.000263, -0.032312, 0.004358]),
	('upper_arm.L_tail',			'vo', [14155, 0.006233, -0.068752, -0.000617]),
	('forearm.L_tail',			'vo', [14057, 0.004179, 0.008681, -0.004887]),
	('hand.L_tail',				'vo', [5828, -0.011023, 0.028669, 0.123052]),
	('palm.01.L_head',			'vo', [14066, 0.034904, 0.039543, 0.000412]),
	('palm.01.L_tail',			'vo', [14083, -0.000314, 0.022303, 0.002184]),
	('finger_index.01.L_tail',		'vo', [14104, -0.022503, 0.001451, 0.001106]),
	('finger_index.02.L_tail',		'vo', [14147, 0.000686, 0.001829, 0.022221]),
	('finger_index.03.L_tail',		'vo', [5983, -0.001169, -0.000999, 0.004105]),
	('thumb.01.L_head',			'vo', [14063, 0.001896, -0.000625, -0.069749]),
	('thumb.01.L_tail',			'vo', [14071, 0.001892, 0.030307, 0.003018]),
	('thumb.02.L_tail',			'vo', [14075, 0.002411, -0.000391, 0.021994]),
	('thumb.03.L_tail',			'vo', [3226, -0.003440, -0.003716, -0.008109]),
	('palm.02.L_head',			'vo', [15262, 0.000543, -0.001391, -0.012671]),
	('palm.02.L_tail',			'vo', [14088, 0.022461, -0.003573, 0.001709]),
	('finger_middle.01.L_tail',		'vo', [14114, -0.000028, -0.017905, -0.005533]),
	('finger_middle.02.L_tail',		'vo', [14144, -0.001652, -0.017482, -0.003376]),
	('finger_middle.03.L_tail',		'vo', [5779, 0.000264, 0.001044, -0.003921]),
	('palm.03.L_head',			'vo', [15269, 0.017008, -0.074894, 0.014063]),
	('palm.03.L_tail',			'vo', [14093, 0.005182, 0.004943, 0.016106]),
	('finger_ring.01.L_tail',		'vo', [14120, -0.003160, -0.020812, 0.000576]),
	('finger_ring.02.L_tail',		'vo', [14134, -0.019649, 0.003439, -0.001024]),
	('finger_ring.03.L_tail',		'vo', [6150, 0.007152, 0.007275, -0.001324]),
	('palm.04.L_head',			'vo', [15272, -0.029683, 0.002840, -0.005472]),
	('palm.04.L_tail',			'vo', [14099, -0.004268, 0.003798, 0.028711]),
	('finger_pinky.01.L_tail',		'vo', [14126, -0.000705, -0.020259, 0.001924]),
	('finger_pinky.02.L_tail',		'vo', [6470, -0.002528, -0.001478, 0.013350]),
	('finger_pinky.03.L_tail',		'vo', [6467, 0.004072, 0.000381, -0.015621]),
	('shoulder.R_head',			'vo', [14291, 0.007489, -0.134305, 0.002279]),
	('shoulder.R_tail',			'vo', [11005, 0.002768, -0.187960, -0.172365]),
	('upper_arm.R_head',			'vo', [14380, -0.000263, -0.032312, 0.004358]),
	('upper_arm.R_tail',			'vo', [14387, -0.006233, -0.068752, -0.000617]),
	('forearm.R_tail',			'vo', [14485, -0.004179, 0.008681, -0.004887]),
	('hand.R_tail',				'vo', [9713, 0.011023, 0.028669, 0.123052]),
	('palm.01.R_head',			'vo', [14476, -0.034904, 0.039543, 0.000412]),
	('palm.01.R_tail',			'vo', [14459, 0.000314, 0.022303, 0.002184]),
	('finger_index.01.R_tail',		'vo', [14438, 0.022503, 0.001451, 0.001106]),
	('finger_index.02.R_tail',		'vo', [14395, -0.000686, 0.001829, 0.022221]),
	('finger_index.03.R_tail',		'vo', [9585, 0.001169, -0.000999, 0.004105]),
	('thumb.01.R_head',			'vo', [14479, -0.001896, -0.000625, -0.069749]),
	('thumb.01.R_tail',			'vo', [14471, -0.001892, 0.030307, 0.003018]),
	('thumb.02.R_tail',			'vo', [14467, -0.002411, -0.000391, 0.021994]),
	('thumb.03.R_tail',			'vo', [10523, 0.003440, -0.003716, -0.008109]),
	('palm.02.R_head',			'vo', [15135, -0.000543, -0.001391, -0.012671]),
	('palm.02.R_tail',			'vo', [14454, -0.022461, -0.003573, 0.001709]),
	('finger_middle.01.R_tail',		'vo', [14428, 0.000028, -0.017905, -0.005533]),
	('finger_middle.02.R_tail',		'vo', [14398, 0.001652, -0.017482, -0.003376]),
	('finger_middle.03.R_tail',		'vo', [9762, -0.000264, 0.001044, -0.003921]),
	('palm.03.R_head',			'vo', [15128, -0.017008, -0.074894, 0.014063]),
	('palm.03.R_tail',			'vo', [14449, -0.005182, 0.004943, 0.016106]),
	('finger_ring.01.R_tail',		'vo', [14422, 0.003160, -0.020812, 0.000576]),
	('finger_ring.02.R_tail',		'vo', [14408, 0.019649, 0.003439, -0.001024]),
	('finger_ring.03.R_tail',		'vo', [9418, -0.007152, 0.007275, -0.001324]),
	('palm.04.R_head',			'vo', [15125, 0.029683, 0.002840, -0.005472]),
	('palm.04.R_tail',			'vo', [14443, 0.004268, 0.003798, 0.028711]),
	('finger_pinky.01.R_tail',		'vo', [14416, 0.000705, -0.020259, 0.001924]),
	('finger_pinky.02.R_tail',		'vo', [9098, 0.002528, -0.001478, 0.013350]),
	('finger_pinky.03.R_tail',		'vo', [9101, -0.004072, 0.000381, -0.015621]),
	('thigh.L_head',			'vo', [14163, -0.006488, 0.002644, -0.073348]),
	('thigh.L_tail',			'vo', [14169, 0.004895, -0.001658, -0.075635]),
	('shin.L_tail',				'vo', [14180, -0.007381, -0.070216, -0.014005]),
	('foot.L_tail',				'vo', [15315, -0.030381, 0.069920, -0.004289]),
	('toe.L_tail',				'vo', [15307, 0.025519, -0.006347, -0.001478]),
	('heel.L_tail',				'vo', [5734, -0.045981, 0.104068, -0.244700]),
	('heel.02.L_head',			'vo', [5730, -0.227754, -0.066153, -0.257800]),
	('heel.02.L_tail',			'vo', [12348, 0.085510, -0.028553, -0.228400]),
	('thigh.R_head',			'vo', [14379, 0.006488, 0.002644, -0.073348]),
	('thigh.R_tail',			'vo', [14373, -0.004895, -0.001658, -0.075635]),
	('shin.R_tail',				'vo', [14362, 0.007381, -0.070216, -0.014005]),
	('foot.R_tail',				'vo', [15082, 0.030381, 0.069920, -0.004289]),
	('toe.R_tail',				'vo', [15090, -0.025519, -0.006347, -0.001478]),
	('heel.R_tail',				'vo', [13328, 0.045981, 0.104068, -0.244700]),
	('heel.02.R_head',			'vo', [13332, 0.227754, -0.066153, -0.257800]),
	('heel.02.R_tail',			'vo', [13168, -0.085510, -0.028553, -0.228400]),
]

RigifyHeadsTails = [
	('hips',			'hips_head', 'hips_tail'),
	('spine',			'hips_tail', 'spine_tail'),
	('ribs',			'spine_tail', 'ribs_tail'),
	('neck',			'ribs_tail', 'neck_tail'),
	('head',			'neck_tail', 'head_tail'),
	('shoulder.L',			'shoulder.L_head', 'shoulder.L_tail'),
	('upper_arm.L',			'upper_arm.L_head', 'upper_arm.L_tail'),
	('forearm.L',			'upper_arm.L_tail', 'forearm.L_tail'),
	('hand.L',			'forearm.L_tail', 'hand.L_tail'),
	('palm.01.L',			'palm.01.L_head', 'palm.01.L_tail'),
	('finger_index.01.L',		'palm.01.L_tail', 'finger_index.01.L_tail'),
	('finger_index.02.L',		'finger_index.01.L_tail', 'finger_index.02.L_tail'),
	('finger_index.03.L',		'finger_index.02.L_tail', 'finger_index.03.L_tail'),
	('thumb.01.L',			'thumb.01.L_head', 'thumb.01.L_tail'),
	('thumb.02.L',			'thumb.01.L_tail', 'thumb.02.L_tail'),
	('thumb.03.L',			'thumb.02.L_tail', 'thumb.03.L_tail'),
	('palm.02.L',			'palm.02.L_head', 'palm.02.L_tail'),
	('finger_middle.01.L',		'palm.02.L_tail', 'finger_middle.01.L_tail'),
	('finger_middle.02.L',		'finger_middle.01.L_tail', 'finger_middle.02.L_tail'),
	('finger_middle.03.L',		'finger_middle.02.L_tail', 'finger_middle.03.L_tail'),
	('palm.03.L',			'palm.03.L_head', 'palm.03.L_tail'),
	('finger_ring.01.L',		'palm.03.L_tail', 'finger_ring.01.L_tail'),
	('finger_ring.02.L',		'finger_ring.01.L_tail', 'finger_ring.02.L_tail'),
	('finger_ring.03.L',		'finger_ring.02.L_tail', 'finger_ring.03.L_tail'),
	('palm.04.L',			'palm.04.L_head', 'palm.04.L_tail'),
	('finger_pinky.01.L',		'palm.04.L_tail', 'finger_pinky.01.L_tail'),
	('finger_pinky.02.L',		'finger_pinky.01.L_tail', 'finger_pinky.02.L_tail'),
	('finger_pinky.03.L',		'finger_pinky.02.L_tail', 'finger_pinky.03.L_tail'),
	('shoulder.R',			'shoulder.R_head', 'shoulder.R_tail'),
	('upper_arm.R',			'upper_arm.R_head', 'upper_arm.R_tail'),
	('forearm.R',			'upper_arm.R_tail', 'forearm.R_tail'),
	('hand.R',			'forearm.R_tail', 'hand.R_tail'),
	('palm.01.R',			'palm.01.R_head', 'palm.01.R_tail'),
	('finger_index.01.R',		'palm.01.R_tail', 'finger_index.01.R_tail'),
	('finger_index.02.R',		'finger_index.01.R_tail', 'finger_index.02.R_tail'),
	('finger_index.03.R',		'finger_index.02.R_tail', 'finger_index.03.R_tail'),
	('thumb.01.R',			'thumb.01.R_head', 'thumb.01.R_tail'),
	('thumb.02.R',			'thumb.01.R_tail', 'thumb.02.R_tail'),
	('thumb.03.R',			'thumb.02.R_tail', 'thumb.03.R_tail'),
	('palm.02.R',			'palm.02.R_head', 'palm.02.R_tail'),
	('finger_middle.01.R',		'palm.02.R_tail', 'finger_middle.01.R_tail'),
	('finger_middle.02.R',		'finger_middle.01.R_tail', 'finger_middle.02.R_tail'),
	('finger_middle.03.R',		'finger_middle.02.R_tail', 'finger_middle.03.R_tail'),
	('palm.03.R',			'palm.03.R_head', 'palm.03.R_tail'),
	('finger_ring.01.R',		'palm.03.R_tail', 'finger_ring.01.R_tail'),
	('finger_ring.02.R',		'finger_ring.01.R_tail', 'finger_ring.02.R_tail'),
	('finger_ring.03.R',		'finger_ring.02.R_tail', 'finger_ring.03.R_tail'),
	('palm.04.R',			'palm.04.R_head', 'palm.04.R_tail'),
	('finger_pinky.01.R',		'palm.04.R_tail', 'finger_pinky.01.R_tail'),
	('finger_pinky.02.R',		'finger_pinky.01.R_tail', 'finger_pinky.02.R_tail'),
	('finger_pinky.03.R',		'finger_pinky.02.R_tail', 'finger_pinky.03.R_tail'),
	('thigh.L',			'thigh.L_head', 'thigh.L_tail'),
	('shin.L',			'thigh.L_tail', 'shin.L_tail'),
	('foot.L',			'shin.L_tail', 'foot.L_tail'),
	('toe.L',			'foot.L_tail', 'toe.L_tail'),
	('heel.L',			'shin.L_tail', 'heel.L_tail'),
	('heel.02.L',			'heel.02.L_head', 'heel.02.L_tail'),
	('thigh.R',			'thigh.R_head', 'thigh.R_tail'),
	('shin.R',			'thigh.R_tail', 'shin.R_tail'),
	('foot.R',			'shin.R_tail', 'foot.R_tail'),
	('toe.R',			'foot.R_tail', 'toe.R_tail'),
	('heel.R',			'shin.R_tail', 'heel.R_tail'),
	('heel.02.R',			'heel.02.R_head', 'heel.02.R_tail'),
]

RigifyArmature = [
	('hips',			0.0, None, F_DEF, 0x1, (1,1,1) ),
	('spine',			0.0, 'hips', F_DEF+F_CON, 0x1, (1,1,1) ),
	('ribs',			0.0, 'spine', F_DEF+F_CON, 0x1, (1,1,1) ),
	('neck',			0.0, 'ribs', F_DEF, 0x4, (1,1,1) ),
	('head',			0.0, 'neck', F_DEF+F_CON, 0x4, (1,1,1) ),
	('shoulder.L',			-0.0743, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('upper_arm.L',			1.75, 'shoulder.L', F_DEF, 0x40, (1,1,1) ),
	('forearm.L',			1.54, 'upper_arm.L', F_DEF+F_CON, 0x40, (1,1,1) ),
	('hand.L',			3, 'forearm.L', F_DEF+F_CON, 0x40, (1,1,1) ),
	('palm.01.L',			2.78, 'hand.L', F_DEF, 0x10, (1,1,1) ),
	('finger_index.01.L',		-2.94, 'palm.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_index.02.L',		-2.96, 'finger_index.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_index.03.L',		-2.95, 'finger_index.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('thumb.01.L',			-1.41, 'palm.01.L', F_DEF, 0x10, (1,1,1) ),
	('thumb.02.L',			-1.59, 'thumb.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('thumb.03.L',			-1.5, 'thumb.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('palm.02.L',			2.83, 'hand.L', F_DEF, 0x10, (1,1,1) ),
	('finger_middle.01.L',		-3.11, 'palm.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_middle.02.L',		-3.07, 'finger_middle.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_middle.03.L',		-3.11, 'finger_middle.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('palm.03.L',			2.96, 'hand.L', F_DEF, 0x10, (1,1,1) ),
	('finger_ring.01.L',		3.04, 'palm.03.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_ring.02.L',		3.08, 'finger_ring.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_ring.03.L',		2.97, 'finger_ring.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('palm.04.L',			-3.12, 'hand.L', F_DEF, 0x10, (1,1,1) ),
	('finger_pinky.01.L',		3.03, 'palm.04.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_pinky.02.L',		2.99, 'finger_pinky.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_pinky.03.L',		2.83, 'finger_pinky.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('shoulder.R',			0.0743, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('upper_arm.R',			-1.75, 'shoulder.R', F_DEF, 0x100, (1,1,1) ),
	('forearm.R',			-1.54, 'upper_arm.R', F_DEF+F_CON, 0x100, (1,1,1) ),
	('hand.R',			-3, 'forearm.R', F_DEF+F_CON, 0x100, (1,1,1) ),
	('palm.01.R',			-2.78, 'hand.R', F_DEF, 0x10, (1,1,1) ),
	('finger_index.01.R',		2.94, 'palm.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_index.02.R',		2.96, 'finger_index.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_index.03.R',		2.95, 'finger_index.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('thumb.01.R',			1.41, 'palm.01.R', F_DEF, 0x10, (1,1,1) ),
	('thumb.02.R',			1.59, 'thumb.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('thumb.03.R',			1.5, 'thumb.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('palm.02.R',			-2.83, 'hand.R', F_DEF, 0x10, (1,1,1) ),
	('finger_middle.01.R',		3.11, 'palm.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_middle.02.R',		3.07, 'finger_middle.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_middle.03.R',		3.11, 'finger_middle.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('palm.03.R',			-2.96, 'hand.R', F_DEF, 0x10, (1,1,1) ),
	('finger_ring.01.R',		-3.04, 'palm.03.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_ring.02.R',		-3.08, 'finger_ring.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_ring.03.R',		-2.97, 'finger_ring.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('palm.04.R',			3.12, 'hand.R', F_DEF, 0x10, (1,1,1) ),
	('finger_pinky.01.R',		-3.03, 'palm.04.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_pinky.02.R',		-2.99, 'finger_pinky.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_pinky.03.R',		-2.83, 'finger_pinky.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('thigh.L',			0.0296, 'hips', F_DEF, 0x400, (1,1,1) ),
	('shin.L',			0.0574, 'thigh.L', F_DEF+F_CON, 0x400, (1,1,1) ),
	('foot.L',			0.0, 'shin.L', F_DEF+F_CON, 0x400, (1,1,1) ),
	('toe.L',			3.14, 'foot.L', F_DEF+F_CON, 0x400, (1,1,1) ),
	('heel.L',			3.14, 'shin.L', F_DEF+F_CON, 0x400, (1,1,1) ),
	('heel.02.L',			0.0, 'heel.L', F_DEF, 0x400, (1,1,1) ),
	('thigh.R',			-0.0296, 'hips', F_DEF, 0x1000, (1,1,1) ),
	('shin.R',			-0.0574, 'thigh.R', F_DEF+F_CON, 0x1000, (1,1,1) ),
	('foot.R',			0.0, 'shin.R', F_DEF+F_CON, 0x1000, (1,1,1) ),
	('toe.R',			-3.14, 'foot.R', F_DEF+F_CON, 0x1000, (1,1,1) ),
	('heel.R',			-3.14, 'shin.R', F_DEF+F_CON, 0x1000, (1,1,1) ),
	('heel.02.R',			0.0, 'heel.R', F_DEF, 0x1000, (1,1,1) ),
]

def RigifyWritePoses(fp):
	global boneGroups
	boneGroups = {}

	mhx_rig.addPoseBone(fp, 'hips', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'spine', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'ribs', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'neck', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'head', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'shoulder.L', None, None, (1,1,1), (0,1,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'upper_arm.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'forearm.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'hand.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'palm.01.L', None, None, (1,1,1), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_index.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_index.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_index.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'thumb.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'thumb.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'thumb.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'palm.02.L', None, None, (1,1,1), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_middle.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_middle.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_middle.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'palm.03.L', None, None, (1,1,1), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_ring.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_ring.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_ring.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'palm.04.L', None, None, (1,1,1), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_pinky.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_pinky.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_pinky.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'shoulder.R', None, None, (1,1,1), (0,1,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'upper_arm.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'forearm.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'hand.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'palm.01.R', None, None, (0,0,0), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_index.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_index.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_index.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'thumb.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'thumb.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'thumb.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'palm.02.R', None, None, (0,0,0), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_middle.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_middle.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_middle.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'palm.03.R', None, None, (0,0,0), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_ring.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_ring.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_ring.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'palm.04.R', None, None, (0,0,0), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_pinky.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_pinky.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'finger_pinky.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'thigh.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'shin.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'foot.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'toe.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'heel.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'heel.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'thigh.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'shin.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'foot.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'toe.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'heel.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	mhx_rig.addPoseBone(fp, 'heel.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	return

RigifyObjectProps = [
]

RigifyArmatureProps = []


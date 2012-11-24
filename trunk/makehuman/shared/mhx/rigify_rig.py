#
#  Bone definitions for Rigify rig
#

from . import the
from the import *
from . import posebone
from posebone import addPoseBone

RigifyJoints = [
	('hips_head',				'vo', [7186, 0.000000, -0.144970, 0.144290]),
	('hips_tail',				'vo', [15318, 0.000000, -0.006396, 0.084900]),
	('spine_tail',				'vo', [14048, 0.000000, -0.001900, -0.093800]),
	('ribs_tail',				'vo', [14040, 0.000000, -0.131110, -0.095301]),
	('neck_tail',				'vo', [14035, 0.066178, 0.000900, 0.001100]),
	('head_tail',				'vo', [8225, 0.000000, -0.004820, -0.008902]),
	('shoulder.L_head',			'vo', [14251, -0.007515, -0.134283, 0.002300]),
	('shoulder.L_tail',			'vo', [2605, -0.002720, -0.187990, -0.172400]),
	('upper_arm.L_head',			'vo', [14162, 0.000270, -0.032300, 0.004300]),
	('upper_arm.L_tail',			'vo', [14155, 0.006240, -0.068790, -0.000600]),
	('forearm.L_tail',			'vo', [14057, 0.004140, 0.008700, -0.004900]),
	('hand.L_tail',				'vo', [5828, -0.011030, 0.028660, 0.123099]),
	('palm.01.L_head',			'vo', [14066, 0.034900, 0.039546, 0.000400]),
	('palm.01.L_tail',			'vo', [14083, -0.000280, 0.022316, 0.002200]),
	('finger_index.01.L_tail',		'vo', [14104, -0.022520, 0.001425, 0.001101]),
	('finger_index.02.L_tail',		'vo', [14147, 0.000730, 0.001850, 0.022200]),
	('finger_index.03.L_tail',		'vo', [5983, -0.001150, -0.000974, 0.004100]),
	('UP-index.L_head',			'vo', [5970, -0.002509, 0.017725, -0.003098]),
	('UP-index.L_tail',			'vo', [5974, -0.018059, 0.013850, 0.005477]),
	('thumb.01.L_head',			'vo', [14063, 0.001850, -0.000648, -0.069699]),
	('thumb.01.L_tail',			'vo', [14071, 0.001850, 0.030284, 0.003000]),
	('thumb.02.L_tail',			'vo', [14075, 0.002460, -0.000420, 0.022000]),
	('thumb.03.L_tail',			'vo', [3226, -0.003440, -0.003714, -0.008101]),
	('UP-thumb.L_head',			'vo', [6301, 0.019157, -0.007631, 0.017700]),
	('UP-thumb.L_tail',			'vo', [3278, 0.012813, -0.000641, 0.023400]),
	('palm.02.L_head',			'vo', [15262, 0.000540, -0.001400, -0.012600]),
	('palm.02.L_tail',			'vo', [14088, 0.022500, -0.003545, 0.001700]),
	('finger_middle.01.L_tail',		'vo', [14114, -0.000050, -0.017878, -0.005500]),
	('finger_middle.02.L_tail',		'vo', [14144, -0.001630, -0.017451, -0.003300]),
	('finger_middle.03.L_tail',		'vo', [5779, 0.000220, 0.001039, -0.003900]),
	('UP-middle.L_head',			'vo', [2662, -0.011609, -0.020000, -0.002546]),
	('UP-middle.L_tail',			'vo', [5790, -0.012938, 0.004046, -0.005461]),
	('palm.03.L_head',			'vo', [15269, 0.017020, -0.074860, 0.014100]),
	('palm.03.L_tail',			'vo', [14093, 0.005150, 0.004920, 0.016100]),
	('finger_ring.01.L_tail',		'vo', [14120, -0.003170, -0.020780, 0.000600]),
	('finger_ring.02.L_tail',		'vo', [14134, -0.019600, 0.003470, -0.001000]),
	('finger_ring.03.L_tail',		'vo', [6150, 0.007140, 0.007310, -0.001301]),
	('UP-ring.L_head',			'vo', [6131, -0.005683, 0.001401, -0.007302]),
	('UP-ring.L_tail',			'vo', [6135, 0.001684, 0.002308, -0.002637]),
	('palm.04.L_head',			'vo', [15272, -0.029640, 0.002860, -0.005500]),
	('palm.04.L_tail',			'vo', [14099, -0.004290, 0.003780, 0.028700]),
	('finger_pinky.01.L_tail',		'vo', [14121, 0.003247, 0.003190, -0.000827]),
	('finger_pinky.02.L_tail',		'vo', [14127, 0.001214, 0.000980, -0.003234]),
	('finger_pinky.03.L_tail',		'vo', [6467, 0.004090, 0.000360, -0.015600]),
	('UP-pinky.L_head',			'vo', [6479, 0.002017, -0.001622, -0.000694]),
	('UP-pinky.L_tail',			'vo', [6475, 0.000692, 0.001181, -0.004421]),
	('UP-arm.L_head',			'vo', [3012, -0.008317, -0.002296, 0.005117]),
	('UP-arm.L_tail',			'vo', [4535, 0.002990, -0.005289, 0.003494]),
	('deltoid_target.L_tail',		'vo', [3029, 0.000891, -0.052622, 0.013642]),
	('shoulder.R_head',			'vo', [14291, 0.007516, -0.134283, 0.002300]),
	('shoulder.R_tail',			'vo', [11005, 0.002720, -0.187990, -0.172400]),
	('upper_arm.R_head',			'vo', [14380, -0.000270, -0.032300, 0.004300]),
	('upper_arm.R_tail',			'vo', [14387, -0.006240, -0.068790, -0.000600]),
	('forearm.R_tail',			'vo', [14485, -0.004140, 0.008700, -0.004900]),
	('hand.R_tail',				'vo', [9713, 0.011030, 0.028660, 0.123099]),
	('palm.01.R_head',			'vo', [14476, -0.034900, 0.039546, 0.000400]),
	('palm.01.R_tail',			'vo', [14459, 0.000280, 0.022316, 0.002200]),
	('finger_index.01.R_tail',		'vo', [14438, 0.022520, 0.001425, 0.001101]),
	('finger_index.02.R_tail',		'vo', [14395, -0.000730, 0.001850, 0.022200]),
	('finger_index.03.R_tail',		'vo', [9585, 0.001150, -0.000974, 0.004100]),
	('UP-index.R_head',			'vo', [9598, 0.002509, 0.017725, -0.003098]),
	('UP-index.R_tail',			'vo', [9594, 0.018059, 0.013850, 0.005477]),
	('thumb.01.R_head',			'vo', [14479, -0.001850, -0.000648, -0.069699]),
	('thumb.01.R_tail',			'vo', [14471, -0.001850, 0.030284, 0.003000]),
	('thumb.02.R_tail',			'vo', [14467, -0.002460, -0.000420, 0.022000]),
	('thumb.03.R_tail',			'vo', [10523, 0.003440, -0.003714, -0.008101]),
	('UP-thumb.R_head',			'vo', [9267, -0.019157, -0.007631, 0.017700]),
	('UP-thumb.R_tail',			'vo', [10473, -0.012813, -0.000641, 0.023400]),
	('palm.02.R_head',			'vo', [15135, -0.000540, -0.001400, -0.012600]),
	('palm.02.R_tail',			'vo', [14454, -0.022500, -0.003545, 0.001700]),
	('finger_middle.01.R_tail',		'vo', [14428, 0.000050, -0.017878, -0.005500]),
	('finger_middle.02.R_tail',		'vo', [14398, 0.001630, -0.017451, -0.003300]),
	('finger_middle.03.R_tail',		'vo', [9762, -0.000220, 0.001039, -0.003900]),
	('UP-middle.R_head',			'vo', [10948, 0.011609, -0.020000, -0.002546]),
	('UP-middle.R_tail',			'vo', [9751, 0.012938, 0.004046, -0.005461]),
	('palm.03.R_head',			'vo', [15128, -0.017020, -0.074860, 0.014100]),
	('palm.03.R_tail',			'vo', [14449, -0.005150, 0.004920, 0.016100]),
	('finger_ring.01.R_tail',		'vo', [14422, 0.003170, -0.020780, 0.000600]),
	('finger_ring.02.R_tail',		'vo', [14408, 0.019600, 0.003470, -0.001000]),
	('finger_ring.03.R_tail',		'vo', [9418, -0.007140, 0.007310, -0.001301]),
	('UP-ring.R_head',			'vo', [9437, 0.005683, 0.001401, -0.007302]),
	('UP-ring.R_tail',			'vo', [9433, -0.001684, 0.002308, -0.002637]),
	('palm.04.R_head',			'vo', [15125, 0.029640, 0.002860, -0.005500]),
	('palm.04.R_tail',			'vo', [14443, 0.004290, 0.003780, 0.028700]),
	('finger_pinky.01.R_tail',		'vo', [14421, -0.003247, 0.003190, -0.000827]),
	('finger_pinky.02.R_tail',		'vo', [14415, -0.001214, 0.000980, -0.003234]),
	('finger_pinky.03.R_tail',		'vo', [9101, -0.004090, 0.000360, -0.015600]),
	('UP-pinky.R_head',			'vo', [9089, -0.002017, -0.001622, -0.000694]),
	('UP-pinky.R_tail',			'vo', [9093, -0.000692, 0.001181, -0.004421]),
	('UP-arm.R_head',			'vo', [10714, 0.008317, -0.002296, 0.005117]),
	('UP-arm.R_tail',			'vo', [9938, -0.002990, -0.005289, 0.003494]),
	('deltoid_target.R_tail',		'vo', [10697, -0.000891, -0.052622, 0.013642]),
	('pect1.L_head',			'vo', [3666, 0.116346, 0.051171, -0.061019]),
	('pect1.R_head',			'vo', [10135, -0.116346, 0.051171, -0.061019]),
	('pect2.L_head',			'vo', [2549, -0.042284, 0.049440, -0.066677]),
	('pect2.R_head',			'vo', [11059, 0.042284, 0.049440, -0.066677]),
	('lat.L_head',				'vo', [4434, 0.054409, -0.045201, 0.018841]),
	('lat.R_head',				'vo', [9993, -0.054409, -0.045201, 0.018841]),
	('trap.L_head',				'vo', [2598, -0.079100, -0.017038, -0.048916]),
	('trap.R_head',				'vo', [11068, 0.079100, -0.017038, -0.048916]),
	('deltoid.L_head',			'vo', [5867, -0.021985, 0.021378, -0.039226]),
	('deltoid.R_head',			'vo', [9674, 0.021985, 0.021378, -0.039226]),
	('breast_head',				'vo', [7310, 0.000000, -0.020253, 0.002830]),
	('breast_tail',				'vo', [7291, 0.000000, 0.013208, 0.056455]),
	('stomach_tail',			'vo', [7297, 0.000000, 0.011680, 0.051711]),
	('breast_target_tail',			'vo', [7291, 0.000000, -0.044016, 0.056455]),
	('thigh.L_head',			'vo', [14163, -0.006460, 0.002648, -0.073350]),
	('thigh.L_tail',			'vo', [14169, 0.004907, -0.001670, -0.075590]),
	('shin.L_tail',				'vo', [14180, -0.007347, -0.070220, -0.013970]),
	('foot.L_tail',				'vo', [15315, -0.030363, 0.069909, -0.004309]),
	('toe.L_tail',				'vo', [15307, 0.025542, -0.006313, -0.001457]),
	('heel.L_tail',				'vo', [5734, -0.045989, 0.104040, -0.244742]),
	('heel.02.L_head',			'vo', [5730, -0.227798, -0.066113, -0.257760]),
	('heel.02.L_tail',			'vo', [12348, 0.085460, -0.028525, -0.228430]),
	('UP-leg.L_head',			'vo', [3793, 0.014076, 0.017775, -0.001229]),
	('UP-leg.L_tail',			'vo', [3897, -0.011419, 0.002995, -0.000837]),
	('thigh.R_head',			'vo', [14379, 0.006460, 0.002648, -0.073350]),
	('thigh.R_tail',			'vo', [14373, -0.004907, -0.001670, -0.075590]),
	('shin.R_tail',				'vo', [14362, 0.007347, -0.070220, -0.013970]),
	('foot.R_tail',				'vo', [15082, 0.030363, 0.069909, -0.004309]),
	('toe.R_tail',				'vo', [15090, -0.025542, -0.006313, -0.001457]),
	('heel.R_tail',				'vo', [13328, 0.045989, 0.104040, -0.244742]),
	('heel.02.R_head',			'vo', [13332, 0.227799, -0.066113, -0.257760]),
	('heel.02.R_tail',			'vo', [13168, -0.085460, -0.028525, -0.228430]),
	('UP-leg.R_head',			'vo', [7218, -0.014076, 0.017775, -0.001229]),
	('UP-leg.R_tail',			'vo', [7112, 0.011419, 0.002995, -0.000837]),
	('penis_head',				'vo', [2791, -0.203300, 0.073516, 0.133896]),
	('penis_tail',				'vo', [7411, 0.001300, 0.001352, -0.016244]),
	('scrotum_head',			'vo', [7417, 0.001300, -0.011799, 0.057327]),
	('scrotum_tail',			'vo', [7442, 0.001300, 0.128670, -0.004701]),
	('butt.R_head',				'vo', [6793, 0.024120, 0.009064, -0.012368]),
	('butt.L_head',				'vo', [5680, -0.024120, 0.009064, -0.012368]),
	('hip.R_head',				'vo', [7306, 0.049387, 0.026350, 0.109084]),
	('hip.L_head',				'vo', [2930, -0.049387, 0.026350, 0.109084]),
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
	('UP-index.L',			'UP-index.L_head', 'UP-index.L_tail'),
	('thumb.01.L',			'thumb.01.L_head', 'thumb.01.L_tail'),
	('thumb.02.L',			'thumb.01.L_tail', 'thumb.02.L_tail'),
	('thumb.03.L',			'thumb.02.L_tail', 'thumb.03.L_tail'),
	('UP-thumb.L',			'UP-thumb.L_head', 'UP-thumb.L_tail'),
	('palm.02.L',			'palm.02.L_head', 'palm.02.L_tail'),
	('finger_middle.01.L',		'palm.02.L_tail', 'finger_middle.01.L_tail'),
	('finger_middle.02.L',		'finger_middle.01.L_tail', 'finger_middle.02.L_tail'),
	('finger_middle.03.L',		'finger_middle.02.L_tail', 'finger_middle.03.L_tail'),
	('UP-middle.L',			'UP-middle.L_head', 'UP-middle.L_tail'),
	('palm.03.L',			'palm.03.L_head', 'palm.03.L_tail'),
	('finger_ring.01.L',		'palm.03.L_tail', 'finger_ring.01.L_tail'),
	('finger_ring.02.L',		'finger_ring.01.L_tail', 'finger_ring.02.L_tail'),
	('finger_ring.03.L',		'finger_ring.02.L_tail', 'finger_ring.03.L_tail'),
	('UP-ring.L',			'UP-ring.L_head', 'UP-ring.L_tail'),
	('palm.04.L',			'palm.04.L_head', 'palm.04.L_tail'),
	('finger_pinky.01.L',		'palm.04.L_tail', 'finger_pinky.01.L_tail'),
	('finger_pinky.02.L',		'finger_pinky.01.L_tail', 'finger_pinky.02.L_tail'),
	('finger_pinky.03.L',		'finger_pinky.02.L_tail', 'finger_pinky.03.L_tail'),
	('UP-pinky.L',			'UP-pinky.L_head', 'UP-pinky.L_tail'),
	('DEF-elbow-fan.L',			'upper_arm.L_tail', 'forearm.L_tail'),
	('UP-arm.L',			'UP-arm.L_head', 'UP-arm.L_tail'),
	('MCH-deltoid_target.L',		'upper_arm.L_head', 'deltoid_target.L_tail'),
	('shoulder.R',			'shoulder.R_head', 'shoulder.R_tail'),
	('upper_arm.R',			'upper_arm.R_head', 'upper_arm.R_tail'),
	('forearm.R',			'upper_arm.R_tail', 'forearm.R_tail'),
	('hand.R',			'forearm.R_tail', 'hand.R_tail'),
	('palm.01.R',			'palm.01.R_head', 'palm.01.R_tail'),
	('finger_index.01.R',		'palm.01.R_tail', 'finger_index.01.R_tail'),
	('finger_index.02.R',		'finger_index.01.R_tail', 'finger_index.02.R_tail'),
	('finger_index.03.R',		'finger_index.02.R_tail', 'finger_index.03.R_tail'),
	('UP-index.R',			'UP-index.R_head', 'UP-index.R_tail'),
	('thumb.01.R',			'thumb.01.R_head', 'thumb.01.R_tail'),
	('thumb.02.R',			'thumb.01.R_tail', 'thumb.02.R_tail'),
	('thumb.03.R',			'thumb.02.R_tail', 'thumb.03.R_tail'),
	('UP-thumb.R',			'UP-thumb.R_head', 'UP-thumb.R_tail'),
	('palm.02.R',			'palm.02.R_head', 'palm.02.R_tail'),
	('finger_middle.01.R',		'palm.02.R_tail', 'finger_middle.01.R_tail'),
	('finger_middle.02.R',		'finger_middle.01.R_tail', 'finger_middle.02.R_tail'),
	('finger_middle.03.R',		'finger_middle.02.R_tail', 'finger_middle.03.R_tail'),
	('UP-middle.R',			'UP-middle.R_head', 'UP-middle.R_tail'),
	('palm.03.R',			'palm.03.R_head', 'palm.03.R_tail'),
	('finger_ring.01.R',		'palm.03.R_tail', 'finger_ring.01.R_tail'),
	('finger_ring.02.R',		'finger_ring.01.R_tail', 'finger_ring.02.R_tail'),
	('finger_ring.03.R',		'finger_ring.02.R_tail', 'finger_ring.03.R_tail'),
	('UP-ring.R',			'UP-ring.R_head', 'UP-ring.R_tail'),
	('palm.04.R',			'palm.04.R_head', 'palm.04.R_tail'),
	('finger_pinky.01.R',		'palm.04.R_tail', 'finger_pinky.01.R_tail'),
	('finger_pinky.02.R',		'finger_pinky.01.R_tail', 'finger_pinky.02.R_tail'),
	('finger_pinky.03.R',		'finger_pinky.02.R_tail', 'finger_pinky.03.R_tail'),
	('UP-pinky.R',			'UP-pinky.R_head', 'UP-pinky.R_tail'),
	('DEF-elbow-fan.R',			'upper_arm.R_tail', 'forearm.R_tail'),
	('UP-arm.R',			'UP-arm.R_head', 'UP-arm.R_tail'),
	('MCH-deltoid_target.R',		'upper_arm.R_head', 'deltoid_target.R_tail'),
	('DEF-pect1.L',			'pect1.L_head', 'upper_arm.L_head'),
	('DEF-pect1.R',			'pect1.R_head', 'upper_arm.R_head'),
	('DEF-pect2.L',			'pect2.L_head', 'upper_arm.L_head'),
	('DEF-pect2.R',			'pect2.R_head', 'upper_arm.R_head'),
	('DEF-lat.L',			'lat.L_head', 'upper_arm.L_head'),
	('DEF-lat.R',			'lat.R_head', 'upper_arm.R_head'),
	('DEF-trap.L',			'trap.L_head', 'upper_arm.L_head'),
	('DEF-trap.R',			'trap.R_head', 'upper_arm.R_head'),
	('DEF-deltoid.L',			'deltoid.L_head', 'deltoid_target.L_tail'),
	('DEF-deltoid.R',			'deltoid.R_head', 'deltoid_target.R_tail'),
	('DEF-breast',			'breast_head', 'breast_tail'),
	('DEF-stomach',			'breast_tail', 'stomach_tail'),
	('MCH-breast_target',		'spine_tail', 'breast_target_tail'),
	('thigh.L',			'thigh.L_head', 'thigh.L_tail'),
	('shin.L',			'thigh.L_tail', 'shin.L_tail'),
	('foot.L',			'shin.L_tail', 'foot.L_tail'),
	('toe.L',			'foot.L_tail', 'toe.L_tail'),
	('heel.L',			'shin.L_tail', 'heel.L_tail'),
	('heel.02.L',			'heel.02.L_head', 'heel.02.L_tail'),
	('DEF-knee-fan.L',			'thigh.L_tail', 'shin.L_tail'),
	('UP-leg.L',			'UP-leg.L_head', 'UP-leg.L_tail'),
	('thigh.R',			'thigh.R_head', 'thigh.R_tail'),
	('shin.R',			'thigh.R_tail', 'shin.R_tail'),
	('foot.R',			'shin.R_tail', 'foot.R_tail'),
	('toe.R',			'foot.R_tail', 'toe.R_tail'),
	('heel.R',			'shin.R_tail', 'heel.R_tail'),
	('heel.02.R',			'heel.02.R_head', 'heel.02.R_tail'),
	('DEF-knee-fan.R',			'thigh.R_tail', 'shin.R_tail'),
	('UP-leg.R',			'UP-leg.R_head', 'UP-leg.R_tail'),
	('penis',			'penis_head', 'penis_tail'),
	('scrotum',			'scrotum_head', 'scrotum_tail'),
	('MCH-stomach_target',		'hips_tail', 'stomach_tail'),
	('DEF-butt.R',			'butt.R_head', 'thigh.R_head'),
	('DEF-butt.L',			'butt.L_head', 'thigh.L_head'),
	('DEF-hip.R',			'hip.R_head', 'thigh.R_head'),
	('DEF-hip.L',			'hip.L_head', 'thigh.L_head'),
]

RigifyArmature = [
	('hips',			0.0, None, F_DEF, 0x1, (1,1,1) ),
	('spine',			0.0, 'hips', F_DEF+F_CON, 0x1, (1,1,1) ),
	('ribs',			0.0, 'spine', F_DEF+F_CON, 0x1, (1,1,1) ),
	('neck',			0.0, 'ribs', F_DEF, 0x4, (1,1,1) ),
	('head',			0.0, 'neck', F_DEF+F_CON, 0x4, (1,1,1) ),
	('shoulder.L',			-0.0743, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('upper_arm.L',			1.75, 'shoulder.L', F_DEF, 0x40, (1,1,1) ),
	('forearm.L',			1.57, 'upper_arm.L', F_DEF+F_CON, 0x40, (1,1,1) ),
	('hand.L',			3, 'forearm.L', F_DEF+F_CON, 0x40, (1,1,1) ),
	('palm.01.L',			2.78, 'hand.L', F_DEF, 0x10, (1,1,1) ),
	('finger_index.01.L',		-2.94, 'palm.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_index.02.L',		-2.96, 'finger_index.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_index.03.L',		-2.95, 'finger_index.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-index.L',			-2.89, 'finger_index.01.L', 0, 0x10, (1,1,1) ),
	('thumb.01.L',			-1.41, 'palm.01.L', F_DEF, 0x10, (1,1,1) ),
	('thumb.02.L',			-1.59, 'thumb.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('thumb.03.L',			-1.5, 'thumb.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-thumb.L',			-1.59, 'thumb.01.L', 0, 0x10, (1,1,1) ),
	('palm.02.L',			2.83, 'hand.L', F_DEF, 0x10, (1,1,1) ),
	('finger_middle.01.L',		-3.11, 'palm.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_middle.02.L',		-3.07, 'finger_middle.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_middle.03.L',		-3.11, 'finger_middle.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-middle.L',			-2.99, 'finger_middle.01.L', 0, 0x10, (1,1,1) ),
	('palm.03.L',			2.96, 'hand.L', F_DEF, 0x10, (1,1,1) ),
	('finger_ring.01.L',		3.04, 'palm.03.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_ring.02.L',		3.08, 'finger_ring.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_ring.03.L',		2.97, 'finger_ring.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-ring.L',			-3.11, 'finger_ring.01.L', 0, 0x10, (1,1,1) ),
	('palm.04.L',			-3.12, 'hand.L', F_DEF, 0x10, (1,1,1) ),
	('finger_pinky.01.L',		2.95, 'palm.04.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_pinky.02.L',		2.98, 'finger_pinky.01.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_pinky.03.L',		2.98, 'finger_pinky.02.L', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-pinky.L',			3.08, 'finger_pinky.01.L', 0, 0x10, (1,1,1) ),
	('DEF-elbow-fan.L',		1.57, 'upper_arm.L', F_DEF+F_CON, 0x40, (1,1,1) ),
	('UP-arm.L',			0.027, 'upper_arm.L', 0, 0x100, (1,1,1) ),
	('MCH-deltoid_target.L',	-0.277, 'shoulder.L', 0, 0x40, (1,1,1) ),
	('shoulder.R',			0.0743, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('upper_arm.R',			-1.75, 'shoulder.R', F_DEF, 0x40, (1,1,1) ),
	('forearm.R',			-1.57, 'upper_arm.R', F_DEF+F_CON, 0x40, (1,1,1) ),
	('hand.R',			-3, 'forearm.R', F_DEF+F_CON, 0x100, (1,1,1) ),
	('palm.01.R',			-2.78, 'hand.R', F_DEF, 0x10, (1,1,1) ),
	('finger_index.01.R',		2.94, 'palm.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_index.02.R',		2.96, 'finger_index.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_index.03.R',		2.95, 'finger_index.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-index.R',			2.89, 'finger_index.01.R', 0, 0x10, (1,1,1) ),
	('thumb.01.R',			1.41, 'palm.01.R', F_DEF, 0x10, (1,1,1) ),
	('thumb.02.R',			1.59, 'thumb.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('thumb.03.R',			1.5, 'thumb.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-thumb.R',			1.59, 'thumb.01.R', 0, 0x10, (1,1,1) ),
	('palm.02.R',			-2.83, 'hand.R', F_DEF, 0x10, (1,1,1) ),
	('finger_middle.01.R',		3.11, 'palm.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_middle.02.R',		3.07, 'finger_middle.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_middle.03.R',		3.11, 'finger_middle.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-middle.R',			2.99, 'finger_middle.01.R', 0, 0x10, (1,1,1) ),
	('palm.03.R',			-2.96, 'hand.R', F_DEF, 0x10, (1,1,1) ),
	('finger_ring.01.R',		-3.04, 'palm.03.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_ring.02.R',		-3.08, 'finger_ring.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_ring.03.R',		-2.97, 'finger_ring.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-ring.R',			3.11, 'finger_ring.01.R', 0, 0x10, (1,1,1) ),
	('palm.04.R',			3.12, 'hand.R', F_DEF, 0x10, (1,1,1) ),
	('finger_pinky.01.R',		-2.95, 'palm.04.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_pinky.02.R',		-2.98, 'finger_pinky.01.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('finger_pinky.03.R',		-2.98, 'finger_pinky.02.R', F_DEF+F_CON, 0x10, (1,1,1) ),
	('UP-pinky.R',			-3.08, 'finger_pinky.01.R', 0, 0x10, (1,1,1) ),
	('DEF-elbow-fan.R',		-1.57, 'upper_arm.R', F_DEF+F_CON, 0x40, (1,1,1) ),
	('UP-arm.R',			-0.027, 'upper_arm.R', 0, 0x100, (1,1,1) ),
	('MCH-deltoid_target.R',	0.277, 'shoulder.R', 0, 0x40, (1,1,1) ),
	('DEF-pect1.L',			0.0, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-pect1.R',			0.0, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-pect2.L',			0.02, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-pect2.R',			-0.02, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-lat.L',			-0.0554, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-lat.R',			0.0554, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-trap.L',			0.0, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-trap.R',			0.0, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-deltoid.L',		-0.102, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-deltoid.R',		0.102, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-breast',			0.0, 'ribs', F_DEF, 0x1, (1,1,1) ),
	('DEF-stomach',			0.0, 'DEF-breast', F_DEF+F_CON+F_NOROT, 0x1, (1,1,1) ),
	('MCH-breast_target',		0.0, 'spine', F_CON, 0x1, (1,1,1) ),
	('thigh.L',			0.0, 'hips', F_DEF, 0x400, (1,1,1) ),
	('shin.L',			0.0574, 'thigh.L', F_DEF+F_CON, 0x400, (1,1,1) ),
	('foot.L',			0.0, 'shin.L', F_DEF+F_CON, 0x400, (1,1,1) ),
	('toe.L',			3.14, 'foot.L', F_DEF+F_CON, 0x400, (1,1,1) ),
	('heel.L',			3.14, 'shin.L', F_DEF+F_CON, 0x400, (1,1,1) ),
	('heel.02.L',			0.0, 'heel.L', F_DEF, 0x400, (1,1,1) ),
	('DEF-knee-fan.L',		0.032, 'thigh.L', F_DEF+F_CON, 0x1000, (1,1,1) ),
	('UP-leg.L',			0.0, 'thigh.L', 0, 0x400, (1,1,1) ),
	('thigh.R',			0.0, 'hips', F_DEF, 0x400, (1,1,1) ),
	('shin.R',			-0.0574, 'thigh.R', F_DEF+F_CON, 0x400, (1,1,1) ),
	('foot.R',			0.0, 'shin.R', F_DEF+F_CON, 0x400, (1,1,1) ),
	('toe.R',			-3.14, 'foot.R', F_DEF+F_CON, 0x400, (1,1,1) ),
	('heel.R',			-3.14, 'shin.R', F_DEF+F_CON, 0x1000, (1,1,1) ),
	('heel.02.R',			0.0, 'heel.R', F_DEF, 0x1000, (1,1,1) ),
	('DEF-knee-fan.R',		-0.032, 'thigh.R', F_DEF+F_CON, 0x1000, (1,1,1) ),
	('UP-leg.R',			0.0, 'thigh.R', 0, 0x1000, (1,1,1) ),
	('penis',			-3.14, 'hips', F_DEF, 0x1, (1,1,1) ),
	('scrotum',			-3.14, 'hips', F_DEF, 0x1, (1,1,1) ),
	('MCH-stomach_target',		0.0, 'hips', F_CON, 0x1, (1,1,1) ),
	('DEF-butt.R',			-0.0181, 'hips', F_DEF, 0x1, (1,1,1) ),
	('DEF-butt.L',			0.0181, 'hips', F_DEF, 0x1, (1,1,1) ),
	('DEF-hip.R',			0.0, 'hips', F_DEF, 0x1, (1,1,1) ),
	('DEF-hip.L',			0.0, 'hips', F_DEF, 0x1, (1,1,1) ),
]

def RigifyWritePoses(fp, config):
	global boneGroups
	boneGroups = {}

	addPoseBone(fp, config, 'hips', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'spine', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'ribs', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'neck', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'head', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'shoulder.L', None, None, (1,1,1), (0,1,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'upper_arm.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'forearm.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'hand.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'palm.01.L', None, None, (1,1,1), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_index.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_index.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_index.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-index.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'thumb.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'thumb.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'thumb.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-thumb.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'palm.02.L', None, None, (1,1,1), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_middle.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_middle.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_middle.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-middle.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'palm.03.L', None, None, (1,1,1), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_ring.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_ring.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_ring.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-ring.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'palm.04.L', None, None, (1,1,1), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_pinky.01.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_pinky.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_pinky.03.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-pinky.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'DEF-elbow-fan.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('CopyRot', 0, 0.5, ['Copy_Rotation', 'forearm.L', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, config, 'UP-arm.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'MCH-deltoid_target.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'shoulder.R', None, None, (1,1,1), (0,1,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'upper_arm.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'forearm.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'hand.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'palm.01.R', None, None, (0,0,0), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_index.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_index.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_index.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-index.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'thumb.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'thumb.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'thumb.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-thumb.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'palm.02.R', None, None, (0,0,0), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_middle.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_middle.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_middle.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-middle.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'palm.03.R', None, None, (0,0,0), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_ring.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_ring.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_ring.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-ring.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'palm.04.R', None, None, (0,0,0), (0,1,1), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_pinky.01.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_pinky.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'finger_pinky.03.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'UP-pinky.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'DEF-elbow-fan.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('CopyRot', 0, 0.5, ['Copy_Rotation', 'forearm.R', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, config, 'UP-arm.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'MCH-deltoid_target.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'DEF-pect1.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'upper_arm.L', 0, 1])])

	addPoseBone(fp, config, 'DEF-pect2.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'upper_arm.L', 0, 1])])

	addPoseBone(fp, config, 'DEF-pect1.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'upper_arm.R', 0, 1])])

	addPoseBone(fp, config, 'DEF-pect2.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'upper_arm.R', 0, 1])])

	addPoseBone(fp, config, 'DEF-lat.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'upper_arm.L', 0, 1])])

	addPoseBone(fp, config, 'DEF-lat.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'upper_arm.R', 0, 1])])

	addPoseBone(fp, config, 'DEF-trap.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'upper_arm.L', 0, 1])])

	addPoseBone(fp, config, 'DEF-trap.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'upper_arm.R', 0, 1])])

	addPoseBone(fp, config, 'DEF-deltoid.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'MCH-deltoid_target.L', 1, 1])])

	addPoseBone(fp, config, 'DEF-deltoid.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'MCH-deltoid_target.R', 1, 1])])

	addPoseBone(fp, config, 'MCH-breast_target', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('CopyRot', 0+C_OW_LOCAL+C_TG_LOCAL, 0.5, ['Copy_Rotation', 'ribs', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, config, 'DEF-breast', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'MCH-breast_target', 1, 1])])

	addPoseBone(fp, config, 'thigh.L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'shin.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'foot.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'toe.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'heel.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'heel.02.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'DEF-knee-fan.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('CopyRot', 0, 0.5, ['Copy_Rotation', 'shin.L', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, config, 'UP-leg.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'thigh.R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'shin.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'foot.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'toe.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'heel.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'heel.02.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'DEF-knee-fan.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('CopyRot', 0, 0.5, ['Copy_Rotation', 'shin.R', (1,1,1), (0,0,0), False])])

	addPoseBone(fp, config, 'UP-leg.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'penis', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'scrotum', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'MCH-stomach_target', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4, [])

	addPoseBone(fp, config, 'DEF-stomach', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'MCH-stomach_target', 1, 1])])

	addPoseBone(fp, config, 'DEF-butt.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'thigh.R', 0, 1])])

	addPoseBone(fp, config, 'DEF-hip.R', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'thigh.R', 0, 1])])

	addPoseBone(fp, config, 'DEF-butt.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'thigh.L', 0, 1])])

	addPoseBone(fp, config, 'DEF-hip.L', None, None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), P_LKROT4,
		[('StretchTo', 0, 1, ['Stretch_To', 'thigh.L', 0, 1])])

	return

RigifyObjectProps = [
]

RigifyArmatureProps = [
	('MhxScale', 1.000),
	('MhxRig', '"Control"'),
	('MhxVisemeSet', '"BodyLanguage"'),]


def getRigifyDrivers():
	human = mh2mhx.theHuman
	return [
  ('DfmUpLid_L', 'ROTQ', 'AVERAGE', None, 1, (0,0.698), [
		('var', 'TRANSFORMS', [('OBJECT', human, 'PUpLid_L', 'LOC_Z', C_LOCAL) ]),]),
  ('DfmLoLid_L', 'ROTQ', 'AVERAGE', None, 1, (0,0.349), [
		('var', 'TRANSFORMS', [('OBJECT', human, 'PLoLid_L', 'LOC_Z', C_LOCAL) ]),]),
  ('DfmUpLid_R', 'ROTQ', 'AVERAGE', None, 1, (0,0.698), [
		('var', 'TRANSFORMS', [('OBJECT', human, 'PUpLid_R', 'LOC_Z', C_LOCAL) ]),]),
  ('DfmLoLid_R', 'ROTQ', 'AVERAGE', None, 1, (0,0.349), [
		('var', 'TRANSFORMS', [('OBJECT', human, 'PLoLid_R', 'LOC_Z', C_LOCAL) ]),]),
]


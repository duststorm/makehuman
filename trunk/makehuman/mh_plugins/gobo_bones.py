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
Bones for the Gobo rig

"""

import mhx_rig
from mhx_rig import *

GoboJoints = [
	('mid-feet'			,'l', ((0.5, 'l-ankle'), (0.5, 'r-ankle'))),
	('root_head'			, 'o', ('mid-feet', [0,-0.3,0])),
	('root_tail'			, 'o', ('root_head', [0,0,-1])),
	('hand_L_head'			, 'j', 'r-hand'),
	('hand_L_tail'			, 'j', 'r-finger-3-3'),
	('hand_R_head'			, 'j', 'l-hand'),
	('hand_R_tail'			, 'j', 'l-finger-3-3'),
	('hip_head'			, 'j', 'spine3'),
	('hip_tail'			, 'j', 'pelvis'),
	('spine_3_head'			, 'j', 'spine3'),
	('spine_3_tail'			, 'j', 'spine2'),
	('spine_2_tail'			, 'j', 'spine1'),
	('spine_1_tail'			, 'j', 'neck'),
	('neck_tail'			, 'j', 'head'),
	('head_tail'			, 'l', ((2.0, 'head'), (-1.0, 'neck'))),
	('chest-front'			,'v', 7292 ),
	
	('shoulder_L_head'		, 'j', 'r-clavicle'),
	('shoulder_L_tail'		, 'j', 'r-shoulder'),
	('ikfk_hand_L_head'		, 'o', ('r-finger-3-3', [2,0,0])),
	('ikfk_hand_L_tail'		, 'o', ('ikfk_hand_L_head', [-1,0,0])),
	('arm_root_L_head'		, 'j', 'r-clavicle'),
	('arm_root_L_tail'		, 'j', 'r-shoulder'),
	('armupper_L_tail'		, 'j', 'r-elbow'),
	('armlower_L_tail'		, 'j', 'r-hand'),
	('hand_L_head'			, 'j', 'r-hand'),
	('hand_L_tail'			, 'j', 'r-finger-3-1'),
	('finger_curl_L_head'		, 'o', ('r-hand', [0, 1.0, 0])),
	('finger_curl_L_tail'		, 'o', ('finger_curl_L_head', [0, 1.0, 0])),
	('elbow_L_head'			, 'o', ('arm_root_L_tail', [0,0,-3])),
	('elbow_L_tail'			, 'o', ('elbow_L_head', [0,0.5,0])),

	('shoulder_R_head'		, 'j', 'l-clavicle'),
	('shoulder_R_tail'		, 'j', 'l-shoulder'),
	('ikfk_hand_R_head'		, 'o', ('l-finger-3-3', [-2,0,0])),
	('ikfk_hand_R_tail'		, 'o', ('ikfk_hand_R_head', [1,0,0])),
	('arm_root_R_head'		, 'j', 'l-clavicle'),
	('arm_root_R_tail'		, 'j', 'l-shoulder'),
	('armupper_R_tail'		, 'j', 'l-elbow'),
	('armlower_R_tail'		, 'j', 'l-hand'),
	('hand_R_head'			, 'j', 'l-hand'),
	('hand_R_tail'			, 'j', 'l-finger-3-1'),
	('finger_curl_R_head'		, 'o', ('l-hand', [0, 1.0, 0])),
	('finger_curl_R_tail'		, 'o', ('finger_curl_R_head', [0, 1.0, 0])),
	('elbow_R_head'			, 'o', ('arm_root_R_tail', [0,0,-3])),
	('elbow_R_tail'			, 'o', ('elbow_R_head', [0,0.5,0])),

	('finger-1-1_L_head'		, 'j', 'r-finger-1-1'),
	('finger-1-1_L_tail'		, 'j', 'r-finger-1-2'),
	('finger-1-2_L_tail'		, 'j', 'r-finger-1-3'),
	('finger-1-3_L_tail'		, 'l', ((2,'r-finger-1-3'), (-1,'r-finger-1-2'))),
	('finger-2-1_L_head'		, 'j', 'r-finger-2-1'),
	('finger-2-1_L_tail'		, 'j', 'r-finger-2-2'),
	('finger-2-2_L_tail'		, 'j', 'r-finger-2-3'),
	('finger-2-3_L_tail'		, 'l', ((2,'r-finger-2-3'), (-1,'r-finger-2-2'))),
	('finger-3-1_L_head'		, 'j', 'r-finger-3-1'),
	('finger-3-1_L_tail'		, 'j', 'r-finger-3-2'),
	('finger-3-2_L_tail'		, 'j', 'r-finger-3-3'),
	('finger-3-3_L_tail'		, 'l', ((2,'r-finger-3-3'), (-1,'r-finger-3-2'))),
	('finger-4-1_L_head'		, 'j', 'r-finger-4-1'),
	('finger-4-1_L_tail'		, 'j', 'r-finger-4-2'),
	('finger-4-2_L_tail'		, 'j', 'r-finger-4-3'),
	('finger-4-3_L_tail'		, 'l', ((2,'r-finger-4-3'), (-1,'r-finger-4-2'))),
	('finger-5-1_L_head'		, 'j', 'r-finger-5-1'),
	('finger-5-1_L_tail'		, 'j', 'r-finger-5-2'),
	('finger-5-2_L_tail'		, 'j', 'r-finger-5-3'),
	('finger-5-3_L_tail'		, 'l', ((2,'r-finger-5-3'), (-1,'r-finger-5-2'))),

	('finger-1-1_R_head'		, 'j', 'l-finger-1-1'),
	('finger-1-1_R_tail'		, 'j', 'l-finger-1-2'),
	('finger-1-2_R_tail'		, 'j', 'l-finger-1-3'),
	('finger-1-3_R_tail'		, 'l', ((2,'l-finger-1-3'), (-1,'l-finger-1-2'))),
	('finger-2-1_R_head'		, 'j', 'l-finger-2-1'),
	('finger-2-1_R_tail'		, 'j', 'l-finger-2-2'),
	('finger-2-2_R_tail'		, 'j', 'l-finger-2-3'),
	('finger-2-3_R_tail'		, 'l', ((2,'l-finger-2-3'), (-1,'l-finger-2-2'))),
	('finger-3-1_R_head'		, 'j', 'l-finger-3-1'),
	('finger-3-1_R_tail'		, 'j', 'l-finger-3-2'),
	('finger-3-2_R_tail'		, 'j', 'l-finger-3-3'),
	('finger-3-3_R_tail'		, 'l', ((2,'l-finger-3-3'), (-1,'l-finger-3-2'))),
	('finger-4-1_R_head'		, 'j', 'l-finger-4-1'),
	('finger-4-1_R_tail'		, 'j', 'l-finger-4-2'),
	('finger-4-2_R_tail'		, 'j', 'l-finger-4-3'),
	('finger-4-3_R_tail'		, 'l', ((2,'l-finger-4-3'), (-1,'l-finger-4-2'))),
	('finger-5-1_R_head'		, 'j', 'l-finger-5-1'),
	('finger-5-1_R_tail'		, 'j', 'l-finger-5-2'),
	('finger-5-2_R_tail'		, 'j', 'l-finger-5-3'),
	('finger-5-3_R_tail'		, 'l', ((2,'l-finger-5-3'), (-1,'l-finger-5-2'))),

	('toe-1-1_L_head'		, 'j', 'r-toe-1-1'),
	('toe-1-1_L_tail'		, 'j', 'r-toe-1-2'),
	('toe-1-2_L_tail'		, 'l', ((2,'toe-1-1_L_tail'), (-1,'toe-1-1_L_head'))),
	('toe-2-1_L_head'		, 'j', 'r-toe-2-1'),
	('toe-2-1_L_tail'		, 'j', 'r-toe-2-2'),
	('toe-2-2_L_tail'		, 'j', 'r-toe-2-3'),
	('toe-2-3_L_tail'		, 'l', ((2,'toe-2-2_L_tail'), (-1,'toe-2-1_L_tail'))),
	('toe-3-1_L_head'		, 'j', 'r-toe-3-1'),
	('toe-3-1_L_tail'		, 'j', 'r-toe-3-2'),
	('toe-3-2_L_tail'		, 'j', 'r-toe-3-3'),
	('toe-3-3_L_tail'		, 'l', ((2,'toe-3-2_L_tail'), (-1,'toe-3-1_L_tail'))),
	('toe-4-1_L_head'		, 'j', 'r-toe-4-1'),
	('toe-4-1_L_tail'		, 'j', 'r-toe-4-2'),
	('toe-4-2_L_tail'		, 'j', 'r-toe-4-3'),
	('toe-4-3_L_tail'		, 'l', ((2,'toe-4-2_L_tail'), (-1,'toe-4-1_L_tail'))),
	('toe-5-1_L_head'		, 'j', 'r-toe-5-1'),
	('toe-5-1_L_tail'		, 'j', 'r-toe-5-2'),
	('toe-5-2_L_tail'		, 'j', 'r-toe-5-3'),
	('toe-5-3_L_tail'		, 'l', ((2,'toe-5-2_L_tail'), (-1,'toe-5-1_L_tail'))),

	('toe-1-1_R_head'		, 'j', 'l-toe-1-1'),
	('toe-1-1_R_tail'		, 'j', 'l-toe-1-2'),
	('toe-1-2_R_tail'		, 'l', ((2,'toe-1-1_R_tail'), (-1,'toe-1-1_R_head'))),
	('toe-2-1_R_head'		, 'j', 'l-toe-2-1'),
	('toe-2-1_R_tail'		, 'j', 'l-toe-2-2'),
	('toe-2-2_R_tail'		, 'j', 'l-toe-2-3'),
	('toe-2-3_R_tail'		, 'l', ((2,'toe-2-2_R_tail'), (-1,'toe-2-1_R_tail'))),
	('toe-3-1_R_head'		, 'j', 'l-toe-3-1'),
	('toe-3-1_R_tail'		, 'j', 'l-toe-3-2'),
	('toe-3-2_R_tail'		, 'j', 'l-toe-3-3'),
	('toe-3-3_R_tail'		, 'l', ((2,'toe-3-2_R_tail'), (-1,'toe-3-1_R_tail'))),
	('toe-4-1_R_head'		, 'j', 'l-toe-4-1'),
	('toe-4-1_R_tail'		, 'j', 'l-toe-4-2'),
	('toe-4-2_R_tail'		, 'j', 'l-toe-4-3'),
	('toe-4-3_R_tail'		, 'l', ((2,'toe-4-2_R_tail'), (-1,'toe-4-1_R_tail'))),
	('toe-5-1_R_head'		, 'j', 'l-toe-5-1'),
	('toe-5-1_R_tail'		, 'j', 'l-toe-5-2'),
	('toe-5-2_R_tail'		, 'j', 'l-toe-5-3'),
	('toe-5-3_R_tail'		, 'l', ((2,'toe-5-2_R_tail'), (-1,'toe-5-1_R_tail'))),

	('thigh_root_L_head'		, 'l', ((0.5, 'pelvis'), (0.5, 'r-upper-leg'))),
	('thigh_root_L_tail'		, 'j', 'r-upper-leg'),
	('thigh_L_tail'			, 'j', 'r-knee'),
	('shin_L_tail'			, 'j', 'r-ankle'),
	('foot_L_tail'			, 'b', 'toe-3-1_L_head'),
	('toe_L_tail'			, 'v', 12258),

	('thigh_root_R_head'		, 'l', ((0.5, 'pelvis'), (0.5, 'l-upper-leg'))),
	('thigh_root_R_tail'		, 'j', 'l-upper-leg'),
	('thigh_R_tail'			, 'j', 'l-knee'),
	('shin_R_tail'			, 'j', 'l-ankle'),
	('foot_R_tail'			, 'b', 'toe-3-1_R_head'),
	('toe_R_tail'			, 'v', 13258),

	('foot_L_center'		, 'v', 5736),
	('foot_R_center'		, 'v', 13326),

	('footCtrl_L_head'		, 'o', ('shin_L_tail', [0,-0.3,-0.3])),
	('footCtrl_L_tail'		, 'o', ('footCtrl_L_head', [0,1.5,0])),
	('tiptoe_L_head'		, 'b', 'toe_L_tail'),
	('tiptoe_L_tail'		, 'o', ('tiptoe_L_head', [0,0.6,0])),
	('tumble_out_L_head'		, 'l', ((1.25, 'foot_L_center'), (-0.25, 'foot_R_center'))),
	('tumble_out_L_tail'		, 'o', ('tumble_out_L_head', [0,0.6,0])),
	('tumble_in_L_head'		, 'l', ((0.7, 'foot_L_center'), (0.3, 'foot_R_center'))),
	('tumble_in_L_tail'		, 'o', ('tumble_in_L_head', [0,0.6,0])),
	('heel_L_head'			, 'v', 5721),
	('heel_L_tail'			, 'o', ('heel_L_head', [0,0.6,0])),
	('rotate_toe_L_head'		, 'b', 'foot_L_tail'),
	('rotate_toe_L_tail'		, 'o', ('rotate_toe_L_head', [0,0.6,0])),
	('toe_target_L_head'		, 'b', 'toe_L_tail'),
	('toe_target_L_tail'		, 'l', ((2, 'toe_L_tail'), (-1, 'foot_L_tail'))),
	('foot_target_L_head'		, 'b', 'foot_L_tail'),
	('foot_target_L_tail'		, 'l', ((2, 'foot_L_tail'), (-1, 'shin_L_tail'))),
	('leg_target_L_head'		, 'b', 'shin_L_tail'),
	('leg_target_L_tail'		, 'l', ((2, 'shin_L_tail'), (-1, 'thigh_L_tail'))),
	('foot_tumble_L_head'		, 'o', ('tiptoe_L_head', [0,1.0,0])),
	('foot_tumble_L_tail'		, 'o', ('foot_tumble_L_head', [0,0.6,0])),
	('foot_roll_L_head'		, 'o', ('toe_L_tail', [0.3,0,0.6])),
	('foot_roll_L_tail'		, 'o', ('foot_roll_L_head', [-0.6,0,0])),
	('knee_L_tail'			, 'o', ('thigh_L_tail', [0,0,6.0])),
	('knee_L_head'			, 'o', ('knee_L_tail', [0,-0.6,0])),
	('ikfk_foot_L_head'		, 'o', ('foot_roll_L_head', [0.0,0,0.6])),
	('ikfk_foot_L_tail'		, 'o', ('ikfk_foot_L_head', [-0.6,0,0])),

	('footCtrl_R_head'		, 'o', ('shin_R_tail', [0,-0.3,-0.3])),
	('footCtrl_R_tail'		, 'o', ('footCtrl_R_head', [0,1.5,0])),
	('tiptoe_R_head'		, 'b', 'toe_R_tail'),
	('tiptoe_R_tail'		, 'o', ('tiptoe_R_head', [0,0.6,0])),
	('tumble_out_R_head'		, 'l', ((1.25, 'foot_R_center'), (-0.25, 'foot_L_center'))),
	('tumble_out_R_tail'		, 'o', ('tumble_out_R_head', [0,0.6,0])),
	('tumble_in_R_head'		, 'l', ((0.7, 'foot_R_center'), (0.3, 'foot_L_center'))),
	('tumble_in_R_tail'		, 'o', ('tumble_in_R_head', [0,0.6,0])),
	('heel_R_head'			, 'v', 13338),
	('heel_R_tail'			, 'o', ('heel_R_head', [0,0.6,0])),
	('rotate_toe_R_head'		, 'b', 'foot_R_tail'),
	('rotate_toe_R_tail'		, 'o', ('rotate_toe_R_head', [0,0.6,0])),
	('toe_target_R_head'		, 'b', 'toe_R_tail'),
	('toe_target_R_tail'		, 'l', ((2, 'toe_R_tail'), (-1, 'foot_R_tail'))),
	('foot_target_R_head'		, 'b', 'foot_R_tail'),
	('foot_target_R_tail'		, 'l', ((2, 'foot_R_tail'), (-1, 'shin_R_tail'))),
	('leg_target_R_head'		, 'b', 'shin_R_tail'),
	('leg_target_R_tail'		, 'l', ((2, 'shin_R_tail'), (-1, 'thigh_R_tail'))),
	('foot_tumble_R_head'		, 'o', ('tiptoe_R_head', [0,1.0,0])),
	('foot_tumble_R_tail'		, 'o', ('foot_tumble_R_head', [0,0.6,0])),
	('foot_roll_R_head'		, 'o', ('toe_R_tail', [0.3,0,0.6])),
	('foot_roll_R_tail'		, 'o', ('foot_roll_R_head', [-0.6,0,0])),
	('knee_R_tail'			, 'o', ('thigh_R_tail', [0,0,6.0])),
	('knee_R_head'			, 'o', ('knee_R_tail', [0,-0.6,0])),
	('ikfk_foot_R_head'		, 'o', ('foot_roll_R_head', [0,0,0.6])),
	('ikfk_foot_R_tail'		, 'o', ('ikfk_foot_R_head', [-0.6,0,0])),
]


GoboHeadsTails = [
	('Root'			, 'root_head', 'root_tail'),
	('HandCtrl_L'		, 'hand_L_head', 'hand_L_tail'),
	('HandCtrl_R'		, 'hand_R_head', 'hand_R_tail'),
	('Hips'			, 'hip_head', 'hip_tail'),
	('Spine3'		, 'spine_3_head', 'spine_3_tail'),
	('Spine2'		, 'spine_3_tail', 'spine_2_tail'),
	('Spine1'		, 'spine_2_tail', 'spine_1_tail'),
	('Neck'			, 'spine_1_tail', 'neck_tail'),
	('Head'			, 'neck_tail', 'head_tail'),

	('Clavicle_L'		, 'shoulder_L_head', 'shoulder_L_tail'),
	('ArmFkIk_L'		, 'ikfk_hand_L_head', 'ikfk_hand_L_tail'),
	('ArmRoot_L'		, 'arm_root_L_head', 'arm_root_L_tail'),
	('UpArm_L'		, 'arm_root_L_tail', 'armupper_L_tail'),
	('LoArm_L'		, 'armupper_L_tail', 'armlower_L_tail'),
	('Hand_L'		, 'armlower_L_tail', 'hand_L_tail'),

	('UpArmIK_L'		, 'arm_root_L_tail', 'armupper_L_tail'),
	('LoArmIK_L'		, 'armupper_L_tail', 'armlower_L_tail'),
	('HandIK_L'		, 'armlower_L_tail', 'hand_L_tail'),
	('UpArmFK_L'		, 'arm_root_L_tail', 'armupper_L_tail'),
	('LoArmFK_L'		, 'armupper_L_tail', 'armlower_L_tail'),
	('HandFK_L'		, 'hand_L_head', 'hand_L_tail'),
	('Elbow_L'		, 'elbow_L_head', 'elbow_L_tail'),
	('FingerCurl_L'		, 'finger_curl_L_head', 'finger_curl_L_tail'),

	('Finger-1-1_L'		, 'finger-1-1_L_head', 'finger-1-1_L_tail'),
	('Finger-1-2_L'		, 'finger-1-1_L_tail', 'finger-1-2_L_tail'),
	('Finger-1-3_L'		, 'finger-1-2_L_tail', 'finger-1-3_L_tail'),
	('Finger-2-1_L'		, 'finger-2-1_L_head', 'finger-2-1_L_tail'),
	('Finger-2-2_L'		, 'finger-2-1_L_tail', 'finger-2-2_L_tail'),
	('Finger-2-3_L'		, 'finger-2-2_L_tail', 'finger-2-3_L_tail'),
	('Finger-3-1_L'		, 'finger-3-1_L_head', 'finger-3-1_L_tail'),
	('Finger-3-2_L'		, 'finger-3-1_L_tail', 'finger-3-2_L_tail'),
	('Finger-3-3_L'		, 'finger-3-2_L_tail', 'finger-3-3_L_tail'),
	('Finger-4-1_L'		, 'finger-4-1_L_head', 'finger-4-1_L_tail'),
	('Finger-4-2_L'		, 'finger-4-1_L_tail', 'finger-4-2_L_tail'),
	('Finger-4-3_L'		, 'finger-4-2_L_tail', 'finger-4-3_L_tail'),
	('Finger-5-1_L'		, 'finger-5-1_L_head', 'finger-5-1_L_tail'),
	('Finger-5-2_L'		, 'finger-5-1_L_tail', 'finger-5-2_L_tail'),
	('Finger-5-3_L'		, 'finger-5-2_L_tail', 'finger-5-3_L_tail'),

	('Finger-1-1IK_L'	, 'finger-1-1_L_head', 'finger-1-1_L_tail'),
	('Finger-1-2IK_L'	, 'finger-1-1_L_tail', 'finger-1-2_L_tail'),
	('Finger-1-3IK_L'	, 'finger-1-2_L_tail', 'finger-1-3_L_tail'),
	('Finger-2-1IK_L'	, 'finger-2-1_L_head', 'finger-2-1_L_tail'),
	('Finger-2-2IK_L'	, 'finger-2-1_L_tail', 'finger-2-2_L_tail'),
	('Finger-2-3IK_L'	, 'finger-2-2_L_tail', 'finger-2-3_L_tail'),
	('Finger-3-1IK_L'	, 'finger-3-1_L_head', 'finger-3-1_L_tail'),
	('Finger-3-2IK_L'	, 'finger-3-1_L_tail', 'finger-3-2_L_tail'),
	('Finger-3-3IK_L'	, 'finger-3-2_L_tail', 'finger-3-3_L_tail'),
	('Finger-4-1IK_L'	, 'finger-4-1_L_head', 'finger-4-1_L_tail'),
	('Finger-4-2IK_L'	, 'finger-4-1_L_tail', 'finger-4-2_L_tail'),
	('Finger-4-3IK_L'	, 'finger-4-2_L_tail', 'finger-4-3_L_tail'),
	('Finger-5-1IK_L'	, 'finger-5-1_L_head', 'finger-5-1_L_tail'),
	('Finger-5-2IK_L'	, 'finger-5-1_L_tail', 'finger-5-2_L_tail'),
	('Finger-5-3IK_L'	, 'finger-5-2_L_tail', 'finger-5-3_L_tail'),

	('Finger-1-1FK_L'	, 'finger-1-1_L_head', 'finger-1-1_L_tail'),
	('Finger-1-2FK_L'	, 'finger-1-1_L_tail', 'finger-1-2_L_tail'),
	('Finger-1-3FK_L'	, 'finger-1-2_L_tail', 'finger-1-3_L_tail'),
	('Finger-2-1FK_L'	, 'finger-2-1_L_head', 'finger-2-1_L_tail'),
	('Finger-2-2FK_L'	, 'finger-2-1_L_tail', 'finger-2-2_L_tail'),
	('Finger-2-3FK_L'	, 'finger-2-2_L_tail', 'finger-2-3_L_tail'),
	('Finger-3-1FK_L'	, 'finger-3-1_L_head', 'finger-3-1_L_tail'),
	('Finger-3-2FK_L'	, 'finger-3-1_L_tail', 'finger-3-2_L_tail'),
	('Finger-3-3FK_L'	, 'finger-3-2_L_tail', 'finger-3-3_L_tail'),
	('Finger-4-1FK_L'	, 'finger-4-1_L_head', 'finger-4-1_L_tail'),
	('Finger-4-2FK_L'	, 'finger-4-1_L_tail', 'finger-4-2_L_tail'),
	('Finger-4-3FK_L'	, 'finger-4-2_L_tail', 'finger-4-3_L_tail'),
	('Finger-5-1FK_L'	, 'finger-5-1_L_head', 'finger-5-1_L_tail'),
	('Finger-5-2FK_L'	, 'finger-5-1_L_tail', 'finger-5-2_L_tail'),
	('Finger-5-3FK_L'	, 'finger-5-2_L_tail', 'finger-5-3_L_tail'),

	('Clavicle_R'		, 'shoulder_R_head', 'shoulder_R_tail'),
	('ArmFkIk_R'		, 'ikfk_hand_R_head', 'ikfk_hand_R_tail'),
	('ArmRoot_R'		, 'arm_root_R_head', 'arm_root_R_tail'),
	('UpArm_R'		, 'arm_root_R_tail', 'armupper_R_tail'),
	('LoArm_R'		, 'armupper_R_tail', 'armlower_R_tail'),
	('Hand_R'		, 'armlower_R_tail', 'hand_R_tail'),

	('UpArmIK_R'		, 'arm_root_R_tail', 'armupper_R_tail'),
	('LoArmIK_R'		, 'armupper_R_tail', 'armlower_R_tail'),
	('HandIK_R'		, 'armlower_R_tail', 'hand_R_tail'),
	('UpArmFK_R'		, 'arm_root_R_tail', 'armupper_R_tail'),
	('LoArmFK_R'		, 'armupper_R_tail', 'armlower_R_tail'),
	('HandFK_R'		, 'hand_R_head', 'hand_R_tail'),
	('Elbow_R'		, 'elbow_R_head', 'elbow_R_tail'),
	('FingerCurl_R'		, 'finger_curl_R_head', 'finger_curl_R_tail'),

	('Finger-1-1_R'		, 'finger-1-1_R_head', 'finger-1-1_R_tail'),
	('Finger-1-2_R'		, 'finger-1-1_R_tail', 'finger-1-2_R_tail'),
	('Finger-1-3_R'		, 'finger-1-2_R_tail', 'finger-1-3_R_tail'),
	('Finger-2-1_R'		, 'finger-2-1_R_head', 'finger-2-1_R_tail'),
	('Finger-2-2_R'		, 'finger-2-1_R_tail', 'finger-2-2_R_tail'),
	('Finger-2-3_R'		, 'finger-2-2_R_tail', 'finger-2-3_R_tail'),
	('Finger-3-1_R'		, 'finger-3-1_R_head', 'finger-3-1_R_tail'),
	('Finger-3-2_R'		, 'finger-3-1_R_tail', 'finger-3-2_R_tail'),
	('Finger-3-3_R'		, 'finger-3-2_R_tail', 'finger-3-3_R_tail'),
	('Finger-4-1_R'		, 'finger-4-1_R_head', 'finger-4-1_R_tail'),
	('Finger-4-2_R'		, 'finger-4-1_R_tail', 'finger-4-2_R_tail'),
	('Finger-4-3_R'		, 'finger-4-2_R_tail', 'finger-4-3_R_tail'),
	('Finger-5-1_R'		, 'finger-5-1_R_head', 'finger-5-1_R_tail'),
	('Finger-5-2_R'		, 'finger-5-1_R_tail', 'finger-5-2_R_tail'),
	('Finger-5-3_R'		, 'finger-5-2_R_tail', 'finger-5-3_R_tail'),

	('Finger-1-1IK_R'	, 'finger-1-1_R_head', 'finger-1-1_R_tail'),
	('Finger-1-2IK_R'	, 'finger-1-1_R_tail', 'finger-1-2_R_tail'),
	('Finger-1-3IK_R'	, 'finger-1-2_R_tail', 'finger-1-3_R_tail'),
	('Finger-2-1IK_R'	, 'finger-2-1_R_head', 'finger-2-1_R_tail'),
	('Finger-2-2IK_R'	, 'finger-2-1_R_tail', 'finger-2-2_R_tail'),
	('Finger-2-3IK_R'	, 'finger-2-2_R_tail', 'finger-2-3_R_tail'),
	('Finger-3-1IK_R'	, 'finger-3-1_R_head', 'finger-3-1_R_tail'),
	('Finger-3-2IK_R'	, 'finger-3-1_R_tail', 'finger-3-2_R_tail'),
	('Finger-3-3IK_R'	, 'finger-3-2_R_tail', 'finger-3-3_R_tail'),
	('Finger-4-1IK_R'	, 'finger-4-1_R_head', 'finger-4-1_R_tail'),
	('Finger-4-2IK_R'	, 'finger-4-1_R_tail', 'finger-4-2_R_tail'),
	('Finger-4-3IK_R'	, 'finger-4-2_R_tail', 'finger-4-3_R_tail'),
	('Finger-5-1IK_R'	, 'finger-5-1_R_head', 'finger-5-1_R_tail'),
	('Finger-5-2IK_R'	, 'finger-5-1_R_tail', 'finger-5-2_R_tail'),
	('Finger-5-3IK_R'	, 'finger-5-2_R_tail', 'finger-5-3_R_tail'),

	('Finger-1-1FK_R'	, 'finger-1-1_R_head', 'finger-1-1_R_tail'),
	('Finger-1-2FK_R'	, 'finger-1-1_R_tail', 'finger-1-2_R_tail'),
	('Finger-1-3FK_R'	, 'finger-1-2_R_tail', 'finger-1-3_R_tail'),
	('Finger-2-1FK_R'	, 'finger-2-1_R_head', 'finger-2-1_R_tail'),
	('Finger-2-2FK_R'	, 'finger-2-1_R_tail', 'finger-2-2_R_tail'),
	('Finger-2-3FK_R'	, 'finger-2-2_R_tail', 'finger-2-3_R_tail'),
	('Finger-3-1FK_R'	, 'finger-3-1_R_head', 'finger-3-1_R_tail'),
	('Finger-3-2FK_R'	, 'finger-3-1_R_tail', 'finger-3-2_R_tail'),
	('Finger-3-3FK_R'	, 'finger-3-2_R_tail', 'finger-3-3_R_tail'),
	('Finger-4-1FK_R'	, 'finger-4-1_R_head', 'finger-4-1_R_tail'),
	('Finger-4-2FK_R'	, 'finger-4-1_R_tail', 'finger-4-2_R_tail'),
	('Finger-4-3FK_R'	, 'finger-4-2_R_tail', 'finger-4-3_R_tail'),
	('Finger-5-1FK_R'	, 'finger-5-1_R_head', 'finger-5-1_R_tail'),
	('Finger-5-2FK_R'	, 'finger-5-1_R_tail', 'finger-5-2_R_tail'),
	('Finger-5-3FK_R'	, 'finger-5-2_R_tail', 'finger-5-3_R_tail'),

	('Hip_L'		, 'hip_tail', 'thigh_root_L_head'),
	('LegRoot_L'		, 'thigh_root_L_head', 'thigh_root_L_tail'),
	('UpLegFK_L'		, 'thigh_root_L_tail', 'thigh_L_tail'),
	('LoLegFK_L'		, 'thigh_L_tail', 'shin_L_tail'),
	('FootFK_L'		, 'shin_L_tail', 'foot_L_tail'),
	('ToeFK_L'		, 'foot_L_tail', 'toe_L_tail'),
	('UpLegIK_L'		, 'thigh_root_L_tail', 'thigh_L_tail'),
	('LoLegIK_L'		, 'thigh_L_tail', 'shin_L_tail'),
	('FootIK_L'		, 'shin_L_tail', 'foot_L_tail'),
	('ToeIK_L'		, 'foot_L_tail', 'toe_L_tail'),
	('UpLeg_L'		, 'thigh_root_L_tail', 'thigh_L_tail'),
	('LoLeg_L'		, 'thigh_L_tail', 'shin_L_tail'),
	('Foot_L'		, 'shin_L_tail', 'foot_L_tail'),
	('Toe_L'		, 'foot_L_tail', 'toe_L_tail'),

	('Hip_R'		, 'hip_tail', 'thigh_root_R_head'),
	('LegRoot_R'		, 'thigh_root_R_head', 'thigh_root_R_tail'),
	('UpLegFK_R'		, 'thigh_root_R_tail', 'thigh_R_tail'),
	('LoLegFK_R'		, 'thigh_R_tail', 'shin_R_tail'),
	('FootFK_R'		, 'shin_R_tail', 'foot_R_tail'),
	('ToeFK_R'		, 'foot_R_tail', 'toe_R_tail'),
	('UpLegIK_R'		, 'thigh_root_R_tail', 'thigh_R_tail'),
	('LoLegIK_R'		, 'thigh_R_tail', 'shin_R_tail'),
	('FootIK_R'		, 'shin_R_tail', 'foot_R_tail'),
	('ToeIK_R'		, 'foot_R_tail', 'toe_R_tail'),
	('UpLeg_R'		, 'thigh_root_R_tail', 'thigh_R_tail'),
	('LoLeg_R'		, 'thigh_R_tail', 'shin_R_tail'),
	('Foot_R'		, 'shin_R_tail', 'foot_R_tail'),
	('Toe_R'		, 'foot_R_tail', 'toe_R_tail'),

	('FootCtrl_L'		, 'footCtrl_L_head', 'footCtrl_L_tail'),
	('TipToe_L'		, 'tiptoe_L_head', 'tiptoe_L_tail'),
	('TumbleOut_L'		, 'tumble_out_L_head', 'tumble_out_L_tail'),
	('TumbleIn_L'		, 'tumble_in_L_head', 'tumble_in_L_tail'),
	('Heel_L'		, 'heel_L_head', 'heel_L_tail'),
	('RotateToe_L'		, 'rotate_toe_L_head', 'rotate_toe_L_tail'),
	('ToeTarget_L'		, 'toe_target_L_head', 'toe_target_L_tail'),
	('FootTarget_L'		, 'foot_target_L_head', 'foot_target_L_tail'),
	('LegTarget_L'		, 'leg_target_L_head', 'leg_target_L_tail'),
	('FootTumble_L'		, 'foot_tumble_L_head', 'foot_tumble_L_tail'),
	('FootRoll_L'		, 'foot_roll_L_head', 'foot_roll_L_tail'),
	('Knee_L'		, 'knee_L_head', 'knee_L_tail'),
	('LegFkIk_L'		, 'ikfk_foot_L_head', 'ikfk_foot_L_tail'),

	('FootCtrl_R'		, 'footCtrl_R_head', 'footCtrl_R_tail'),
	('TipToe_R'		, 'tiptoe_R_head', 'tiptoe_R_tail'),
	('TumbleOut_R'		, 'tumble_out_R_head', 'tumble_out_R_tail'),
	('TumbleIn_R'		, 'tumble_in_R_head', 'tumble_in_R_tail'),
	('Heel_R'		, 'heel_R_head', 'heel_R_tail'),
	('RotateToe_R'		, 'rotate_toe_R_head', 'rotate_toe_R_tail'),
	('ToeTarget_R'		, 'toe_target_R_head', 'toe_target_R_tail'),
	('FootTarget_R'		, 'foot_target_R_head', 'foot_target_R_tail'),
	('LegTarget_R'		, 'leg_target_R_head', 'leg_target_R_tail'),
	('FootTumble_R'		, 'foot_tumble_R_head', 'foot_tumble_R_tail'),
	('FootRoll_R'		, 'foot_roll_R_head', 'foot_roll_R_tail'),
	('Knee_R'		, 'knee_R_head', 'knee_R_tail'),
	('LegFkIk_R'		, 'ikfk_foot_R_head', 'ikfk_foot_R_tail'),

	('Breathe'		, 'spine1', 'chest-front'),
	('Stomach'		, 'chest-front', 'pelvis'),

	('UpArmTwist_L'		, 'r-shoulder', 'r-elbow'),
	('LoArmTwist_L'		, 'r-elbow', 'r-hand'),
	('UpLegTwist_L'		, 'r-upper-leg', 'r-knee'),
	('UpArmTwist_R'		, 'l-shoulder', 'l-elbow'),
	('LoArmTwist_R'		, 'l-elbow', 'l-hand'),
	('UpLegTwist_R'		, 'l-upper-leg', 'l-knee'),
]

GoboArmature = [
	('Root',		0.0, None, F_WIR, L_MAIN, (1,1,1)),

	('HandCtrl_L',		1.5708, 'Root', F_WIR, L_ARMIK, (1,1,1)),
	('HandCtrl_R',		-1.5708, 'Root', F_WIR, L_ARMIK, (1,1,1)),

	('Hips',		0.0, 'Root', F_DEF+F_WIR, L_MAIN+L_DEF, (1,1,1)),
	('Spine3',		0.0, 'Hips', F_DEF+F_WIR, L_MAIN+L_DEF, (1,1,1)),
	('Spine2',		0.0, 'Spine3', F_DEF+F_CON+F_WIR, L_MAIN+L_DEF, (1,1,1)),
	('Spine1',		0.0, 'Spine2', F_DEF+F_CON+F_WIR, L_MAIN+L_DEF, (1,1,1)),
	('Neck',		0.0, 'Spine1', F_DEF+F_CON+F_WIR, L_MAIN+L_DEF, (1,1,1)),
	('Head',		0.0, 'Neck', F_DEF+F_CON+F_WIR, L_MAIN+L_DEF, (1,1,1)),

	('Clavicle_L',		1.5708, 'Spine1', F_DEF+F_WIR, L_SKEL+L_DEF, (1,1,1)),
	('ArmFkIk_L',		-1.5708, 'Clavicle_L', F_WIR, L_MAIN+L_ARMIK+L_ARMFK, (1,1,1)),
	('ArmRoot_L',		1.5708, 'Clavicle_L', F_RES, L_SKEL, (0,0,2)),
	('Elbow_L',		0, 'ArmRoot_L', F_WIR,  L_ARMIK, (1,1,1)),
	('UpArm_L',		1.5708, 'ArmRoot_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,10)),
	('LoArm_L',		1.5708, 'UpArm_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,10)),
	('Hand_L',		1.5708, 'LoArm_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('UpArmIK_L',		1.5708, 'ArmRoot_L', F_CON+F_RES, L_HLPIK, (0,0,10)),
	('LoArmIK_L',		1.5708, 'UpArmIK_L', F_CON+F_RES, L_HLPIK, (0,0,10)),
	('HandIK_L',		1.5708, 'LoArmIK_L', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('UpArmFK_L',		1.5708, 'ArmRoot_L', F_CON+F_WIR, L_ARMFK, (0,0,10)),
	('LoArmFK_L',		1.5708, 'UpArmFK_L', F_CON+F_WIR, L_ARMFK, (0,0,10)),
	('HandFK_L',		1.5708, 'LoArmFK_L', F_CON+F_WIR, L_ARMFK, (1,1,1)),
	('FingerCurl_L',	0, 'LoArm_L',	 F_WIR, L_ARMIK+L_ARMFK, (1,1,1)),

	('Clavicle_R',		-1.5708, 'Spine1', F_DEF+F_WIR, L_SKEL+L_DEF, (1,1,1)),
	('ArmFkIk_R',		-1.5708, 'Clavicle_R', F_WIR, L_MAIN+L_ARMIK+L_ARMFK, (1,1,1)),
	('ArmRoot_R',		-1.5708, 'Clavicle_R', F_RES, L_SKEL, (0,0,2)),
	('Elbow_R',		0, 'ArmRoot_R', F_WIR, L_ARMIK, (1,1,1)),
	('UpArm_R',		-1.5708, 'ArmRoot_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,10)),
	('LoArm_R',		-1.5708, 'UpArm_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,10)),
	('Hand_R',		-1.5708, 'LoArm_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('UpArmIK_R',		-1.5708, 'ArmRoot_R', F_CON+F_RES, L_HLPIK, (0,0,10)),
	('LoArmIK_R',		-1.5708, 'UpArmIK_R', F_CON+F_RES, L_HLPIK, (0,0,10)),
	('HandIK_R',		-1.5708, 'LoArmIK_R', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('UpArmFK_R',		-1.5708, 'ArmRoot_R', F_CON+F_WIR, L_ARMFK, (0,0,10)),
	('LoArmFK_R',		-1.5708, 'UpArmFK_R', F_CON+F_WIR, L_ARMFK, (0,0,10)),
	('HandFK_R',		-1.5708, 'LoArmFK_R', F_CON+F_WIR, L_ARMFK, (1,1,1)),
	('FingerCurl_R',	-3.14158, 'LoArm_R', F_WIR, L_ARMFK+L_ARMIK, (1,1,1)),

	('Finger-1-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-1-2_L',	1.5708, 'Finger-1-1_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-1-3_L',	1.5708, 'Finger-1-2_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-2-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-2-2_L',	1.5708, 'Finger-2-1_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-2-3_L',	1.5708, 'Finger-2-2_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-3-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-3-2_L',	1.5708, 'Finger-3-1_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-3-3_L',	1.5708, 'Finger-3-2_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-4-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-4-2_L',	1.5708, 'Finger-4-1_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-4-3_L',	1.5708, 'Finger-4-2_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-5-1_L',	1.5708, 'Hand_L', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-5-2_L',	1.5708, 'Finger-5-1_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-5-3_L',	1.5708, 'Finger-5-2_L', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),

	('Finger-1-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-1-2_R',	1.5708, 'Finger-1-1_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-1-3_R',	1.5708, 'Finger-1-2_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-2-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-2-2_R',	1.5708, 'Finger-2-1_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-2-3_R',	1.5708, 'Finger-2-2_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-3-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-3-2_R',	1.5708, 'Finger-3-1_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-3-3_R',	1.5708, 'Finger-3-2_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-4-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-4-2_R',	1.5708, 'Finger-4-1_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-4-3_R',	1.5708, 'Finger-4-2_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-5-1_R',	1.5708, 'Hand_R', F_DEF+F_RES, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-5-2_R',	1.5708, 'Finger-5-1_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),
	('Finger-5-3_R',	1.5708, 'Finger-5-2_R', F_DEF+F_RES+F_CON, L_DEF+L_HANDIK+L_HANDFK, (1,1,1)),

	('Hip_L',		0.0, 'Hips', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('LegRoot_L',		0.0, 'Hip_L', F_CON+F_RES, L_SKEL, (0,0,2)),
	('UpLeg_L',		0.0, 'LegRoot_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,8)),
	('LoLeg_L',		0.0, 'UpLeg_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,5)),
	('Foot_L',		0.0, 'LoLeg_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('Toe_L',		0.0, 'Foot_L', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('UpLegIK_L',		0.0, 'LegRoot_L', F_CON+F_RES, L_HLPIK, (0,0,8)),
	('LoLegIK_L',		0.0, 'UpLegIK_L', F_CON+F_RES, L_HLPIK, (0,0,5)),
	('FootIK_L',		0.0, 'LoLegIK_L', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('ToeIK_L',		0.0, 'FootIK_L', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('UpLegFK_L',		0.0, 'LegRoot_L', F_CON, L_LEGFK, (0,0,8)),
	('LoLegFK_L',		0.0, 'UpLegFK_L', F_CON, L_LEGFK, (0,0,5)),
	('FootFK_L',		0.0, 'LoLegFK_L', F_CON, L_LEGFK, (1,1,1)),
	('ToeFK_L',		0.0, 'FootFK_L', F_CON, L_LEGFK, (1,1,1)),

	('Hip_R',		0.0, 'Hips', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('LegRoot_R',		0.0, 'Hip_R', F_CON+F_RES, L_SKEL, (0,0,2)),
	('UpLeg_R',		0.0, 'LegRoot_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,8)),
	('LoLeg_R',		0.0, 'UpLeg_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (0,0,5)),
	('Foot_R',		0.0, 'LoLeg_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('Toe_R',		0.0, 'Foot_R', F_DEF+F_CON+F_RES, L_SKEL+L_DEF, (1,1,1)),
	('UpLegIK_R',		0.0, 'LegRoot_R', F_CON+F_RES, L_HLPIK, (0,0,8)),
	('LoLegIK_R',		0.0, 'UpLegIK_R', F_CON+F_RES, L_HLPIK, (0,0,5)),
	('FootIK_R',		0.0, 'LoLegIK_R', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('ToeIK_R',		0.0, 'FootIK_R', F_CON+F_RES, L_HLPIK, (1,1,1)),
	('UpLegFK_R',		0.0, 'LegRoot_R', F_CON, L_LEGFK, (0,0,8)),
	('LoLegFK_R',		0.0, 'UpLegFK_R', F_CON, L_LEGFK, (0,0,5)),
	('FootFK_R',		0.0, 'LoLegFK_R', F_CON, L_LEGFK, (1,1,1)),
	('ToeFK_R',		0.0, 'FootFK_R', F_CON, L_LEGFK, (1,1,1)),

	('FootCtrl_L',		0.0, 'Root', F_WIR, L_LEGIK, (1,1,1)),
	('TipToe_L',		0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_L',		0.0, 'TipToe_L', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_L',		0.0, 'TumbleOut_L', F_RES, L_HELP, (1,1,1)),
	('Heel_L',		0.0, 'TumbleIn_L', F_RES, L_HELP, (1,1,1)),
	('RotateToe_L',		0.0, 'Heel_L', F_WIR, L_LEGIK, (1,1,1)),
	('ToeTarget_L',		0.0, 'RotateToe_L', F_RES, L_HELP, (1,1,1)),
	('FootTarget_L',	0.0, 'Heel_L', F_RES, L_HELP, (1,1,1)),
	('LegTarget_L',		0.0, 'FootCtrl_L', F_RES, L_HELP, (1,1,1)),
	('FootTumble_L',	0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_L',		-1.5708, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('Knee_L',		0.0, 'FootCtrl_L', F_WIR, L_LEGIK, (1,1,1)),
	('LegFkIk_L',		-1.5708, 'FootCtrl_L', F_WIR, L_MAIN+L_LEGIK+L_LEGFK, (1,1,1)),

	('FootCtrl_R',		0.0, 'Root', F_WIR, L_LEGIK, (1,1,1)),
	('TipToe_R',		0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('TumbleOut_R',		0.0, 'TipToe_R', F_RES, L_HELP, (1,1,1)),
	('TumbleIn_R',		0.0, 'TumbleOut_R', F_RES, L_HELP, (1,1,1)),
	('Heel_R',		0.0, 'TumbleIn_R', F_RES, L_HELP, (1,1,1)),
	('RotateToe_R',		0.0, 'Heel_R', F_WIR, L_LEGIK, (1,1,1)),
	('ToeTarget_R',		0.0, 'RotateToe_R', F_RES, L_HELP, (1,1,1)),
	('FootTarget_R',	0.0, 'Heel_R', F_RES, L_HELP, (1,1,1)),
	('LegTarget_R',		0.0, 'FootCtrl_R', F_RES, L_HELP, (1,1,1)),
	('FootTumble_R',	0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('FootRoll_R',		-1.5708, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('Knee_R',		0.0, 'FootCtrl_R', F_WIR, L_LEGIK, (1,1,1)),
	('LegFkIk_R',		-1.5708, 'FootCtrl_R', F_WIR, L_MAIN+L_LEGIK, (1,1,1)),

	('Breathe', 		0.0, 'Spine2', F_CON+F_DEF, L_DEF, (1,1,1)),
	('Stomach', 		0.0, 'Breathe', F_CON+F_DEF+F_NOSCALE+F_RES, L_DEF, (1,1,1)),

	('UpArmTwist_L', 	0.0, 'ArmRoot_L', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
	('LoArmTwist_L', 	0.0, 'UpArm_L', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
 	('UpLegTwist_L', 	0.0, 'LegRoot_L', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
	('UpArmTwist_R', 	0.0, 'ArmRoot_R', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
	('LoArmTwist_R', 	0.0, 'UpArm_R', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
	('UpLegTwist_R', 	0.0, 'LegRoot_R', F_CON+F_DEF+F_RES, L_DEF, (1,1,1)),
]	

#
#	GoboBoneGroups
#

GoboBoneGroups = [
	('fk', 'THEME11'),
	('ik', 'THEME09'),
	('spinal_column', 'THEME11'),
	('grabable', 'DEFAULT'),
]
	
#
#	GoboWritePoses(fp):
#

def GoboWritePoses(fp):
	global boneGroups
	boneGroups = {}

	writeBoneGroups(fp, GoboBoneGroups) 

	addPoseBone(fp, 'Root', 'MHRoot', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (0,2.96706, 0,0, 0,0), (True, False, False)])])

	# Left foot
	addPoseBone(fp, 'FootCtrl_L', 'MHFootCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'TipToe_L', 'MHTipToe_L', None, (1,1,1), (0,0,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (0,2.96706, 0,0, 0,0), (True, False, False)])])

	addPoseBone(fp, 'FootRoll_L', 'MHArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'FootTumble_L', 'MHArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'TumbleOut_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['goboFootTumble', 'FootTumble_L', 'LOCATION_X', (1,21), (-0.5,0.5)])])

	addPoseBone(fp, 'TumbleIn_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['goboFootTumble', 'FootTumble_L', 'LOCATION_X', (1,21), (-0.5,0.5)])])

	addPoseBone(fp, 'Heel_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['goboFootRoll', 'FootRoll_L', 'LOCATION_X', (1,21), (-0.5,0.5)])])

	addPoseBone(fp, 'RotateToe_L', 'MHRotate_L', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'FootTarget_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['goboFootRoll', 'FootRoll_L', 'LOCATION_X', (1,21), (-0.5,0.5)])])

	addPoseBone(fp, 'Knee_L', 'MHCircle', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LegFkIk_L', 'MHIkfk', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	# Right foot
	addPoseBone(fp, 'FootCtrl_R', 'MHFootCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'TipToe_R', 'MHTipToe_R', None, (1,1,1), (0,0,1), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (0,2.96706, 0,0, 0,0), (True, False, False)])])

	addPoseBone(fp, 'FootRoll_R', 'MHArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'FootTumble_R', 'MHArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'TumbleOut_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['goboFootTumble', 'FootTumble_R', 'LOCATION_X', (1,21), (-0.5,0.5)])])

	addPoseBone(fp, 'TumbleIn_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['goboFootTumble', 'FootTumble_R', 'LOCATION_X', (1,21), (-0.5,0.5)])])

	addPoseBone(fp, 'Heel_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['goboFootRoll', 'FootRoll_R', 'LOCATION_X', (1,21), (-0.5,0.5)])])

	addPoseBone(fp, 'RotateToe_R', 'MHRotate_R', None, (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'FootTarget_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('Action', C_TARGET, ['goboFootRoll', 'FootRoll_R', 'LOCATION_X', (1,21), (-0.5,0.5)])])

	addPoseBone(fp, 'Knee_R', 'MHCircle', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LegFkIk_R', 'MHIkfk', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	# Spinal column
	addPoseBone(fp, 'Hips', 'MHHips', 'spinal_column', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'Spine3', 'MHCircle15', 'spinal_column', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'Spine2', 'MHCircle15', 'spinal_column', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'Spine1', 'MHCircle10', 'spinal_column', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'Neck', 'MHNeck', 'spinal_column', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'Head', 'MHHead', 'spinal_column', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Left arm
	addPoseBone(fp, 'Clavicle_L', 'MHShldr_L', 'grabable', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (-0.785398,0.349066, 0,0, -0.349066,0.785398), (True, True, True)])])

	addPoseBone(fp, 'ArmFkIk_L', 'MHIkfk', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'Elbow_L', 'MHCircle', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpArmFK_L', 'MHCircle025', 'fk', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'LoArmFK_L', 'MHCircle025', 'fk', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'HandFK_L', 'MHCircle10', 'fk', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoArmIK_L', None, 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['HandCtrl_L', 2, (-1.5708, 'Elbow_L'), (True, False)])])

	addPoseBone(fp, 'HandIK_L', None, None, (0,0,0), (0,0,0),  (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'HandCtrl_L', 1, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'UpArm_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'UpArmIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'UpArmFK_L', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'LoArm_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'LoArmIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'LoArmFK_L', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'Hand_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'HandIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'HandFK_L', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'FingerCurl_L', 'MHArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.2,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'HandCtrl_L', 'MHHandCtrl_L', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Right arm
	addPoseBone(fp, 'Clavicle_R', 'MHShldr_R', 'grabable', (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0,
		[('LimitRot', C_OWNER, ['LimitRot', (-0.785398,0.349066, 0,0, -0.785398,0.349066), (True, True, True)])])

	addPoseBone(fp, 'ArmFkIk_R', 'MHIkfk', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.5,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'Elbow_R', 'MHCircle', 'ik', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'UpArmFK_R', 'MHCircle025', 'fk', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'LoArmFK_R', 'MHCircle025', 'fk', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'HandFK_R', 'MHCircle10', 'fk', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoArmIK_R', None, 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['HandCtrl_R', 2, (-1.5708, 'Elbow_R'), (True, False)])])

	addPoseBone(fp, 'HandIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('CopyRot', 0, ['CopyRotIK', 'HandCtrl_R', 1, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'UpArm_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'UpArmIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'UpArmFK_R', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'LoArm_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'LoArmIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'LoArmFK_R', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'Hand_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'HandIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'HandFK_R', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'FingerCurl_R', 'MHArrows', 'grabable', (0,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER, ['LimitLoc', (-0.2,0.5, 0,0, 0,0), (True,True, False,False, False,False)])])

	addPoseBone(fp, 'HandCtrl_R', 'MHHandCtrl_R', 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Left leg
	addPoseBone(fp, 'UpLegFK_L', 'MHCircle025', 'fk', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'LoLegFK_L', 'MHCircle025', 'fk', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'FootFK_L', 'MHCircle05', 'fk', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'ToeFK_L', 'MHCircle05', 'fk', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoLegIK_L', None, 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['LegTarget_L', 2, (-1.87, 'Knee_L'), (True, False)])])

	addPoseBone(fp, 'FootIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['FootTarget_L', 1, None, (True, True)])])
	addPoseBone(fp, 'ToeIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['ToeTarget_L', 1, None, (True, True)])])

	addPoseBone(fp, 'UpLeg_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'UpLegIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'UpLegFK_L', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'LoLeg_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'LoLegIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'LoLegFK_L', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'Foot_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'FootIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'FootFK_L', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'Toe_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'ToeIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'ToeFK_L', 0, (1,1,1), (0,0,0)])])

	# Right leg
	addPoseBone(fp, 'UpLegFK_R', 'MHCircle025', 'fk', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'LoLegFK_R', 'MHCircle025', 'fk', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'FootFK_R', 'MHCircle10', 'fk', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])
	addPoseBone(fp, 'ToeFK_R', 'MHCircle10', 'fk', (1,1,1), (0,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoLegIK_R', None, 'ik', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['LegTarget_R', 2, (-1.27, 'Knee_R'), (True, False)])])

	addPoseBone(fp, 'FootIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['FootTarget_R', 1, None, (True, True)])])
	addPoseBone(fp, 'ToeIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['ToeTarget_R', 1, None, (True, True)])])

	addPoseBone(fp, 'UpLeg_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'UpLegIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'UpLegFK_R', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'LoLeg_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'LoLegIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'LoLegFK_R', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'Foot_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'FootIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'FootFK_R', 0, (1,1,1), (0,0,0)])])
	addPoseBone(fp, 'Toe_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'ToeIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'ToeFK_R', 0, (1,1,1), (0,0,0)])])

	for m in range(1,6):
		for n in range(1,4):
			poseFinger(fp, m, n, 'L', 'MHCircle025')
			poseFinger(fp, m, n, 'R', 'MHCircle025')

	addPoseBone(fp, 'UpArmTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['LoArm_L', 1, None, (True, False)])]) 
	addPoseBone(fp, 'LoArmTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['Hand_L', 1, None, (True, False)])])
	addPoseBone(fp, 'UpLegTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['LoLeg_L', 1, None, (True, False)])])
	addPoseBone(fp, 'UpArmTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
		[('IK', 0, ['LoArm_R', 1, None, (True, False)])])
	addPoseBone(fp, 'LoArmTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['Hand_R', 1, None, (True, False)])])
	addPoseBone(fp, 'UpLegTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		 [('IK', 0, ['LoLeg_R', 1, None, (True, False)])])

	return

#
#	poseFinger(fp, m, n, suffix, shape):
#

def poseFinger(fp, m, n, suffix, shape):
	if n == 1:
		addPoseBone(fp, "Finger-%d-%d_%s \n" % (m, n, suffix), shape, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, [])
	else:
		constraints = [('Action', C_TARGET, ['goboFingerCurl', 'FingerCurl_%s' % (suffix), 'LOCATION_X', (1,21), (-0.5,0.5)])]
		if m == 1:
			lockRot = (0,1,0)
		else:
			lockRot = (1,1,0)
		addPoseBone(fp, "Finger-%d-%d_%s \n" % (m, n, suffix), shape, None, (0,0,0), lockRot, (1,1,1), (1,1,1), 0, constraints)
	return

#
#	actionFingerCurl
#	actionFootTumble
#	actionFootRoll
#	GoboWriteActions(fp):
#

actionFingerCurl = [
	("Finger-2-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-2-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-2-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-3-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-3-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-3-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-4-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-4-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-4-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-5-1", (0.923880, 0.0, 0.0, 0.382683), (0.793353, 0.0, 0.0, -0.608761) ), 
	("Finger-5-2", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
	("Finger-5-3", (0.887011, 0.0, 0.0, 0.461749), ( 0.707107, 0.0, 0.0, -0.707107) ), 
]

actionFootTumble = [
	("TumbleOut_L", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.0, 0.0, -0.707107) ),
	("TumbleIn_L", (0.707107, 0.0, 0.0, 0.707107), (1.0, 0.0, 0.0, 0.0) ),
	("TumbleOut_R", (0.707107, 0.0, 0.0, 0.707107), (1.0, 0.0, 0.0, 0.0) ),
	("TumbleIn_R", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.0, 0.0, -0.707107) ),
]

actionFootRoll = [
	("Heel_L", (0.707107, -0.707107, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ),
	("FootTarget_L", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.707107, 0.0, 0.0) ),
	("Heel_R", (0.707107, -0.707107, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ),
	("FootTarget_R", (1.0, 0.0, 0.0, 0.0), (0.707107, 0.707107, 0.0, 0.0) ),
]


def GoboWriteActions(fp):
	writeAction("goboFingerCurl", actionFingerCurl, True, False, fp)
	writeAction("goboFootRoll", actionFootRoll, False,  False, fp)
	writeAction("goboFootTumble", actionFootTumble, False,  False, fp)
	return

#
#	GoboDrivers
#

GoboDrivers = [
	("UpLeg_L", "CopyRotFK", "CopyRotIK", "PLegIK_L"),
	("LoLeg_L", "CopyRotFK", "CopyRotIK", "PLegIK_L"),
	("Foot_L", "CopyRotFK", "CopyRotIK", "PLegIK_L"),
	("Toe_L", "CopyRotFK", "CopyRotIK", "PLegIK_L"),
	("UpLeg_R", "CopyRotFK", "CopyRotIK", "PLegIK_R"),
	("LoLeg_R", "CopyRotFK", "CopyRotIK", "PLegIK_R"),
	("Foot_R", "CopyRotFK", "CopyRotIK", "PLegIK_R"),
	("Toe_R", "CopyRotFK", "CopyRotIK", "PLegIK_R"),

	("UpArm_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("LoArm_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Hand_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("UpArm_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("LoArm_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Hand_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
]
'''
	("Finger-1-1_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-1-2_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-1-3_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-2-1_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-2-2_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-2-3_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-3-1_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-3-2_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-3-3_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-4-1_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-4-2_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-4-3_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-5-1_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-5-2_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),
	("Finger-5-3_L", "CopyRotFK", "CopyRotIK", "PArmIK_L"),

	("Finger-1-1_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-1-2_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-1-3_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-2-1_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-2-2_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-2-3_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-3-1_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-3-2_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-3-3_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-4-1_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-4-2_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-4-3_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-5-1_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-5-2_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
	("Finger-5-3_R", "CopyRotFK", "CopyRotIK", "PArmIK_R"),
'''

#
#	GoboWriteDrivers(fp):
#

def GoboWriteDrivers(fp):
	for (bone, cnsIK, cnsFK, targ) in GoboDrivers:
		writeDriver(fp, "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsIK), 0, "2*ik", 
			[("ik", 'TRANSFORMS', [('HumanRig', targ, 'LOC_X', C_LOCAL)])])
		writeDriver(fp, "pose.bones[\"%s\"].constraints[\"%s\"].influence" % (bone, cnsFK), 0, "1.0-2*ik",
			[("ik", 'TRANSFORMS', [('HumanRig', targ, 'LOC_X', C_LOCAL)])])



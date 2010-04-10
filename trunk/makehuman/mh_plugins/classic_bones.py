#
#	Bone definitions for Classic rig
#
import mhx_rig
from mhx_rig import *

ClassicJoints = [
	('pelvis',			'j', 'pelvis'),
	('spine3',			'j', 'spine3'),
	('spine2',			'j', 'spine2'),
	('spine1',			'j', 'spine1'),
	('chest-front',			'v', 7292),
	('neck',			'j', 'neck'),
	('head',			'j', 'head'),
	('mouth',			'j', 'mouth'),
	('l-eye',			'j', 'l-eye'),
	('r-eye',			'j', 'r-eye'),

	('r-clavicle',			'j', 'r-clavicle'),
	('r-shoulder',			'j', 'r-shoulder'),
	('r-elbow',			'j', 'r-elbow'),
	('r-hand',			'j', 'r-hand'),

	('r-finger-1-1',		'j', 'r-finger-1-1'),
	('r-finger-1-2',		'j', 'r-finger-1-2'),
	('r-finger-1-3',		'j', 'r-finger-1-3'),
	('r-finger-2-1',		'j', 'r-finger-2-1'),
	('r-finger-2-2',		'j', 'r-finger-2-2'),
	('r-finger-2-3',		'j', 'r-finger-2-3'),
	('r-finger-3-1',		'j', 'r-finger-3-1'),
	('r-finger-3-2',		'j', 'r-finger-3-2'),
	('r-finger-3-3',		'j', 'r-finger-3-3'),
	('r-finger-4-1',		'j', 'r-finger-4-1'),
	('r-finger-4-2',		'j', 'r-finger-4-2'),
	('r-finger-4-3',		'j', 'r-finger-4-3'),
	('r-finger-5-1',		'j', 'r-finger-5-1'),
	('r-finger-5-2',		'j', 'r-finger-5-2'),
	('r-finger-5-3',		'j', 'r-finger-5-3'),

	('l-clavicle',			'j', 'l-clavicle'),
	('l-shoulder',			'j', 'l-shoulder'),
	('l-elbow',			'j', 'l-elbow'),
	('l-hand',			'j', 'l-hand'),

	('l-finger-1-1',		'j', 'l-finger-1-1'),
	('l-finger-1-2',		'j', 'l-finger-1-2'),
	('l-finger-1-3',		'j', 'l-finger-1-3'),
	('l-finger-2-1',		'j', 'l-finger-2-1'),
	('l-finger-2-2',		'j', 'l-finger-2-2'),
	('l-finger-2-3',		'j', 'l-finger-2-3'),
	('l-finger-3-1',		'j', 'l-finger-3-1'),
	('l-finger-3-2',		'j', 'l-finger-3-2'),
	('l-finger-3-3',		'j', 'l-finger-3-3'),
	('l-finger-4-1',		'j', 'l-finger-4-1'),
	('l-finger-4-2',		'j', 'l-finger-4-2'),
	('l-finger-4-3',		'j', 'l-finger-4-3'),
	('l-finger-5-1',		'j', 'l-finger-5-1'),
	('l-finger-5-2',		'j', 'l-finger-5-2'),
	('l-finger-5-3',		'j', 'l-finger-5-3'),

	('r-upper-leg',			'j', 'r-upper-leg'),
	('r-knee',			'j', 'r-knee'),
	('r-ankle',			'j', 'r-ankle'),

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

	('l-upper-leg',			'j', 'l-upper-leg'),
	('l-knee',			'j', 'l-knee'),
	('l-ankle',			'j', 'l-ankle'),

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

	('jaw-tip',			'v', 8162),
	('tounge-tip',			'v', 8049),
	('tounge-mid',			'v', 8103),
	('tounge-root',			'v', 8099),
	('l-upLid',			'v', 12630),
	('l-loLid',			'v', 12594),
	('r-upLid',			'v', 2442),
	('r-loLid',			'v', 2520),
	('head-end',			'l', ((2.0, 'head'), (-1.0, 'neck'))),
	('mouth-end',			'l', ((3.0, 'mouth'), (-2.0, 'head'))),

	('l-finger-1-end',		'l', ((2.0, 'l-finger-1-3'), (-1.0, 'l-finger-1-2'))),
	('l-finger-2-end',		'l', ((2.0, 'l-finger-2-3'), (-1.0, 'l-finger-2-2'))),
	('l-finger-3-end',		'l', ((2.0, 'l-finger-3-3'), (-1.0, 'l-finger-3-2'))),
	('l-finger-4-end',		'l', ((2.0, 'l-finger-4-3'), (-1.0, 'l-finger-4-2'))),
	('l-finger-5-end',		'l', ((2.0, 'l-finger-5-3'), (-1.0, 'l-finger-5-2'))),
	('r-finger-1-end',		'l', ((2.0, 'r-finger-1-3'), (-1.0, 'r-finger-1-2'))),
	('r-finger-2-end',		'l', ((2.0, 'r-finger-2-3'), (-1.0, 'r-finger-2-2'))),
	('r-finger-3-end',		'l', ((2.0, 'r-finger-3-3'), (-1.0, 'r-finger-3-2'))),
	('r-finger-4-end',		'l', ((2.0, 'r-finger-4-3'), (-1.0, 'r-finger-4-2'))),
	('r-finger-5-end',		'l', ((2.0, 'r-finger-5-3'), (-1.0, 'r-finger-5-2'))),

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

	('l-knee-target',		'l', ((1.2, 'l-knee'), (-0.2, 'l-upper-leg'))),
	('l-elbow-target',		'l', ((1.2, 'l-elbow'), (-0.2, 'l-shoulder'))),
	('r-knee-target',		'l', ((1.2, 'r-knee'), (-0.2, 'r-upper-leg'))),
	('r-elbow-target',		'l', ((1.2, 'r-elbow'), (-0.2, 'r-shoulder'))),

	('l-clavicle-pt2',		'l', ((0.5, 'l-clavicle'), (0.5, 'l-shoulder'))),
	('l-uparm-pt1',			'l', ((0.5, 'l-shoulder'), (0.5, 'l-elbow'))),
	('l-uparm-pt2',			'l', ((0.7, 'l-shoulder'), (0.3, 'l-elbow'))),
	('l-loarm-pt1',			'l', ((0.3, 'l-elbow'), (0.7, 'l-hand'))),
	('l-loarm-pt2',			'l', ((0.7, 'l-elbow'), (0.3, 'l-hand'))),
	('l-upleg-pt1',			'l', ((0.3, 'l-upper-leg'), (0.7, 'l-knee'))),
	('l-upleg-pt2',			'l', ((0.7, 'l-upper-leg'), (0.3, 'l-knee'))),
	('l-loleg-pt1',			'l', ((0.3, 'l-knee'), (0.7, 'l-ankle'))),
	('l-loleg-pt2',			'l', ((0.7, 'l-knee'), (0.3, 'l-ankle'))),

	('r-clavicle-pt2',		'l', ((0.5, 'r-clavicle'), (0.5, 'r-shoulder'))),
	('r-uparm-pt1',			'l', ((0.5, 'r-shoulder'), (0.5, 'r-elbow'))),
	('r-uparm-pt2',			'l', ((0.7, 'r-shoulder'), (0.3, 'r-elbow'))),
	('r-loarm-pt1',			'l', ((0.3, 'r-elbow'), (0.7, 'r-hand'))),
	('r-loarm-pt2',			'l', ((0.7, 'r-elbow'), (0.3, 'r-hand'))),
	('r-upleg-pt1',			'l', ((0.3, 'r-upper-leg'), (0.7, 'r-knee'))),
	('r-upleg-pt2',			'l', ((0.7, 'r-upper-leg'), (0.3, 'r-knee'))),
	('r-loleg-pt1',			'l', ((0.3, 'r-knee'), (0.7, 'r-ankle'))),
	('r-loleg-pt2',			'l', ((0.7, 'r-knee'), (0.3, 'r-ankle'))),

	('mid-feet',			'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
	('Root_head',			'o', ('mid-feet', [0.0, 1.0, 0.0])),
	('Root_tail',			'o', ('mid-feet', [0.0, -1.0, 0.0])),
	('Torso_head',			'o', ('pelvis', [0.0, 0.0, -3.0])),
	('Hips_tail',			'o', ('pelvis', [0.0, -1.5, 0.0])),
	('Hips-inv_head',		'o', ('pelvis', [0.0, -1.5, 0.0])),

	('Eye_R_tail',			'o', ('l-eye', [0.0, 0.0, 0.5])),
	('Eye_L_tail',			'o', ('r-eye', [0.0, 0.0, 0.5])),
	('mid-eyes',			'l', ((0.5, 'l-eye'), (0.5, 'r-eye'))),
	('Gaze_head',			'o', ('mid-eyes', [0.0, 0.0, 5.2])),
	('Gaze_tail',			'o', ('mid-eyes', [0.0, 0.0, 4.2])),
	('Gaze_R_head',			'o', ('l-eye', [0.0, 0.0, 5.0])),
	('Gaze_R_tail',			'o', ('l-eye', [0.0, 0.0, 4.5])),
	('Gaze_L_head',			'o', ('r-eye', [0.0, 0.0, 5.0])),
	('Gaze_L_tail',			'o', ('r-eye', [0.0, 0.0, 4.5])),
	('ElbowIK_L_tail',		'o', ('r-elbow-target', [0.0, 0.0, -0.5])),
	('ElbowIK_R_tail',		'o', ('l-elbow-target', [0.0, 0.0, -0.5])),

	('LegCtrl_L_head',		'o', ('r-ankle', [0.0, -1.0, 0.0])),
	('LegCtrl_L_tail',		'o', ('r-ankle', [0.0, -1.0, -2.0])),
	('Ankle_L_tail',		'o', ('r-ankle', [0.0, 0.0, -1.0])),
	('KneeIK_L_tail',		'o', ('r-knee-target', [0.0, 0.5, 0.5])),

	('LegCtrl_R_head',		'o', ('l-ankle', [0.0, -1.0, 0.0])),
	('LegCtrl_R_tail',		'o', ('l-ankle', [0.0, -1.0, -2.0])),
	('Ankle_R_tail',		'o', ('l-ankle', [0.0, 0.0, -1.0])),
	('KneeIK_R_tail',		'o', ('l-knee-target', [0.0, 0.5, 0.5])),

	('Fingers_R_head',		'o', ('l-finger-3-1', [0.0, 1.0, 0.0])),
	('Fingers_R_tail',		'o', ('l-finger-3-end', [0.0, 1.0, 0.0])),
	('Finger-1-Pole_R_tail',	'o', ('l-finger-1-2', [0.0, 0.3, 0.0])),
	('Finger-2-Pole_R_tail',	'o', ('l-finger-2-2', [0.0, 0.3, 0.0])),
	('Finger-3-Pole_R_tail',	'o', ('l-finger-3-2', [0.0, 0.3, 0.0])),
	('Finger-4-Pole_R_tail',	'o', ('l-finger-4-2', [0.0, 0.3, 0.0])),
	('Finger-5-Pole_R_tail',	'o', ('l-finger-5-2', [0.0, 0.3, 0.0])),
	('Fingers_L_head',		'o', ('r-finger-3-1', [0.0, 1.0, 0.0])),
	('Fingers_L_tail',		'o', ('r-finger-3-end', [0.0, 1.0, 0.0])),
	('Finger-1-Pole_L_tail',	'o', ('r-finger-1-2', [0.0, 0.3, 0.0])),
	('Finger-2-Pole_L_tail',	'o', ('r-finger-2-2', [0.0, 0.3, 0.0])),
	('Finger-3-Pole_L_tail',	'o', ('r-finger-3-2', [0.0, 0.3, 0.0])),
	('Finger-4-Pole_L_tail',	'o', ('r-finger-4-2', [0.0, 0.3, 0.0])),
	('Finger-5-Pole_L_tail',	'o', ('r-finger-5-2', [0.0, 0.3, 0.0])),

	
	('origin',			'o', ('head', [-2.5, 0.5, 0.0])),
	('PFace_tail',			'o', ('origin', [0.0, 0.0, 1.0])),
	('PBrow_R_head',		'o', ('origin', [-0.4, 0.8, 0.0])),
	('PBrow_R_tail',		'o', ('origin', [-0.4, 0.8, 0.3])),
	('PBrow_L_head',		'o', ('origin', [0.4, 0.8, 0.0])),
	('PBrow_L_tail',		'o', ('origin', [0.4, 0.8, 0.3])),
	('PBrows_head',			'o', ('origin', [0.0, 0.8, 0.0])),
	('PBrows_tail',			'o', ('origin', [0.0, 0.8, 0.3])),
	('PUpLid_R_head',		'o', ('origin', [-0.4, 0.6, 0.0])),
	('PUpLid_R_tail',		'o', ('origin', [-0.4, 0.6, 0.3])),
	('PUpLid_L_head',		'o', ('origin', [0.4, 0.6, 0.0])),
	('PUpLid_L_tail',		'o', ('origin', [0.4, 0.6, 0.3])),
	('PLoLid_R_head',		'o', ('origin', [-0.4, 0.2, 0.0])),
	('PLoLid_R_tail',		'o', ('origin', [-0.4, 0.2, 0.3])),
	('PLoLid_L_head',		'o', ('origin', [0.4, 0.2, 0.0])),
	('PLoLid_L_tail',		'o', ('origin', [0.4, 0.2, 0.3])),
	('PCheek_R_head',		'o', ('origin', [-0.4, 0.0, 0.0])),
	('PCheek_R_tail',		'o', ('origin', [-0.4, 0.0, 0.3])),
	('PCheek_L_head',		'o', ('origin', [0.4, 0.0, 0.0])),
	('PCheek_L_tail',		'o', ('origin', [0.4, 0.0, 0.3])),
	('PNose_tail',			'o', ('origin', [0.0, 0.0, 0.3])),
	('PUpLip_head',			'o', ('origin', [0.0, -0.2, 0.0])),
	('PUpLip_tail',			'o', ('origin', [0.0, -0.2, 0.3])),
	('PLoLip_head',			'o', ('origin', [0.0, -0.8, 0.0])),
	('PLoLip_tail',			'o', ('origin', [0.0, -0.8, 0.3])),
	('PMouth_head',			'o', ('origin', [0.0, -0.5, 0.0])),
	('PMouth_tail',			'o', ('origin', [0.0, -0.5, 0.3])),
	('PUpLip_R_head',		'o', ('origin', [-0.2, -0.4, 0.0])),
	('PUpLip_R_tail',		'o', ('origin', [-0.2, -0.4, 0.3])),
	('PUpLip_L_head',		'o', ('origin', [0.2, -0.4, 0.0])),
	('PUpLip_L_tail',		'o', ('origin', [0.2, -0.4, 0.3])),
	('PLoLip_R_head',		'o', ('origin', [-0.2, -0.6, 0.0])),
	('PLoLip_R_tail',		'o', ('origin', [-0.2, -0.6, 0.3])),
	('PLoLip_L_head',		'o', ('origin', [0.2, -0.6, 0.0])),
	('PLoLip_L_tail',		'o', ('origin', [0.2, -0.6, 0.3])),
	('PMouth_R_head',		'o', ('origin', [-0.5, -0.5, 0.0])),
	('PMouth_R_tail',		'o', ('origin', [-0.5, -0.5, 0.3])),
	('PMouth_L_head',		'o', ('origin', [0.5, -0.5, 0.0])),
	('PMouth_L_tail',		'o', ('origin', [0.5, -0.5, 0.3])),
	('PTounge_head',		'o', ('origin', [0.0, -1.0, 0.0])),
	('PTounge_tail',		'o', ('origin', [0.0, -1.0, 0.3])),
	('PJaw_head',			'o', ('origin', [0.0, -1.1, 0.0])),
	('PJaw_tail',			'o', ('origin', [0.0, -1.1, 0.3])),
	('PArmIK_R_head',		'o', ('origin', [-1.1, 2.0, 0.0])),
	('PArmIK_R_tail',		'o', ('origin', [-1.1, 2.0, 0.3])),
	('PArmIK_L_head',		'o', ('origin', [0.1, 2.0, 0.0])),
	('PArmIK_L_tail',		'o', ('origin', [0.1, 2.0, 0.3])),
	('PLegIK_R_head',		'o', ('origin', [-1.1, 1.5, 0.0])),
	('PLegIK_R_tail',		'o', ('origin', [-1.1, 1.5, 0.3])),
	('PLegIK_L_head',		'o', ('origin', [0.1, 1.5, 0.0])),
	('PLegIK_L_tail',		'o', ('origin', [0.1, 1.5, 0.3])),
]

ClassicHeadsTails = [
	('Root',			'Root_head', 'Root_tail'),
	('Torso',			'Torso_head', 'pelvis'),
	('Hips',			'pelvis', 'Hips_tail'),
	('Hips-inv',			'Hips-inv_head', 'pelvis'),
	('Pelvis',			'pelvis', 'spine3'),
	('Spine3',			'spine3', 'spine2'),
	('Spine2',			'spine2', 'spine1'),
	('Spine1',			'spine1', 'neck'),
	('Neck',			'neck', 'head'),
	('Breathe',			'spine1', 'chest-front'),
	('Stomach',			'chest-front', 'pelvis'),

	('Head',			'head', 'head-end'),
	('Head-inv',			'head-end', 'mouth'),
	('Jaw',				'mouth', 'jaw-tip'),
	('ToungeBase',			'tounge-root', 'tounge-mid'),
	('ToungeTip',			'tounge-mid', 'tounge-tip'),
	('Eye_R',			'l-eye', 'Eye_R_tail'),
	('UpLid_R',			'l-eye', 'l-upLid'),
	('LoLid_R',			'l-eye', 'l-loLid'),
	('Eye_L',			'r-eye', 'Eye_L_tail'),
	('UpLid_L',			'r-eye', 'r-upLid'),
	('LoLid_L',			'r-eye', 'r-loLid'),
	('Gaze',			'Gaze_head', 'Gaze_tail'),
	('Gaze_R',			'Gaze_R_head', 'Gaze_R_tail'),
	('Gaze_L',			'Gaze_L_head', 'Gaze_L_tail'),

	('Clavicle_L',			'r-clavicle', 'r-shoulder'),
	('UpArm_L',			'r-shoulder', 'r-elbow'),
	('LoArm_L',			'r-elbow', 'r-hand'),
	('Hand_L',			'r-hand', 'r-finger-3-1'),
	('UpArmTwist_L',		'r-shoulder', 'r-elbow'),
	('LoArmTwist_L',		'r-elbow', 'r-hand'),
	('UpArmFK_L',			'r-shoulder', 'r-elbow'),
	('LoArmFK_L',			'r-elbow', 'r-hand'),
	('HandFK_L',			'r-hand', 'r-finger-3-1'),
	('UpArmIK_L',			'r-shoulder', 'r-elbow'),
	('LoArmIK_L',			'r-elbow', 'r-hand'),
	('HandIK_L',			'r-hand', 'r-finger-3-1'),
	('ElbowIK_L',			'r-elbow-target', 'ElbowIK_L_tail'),

	('Finger-1-1_L',		'r-finger-1-1', 'r-finger-1-2'),
	('Finger-1-2_L',		'r-finger-1-2', 'r-finger-1-3'),
	('Finger-1-3_L',		'r-finger-1-3', 'r-finger-1-end'),
	('Finger-2-1_L',		'r-finger-2-1', 'r-finger-2-2'),
	('Finger-2-2_L',		'r-finger-2-2', 'r-finger-2-3'),
	('Finger-2-3_L',		'r-finger-2-3', 'r-finger-2-end'),
	('Finger-3-1_L',		'r-finger-3-1', 'r-finger-3-2'),
	('Finger-3-2_L',		'r-finger-3-2', 'r-finger-3-3'),
	('Finger-3-3_L',		'r-finger-3-3', 'r-finger-3-end'),
	('Finger-4-1_L',		'r-finger-4-1', 'r-finger-4-2'),
	('Finger-4-2_L',		'r-finger-4-2', 'r-finger-4-3'),
	('Finger-4-3_L',		'r-finger-4-3', 'r-finger-4-end'),
	('Finger-5-1_L',		'r-finger-5-1', 'r-finger-5-2'),
	('Finger-5-2_L',		'r-finger-5-2', 'r-finger-5-3'),
	('Finger-5-3_L',		'r-finger-5-3', 'r-finger-5-end'),

	('Clavicle_R',			'l-clavicle', 'l-shoulder'),
	('UpArm_R',			'l-shoulder', 'l-elbow'),
	('LoArm_R',			'l-elbow', 'l-hand'),
	('Hand_R',			'l-hand', 'l-finger-3-1'),
	('UpArmTwist_R',		'l-shoulder', 'l-elbow'),
	('LoArmTwist_R',		'l-elbow', 'l-hand'),
	('UpArmFK_R',			'l-shoulder', 'l-elbow'),
	('LoArmFK_R',			'l-elbow', 'l-hand'),
	('HandFK_R',			'l-hand', 'l-finger-3-1'),
	('UpArmIK_R',			'l-shoulder', 'l-elbow'),
	('LoArmIK_R',			'l-elbow', 'l-hand'),
	('HandIK_R',			'l-hand', 'l-finger-3-1'),
	('ElbowIK_R',			'l-elbow-target', 'ElbowIK_R_tail'),

	('Finger-1-1_R',		'l-finger-1-1', 'l-finger-1-2'),
	('Finger-1-2_R',		'l-finger-1-2', 'l-finger-1-3'),
	('Finger-1-3_R',		'l-finger-1-3', 'l-finger-1-end'),
	('Finger-2-1_R',		'l-finger-2-1', 'l-finger-2-2'),
	('Finger-2-2_R',		'l-finger-2-2', 'l-finger-2-3'),
	('Finger-2-3_R',		'l-finger-2-3', 'l-finger-2-end'),
	('Finger-3-1_R',		'l-finger-3-1', 'l-finger-3-2'),
	('Finger-3-2_R',		'l-finger-3-2', 'l-finger-3-3'),
	('Finger-3-3_R',		'l-finger-3-3', 'l-finger-3-end'),
	('Finger-4-1_R',		'l-finger-4-1', 'l-finger-4-2'),
	('Finger-4-2_R',		'l-finger-4-2', 'l-finger-4-3'),
	('Finger-4-3_R',		'l-finger-4-3', 'l-finger-4-end'),
	('Finger-5-1_R',		'l-finger-5-1', 'l-finger-5-2'),
	('Finger-5-2_R',		'l-finger-5-2', 'l-finger-5-3'),
	('Finger-5-3_R',		'l-finger-5-3', 'l-finger-5-end'),

	('Hip_L',			'pelvis', 'r-upper-leg'),
	('UpLegTwist_L',		'r-upper-leg', 'r-knee'),
	('UpLeg_L',			'r-upper-leg', 'r-knee'),
	('LoLeg_L',			'r-knee', 'r-ankle'),
	('Foot_L',			'r-ankle', 'r-toe-3-1'),
	('Toe_L',			'r-toe-3-1', 'r-toe-end'),
	('UpLegFK_L',			'r-upper-leg', 'r-knee'),
	('LoLegFK_L',			'r-knee', 'r-ankle'),
	('FootFK_L',			'r-ankle', 'r-toe-3-1'),
	('ToeFK_L',			'r-toe-3-1', 'r-toe-end'),

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

	('Hip_R',			'pelvis', 'l-upper-leg'),
	('UpLegTwist_R',		'l-upper-leg', 'l-knee'),
	('UpLeg_R',			'l-upper-leg', 'l-knee'),
	('LoLeg_R',			'l-knee', 'l-ankle'),
	('Foot_R',			'l-ankle', 'l-toe-3-1'),
	('Toe_R',			'l-toe-3-1', 'l-toe-end'),
	('UpLegFK_R',			'l-upper-leg', 'l-knee'),
	('LoLegFK_R',			'l-knee', 'l-ankle'),
	('FootFK_R',			'l-ankle', 'l-toe-3-1'),
	('ToeFK_R',			'l-toe-3-1', 'l-toe-end'),

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

	('LegCtrl_L',			'LegCtrl_L_head', 'LegCtrl_L_tail'),
	('UpLegIK_L',			'r-upper-leg', 'r-knee'),
	('LoLegIK_L',			'r-knee', 'r-ankle'),
	('FootIK_L',			'r-toe-3-1', 'r-ankle'),
	('ToeIK_L',			'r-toe-3-1', 'r-toe-end'),
	('Ankle_L',			'r-ankle', 'Ankle_L_tail'),
	('KneeIK_L',			'r-knee-target', 'KneeIK_L_tail'),
	('LegCtrl_R',			'LegCtrl_R_head', 'LegCtrl_R_tail'),
	('UpLegIK_R',			'l-upper-leg', 'l-knee'),
	('LoLegIK_R',			'l-knee', 'l-ankle'),
	('FootIK_R',			'l-toe-3-1', 'l-ankle'),
	('ToeIK_R',			'l-toe-3-1', 'l-toe-end'),
	('Ankle_R',			'l-ankle', 'Ankle_R_tail'),
	('KneeIK_R',			'l-knee-target', 'KneeIK_R_tail'),

	('Fingers_R',			'Fingers_R_head', 'Fingers_R_tail'),
	('Finger-1_R',			'l-finger-1-1', 'l-finger-1-end'),
	('Finger-1-IK_R',		'l-finger-1-end', 'l-finger-1-3'),
	('Finger-1-Pole_R',		'l-finger-1-2', 'Finger-1-Pole_R_tail'),
	('Finger-2_R',			'l-finger-2-1', 'l-finger-2-end'),
	('Finger-2-IK_R',		'l-finger-2-end', 'l-finger-2-3'),
	('Finger-2-Pole_R',		'l-finger-2-2', 'Finger-2-Pole_R_tail'),
	('Finger-3_R',			'l-finger-3-1', 'l-finger-3-end'),
	('Finger-3-IK_R',		'l-finger-3-end', 'l-finger-3-3'),
	('Finger-3-Pole_R',		'l-finger-3-2', 'Finger-3-Pole_R_tail'),
	('Finger-4_R',			'l-finger-4-1', 'l-finger-4-end'),
	('Finger-4-IK_R',		'l-finger-4-end', 'l-finger-4-3'),
	('Finger-4-Pole_R',		'l-finger-4-2', 'Finger-4-Pole_R_tail'),
	('Finger-5_R',			'l-finger-5-1', 'l-finger-5-end'),
	('Finger-5-IK_R',		'l-finger-5-end', 'l-finger-5-3'),
	('Finger-5-Pole_R',		'l-finger-5-2', 'Finger-5-Pole_R_tail'),

	('Fingers_L',			'Fingers_L_head', 'Fingers_L_tail'),
	('Finger-1_L',			'r-finger-1-1', 'r-finger-1-end'),
	('Finger-1-IK_L',		'r-finger-1-end', 'r-finger-1-3'),
	('Finger-1-Pole_L',		'r-finger-1-2', 'Finger-1-Pole_L_tail'),
	('Finger-2_L',			'r-finger-2-1', 'r-finger-2-end'),
	('Finger-2-IK_L',		'r-finger-2-end', 'r-finger-2-3'),
	('Finger-2-Pole_L',		'r-finger-2-2', 'Finger-2-Pole_L_tail'),
	('Finger-3_L',			'r-finger-3-1', 'r-finger-3-end'),
	('Finger-3-IK_L',		'r-finger-3-end', 'r-finger-3-3'),
	('Finger-3-Pole_L',		'r-finger-3-2', 'Finger-3-Pole_L_tail'),
	('Finger-4_L',			'r-finger-4-1', 'r-finger-4-end'),
	('Finger-4-IK_L',		'r-finger-4-end', 'r-finger-4-3'),
	('Finger-4-Pole_L',		'r-finger-4-2', 'Finger-4-Pole_L_tail'),
	('Finger-5_L',			'r-finger-5-1', 'r-finger-5-end'),
	('Finger-5-IK_L',		'r-finger-5-end', 'r-finger-5-3'),
	('Finger-5-Pole_L',		'r-finger-5-2', 'Finger-5-Pole_L_tail'),

	('PFace',			'origin', 'PFace_tail'),
	('PBrow_R',			'PBrow_R_head', 'PBrow_R_tail'),
	('PBrow_L',			'PBrow_L_head', 'PBrow_L_tail'),
	('PBrows',			'PBrows_head', 'PBrows_tail'),
	('PUpLid_R',			'PUpLid_R_head', 'PUpLid_R_tail'),
	('PUpLid_L',			'PUpLid_L_head', 'PUpLid_L_tail'),
	('PLoLid_R',			'PLoLid_R_head', 'PLoLid_R_tail'),
	('PLoLid_L',			'PLoLid_L_head', 'PLoLid_L_tail'),
	('PCheek_R',			'PCheek_R_head', 'PCheek_R_tail'),
	('PCheek_L',			'PCheek_L_head', 'PCheek_L_tail'),
	('PNose',			'origin', 'PNose_tail'),
	('PUpLip',			'PUpLip_head', 'PUpLip_tail'),
	('PLoLip',			'PLoLip_head', 'PLoLip_tail'),
	('PMouth',			'PMouth_head', 'PMouth_tail'),
	('PUpLip_R',			'PUpLip_R_head', 'PUpLip_R_tail'),
	('PUpLip_L',			'PUpLip_L_head', 'PUpLip_L_tail'),
	('PLoLip_R',			'PLoLip_R_head', 'PLoLip_R_tail'),
	('PLoLip_L',			'PLoLip_L_head', 'PLoLip_L_tail'),
	('PMouth_R',			'PMouth_R_head', 'PMouth_R_tail'),
	('PMouth_L',			'PMouth_L_head', 'PMouth_L_tail'),
	('PTounge',			'PTounge_head', 'PTounge_tail'),
	('PJaw',			'PJaw_head', 'PJaw_tail'),
	('PArmIK_R',			'PArmIK_R_head', 'PArmIK_R_tail'),
	('PArmIK_L',			'PArmIK_L_head', 'PArmIK_L_tail'),
	('PLegIK_R',			'PLegIK_R_head', 'PLegIK_R_tail'),
	('PLegIK_L',			'PLegIK_L_head', 'PLegIK_L_tail'),
	]

ClassicArmature = [
	('Root',			0.0, None, F_WIR, L_MAIN, (1,1,1) ),
	('Torso',			0.0, 'Root', 0, L_MAIN+L_SKEL, (1,1,1) ),
	('Hips',			-3.14159, 'Torso', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_DEF, (1,1,1) ),
	('Hips-inv',			0.0, 'Hips', F_CON, L_HELP, (1,1,1) ),

	# Left leg
	('Hip_L',			1.62316, 'Hips-inv', F_DEF+F_CON, L_HELP, (1,1,1) ),
	('UpLeg_L',			-3.08923, 'Hip_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoLeg_L',			-3.14159, 'UpLeg_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Foot_L',			-0.488688, 'LoLeg_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Toe_L',			-2.86233, 'Foot_L', F_CON, L_DEF, (1,1,1) ),
	('UpLegTwist_L',		-3.08923, 'Hip_L', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('UpLegFK_L',			-3.08923, 'Hip_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_L',			-3.14159, 'UpLegFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_L',			-0.488688, 'LoLegFK_L', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_L',			-2.86233, 'FootFK_L', F_WIR, L_LEGFK, (1,1,1) ),

	('UpLegIK_L',			-3.08923, 'Hip_L', F_CON, L_HELP, (1,1,1) ),
	('LoLegIK_L',			-3.14159, 'UpLegIK_L', F_CON, L_HELP, (1,1,1) ),
	('KneeIK_L',			0.0, 'Hip_L', F_WIR, L_LEGIK, (1,1,1) ),
	('LegCtrl_L',			-3.14159, 'Root', F_WIR, L_LEGIK, (1,1,1) ),
	('FootIK_L',			-3.08923, 'LegCtrl_L', F_WIR, L_LEGIK, (1,1,1) ),
	('Ankle_L',			-3.14159, 'FootIK_L', 0, L_HELP, (1,1,1) ),
	('ToeIK_L',			-2.86234, 'LegCtrl_L', 0, L_LEGIK, (1,1,1) ),

	# Right leg
	('Hip_R',			-1.62316, 'Hips-inv', F_DEF+F_CON, L_HELP, (1,1,1) ),
	('UpLeg_R',			3.08923, 'Hip_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoLeg_R',			-3.14159, 'UpLeg_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Foot_R',			0.488689, 'LoLeg_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Toe_R',			2.86233, 'Foot_R', F_CON, L_DEF, (1,1,1) ),
	('UpLegTwist_R',		3.08923, 'Hip_R', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('UpLegFK_R',			3.08923, 'Hip_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('LoLegFK_R',			-3.14159, 'UpLegFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('FootFK_R',			0.488689, 'LoLegFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),
	('ToeFK_R',			2.86233, 'FootFK_R', F_CON+F_WIR, L_LEGFK, (1,1,1) ),

	('UpLegIK_R',			3.08923, 'Hip_R', F_CON, L_HELP, (1,1,1) ),
	('LoLegIK_R',			-3.14159, 'UpLegIK_R', F_CON, L_HELP, (1,1,1) ),
	('KneeIK_R',			0.0, 'Hip_R', F_WIR, L_LEGIK, (1,1,1) ),
	('LegCtrl_R',			-3.14159, 'Root', F_WIR, L_LEGIK, (1,1,1) ),
	('FootIK_R',			3.08923, 'LegCtrl_R', F_WIR, L_LEGIK, (1,1,1) ),
	('Ankle_R',			-3.14159, 'FootIK_R', 0, L_HELP, (1,1,1) ),
	('ToeIK_R',			2.86234, 'LegCtrl_R', 0, L_LEGIK, (1,1,1) ),

	# Left toes
	('Toe-1-1_L',			2.42599, 'Toe_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-1-2_L',			2.42596, 'Toe-1-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-2-1_L',			1.79768, 'Toe_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-2-2_L',			-0.506141, 'Toe-2-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-2-3_L',			-0.506141, 'Toe-2-2_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-3-1_L',			2.77507, 'Toe_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-3-2_L',			3.05438, 'Toe-3-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-3-3_L',			3.05438, 'Toe-3-2_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-4-1_L',			-2.82743, 'Toe_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-4-2_L',			3.00198, 'Toe-4-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-4-3_L',			3.00198, 'Toe-4-2_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-5-1_L',			2.79252, 'Toe_L', F_DEF, L_TOE, (1,1,1) ),
	('Toe-5-2_L',			-2.9845, 'Toe-5-1_L', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-5-3_L',			-2.9845, 'Toe-5-2_L', F_DEF+F_CON, L_TOE, (1,1,1) ),

	# Right toes
	('Toe-1-1_R',			-2.42599, 'Toe_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-1-2_R',			-2.42598, 'Toe-1-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-2-1_R',			-1.79768, 'Toe_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-2-2_R',			0.506136, 'Toe-2-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-2-3_R',			0.506138, 'Toe-2-2_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-3-1_R',			-2.77507, 'Toe_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-3-2_R',			-3.05438, 'Toe-3-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-3-3_R',			-3.05439, 'Toe-3-2_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-4-1_R',			2.82743, 'Toe_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-4-2_R',			-3.00197, 'Toe-4-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-4-3_R',			-3.00197, 'Toe-4-2_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-5-1_R',			-2.79252, 'Toe_R', F_DEF, L_TOE, (1,1,1) ),
	('Toe-5-2_R',			2.98449, 'Toe-5-1_R', F_DEF+F_CON, L_TOE, (1,1,1) ),
	('Toe-5-3_R',			2.98449, 'Toe-5-2_R', F_DEF+F_CON, L_TOE, (1,1,1) ),

	# Spinal column
	('Pelvis',			0.0, 'Torso', F_CON, L_HELP, (1,1,1) ),
	('Spine3',			0.0, 'Pelvis', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_DEF, (1,1,1) ),
	('Spine2',			0.0, 'Spine3', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_DEF, (1,1,1) ),
	('Spine1',			0.0, 'Spine2', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_DEF, (1,1,1) ),
	('Breathe',			0.0, 'Spine2', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Stomach',			-3.14159, 'Breathe', F_DEF+F_CON, L_DEF, (1,1,1) ),

	# Face
	('Neck',			0.0, 'Spine1', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_HEAD+L_DEF, (1,1,1) ),
	('Head',			0.0, 'Neck', F_DEF+F_CON+F_WIR, L_MAIN+L_SKEL+L_HEAD+L_DEF, (1,1,1) ),
	('Head-inv',			-3.14159, 'Head', F_CON, L_HELP, (1,1,1) ),
	('Jaw',				0.0, 'Head-inv', F_DEF+F_CON+F_WIR, L_MAIN+L_HEAD+L_DEF, (1,1,1) ),
	('ToungeBase',			0.0, 'Jaw', F_DEF, L_HEAD+L_DEF, (1,1,1) ),
	('ToungeTip',			0.0, 'ToungeBase', F_DEF+F_CON, L_HEAD+L_DEF, (1,1,1) ),
	('Eye_R',			0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('UpLid_R',			0.279253, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('LoLid_R',			0.296705, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('Eye_L',			0.0, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('UpLid_L',			-0.279253, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('LoLid_L',			-0.296705, 'Head', F_DEF, L_DEF, (1,1,1) ),
	('Gaze',			-3.14159, 'Root', 0, L_PANEL+L_HEAD, (1,1,1) ),
	('Gaze_R',			-3.14159, 'Gaze', 0, L_PANEL+L_HEAD, (1,1,1) ),
	('Gaze_L',			-3.14159, 'Gaze', 0, L_PANEL+L_HEAD, (1,1,1) ),

	# Left arm
	('Clavicle_L',			1.91986, 'Spine1', F_DEF+F_WIR, L_ARMFK+L_DEF, (1,1,1) ),
	('UpArm_L',			1.69297, 'Clavicle_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArm_L',			1.58825, 'UpArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hand_L',			1.22173, 'LoArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArmTwist_L',		1.58825, 'UpArm_L', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpArmTwist_L',		1.69297, 'Clavicle_L', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('UpArmFK_L',			1.69297, 'Clavicle_L', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('LoArmFK_L',			1.58825, 'UpArmFK_L', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('HandFK_L',			1.22173, 'LoArmFK_L', F_CON+F_WIR, L_ARMFK+L_HANDFK, (1,1,1) ),

	('UpArmIK_L',			1.69297, 'Clavicle_L', F_CON, L_HELP, (1,1,1) ),
	('LoArmIK_L',			1.58825, 'UpArmIK_L', F_CON, L_HELP, (1,1,1) ),
	('ElbowIK_L',			-2.40855, 'Clavicle_L', F_WIR, L_ARMIK, (1,1,1) ),
	('HandIK_L',			1.22173, 'Root', F_WIR, L_ARMIK, (1,1,1) ),

	# Right arm
	('Clavicle_R',			-1.91986, 'Spine1', F_DEF+F_WIR, L_ARMFK+L_DEF, (1,1,1) ),
	('UpArm_R',			-1.69297, 'Clavicle_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArm_R',			-1.58825, 'UpArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('Hand_R',			-1.22173, 'LoArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('LoArmTwist_R',		-1.58825, 'UpArm_R', F_DEF+F_CON, L_DEF, (1,1,1) ),
	('UpArmTwist_R',		-1.69297, 'Clavicle_R', F_DEF+F_CON, L_DEF, (1,1,1) ),

	('UpArmFK_R',			-1.69297, 'Clavicle_R', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('LoArmFK_R',			-1.58825, 'UpArmFK_R', F_CON+F_WIR, L_ARMFK, (1,1,1) ),
	('HandFK_R',			-1.22173, 'LoArmFK_R', F_CON+F_WIR, L_ARMFK+L_HANDFK, (1,1,1) ),

	('UpArmIK_R',			-1.69297, 'Clavicle_R', F_CON, L_HELP, (1,1,1) ),
	('LoArmIK_R',			-1.58825, 'UpArmIK_R', F_CON, L_HELP, (1,1,1) ),
	('ElbowIK_R',			2.40855, 'Clavicle_R', F_WIR, L_ARMIK, (1,1,1) ),
	('HandIK_R',			-1.22173, 'Root', F_WIR, L_ARMIK+L_HANDIK, (1,1,1) ),

	# Left fingers
	('Finger-1-1_L',		1.71042, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-1-2_L',		1.65806, 'Finger-1-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_L',		1.65806, 'Finger-1-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-1_L',		1.65806, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-2-2_L',		1.62316, 'Finger-2-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-3_L',		1.62316, 'Finger-2-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-1_L',		1.64061, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-3-2_L',		1.62316, 'Finger-3-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-3_L',		1.62316, 'Finger-3-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-1_L',		1.64061, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-4-2_L',		1.62316, 'Finger-4-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-3_L',		1.62316, 'Finger-4-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-1_L',		1.64061, 'Hand_L', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-5-2_L',		1.62316, 'Finger-5-1_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-3_L',		1.62316, 'Finger-5-2_L', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Fingers_L',			1.64061, 'Hand_L', 0, L_HANDIK, (1,1,1) ),

	('Finger-1_L',			1.67551, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-1-IK_L',		-1.6057, 'Finger-1_L', 0, L_HELP, (1,1,1) ),
	('Finger-1-Pole_L',		-0.0698147, 'Finger-1_L', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-2_L',			1.64061, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-2-IK_L',		-1.62316, 'Finger-2_L', 0, L_HELP, (1,1,1) ),
	('Finger-2-Pole_L',		-0.0698144, 'Finger-2_L', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-3_L',			1.64061, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-3-IK_L',		-1.62316, 'Finger-3_L', 0, L_HELP, (1,1,1) ),
	('Finger-3-Pole_L',		-0.0698129, 'Finger-3_L', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-4_L',			1.64061, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-4-IK_L',		-1.62316, 'Finger-4_L', 0, L_HELP, (1,1,1) ),
	('Finger-4-Pole_L',		-0.0698147, 'Finger-4_L', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-5_L',			1.64061, 'Hand_L', 0, L_HANDIK, (1,1,1) ),
	('Finger-5-IK_L',		-1.62316, 'Finger-5_L', 0, L_HELP, (1,1,1) ),
	('Finger-5-Pole_L',		-0.0698135, 'Finger-5_L', F_WIR, L_HANDIK, (1,1,1) ),

	# Right fingers
	('Finger-1-1_R',		-1.71042, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-1-2_R',		-1.65806, 'Finger-1-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-1-3_R',		-1.65806, 'Finger-1-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-1_R',		-1.65806, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-2-2_R',		-1.62316, 'Finger-2-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-2-3_R',		-1.62316, 'Finger-2-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-1_R',		-1.64061, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-3-2_R',		-1.62316, 'Finger-3-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-3-3_R',		-1.62316, 'Finger-3-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-1_R',		-1.64061, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-4-2_R',		-1.62316, 'Finger-4-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-4-3_R',		-1.62316, 'Finger-4-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-1_R',		-1.64061, 'Hand_R', F_DEF, L_HANDFK, (1,1,1) ),
	('Finger-5-2_R',		-1.62316, 'Finger-5-1_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),
	('Finger-5-3_R',		-1.62316, 'Finger-5-2_R', F_DEF+F_CON, L_HANDFK, (1,1,1) ),

	('Fingers_R',			-1.64061, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-1_R',			-1.67551, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-1-IK_R',		1.6057, 'Finger-1_R', 0, L_HELP, (1,1,1) ),
	('Finger-1-Pole_R',		0.0698128, 'Finger-1_R', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-2_R',			-1.64061, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-2-IK_R',		1.62316, 'Finger-2_R', 0, L_HELP, (1,1,1) ),
	('Finger-2-Pole_R',		0.0698129, 'Finger-2_R', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-3_R',			-1.64061, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-3-IK_R',		1.62316, 'Finger-3_R', 0, L_HELP, (1,1,1) ),
	('Finger-3-Pole_R',		0.069813, 'Finger-3_R', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-4_R',			-1.64061, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-4-IK_R',		1.62316, 'Finger-4_R', 0, L_HELP, (1,1,1) ),
	('Finger-4-Pole_R',		0.0698146, 'Finger-4_R', F_WIR, L_HANDIK, (1,1,1) ),
	('Finger-5_R',			-1.64061, 'Hand_R', 0, L_HANDIK, (1,1,1) ),
	('Finger-5-IK_R',		1.62316, 'Finger-5_R', 0, L_HELP, (1,1,1) ),
	('Finger-5-Pole_R',		0.0698135, 'Finger-5_R', F_WIR, L_HANDIK, (1,1,1) ),
]

PanelArmature = [
	('PFace',			-3.14159, None, F_WIR, L_PANEL, (1,1,1) ),
	('PBrow_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PBrow_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PBrows',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLid_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLid_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLid_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLid_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PCheek_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PCheek_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PNose',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PUpLip_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLoLip_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PMouth_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PTounge',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PJaw',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PArmIK_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PArmIK_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLegIK_R',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
	('PLegIK_L',			-3.14159, 'PFace', 0, L_PANEL, (1,1,1) ),
]

def ClassicWritePoses(fp):
	global boneGroups
	boneGroups = {}

	addPoseBone(fp, 'Root', 'MHCircle15', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Torso', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Hips', 'MHCircle15', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Hips-inv', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Hip_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'KneeIK_L', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Hip_L'])])

	addPoseBone(fp, 'Hip_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'KneeIK_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Hip_R'])])

	# Spinal column
	addPoseBone(fp, 'Pelvis', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Spine3', 'MHCircle10', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Spine2', 'MHCircle15', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Spine1', 'MHCircle10', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Breathe', None, None, (0,0,0), (0,0,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Stomach', None, None, (0,0,0), (0,0,0), (1,0,1), (1,1,1), 0,
		[('LimitRot', C_OWNER+0+C_LTRA, ['Const', (0,0, 0,0, 0,0), (1,0,1)]),
		 ('StretchTo', 0, ['Const.001', 'Hips', 'PLANE_Z'])])

	# Face
	addPoseBone(fp, 'Neck', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Head', 'MHCircle10', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Head-inv', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Jaw', 'MHJaw', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ToungeBase', None, None, (0,0,0), (0,0,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ToungeTip', None, None, (0,0,0), (0,0,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpLid_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoLid_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpLid_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoLid_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Gaze', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Gaze_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Eye_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['Gaze_R', 1, None, (True, False)])])

	addPoseBone(fp, 'Gaze_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Eye_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['Gaze_L', 1, None, (True, False)])])

	# Left arm
	addPoseBone(fp, 'Clavicle_L', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpArmTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['LoArm_L', 1, None, (True, False)])])

	addPoseBone(fp, 'LoArmTwist_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['Hand_L', 1, None, (True, False)])])

	addPoseBone(fp, 'ElbowIK_L', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Clavicle_L'])])

	addPoseBone(fp, 'HandIK_L', 'MHHandCtrl_L', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Clavicle_L'])])

	addPoseBone(fp, 'UpArmIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['ElbowIK_L', 1, None, (True, False)])])

	addPoseBone(fp, 'LoArmIK_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['HandIK_L', 2, None, (True, False)])])

	addPoseBone(fp, 'UpArmFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoArmFK_L', 'MHCircle025', None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'HandFK_L', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpArm_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'UpArmIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'UpArmFK_L', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'LoArm_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'LoArmIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'LoArmFK_L', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'Hand_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'HandIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'HandFK_L', 0, (1,1,1), (0,0,0)])])

	# Right arm
	addPoseBone(fp, 'Clavicle_R', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpArmTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['LoArm_R', 1, None, (True, False)])])

	addPoseBone(fp, 'LoArmTwist_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['Hand_R', 1, None, (True, False)])])

	addPoseBone(fp, 'ElbowIK_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Clavicle_R'])])

	addPoseBone(fp, 'HandIK_R', 'MHHandCtrl_R', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Clavicle_R'])])

	addPoseBone(fp, 'UpArmIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['ElbowIK_R', 1, None, (True, False)])])

	addPoseBone(fp, 'LoArmIK_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['HandIK_R', 2, None, (True, False)])])

	addPoseBone(fp, 'UpArmFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoArmFK_R', 'MHCircle025', None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'HandFK_R', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpArm_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'UpArmIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'UpArmFK_R', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'LoArm_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'LoArmIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'LoArmFK_R', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'Hand_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'HandIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'HandFK_R', 0, (1,1,1), (0,0,0)])])

	# Left fingers
	addPoseBone(fp, 'Fingers_L', None, None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-1_L', None, None, (0,0,0), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-1-IK_L', None, None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-1-Pole_L', 'MHBall', None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-1-1_L', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-1-Pole_L', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-1-2_L', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-1-3_L', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-1-IK_L', 3, None, (True, False)])])

	addPoseBone(fp, 'Finger-2_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-2-IK_L', None, None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-2-Pole_L', 'MHBall', None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-2-1_L', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-2-Pole_L', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-2-2_L', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-2-3_L', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-2-IK_L', 3, None, (True, False)])])

	addPoseBone(fp, 'Finger-3_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-3-IK_L', None, None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-3-Pole_L', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-3-1_L', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-3-Pole_L', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-3-2_L', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-3-3_L', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-3-IK_L', 3, None, (True, False)])])

	addPoseBone(fp, 'Finger-4_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-4-IK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-4-Pole_L', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-4-1_L', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-4-Pole_L', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-4-2_L', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-4-3_L', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-4-IK_L', 3, None, (True, False)])])

	addPoseBone(fp, 'Finger-5_L', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-5-IK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-5-Pole_L', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-5-1_L', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-5-Pole_L', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-5-2_L', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-5-3_L', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-5-IK_L', 3, None, (True, False)])])

	# Right fingers
	addPoseBone(fp, 'Fingers_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-1_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-1-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-1-Pole_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-1-1_R', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-1-Pole_R', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-1-2_R', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-1-3_R', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-1-IK_R', 3, None, (True, False)])])

	addPoseBone(fp, 'Finger-2_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-2-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-2-Pole_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-2-1_R', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-2-Pole_R', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-2-2_R', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-2-3_R', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-2-IK_R', 3, None, (True, False)])])

	addPoseBone(fp, 'Finger-3_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-3-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-3-Pole_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-3-1_R', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-3-Pole_R', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-3-2_R', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-3-3_R', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-3-IK_R', 3, None, (True, False)])])

	addPoseBone(fp, 'Finger-4_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-4-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-4-Pole_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-4-1_R', 'MHCircle05', None, (1,1,1), (0,1,0), (1,1,1), (1,0,1), 0,
		[('IK', 0, ['Finger-4-Pole_R', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-4-2_R', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-4-3_R', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-4-IK_R', 3, None, (True, False)])])

	addPoseBone(fp, 'Finger-5_R', None, None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-5-IK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-5-Pole_R', 'MHBall', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Finger-5-1_R', 'MHCircle05', None, (1,1,1), (0,1,0), (1,0,1), (1,1,1), 0,
		[('IK', 0, ['Finger-5-Pole_R', 1, None, (True, False)])])

	addPoseBone(fp, 'Finger-5-2_R', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0, [])

	addPoseBone(fp, 'Finger-5-3_R', 'MHCircle05', None, (0,0,0), (1,1,0), (1,1,1), (0,0,1), 0,
		[('IK', 0, ['Finger-5-IK_R', 3, None, (True, False)])])


	# Left leg
	addPoseBone(fp, 'LegCtrl_L', 'MHFootCtrl_L', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Hip_L'])])

	addPoseBone(fp, 'UpLegTwist_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['LoLeg_L', 1, None, (True, False)])])


	addPoseBone(fp, 'FootIK_L', 'MHFoot', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Ankle_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpLegIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['KneeIK_L', 1, None, (True, False)])])

	addPoseBone(fp, 'LoLegIK_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['Ankle_L', 2, None, (True, False)])])

	addPoseBone(fp, 'ToeIK_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])


	addPoseBone(fp, 'UpLegFK_L', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoLegFK_L', 'MHCircle025', None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'FootFK_L', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ToeFK_L', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])


	addPoseBone(fp, 'UpLeg_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'UpLegIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'UpLegFK_L', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'LoLeg_L', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'LoLegIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'LoLegFK_L', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'Foot_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['ToeIK_L', 1, None, (True, False)]),
		('CopyRot', 0, ['CopyRotFK', 'FootFK_L', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'Toe_L', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'ToeIK_L', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'ToeFK_L', 0, (1,1,1), (0,0,0)])])


	# Right leg
	addPoseBone(fp, 'LegCtrl_R', 'MHFootCtrl_R', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('LimitDist', 0, ['Const', 'Hip_R'])])

	addPoseBone(fp, 'UpLegTwist_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['LoLeg_R', 1, None, (True, False)])])


	addPoseBone(fp, 'FootIK_R', 'MHFoot', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'Ankle_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'UpLegIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['KneeIK_R', 1, None, (True, False)])])

	addPoseBone(fp, 'LoLegIK_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['Ankle_R', 2, None, (True, False)])])

	addPoseBone(fp, 'ToeIK_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])


	addPoseBone(fp, 'UpLegFK_R', 'MHCircle025', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'LoLegFK_R', 'MHCircle025', None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'FootFK_R', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'ToeFK_R', 'MHCircle05', None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])


	addPoseBone(fp, 'UpLeg_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'UpLegIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'UpLegFK_R', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'LoLeg_R', None, None, (0,0,0), (0,0,1), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'LoLegIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'LoLegFK_R', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'Foot_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('IK', 0, ['ToeIK_R', 1, None, (True, False)]),
		('CopyRot', 0, ['CopyRotFK', 'FootFK_R', 0, (1,1,1), (0,0,0)])])

	addPoseBone(fp, 'Toe_R', None, None, (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
		[('CopyRot', 0, ['CopyRotIK', 'ToeIK_R', 1, (1,1,1), (0,0,0)]),
		('CopyRot', 0, ['CopyRotFK', 'ToeFK_R', 0, (1,1,1), (0,0,0)])])


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

	addPanelPoseBones(fp)
	return

#
#	addPanelPoseBones(fp):
#

def addPanelPoseBones(fp):
	addPoseBone(fp, 'PFace', 'MHFace', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, [])

	addPoseBone(fp, 'PBrow_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PBrow_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PBrows', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PUpLid_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PUpLid_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PLoLid_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PLoLid_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PCheek_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PCheek_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PNose', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PUpLip', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PLoLip', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PMouth', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PUpLip_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PUpLip_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PLoLip_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PLoLip_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PMouth_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PMouth_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PTounge', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PJaw', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp, 'PArmIK_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER+0+C_LTRA, ['Const', (0,1, 0,0, 0,0), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'PArmIK_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER+0+C_LTRA, ['Const', (0,1, 0,0, 0,0), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'PLegIK_R', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER+0+C_LTRA, ['Const', (0,1, 0,0, 0,0), (1,1,1,1,1,1)])])

	addPoseBone(fp, 'PLegIK_L', None, None, (0,1,0), (1,1,1), (1,1,1), (1,1,1), 0,
		[('LimitLoc', C_OWNER+0+C_LTRA, ['Const', (0,1, 0,0, 0,0), (1,1,1,1,1,1)])])

	return


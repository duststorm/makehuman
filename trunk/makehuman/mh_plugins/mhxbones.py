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
Definition of bones for creation of a rig within MakeHuman.

TO DO

"""

__docformat__ = 'restructuredtext'

import aljabr
from aljabr import *

#
#	Flags
#

F_CON = 	0x01
F_NODEF	= 	0x02

#
#	Bone layers
#

L_DEFORM =	0x0001
L_TORSO = 	0x0002
L_ARMIK =	0x0004
L_ARMFK =	0x0008
L_LEGIK =	0x0010
L_LEGFK =	0x0020
L_HANDIK =	0x0040
L_HANDFK =	0x0080

L_ROOT	=	0x0100
L_TOE =		0x0200
L_HEAD =	0x0400

L_HELP	=	0x8000

#
#	List of joints
#	Those are the diamonds in the MH mesh
#

joints = [
	"pelvis",
	"spine3",
	"spine2",
	"spine1",
	"neck",
	"head",
	"mouth",
	"l-eye",
	"r-eye",
	"r-clavicle",
	"r-shoulder",
	"r-elbow",
	"r-hand",
	"r-finger-1-1",
	"r-finger-1-2",
	"r-finger-1-3",
	"r-finger-2-1",
	"r-finger-2-2",
	"r-finger-2-3",
	"r-finger-3-1",
	"r-finger-3-2",
	"r-finger-3-3",
	"r-finger-4-1",
	"r-finger-4-2",
	"r-finger-4-3",
	"r-finger-5-1",
	"r-finger-5-2",
	"r-finger-5-3",
	"l-clavicle",
	"l-shoulder",
	"l-elbow",
	"l-hand",
	"l-finger-1-1",
	"l-finger-1-2",
	"l-finger-1-3",
	"l-finger-2-1",
	"l-finger-2-2",
	"l-finger-2-3",
	"l-finger-3-1",
	"l-finger-3-2",
	"l-finger-3-3",
	"l-finger-4-1",
	"l-finger-4-2",
	"l-finger-4-3",
	"l-finger-5-1",
	"l-finger-5-2",
	"l-finger-5-3",
	"r-upper-leg",
	"r-knee",
	"r-ankle",
	"r-toe-1-1",
	"r-toe-1-2",
	"r-toe-2-1",
	"r-toe-2-2",
	"r-toe-2-3",
	"r-toe-3-1",
	"r-toe-3-2",
	"r-toe-3-3",
	"r-toe-4-1",
	"r-toe-4-2",
	"r-toe-4-3",
	"r-toe-5-1",
	"r-toe-5-2",
	"r-toe-5-3",
	"l-upper-leg",
	"l-knee",
	"l-ankle",
	"l-toe-1-1",
	"l-toe-1-2",
	"l-toe-2-1",
	"l-toe-2-2",
	"l-toe-2-3",
	"l-toe-3-1",
	"l-toe-3-2",
	"l-toe-3-3",
	"l-toe-4-1",
	"l-toe-4-2",
	"l-toe-4-3",
	"l-toe-5-1",
	"l-toe-5-2",
	"l-toe-5-3",
]

#
#	Other locations which can be deduced from the location of the joints
#	( location, tail, head, factor)
#	location = tail + factor*(head-tail)
#
otherLocations = [
	( "head-end", "neck", "head", 1.0),
	( "mouth-end", "head", "mouth", 2.0),
	( "l-finger-1-end", "l-finger-1-2", "l-finger-1-3", 1.0 ),
	( "l-finger-2-end", "l-finger-2-2", "l-finger-2-3", 1.0 ),
	( "l-finger-3-end", "l-finger-3-2", "l-finger-3-3", 1.0 ),
	( "l-finger-4-end", "l-finger-4-2", "l-finger-4-3", 1.0 ),
	( "l-finger-5-end", "l-finger-5-2", "l-finger-5-3", 1.0 ),

	( "r-finger-1-end", "r-finger-1-2", "r-finger-1-3", 1.0 ),
	( "r-finger-2-end", "r-finger-2-2", "r-finger-2-3", 1.0 ),
	( "r-finger-3-end", "r-finger-3-2", "r-finger-3-3", 1.0 ),
	( "r-finger-4-end", "r-finger-4-2", "r-finger-4-3", 1.0 ),
	( "r-finger-5-end", "r-finger-5-2", "r-finger-5-3", 1.0 ),

	( "l-toe-1-end", "l-toe-1-1", "l-toe-1-2", 1.0 ),
	( "l-toe-2-end", "l-toe-2-2", "l-toe-2-3", 1.0 ),
	( "l-toe-3-end", "l-toe-3-2", "l-toe-3-3", 1.0 ),
	( "l-toe-4-end", "l-toe-4-2", "l-toe-4-3", 1.0 ),
	( "l-toe-5-end", "l-toe-5-2", "l-toe-5-3", 1.0 ),

	( "r-toe-1-end", "r-toe-1-1", "r-toe-1-2", 1.0 ),
	( "r-toe-2-end", "r-toe-2-2", "r-toe-2-3", 1.0 ),
	( "r-toe-3-end", "r-toe-3-2", "r-toe-3-3", 1.0 ),
	( "r-toe-4-end", "r-toe-4-2", "r-toe-4-3", 1.0 ),
	( "r-toe-5-end", "r-toe-5-2", "r-toe-5-3", 1.0 ),

	( "r-toe-end", "r-toe-3-1", "r-toe-3-3", 1.0 ),
	( "l-toe-end", "l-toe-3-1", "l-toe-3-3", 1.0 ),

	( "l-knee-target", "l-upper-leg", "l-knee", 0.2 ),
	( "l-elbow-target","l-shoulder",  "l-elbow", 0.2 ),
	( "r-knee-target", "r-upper-leg", "r-knee", 0.2 ),
	( "r-elbow-target", "r-shoulder", "r-elbow", 0.2 ),
]

#
#	The midpoints between two locations
#
midLocations = [
	( "eyes", "l-eye", "r-eye" ),
]


#
#	Definition of armature
#	
#	(Bone, parent, head, headOffset, tail, tailOffset, flags, layers, object)
#
#	Switching left and right compare to the MH joints
#

armature = [
	("Root", "None", "pelvis", [0,-5,0], "pelvis", [0,-5,-3], F_NODEF, L_ROOT, "None"),
	("Torso", "Root", "pelvis", [0,0,-3], "pelvis", 0, F_NODEF, L_TORSO, "None"),

	("Pelvis", "Torso", "pelvis", 0, "spine3", 0, F_CON, L_DEFORM+L_TORSO, "None"),
	("Spine3", "Pelvis", "spine3", 0, "spine2", 0, F_CON, L_DEFORM+L_TORSO, "MHCircle10"),
	("Spine2", "Spine3", "spine2", 0, "spine1", 0, F_CON, L_DEFORM+L_TORSO, "MHCircle15"),
	("Spine1", "Spine2", "spine1", 0, "neck", 0, F_CON, L_DEFORM+L_TORSO, "MHCircle10"),
	("Neck", "Spine1", "neck", 0, "head", 0, F_CON, L_DEFORM+L_TORSO+L_HEAD, "MHCircle05"),

	("Head", "Neck", "head", 0, "head-end", 0, F_CON, L_DEFORM+L_TORSO+L_HEAD, "MHCircle10"),
	("Head-inv", "Head", "head-end", 0, "mouth", 0, F_CON+F_NODEF, L_HELP, "None"),
	("Mouth", "Head-inv", "mouth", 0, "mouth-end", 0, F_CON, L_DEFORM+L_HEAD, "None"),
	("Eye_R", "Head", "l-eye", 0, "l-eye", [0,0,0.5], 0, L_DEFORM, "None"),
	("Eye_L", "Head", "r-eye", 0, "r-eye", [0,0,0.5], 0, L_DEFORM, "None"),
	("Gaze", "Root", "eyes", [0,0,5.25], "eyes", [0,0,4.25], F_NODEF, L_HEAD, "None"),
	("Gaze_R", "Gaze", "l-eye", [0,0,5], "l-eye", [0,0,4.5], F_NODEF, L_HEAD, "None"),
	("Gaze_L", "Gaze", "r-eye", [0,0,5], "r-eye", [0,0,4.5], F_NODEF, L_HEAD, "None"),

	("Clavicle_L", "Spine1", "r-clavicle", 0, "r-shoulder", 0, F_CON, L_DEFORM+L_ARMFK, "MHCircle05"),
	("UpArm_L", "Clavicle_L", "r-shoulder", 0, "r-elbow", 0, F_CON, L_DEFORM+L_ARMFK, "MHCircle03"),
	("LoArm_L", "UpArm_L", "r-elbow", 0, "r-hand", 0, F_CON, L_DEFORM+L_ARMFK, "MHCircle03"),
	("Hand_L", "LoArm_L", "r-hand", 0, "r-finger-3-1", 0, F_CON, L_DEFORM+L_ARMFK+L_HANDFK, "MHCircle05"),
	("Finger-1-1_L", "Hand_L", "r-finger-1-1", 0, "r-finger-1-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-1-2_L", "Finger-1-1_L", "r-finger-1-2", 0, "r-finger-1-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-1-3_L", "Finger-1-2_L", "r-finger-1-3", 0, "r-finger-1-end", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-2-1_L", "Hand_L", "r-finger-2-1", 0, "r-finger-2-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-2-2_L", "Finger-2-1_L", "r-finger-2-2", 0, "r-finger-2-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-2-3_L", "Finger-2-2_L", "r-finger-2-3", 0, "r-finger-2-end", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-3-1_L", "Hand_L", "r-finger-3-1", 0, "r-finger-3-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-3-2_L", "Finger-3-1_L", "r-finger-3-2", 0, "r-finger-3-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-3-3_L", "Finger-3-2_L", "r-finger-3-3", 0, "r-finger-3-end", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-4-1_L", "Hand_L", "r-finger-4-1", 0, "r-finger-4-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-4-2_L", "Finger-4-1_L", "r-finger-4-2", 0, "r-finger-4-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-4-3_L", "Finger-4-2_L", "r-finger-4-3", 0, "r-finger-4-end", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-5-1_L", "Hand_L", "r-finger-5-1", 0, "r-finger-5-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-5-2_L", "Finger-5-1_L", "r-finger-5-2", 0, "r-finger-5-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-5-3_L", "Finger-5-2_L", "r-finger-5-3", 0, "r-finger-5-end", 0, F_CON, L_HANDFK, "MHCircle05"),

	("Clavicle_R", "Spine1", "l-clavicle", 0, "l-shoulder", 0, F_CON, L_DEFORM+L_ARMFK, "MHCircle05"),
	("UpArm_R", "Clavicle_R", "l-shoulder", 0, "l-elbow", 0, F_CON, L_DEFORM+L_ARMFK, "MHCircle03"),
	("LoArm_R", "UpArm_R", "l-elbow", 0, "l-hand", 0, F_CON, L_DEFORM+L_ARMFK, "MHCircle03"),
	("Hand_R", "LoArm_R", "l-hand", 0, "l-finger-3-1", 0, F_CON, L_DEFORM+L_ARMFK+L_HANDFK, "MHCircle05"),
	("Finger-1-1_R", "Hand_R", "l-finger-1-1", 0, "l-finger-1-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-1-2_R", "Finger-1-1_R", "l-finger-1-2", 0, "l-finger-1-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-1-3_R", "Finger-1-2_R", "l-finger-1-3", 0, "l-finger-1-end", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-2-1_R", "Hand_R", "l-finger-2-1", 0, "l-finger-2-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-2-2_R", "Finger-2-1_R", "l-finger-2-2", 0, "l-finger-2-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-2-3_R", "Finger-2-2_R", "l-finger-2-3", 0, "l-finger-2-end", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-3-1_R", "Hand_R", "l-finger-3-1", 0, "l-finger-3-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-3-2_R", "Finger-3-1_R", "l-finger-3-2", 0, "l-finger-3-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-3-3_R", "Finger-3-2_R", "l-finger-3-3", 0, "l-finger-3-end", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-4-1_R", "Hand_R", "l-finger-4-1", 0, "l-finger-4-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-4-2_R", "Finger-4-1_R", "l-finger-4-2", 0, "l-finger-4-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-4-3_R", "Finger-4-2_R", "l-finger-4-3", 0, "l-finger-4-end", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-5-1_R", "Hand_R", "l-finger-5-1", 0, "l-finger-5-2", 0, 0, L_HANDFK, "MHCircle05"),
	("Finger-5-2_R", "Finger-5-1_R", "l-finger-5-2", 0, "l-finger-5-3", 0, F_CON, L_HANDFK, "MHCircle05"),
	("Finger-5-3_R", "Finger-5-2_R", "l-finger-5-3", 0, "l-finger-5-end", 0, F_CON, L_HANDFK, "MHCircle05"),

	("Hip_L", "Torso", "pelvis", 0, "r-upper-leg", 0, F_CON, L_DEFORM+L_LEGFK, "None"),
	("UpLeg_L", "Hip_L", "r-upper-leg", 0, "r-knee", 0, F_CON, L_DEFORM+L_LEGFK, "MHCircle03"),
	("LoLeg_L", "UpLeg_L", "r-knee", 0, "r-ankle", 0, F_CON, L_DEFORM+L_LEGFK, "MHCircle03"),
	("Foot_L", "LoLeg_L", "r-ankle", 0, "r-toe-3-1", 0, F_CON, L_DEFORM+L_LEGFK, "MHCircle03"),
	("Toe_L", "Foot_L", "r-toe-3-1", 0, "r-toe-end", 0, F_CON+F_NODEF, L_DEFORM+L_LEGFK, "MHCircle05"),
	("Toe-1-1_L", "Toe_L", "r-toe-1-1", 0, "r-toe-1-2", 0, 0, L_TOE, "None"),
	("Toe-1-2_L", "Toe-1-1_L", "r-toe-1-2", 0, "r-toe-1-end", 0, F_CON, L_TOE, "None"),
	("Toe-2-1_L", "Toe_L", "r-toe-2-1", 0, "r-toe-2-2", 0, 0, L_TOE, "None"),
	("Toe-2-2_L", "Toe-2-1_L", "r-toe-2-2", 0, "r-toe-2-3", 0, F_CON, L_TOE, "None"),
	("Toe-2-3_L", "Toe-2-2_L", "r-toe-2-3", 0, "r-toe-2-end", 0, F_CON, L_TOE, "None"),
	("Toe-3-1_L", "Toe_L", "r-toe-3-1", 0, "r-toe-3-2", 0, 0, L_TOE, "None"),
	("Toe-3-2_L", "Toe-3-1_L", "r-toe-3-2", 0, "r-toe-3-3", 0, F_CON, L_TOE, "None"),
	("Toe-3-3_L", "Toe-3-2_L", "r-toe-3-3", 0, "r-toe-3-end", 0, F_CON, L_TOE, "None"),
	("Toe-4-1_L", "Toe_L", "r-toe-4-1", 0, "r-toe-4-2", 0, 0, L_TOE, "None"),
	("Toe-4-2_L", "Toe-4-1_L", "r-toe-4-2", 0, "r-toe-4-3", 0, F_CON, L_TOE, "None"),
	("Toe-4-3_L", "Toe-4-2_L", "r-toe-4-3", 0, "r-toe-4-end", 0, F_CON, L_TOE, "None"),
	("Toe-5-1_L", "Toe_L", "r-toe-5-1", 0, "r-toe-5-2", 0, 0, L_TOE, "None"),
	("Toe-5-2_L", "Toe-5-1_L", "r-toe-5-2", 0, "r-toe-5-3", 0, F_CON, L_TOE, "None"),
	("Toe-5-3_L", "Toe-5-2_L", "r-toe-5-3", 0, "r-toe-5-end", 0, F_CON, L_TOE, "None"),

	("Hip_R", "Torso", "pelvis", 0, "l-upper-leg", 0, F_CON, L_DEFORM+L_LEGFK, "None"),
	("UpLeg_R", "Hip_R", "l-upper-leg", 0, "l-knee", 0, F_CON, L_DEFORM+L_LEGFK, "MHCircle03"),
	("LoLeg_R", "UpLeg_R", "l-knee", 0, "l-ankle", 0, F_CON, L_DEFORM+L_LEGFK, "MHCircle03"),
	("Foot_R", "LoLeg_R", "l-ankle", 0, "l-toe-3-1", 0, F_CON, L_DEFORM+L_LEGFK, "MHCircle03"),
	("Toe_R", "Foot_R", "l-toe-3-1", 0, "l-toe-end", 0, F_CON+F_NODEF, L_DEFORM+L_LEGFK, "MHCircle05"),
	("Toe-1-1_R", "Toe_R", "l-toe-1-1", 0, "l-toe-1-2", 0, 0, L_TOE, "None"),
	("Toe-1-2_R", "Toe-1-1_R", "l-toe-1-2", 0, "l-toe-1-end", 0, F_CON, L_TOE, "None"),
	("Toe-2-1_R", "Toe_R", "l-toe-2-1", 0, "l-toe-2-2", 0, 0, L_TOE, "None"),
	("Toe-2-2_R", "Toe-2-1_R", "l-toe-2-2", 0, "l-toe-2-3", 0, F_CON, L_TOE, "None"),
	("Toe-2-3_R", "Toe-2-2_R", "l-toe-2-3", 0, "l-toe-2-end", 0, F_CON, L_TOE, "None"),
	("Toe-3-1_R", "Toe_R", "l-toe-3-1", 0, "l-toe-3-2", 0, 0, L_TOE, "None"),
	("Toe-3-2_R", "Toe-3-1_R", "l-toe-3-2", 0, "l-toe-3-3", 0, F_CON, L_TOE, "None"),
	("Toe-3-3_R", "Toe-3-2_R", "l-toe-3-3", 0, "l-toe-3-end", 0, F_CON, L_TOE, "None"),
	("Toe-4-1_R", "Toe_R", "l-toe-4-1", 0, "l-toe-4-2", 0, 0, L_TOE, "None"),
	("Toe-4-2_R", "Toe-4-1_R", "l-toe-4-2", 0, "l-toe-4-3", 0, F_CON, L_TOE, "None"),
	("Toe-4-3_R", "Toe-4-2_R", "l-toe-4-3", 0, "l-toe-4-end", 0, F_CON, L_TOE, "None"),
	("Toe-5-1_R", "Toe_R", "l-toe-5-1", 0, "l-toe-5-2", 0, 0, L_TOE, "None"),
	("Toe-5-2_R", "Toe-5-1_R", "l-toe-5-2", 0, "l-toe-5-3", 0, F_CON, L_TOE, "None"),
	("Toe-5-3_R", "Toe-5-2_R", "l-toe-5-3", 0, "l-toe-5-end", 0, F_CON, L_TOE, "None"),

	("LegCtrl_L", "Root", "r-ankle", [0,-1,0], "r-ankle", [0,-1,-2], F_NODEF, L_LEGIK, "None"),
	("FootIK_L", "LegCtrl_L", "r-toe-3-1", 0, "r-ankle", 0, F_NODEF, L_LEGIK, "MHCircle03"),
	("ToeIK_L", "LegCtrl_L",  "r-toe-3-1", 0,  "r-toe-end", 0, F_NODEF, L_LEGIK, "MHCircle05"),
	("Ankle_L", "FootIK_L", "r-ankle", 0, "r-ankle", [0,0,-1], F_NODEF, L_HELP, "None"),
	("KneeIK_L", "Hip_L", "r-knee-target", 0, "r-knee-target", [0,0.5,0.5], F_NODEF, L_LEGIK, "MHBall"),

	("LegCtrl_R", "Root", "l-ankle", [0,-1,0], "l-ankle", [0,-1,-2], F_NODEF, L_LEGIK, "None"),
	("FootIK_R", "LegCtrl_R", "l-toe-3-1", 0, "l-ankle", 0, F_NODEF, L_LEGIK, "MHCircle03"),
	("ToeIK_R", "LegCtrl_R",  "l-toe-3-1", 0,  "l-toe-end", 0, F_NODEF, L_LEGIK, "MHCircle05"),
	("Ankle_R", "FootIK_R", "l-ankle", 0, "l-ankle", [0,0,-1], F_NODEF, L_HELP, "None"),
	("KneeIK_R", "Hip_R", "l-knee-target", 0, "l-knee-target", [0,0.5,0.5], F_NODEF, L_LEGIK, "MHBall"),


	("HandIK_L", "Root", "r-hand", 0, "r-finger-3-1", 0, F_NODEF, L_ARMIK+L_HANDIK, "MHCircle05"),
	("ElbowIK_L", "Clavicle_L", "r-elbow-target", 0, "r-elbow-target", [0,0,-0.5], F_NODEF, L_ARMIK, "MHBall"),

	("HandIK_R", "Root", "l-hand", 0, "l-finger-3-1", 0, F_NODEF, L_ARMIK+L_HANDIK, "MHCircle05"),
	("ElbowIK_R", "Clavicle_R", "l-elbow-target", 0, "l-elbow-target", [0,0,-0.5], F_NODEF, L_ARMIK, "MHBall"),

	("Finger-1_R", "Hand_R", "l-finger-1-1", 0, "l-finger-1-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-1-IK_R", "Finger-1_R", "l-finger-1-end", 0, "l-finger-1-3", 0, F_NODEF, L_HELP, "None"),
	("Finger-2_R", "Hand_R", "l-finger-2-1", 0, "l-finger-2-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-2-IK_R", "Finger-2_R", "l-finger-2-end", 0, "l-finger-2-3", 0, F_NODEF, L_HELP, "None"),
	("Finger-3_R", "Hand_R", "l-finger-3-1", 0, "l-finger-3-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-3-IK_R", "Finger-3_R", "l-finger-3-end", 0, "l-finger-3-3", 0, F_NODEF, L_HELP, "None"),
	("Finger-4_R", "Hand_R", "l-finger-4-1", 0, "l-finger-4-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-4-IK_R", "Finger-4_R", "l-finger-4-end", 0, "l-finger-4-3", 0, F_NODEF, L_HELP, "None"),
	("Finger-5_R", "Hand_R", "l-finger-5-1", 0, "l-finger-5-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-5-IK_R", "Finger-5_R", "l-finger-5-end", 0, "l-finger-5-3", 0, F_NODEF, L_HELP, "None"),

	("Finger-1_L", "Hand_L", "r-finger-1-1", 0, "r-finger-1-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-1-IK_L", "Finger-1_L", "r-finger-1-end", 0, "r-finger-1-3", 0, F_NODEF, L_HELP, "None"),
	("Finger-2_L", "Hand_L", "r-finger-2-1", 0, "r-finger-2-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-2-IK_L", "Finger-2_L", "r-finger-2-end", 0, "r-finger-2-3", 0, F_NODEF, L_HELP, "None"),
	("Finger-3_L", "Hand_L", "r-finger-3-1", 0, "r-finger-3-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-3-IK_L", "Finger-3_L", "r-finger-3-end", 0, "r-finger-3-3", 0, F_NODEF, L_HELP, "None"),
	("Finger-4_L", "Hand_L", "r-finger-4-1", 0, "r-finger-4-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-4-IK_L", "Finger-4_L", "r-finger-4-end", 0, "r-finger-4-3", 0, F_NODEF, L_HELP, "None"),
	("Finger-5_L", "Hand_L", "r-finger-5-1", 0, "r-finger-5-end", 0, F_NODEF, L_HANDIK, "None"),
	("Finger-5-IK_L", "Finger-5_L", "r-finger-5-end", 0, "r-finger-5-3", 0, F_NODEF, L_HELP, "None"),

	# IK/FK switch bones. Does not work properly
	# ("ArmIK-switch", "Root", "head-end", [0,1,0], "head-end", [0,1,-1], F_NODEF, L_ROOT),
	# ("LegIK-switch", "Root", "head-end", [0,1.5,0], "head-end", [0,1.5,-1], F_NODEF, L_ROOT),
	# ("FingerIK-switch", "Root", "head-end", [0,2,0], "head-end", [0,2,-1], F_NODEF, L_ROOT),
	# ("Gaze-switch", "Root", "head-end", [0,2.5,0], "head-end", [0,2.5,-1], F_NODEF, L_ROOT),
]




#
#	Definition of constraints
#
#	( Bone, type, target, driver, arg1, arg2 )
#
#	The driver will be a bone that drives the influence, but presently is a flag that can turn the
#	constraint off.
#
constraints = [
	("LoLeg_L", "IK", "Ankle_L", "LegIK-switch", "2",  ""),
	("Foot_L", "IK", "FootIK_L", "LegIK-switch", "1", ""),
	("Toe_L", "CopyRot", "ToeIK_L", "LegIK-switch", "", ""),
	("UpLeg_L", "IK", "KneeIK_L", "LegIK-switch", "1", ""),
	("LegCtrl_L", "LimitDist", "Hip_L", "LegIK-switch", "", ""),

	("LoLeg_R", "IK", "Ankle_R", "LegIK-switch", "2", ""),
	("Foot_R", "IK", "FootIK_R", "LegIK-switch", "1", ""),
	("Toe_R", "CopyRot", "ToeIK_R", "LegIK-switch", "", ""),
	("UpLeg_R", "IK", "KneeIK_R", "LegIK-switch", "1", ""),
	("LegCtrl_R", "LimitDist", "Hip_R", "LegIK-switch", "", ""),

	("LoArm_L", "IK", "HandIK_L", "ArmIK-switch", "2", ""),
	("UpArm_L", "IK", "ElbowIK_L", "ArmIK-switch", "1", ""),
	("Hand_L", "CopyRot", "HandIK_L", "ArmIK-switch", "", ""),
	("HandIK_L", "LimitDist", "Clavicle_L", "ArmIK-switch", "", ""),

	("LoArm_R", "IK", "HandIK_R", "ArmIK-switch", "2", ""),
	("UpArm_R", "IK", "ElbowIK_R", "ArmIK-switch", "1", ""),
	("Hand_R", "CopyRot", "HandIK_R", "ArmIK-switch", "", ""),
	("HandIK_R", "LimitDist", "Clavicle_R", "ArmIK-switch", "", ""),

	("Finger-1-3_R", "IK", "Finger-1-IK_R", "FingerIK-switch", "3", ""),
	("Finger-2-3_R", "IK", "Finger-2-IK_R", "FingerIK-switch", "3", ""),
	("Finger-3-3_R", "IK", "Finger-3-IK_R", "FingerIK-switch", "3", ""),
	("Finger-4-3_R", "IK", "Finger-4-IK_R", "FingerIK-switch", "3", ""),
	("Finger-5-3_R", "IK", "Finger-5-IK_R", "FingerIK-switch", "3", ""),

	("Finger-1-3_L", "IK", "Finger-1-IK_L", "FingerIK-switch", "3", ""),
	("Finger-2-3_L", "IK", "Finger-2-IK_L", "FingerIK-switch", "3", ""),
	("Finger-3-3_L", "IK", "Finger-3-IK_L", "FingerIK-switch", "3", ""),
	("Finger-4-3_L", "IK", "Finger-4-IK_L", "FingerIK-switch", "3", ""),
	("Finger-5-3_L", "IK", "Finger-5-IK_L", "FingerIK-switch", "3", ""),	

	("Eye_R", "IK", "Gaze_R", "Gaze-switch", "1", ""),
	("Eye_L", "IK", "Gaze_L", "Gaze-switch", "1", ""),
]

#
#	calcJointPos(obj, joint):
#

def calcJointPos(obj, joint):
	g = obj.getFaceGroup("joint-"+joint)
	verts = []
	for f in g.faces:
		for v in f.verts:
			verts.append(v.co)
	return centroid(verts)

#
#	setupLocations (obj):
#
def setupLocations (obj):
	global locations
	locations = {}
	for j in joints:
		loc = calcJointPos(obj, j)
		locations[j] = loc
	for (j, h, t, k) in otherLocations:
		hloc = locations[h]
		tloc = locations[t]
		vec = vsub(tloc, hloc)
		vec2 = vmul(vec, k)
		loc = vadd(tloc, vec2)
		locations[j] = loc
	for (j, l, r) in midLocations:
		vec = vadd(locations[l], locations[r])
		loc = vmul(vec, 0.5)
		locations[j] = loc

		

#
#	getOffset(offs, par, bones):
#

def getOffset(offs, par, bones):
	if offs == 0:
		return [0,0,0]
	else:
		return offs

#
#	writeBones(fp, obj)
#

def writeBones(fp, obj):
	global locations
	setupLocations(obj)
	bones = []
	fp.write("object HumanRig %d %d add\n" % (0x001, 0x000))
	fp.write("armature HumanRig\n")
	for (bone, par, hjoint, hoffs, tjoint, toffs, flags, layers, dispOb) in armature:
		dh = getOffset(hoffs, par, bones)
		head = vadd(locations[hjoint], dh)
		dt = getOffset(toffs, par, bones)
		tail = vadd(locations[tjoint], dt)
		roll = 0.0
		if par == "None":
			parName = "None"
		else:
			parName = par
		fp.write("bone %s %s %f %d %d\n" % (bone, parName, roll, flags, layers))
		fp.write("head %f %f %f\n" % (head[0], head[1], head[2]))
		fp.write("tail %f %f %f\n" % (tail[0], tail[1], tail[2]))
		if dispOb != "None":
			fp.write("dispob %s %s\n" % (bone, dispOb))
		bones.append((bone, head, tail))

	for (bone, type, target, driver, arg1, arg2) in constraints:
		fp.write("constraint %s %s %s %s %s %s\n" % (bone, type, target, driver, arg1, arg2))

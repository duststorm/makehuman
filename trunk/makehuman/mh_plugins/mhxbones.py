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

F_CON = 0x001
F_NODEF = 0x004

F_NOSCALE = 0x0e0
#
#	Bone layers
#

L_FK	=	0x0001
L_TORSO = 	0x0002
L_ARMIK =	0x0004
L_ARMFK =	0x0008
L_LEGIK =	0x0010
L_LEGFK =	0x0020
L_HANDIK =	0x0040
L_HANDFK =	0x0080

L_PANEL	=	0x0100
L_TOE =		0x0200
L_HEAD =	0x0400

L_ROOT = 	0x2000
L_DEFORM =	0x4000
L_HELP	=	0x8000

#
#	Flags used by IK chains
#

LimX = 1
LimY = 2
LimZ = 4
LockX = 8
LockY = 0x10
LockZ = 0x20
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
	( "mid-eyes", "l-eye", "r-eye", 0.5 ),
	( "mid-feet", "l-toe-1-1", "r-toe-1-1", 0.5 ),

	( "l-clavicle-pt2", "l-clavicle", "l-shoulder", 0.5 ),
	( "l-uparm-pt1", "l-shoulder", "l-elbow", 0.5 ),
	( "l-uparm-pt2", "l-shoulder", "l-elbow", 0.7 ),
	( "l-loarm-pt1", "l-elbow", "l-hand", 0.3 ),
	( "l-loarm-pt2", "l-elbow", "l-hand", 0.7 ),
	( "l-upleg-pt1", "l-upper-leg", "l-knee", 0.3 ),
	( "l-upleg-pt2", "l-upper-leg", "l-knee", 0.7 ),
	( "l-loleg-pt1", "l-knee", "l-ankle", 0.3 ),
	( "l-loleg-pt2", "l-knee", "l-ankle", 0.7 ),

	( "r-clavicle-pt2", "r-clavicle", "r-shoulder", 0.5 ),
	( "r-uparm-pt1", "r-shoulder", "r-elbow", 0.5 ),
	( "r-uparm-pt2", "r-shoulder", "r-elbow", 0.7 ),
	( "r-loarm-pt1", "r-elbow", "r-hand", 0.3 ),
	( "r-loarm-pt2", "r-elbow", "r-hand", 0.7 ),
	( "r-upleg-pt1", "r-upper-leg", "r-knee", 0.3 ),
	( "r-upleg-pt2", "r-upper-leg", "r-knee", 0.7 ),
	( "r-loleg-pt1", "r-knee", "r-ankle", 0.3 ),
	( "r-loleg-pt2", "r-knee", "r-ankle", 0.7 ),

]

#
#
#

vertLocations = [
	( "chest-front", 7292 ),
	( "jaw-tip", 8162 ),
	( "tounge-tip", 8049 ),
	( "tounge-mid", 8103 ),
	( "tounge-root", 8099 ),
	( "l-upLid", 12630 ),
	( "l-loLid", 12594 ),
	( "r-upLid", 2442 ),
	( "r-loLid", 2520 ),
]

#
#	Definition of armature
#	
#	(Bone, parent, head, headOffset, tail, tailOffset, flags, layers, object)
#
#	Switching left and right compare to the MH joints
#

dx = 0.2
dz = 0.3
armature = [
	("Root", "None", "mid-feet", [0,1,0], "mid-feet", [0,-1,0], F_NODEF, L_FK, "MHCircle15", 0),
	("Torso", "Root", "pelvis", [0,0,-3], "pelvis", 0, F_NODEF, L_FK+L_TORSO, None, 0),
	("Hips", "Torso", "pelvis", 0, "pelvis", [0,-1.5,0], F_CON, L_FK+L_TORSO+L_DEFORM, "MHCircle15", 0),
	("Hips-inv", "Hips", "pelvis", [0,-1.5,0], "pelvis", 0, F_CON+F_NODEF, L_HELP, None, 0),
	
	("Pelvis", "Torso", "pelvis", 0, "spine3", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("Spine3", "Pelvis", "spine3", 0, "spine2", 0, F_CON, L_FK+L_DEFORM+L_TORSO, "MHCircle10", 0),
	("Spine2", "Spine3", "spine2", 0, "spine1", 0, F_CON, L_FK+L_DEFORM+L_TORSO, "MHCircle15", 0),
	("Spine1", "Spine2", "spine1", 0, "neck", 0, F_CON, L_FK+L_DEFORM+L_TORSO, "MHCircle10", 0),
	("Neck", "Spine1", "neck", 0, "head", 0, F_CON, L_FK+L_DEFORM+L_TORSO+L_HEAD, "MHCircle05", 0),
	("Breathe", "Spine2", "spine1", 0, "chest-front", 0, F_CON, L_DEFORM, None, 0),
	("Stomach", "Breathe", "chest-front", 0, "pelvis", 0, F_CON+F_NOSCALE, L_DEFORM, None, 0),

	("Head", "Neck", "head", 0, "head-end", 0, F_CON, L_FK+L_DEFORM+L_TORSO+L_HEAD, "MHCircle10", 0),
	("Head-inv", "Head", "head-end", 0, "mouth", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("Jaw", "Head-inv", "mouth", 0, "jaw-tip", 0, F_CON, L_FK+L_DEFORM+L_HEAD, None, 0),
	("ToungeBase", "Jaw", "tounge-root", 0, "tounge-mid", 0, 0, L_DEFORM+L_HEAD, None, 0),
	("ToungeTip", "ToungeBase", "tounge-mid", 0, "tounge-tip", 0, F_CON, L_DEFORM+L_HEAD, None, 0),

	("Eye_R", "Head", "l-eye", 0, "l-eye", [0,0,0.5], 0, L_DEFORM, None, 0),
	("UpLid_R", "Head", "l-eye", 0, "l-upLid", 0, 0, L_DEFORM, None, 0),
	("LoLid_R", "Head", "l-eye", 0, "l-loLid", 0, 0, L_DEFORM, None, 0),
	("Eye_L", "Head", "r-eye", 0, "r-eye", [0,0,0.5], 0, L_DEFORM, None, 0),
	("UpLid_L", "Head", "r-eye", 0, "r-upLid", 0, 0, L_DEFORM, None, 0),
	("LoLid_L", "Head", "r-eye", 0, "r-loLid", 0, 0, L_DEFORM, None, 0),

	("Gaze", "Root", "mid-eyes", [0,0,5.25], "mid-eyes", [0,0,4.25], F_NODEF, L_HEAD+L_PANEL, None, 0),
	("Gaze_R", "Gaze", "l-eye", [0,0,5], "l-eye", [0,0,4.5], F_NODEF, L_HEAD+L_PANEL, None, 0),
	("Gaze_L", "Gaze", "r-eye", [0,0,5], "r-eye", [0,0,4.5], F_NODEF, L_HEAD+L_PANEL, None, 0),

	("Clavicle_L", "Spine1", "r-clavicle", 0, "r-shoulder", 0, 0, L_FK+L_DEFORM+L_ARMFK, "MHCircle05", 0),
	("UpArm_L", "Clavicle_L", "r-shoulder", 0, "r-elbow", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle03", 0),
	("LoArm_L", "UpArm_L", "r-elbow", 0, "r-hand", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle03", 0),
	("Hand_L", "LoArm_L", "r-hand", 0, "r-finger-3-1", 0, F_CON, L_FK+L_DEFORM+L_ARMFK+L_HANDFK, "MHCircle05", 0),
	("UpArmTwist_L", "Clavicle_L", "r-shoulder", 0, "r-elbow", 0, F_CON, L_DEFORM, None, 0),
	("LoArmTwist_L", "UpArm_L", "r-elbow", 0, "r-hand", 0, F_CON, L_DEFORM, None, 0),

	("UpArmIK_L", "Clavicle_L", "r-shoulder", 0, "r-elbow", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("LoArmIK_L", "UpArmIK_L", "r-elbow", 0, "r-hand", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("HandIK_L", "Root", "r-hand", 0, "r-finger-3-1", 0, F_NODEF, L_ARMIK, None, 0),
	("ElbowIK_L", "Clavicle_L", "r-elbow-target", 0, "r-elbow-target", [0,0,-0.5], F_NODEF, L_ARMIK, "MHBall", 0),

	("Finger-1-1_L", "Hand_L", "r-finger-1-1", 0, "r-finger-1-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-1-2_L", "Finger-1-1_L", "r-finger-1-2", 0, "r-finger-1-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-1-3_L", "Finger-1-2_L", "r-finger-1-3", 0, "r-finger-1-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-2-1_L", "Hand_L", "r-finger-2-1", 0, "r-finger-2-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-2-2_L", "Finger-2-1_L", "r-finger-2-2", 0, "r-finger-2-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-2-3_L", "Finger-2-2_L", "r-finger-2-3", 0, "r-finger-2-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-3-1_L", "Hand_L", "r-finger-3-1", 0, "r-finger-3-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-3-2_L", "Finger-3-1_L", "r-finger-3-2", 0, "r-finger-3-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-3-3_L", "Finger-3-2_L", "r-finger-3-3", 0, "r-finger-3-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-4-1_L", "Hand_L", "r-finger-4-1", 0, "r-finger-4-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-4-2_L", "Finger-4-1_L", "r-finger-4-2", 0, "r-finger-4-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-4-3_L", "Finger-4-2_L", "r-finger-4-3", 0, "r-finger-4-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-5-1_L", "Hand_L", "r-finger-5-1", 0, "r-finger-5-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-5-2_L", "Finger-5-1_L", "r-finger-5-2", 0, "r-finger-5-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-5-3_L", "Finger-5-2_L", "r-finger-5-3", 0, "r-finger-5-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),

	("Clavicle_R", "Spine1", "l-clavicle", 0, "l-shoulder", 0, 0, L_FK+L_DEFORM+L_ARMFK, "MHCircle05", 0),
	("UpArm_R", "Clavicle_R", "l-shoulder", 0, "l-elbow", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle03", 0),
	("LoArm_R", "UpArm_R", "l-elbow", 0, "l-hand", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle03", 0),
	("Hand_R", "LoArm_R", "l-hand", 0, "l-finger-3-1", 0, F_CON, L_FK+L_DEFORM+L_ARMFK+L_HANDFK, "MHCircle05", 0),
	("UpArmTwist_R", "Clavicle_R", "l-shoulder", 0, "l-elbow", 0, F_CON, L_DEFORM, None, 0),
	("LoArmTwist_R", "UpArm_R", "l-elbow", 0, "l-hand", 0, F_CON, L_DEFORM, None, 0),

	("UpArmIK_R", "Clavicle_R", "l-shoulder", 0, "l-elbow", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("LoArmIK_R", "UpArmIK_R", "l-elbow", 0, "l-hand", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("HandIK_R", "Root", "l-hand", 0, "l-finger-3-1", 0, F_NODEF, L_ARMIK+L_HANDIK, None, 0),
	("ElbowIK_R", "Clavicle_R", "l-elbow-target", 0, "l-elbow-target", [0,0,-0.5], F_NODEF, L_ARMIK, "MHBall", 0),

	("Finger-1-1_R", "Hand_R", "l-finger-1-1", 0, "l-finger-1-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-1-2_R", "Finger-1-1_R", "l-finger-1-2", 0, "l-finger-1-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-1-3_R", "Finger-1-2_R", "l-finger-1-3", 0, "l-finger-1-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-2-1_R", "Hand_R", "l-finger-2-1", 0, "l-finger-2-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-2-2_R", "Finger-2-1_R", "l-finger-2-2", 0, "l-finger-2-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-2-3_R", "Finger-2-2_R", "l-finger-2-3", 0, "l-finger-2-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-3-1_R", "Hand_R", "l-finger-3-1", 0, "l-finger-3-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-3-2_R", "Finger-3-1_R", "l-finger-3-2", 0, "l-finger-3-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-3-3_R", "Finger-3-2_R", "l-finger-3-3", 0, "l-finger-3-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-4-1_R", "Hand_R", "l-finger-4-1", 0, "l-finger-4-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-4-2_R", "Finger-4-1_R", "l-finger-4-2", 0, "l-finger-4-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-4-3_R", "Finger-4-2_R", "l-finger-4-3", 0, "l-finger-4-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-5-1_R", "Hand_R", "l-finger-5-1", 0, "l-finger-5-2", 0, 0, L_HANDFK, "MHCircle05", LockY),
	("Finger-5-2_R", "Finger-5-1_R", "l-finger-5-2", 0, "l-finger-5-3", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),
	("Finger-5-3_R", "Finger-5-2_R", "l-finger-5-3", 0, "l-finger-5-end", 0, F_CON, L_HANDFK, "MHCircle05", LockX+LockY),

	("Hip_L", "Hips-inv", "pelvis", 0, "r-upper-leg", 0, F_CON, L_HELP, None, 0),
	("UpLeg_L", "Hip_L", "r-upper-leg", 0, "r-knee", 0, F_CON, L_FK+L_DEFORM+L_LEGFK, "MHCircle03", 0),
	("LoLeg_L", "UpLeg_L", "r-knee", 0, "r-ankle", 0, F_CON, L_FK+L_DEFORM+L_LEGFK, "MHCircle03", 0),
	("Foot_L", "LoLeg_L", "r-ankle", 0, "r-toe-3-1", 0, F_CON, L_FK+L_DEFORM+L_LEGFK, "MHCircle03", 0),
 	("UpLegTwist_L", "Hip_L", "r-upper-leg", 0, "r-knee", 0, F_CON, L_DEFORM, None, 0),

	("Toe_L", "Foot_L", "r-toe-3-1", 0, "r-toe-end", 0, F_CON+F_NODEF, L_FK+L_DEFORM+L_LEGFK, "MHCircle05", 0),
	("Toe-1-1_L", "Toe_L", "r-toe-1-1", 0, "r-toe-1-2", 0, 0, L_TOE, None, 0),
	("Toe-1-2_L", "Toe-1-1_L", "r-toe-1-2", 0, "r-toe-1-end", 0, F_CON, L_TOE, None, 0),
	("Toe-2-1_L", "Toe_L", "r-toe-2-1", 0, "r-toe-2-2", 0, 0, L_TOE, None, 0),
	("Toe-2-2_L", "Toe-2-1_L", "r-toe-2-2", 0, "r-toe-2-3", 0, F_CON, L_TOE, None, 0),
	("Toe-2-3_L", "Toe-2-2_L", "r-toe-2-3", 0, "r-toe-2-end", 0, F_CON, L_TOE, None, 0),
	("Toe-3-1_L", "Toe_L", "r-toe-3-1", 0, "r-toe-3-2", 0, 0, L_TOE, None, 0),
	("Toe-3-2_L", "Toe-3-1_L", "r-toe-3-2", 0, "r-toe-3-3", 0, F_CON, L_TOE, None, 0),
	("Toe-3-3_L", "Toe-3-2_L", "r-toe-3-3", 0, "r-toe-3-end", 0, F_CON, L_TOE, None, 0),
	("Toe-4-1_L", "Toe_L", "r-toe-4-1", 0, "r-toe-4-2", 0, 0, L_TOE, None, 0),
	("Toe-4-2_L", "Toe-4-1_L", "r-toe-4-2", 0, "r-toe-4-3", 0, F_CON, L_TOE, None, 0),
	("Toe-4-3_L", "Toe-4-2_L", "r-toe-4-3", 0, "r-toe-4-end", 0, F_CON, L_TOE, None, 0),
	("Toe-5-1_L", "Toe_L", "r-toe-5-1", 0, "r-toe-5-2", 0, 0, L_TOE, None, 0),
	("Toe-5-2_L", "Toe-5-1_L", "r-toe-5-2", 0, "r-toe-5-3", 0, F_CON, L_TOE, None, 0),
	("Toe-5-3_L", "Toe-5-2_L", "r-toe-5-3", 0, "r-toe-5-end", 0, F_CON, L_TOE, None, 0),

	("Hip_R", "Hips-inv", "pelvis", 0, "l-upper-leg", 0, F_CON, L_HELP, None, 0),
	("UpLeg_R", "Hip_R", "l-upper-leg", 0, "l-knee", 0, F_CON, L_FK+L_DEFORM+L_LEGFK, "MHCircle03", 0),
	("LoLeg_R", "UpLeg_R", "l-knee", 0, "l-ankle", 0, F_CON, L_FK+L_DEFORM+L_LEGFK, "MHCircle03", 0),
	("Foot_R", "LoLeg_R", "l-ankle", 0, "l-toe-3-1", 0, F_CON, L_FK+L_DEFORM+L_LEGFK, "MHCircle03", 0),
	("Toe_R", "Foot_R", "l-toe-3-1", 0, "l-toe-end", 0, F_CON+F_NODEF, L_FK+L_DEFORM+L_LEGFK, "MHCircle05", 0),
	("UpLegTwist_R", "Hip_R", "l-upper-leg", 0, "l-knee", 0, F_CON, L_DEFORM, None, 0),

	("Toe-1-1_R", "Toe_R", "l-toe-1-1", 0, "l-toe-1-2", 0, 0, L_TOE, None, 0),
	("Toe-1-2_R", "Toe-1-1_R", "l-toe-1-2", 0, "l-toe-1-end", 0, F_CON, L_TOE, None, 0),
	("Toe-2-1_R", "Toe_R", "l-toe-2-1", 0, "l-toe-2-2", 0, 0, L_TOE, None, 0),
	("Toe-2-2_R", "Toe-2-1_R", "l-toe-2-2", 0, "l-toe-2-3", 0, F_CON, L_TOE, None, 0),
	("Toe-2-3_R", "Toe-2-2_R", "l-toe-2-3", 0, "l-toe-2-end", 0, F_CON, L_TOE, None, 0),
	("Toe-3-1_R", "Toe_R", "l-toe-3-1", 0, "l-toe-3-2", 0, 0, L_TOE, None, 0),
	("Toe-3-2_R", "Toe-3-1_R", "l-toe-3-2", 0, "l-toe-3-3", 0, F_CON, L_TOE, None, 0),
	("Toe-3-3_R", "Toe-3-2_R", "l-toe-3-3", 0, "l-toe-3-end", 0, F_CON, L_TOE, None, 0),
	("Toe-4-1_R", "Toe_R", "l-toe-4-1", 0, "l-toe-4-2", 0, 0, L_TOE, None, 0),
	("Toe-4-2_R", "Toe-4-1_R", "l-toe-4-2", 0, "l-toe-4-3", 0, F_CON, L_TOE, None, 0),
	("Toe-4-3_R", "Toe-4-2_R", "l-toe-4-3", 0, "l-toe-4-end", 0, F_CON, L_TOE, None, 0),
	("Toe-5-1_R", "Toe_R", "l-toe-5-1", 0, "l-toe-5-2", 0, 0, L_TOE, None, 0),
	("Toe-5-2_R", "Toe-5-1_R", "l-toe-5-2", 0, "l-toe-5-3", 0, F_CON, L_TOE, None, 0),
	("Toe-5-3_R", "Toe-5-2_R", "l-toe-5-3", 0, "l-toe-5-end", 0, F_CON, L_TOE, None, 0),

	("LegCtrl_L", "Root", "r-ankle", [0,-1,0], "r-ankle", [0,-1,-2], F_NODEF, L_LEGIK, None, 0),
	("UpLegIK_L", "Hip_L", "r-upper-leg", 0, "r-knee", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("LoLegIK_L", "UpLegIK_L", "r-knee", 0, "r-ankle", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("FootIK_L", "LegCtrl_L", "r-toe-3-1", 0, "r-ankle", 0, F_NODEF, L_LEGIK, None, 0),
	("ToeIK_L", "LegCtrl_L",  "r-toe-3-1", 0,  "r-toe-end", 0, F_NODEF, L_LEGIK, None, 0),
	("Ankle_L", "FootIK_L", "r-ankle", 0, "r-ankle", [0,0,-1], F_NODEF, L_HELP, None, 0),
	("KneeIK_L", "Hip_L", "r-knee-target", 0, "r-knee-target", [0,0.5,0.5], F_NODEF, L_LEGIK, "MHBall", 0),

	("LegCtrl_R", "Root", "l-ankle", [0,-1,0], "l-ankle", [0,-1,-2], F_NODEF, L_LEGIK, None, 0),
	("UpLegIK_R", "Hip_R", "l-upper-leg", 0, "l-knee", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("LoLegIK_R", "UpLegIK_R", "l-knee", 0, "l-ankle", 0, F_CON+F_NODEF, L_HELP, None, 0),
	("FootIK_R", "LegCtrl_R", "l-toe-3-1", 0, "l-ankle", 0, F_NODEF, L_LEGIK, None, 0),
	("ToeIK_R", "LegCtrl_R",  "l-toe-3-1", 0,  "l-toe-end", 0, F_NODEF, L_LEGIK, None, 0),
	("Ankle_R", "FootIK_R", "l-ankle", 0, "l-ankle", [0,0,-1], F_NODEF, L_HELP, None, 0),
	("KneeIK_R", "Hip_R", "l-knee-target", 0, "l-knee-target", [0,0.5,0.5], F_NODEF, L_LEGIK, "MHBall", 0),

	("Fingers_R", "Hand_R", "l-finger-3-1", [0,1,0], "l-finger-3-end", [0,1,0], F_NODEF, L_HANDIK, None, 0),
	("Finger-1_R", "Hand_R", "l-finger-1-1", 0, "l-finger-1-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-1-IK_R", "Finger-1_R", "l-finger-1-end", 0, "l-finger-1-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-1-Pole_R", "Finger-1_R", "l-finger-1-2", 0, "l-finger-1-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),
	("Finger-2_R", "Hand_R", "l-finger-2-1", 0, "l-finger-2-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-2-IK_R", "Finger-2_R", "l-finger-2-end", 0, "l-finger-2-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-2-Pole_R", "Finger-2_R", "l-finger-2-2", 0, "l-finger-2-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),
	("Finger-3_R", "Hand_R", "l-finger-3-1", 0, "l-finger-3-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-3-IK_R", "Finger-3_R", "l-finger-3-end", 0, "l-finger-3-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-3-Pole_R", "Finger-3_R", "l-finger-3-2", 0, "l-finger-3-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),
	("Finger-4_R", "Hand_R", "l-finger-4-1", 0, "l-finger-4-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-4-IK_R", "Finger-4_R", "l-finger-4-end", 0, "l-finger-4-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-4-Pole_R", "Finger-4_R", "l-finger-4-2", 0, "l-finger-4-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),
	("Finger-5_R", "Hand_R", "l-finger-5-1", 0, "l-finger-5-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-5-IK_R", "Finger-5_R", "l-finger-5-end", 0, "l-finger-5-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-5-Pole_R", "Finger-5_R", "l-finger-5-2", 0, "l-finger-5-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),

	("Fingers_L", "Hand_L", "r-finger-3-1", [0,1,0], "r-finger-3-end", [0,1,0], F_NODEF, L_HANDIK, None, 0),
	("Finger-1_L", "Hand_L", "r-finger-1-1", 0, "r-finger-1-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-1-IK_L", "Finger-1_L", "r-finger-1-end", 0, "r-finger-1-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-1-Pole_L", "Finger-1_L", "r-finger-1-2", 0, "r-finger-1-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),
	("Finger-2_L", "Hand_L", "r-finger-2-1", 0, "r-finger-2-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-2-IK_L", "Finger-2_L", "r-finger-2-end", 0, "r-finger-2-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-2-Pole_L", "Finger-2_L", "r-finger-2-2", 0, "r-finger-2-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),
	("Finger-3_L", "Hand_L", "r-finger-3-1", 0, "r-finger-3-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-3-IK_L", "Finger-3_L", "r-finger-3-end", 0, "r-finger-3-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-3-Pole_L", "Finger-3_L", "r-finger-3-2", 0, "r-finger-3-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),
	("Finger-4_L", "Hand_L", "r-finger-4-1", 0, "r-finger-4-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-4-IK_L", "Finger-4_L", "r-finger-4-end", 0, "r-finger-4-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-4-Pole_L", "Finger-4_L", "r-finger-4-2", 0, "r-finger-4-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),
	("Finger-5_L", "Hand_L", "r-finger-5-1", 0, "r-finger-5-end", 0, F_NODEF, L_HANDIK, None, 0),
	("Finger-5-IK_L", "Finger-5_L", "r-finger-5-end", 0, "r-finger-5-3", 0, F_NODEF, L_HELP, None, 0),
	("Finger-5-Pole_L", "Finger-5_L", "r-finger-5-2", 0, "r-finger-5-2", [0,0.3,0], F_NODEF, L_HANDIK, "MHBall", 0),

	# Face representation
	
	("PFace", "None", "origin", 0, "origin", [0,0,1], F_NODEF, L_PANEL, "MHFace", 0),

	("PBrow_R", "PFace", "origin", [-2*dx,4*dx,0], "origin", [-2*dx,4*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PBrow_L", "PFace", "origin", [2*dx,4*dx,0], "origin", [2*dx,4*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PBrows", "PFace", "origin", [0,4*dx,0], "origin", [0,4*dx,dz], F_NODEF, L_PANEL, None, 0),

	("PUpLid_R", "PFace", "origin", [-2*dx,2.8*dx,0], "origin", [-2*dx,2.8*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PUpLid_L", "PFace", "origin", [2*dx,2.8*dx,0], "origin", [2*dx,2.8*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PLoLid_R", "PFace", "origin", [-2*dx,1*dx,0], "origin", [-2*dx,1*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PLoLid_L", "PFace", "origin", [2*dx,1*dx,0], "origin", [2*dx,1*dx,dz], F_NODEF, L_PANEL, None, 0),

	("PCheek_R", "PFace", "origin", [-2*dx,0,0], "origin", [-2*dx,0,dz], F_NODEF, L_PANEL, None, 0),
	("PCheek_L", "PFace", "origin", [2*dx,0,0], "origin", [2*dx,0,dz], F_NODEF, L_PANEL, None, 0),

	("PNose", "PFace", "origin", 0, "origin", [0,0,dz], F_NODEF, L_PANEL, None, 0),
	("PUpLip", "PFace", "origin", [0,-1.2*dx,0], "origin", [0,-1.2*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PLoLip", "PFace", "origin", [0,-3.8*dx,0], "origin", [0,-3.8*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PMouth", "PFace", "origin", [0,-2.5*dx,0], "origin", [0,-2.5*dx,dz], F_NODEF, L_PANEL, None, 0),

	("PUpLip_R", "PFace", "origin", [-1*dx,-1.8*dx,0], "origin", [-1*dx,-1.8*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PUpLip_L", "PFace", "origin", [1*dx,-1.8*dx,0], "origin", [1*dx,-1.8*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PLoLip_R", "PFace", "origin", [-1*dx,-3.2*dx,0], "origin", [-1*dx,-3.2*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PLoLip_L", "PFace", "origin", [1*dx,-3.2*dx,0], "origin", [1*dx,-3.2*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PMouth_R", "PFace", "origin", [-2.5*dx,-2.5*dx,0], "origin", [-2.5*dx,-2.5*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PMouth_L", "PFace", "origin", [2.5*dx,-2.5*dx,0], "origin", [2.5*dx,-2.5*dx,dz], F_NODEF, L_PANEL, None, 0),

	("PTounge", "PFace", "origin", [0,-4.9*dx,0], "origin", [0,-4.9*dx,dz], F_NODEF, L_PANEL, None, 0),
	("PJaw", "PFace", "origin", [0,-5.7*dx,0], "origin", [0,-5.7*dx,dz], F_NODEF, L_PANEL, None, 0),

	("PArmIK_R", "PFace", "origin", [-1.1,2,0], "origin", [-1.1,2,dz], F_NODEF, L_PANEL, None, 0),
	("PArmIK_L", "PFace", "origin", [0.1,2,0], "origin", [0.1,2,dz], F_NODEF, L_PANEL, None, 0),
	("PLegIK_R", "PFace", "origin", [-1.1,1.5,0], "origin", [-1.1,1.5,dz], F_NODEF, L_PANEL, None, 0),
	("PLegIK_L", "PFace", "origin", [0.1,1.5,0], "origin", [0.1,1.5,dz], F_NODEF, L_PANEL, None, 0),
]

#
#	boneRoll - computer generated list
#

boneRoll = {
	'Ankle_L'	 : (180, 180),
	'Ankle_R'	 : (180, 180),
	'Breathe'	 : (  0,   0),
	'Clavicle_L'	 : (  0, 110),
	'Clavicle_R'	 : (  0, -110),
	'ElbowIK_L'	 : (-135, -138),
	'ElbowIK_R'	 : (135, 138),
	'Eye_L'	 : (  0,   0),
	'Eye_R'	 : (  0,   0),
	'Finger-1-1_L'	 : (-40,  98),
	'Finger-1-1_R'	 : ( 40, -98),
	'Finger-1-2_L'	 : (-22,  95),
	'Finger-1-2_R'	 : ( 22, -95),
	'Finger-1-3_L'	 : (-22,  95),
	'Finger-1-3_R'	 : ( 22, -95),
	'Finger-1-IK_L'	 : (-25, -92),
	'Finger-1-IK_R'	 : ( 25,  92),
	'Finger-1-Pole_L'	 : ( -3,  -4),
	'Finger-1-Pole_R'	 : (  3,   4),
	'Finger-1_L'	 : (-31,  96),
	'Finger-1_R'	 : ( 31, -96),
	'Finger-2-1_L'	 : (  0,  95),
	'Finger-2-1_R'	 : (  0, -95),
	'Finger-2-2_L'	 : ( -3,  93),
	'Finger-2-2_R'	 : (  3, -93),
	'Finger-2-3_L'	 : ( -3,  93),
	'Finger-2-3_R'	 : (  3, -93),
	'Finger-2-IK_L'	 : ( -7, -93),
	'Finger-2-IK_R'	 : (  7,  93),
	'Finger-2-Pole_L'	 : ( -3,  -4),
	'Finger-2-Pole_R'	 : (  3,   4),
	'Finger-2_L'	 : (  0,  94),
	'Finger-2_R'	 : (  0, -94),
	'Finger-3-1_L'	 : (  3,  94),
	'Finger-3-1_R'	 : ( -3, -94),
	'Finger-3-2_L'	 : (  0,  93),
	'Finger-3-2_R'	 : (  0, -93),
	'Finger-3-3_L'	 : (  0,  93),
	'Finger-3-3_R'	 : (  0, -93),
	'Finger-3-IK_L'	 : ( -3, -93),
	'Finger-3-IK_R'	 : (  3,  93),
	'Finger-3-Pole_L'	 : ( -3,  -4),
	'Finger-3-Pole_R'	 : (  3,   4),
	'Finger-3_L'	 : (  2,  94),
	'Finger-3_R'	 : ( -2, -94),
	'Finger-4-1_L'	 : (  5,  94),
	'Finger-4-1_R'	 : ( -5, -94),
	'Finger-4-2_L'	 : (  0,  93),
	'Finger-4-2_R'	 : (  0, -93),
	'Finger-4-3_L'	 : (  0,  93),
	'Finger-4-3_R'	 : (  0, -93),
	'Finger-4-IK_L'	 : ( -4, -93),
	'Finger-4-IK_R'	 : (  4,  93),
	'Finger-4-Pole_L'	 : ( -3,  -4),
	'Finger-4-Pole_R'	 : (  3,   4),
	'Finger-4_L'	 : (  2,  94),
	'Finger-4_R'	 : ( -2, -94),
	'Finger-5-1_L'	 : (  7,  94),
	'Finger-5-1_R'	 : ( -7, -94),
	'Finger-5-2_L'	 : (  3,  93),
	'Finger-5-2_R'	 : ( -3, -93),
	'Finger-5-3_L'	 : (  3,  93),
	'Finger-5-3_R'	 : ( -3, -93),
	'Finger-5-IK_L'	 : (  0, -93),
	'Finger-5-IK_R'	 : (  0,  93),
	'Finger-5-Pole_L'	 : ( -3,  -4),
	'Finger-5-Pole_R'	 : (  3,   4),
	'Finger-5_L'	 : (  5,  94),
	'Finger-5_R'	 : ( -5, -94),
	'Fingers_L'	 : (  2,  94),
	'Fingers_R'	 : ( -2, -94),
	'FootIK_L'	 : (-173, -177),
	'FootIK_R'	 : (173, 177),
	'Foot_L'	 : (  6, -28),
	'Foot_R'	 : ( -6,  28),
	'Gaze'		 : (180, 180),
	'Gaze_L'	 : (180, 180),
	'Gaze_R'	 : (180, 180),
	'HandIK_L'	 : ( -4,  70),
	'HandIK_R'	 : (  4, -70),
	'Hand_L'	 : ( -4,  70),
	'Hand_R'	 : (  4, -70),
	'Head'		 : (  0,   0),
	'Head-inv'	 : (180, 180),
	'Hip_L'		 : (-11,  93),
	'Hip_R'		 : ( 11, -93),
	'Hips'		 : (  0, 180),
	'Hips-inv'	 : (  0,   0),
	'Jaw'		 : (  0,   0),
	'KneeIK_L'	 : (  0,   0),
	'KneeIK_R'	 : (  0,   0),
	'LegCtrl_L'	 : (180, 180),
	'LegCtrl_R'	 : (180, 180),
	'LoArmTwist_L'	 : (  0,  91),
	'LoArmTwist_R'	 : (  0, -91),
	'LoArm_L'	 : (  0,  91),
	'LoArmIK_L'	 : (  0,  91),
	'LoArm_R'	 : (  0, -91),
	'LoArmIK_R'	 : (  0, -91),
	'LoLeg_L'	 : (-172, 180),
	'LoLegIK_L'	 : (-172, 180),
	'LoLeg_R'	 : (172, 180),
	'LoLegIK_R'	 : (172, 180),
	'LoLid_L'	 : (  2, -17),
	'LoLid_R'	 : ( -2,  17),
	'Neck'		 : (  0,   0),
	'PArmIK_L'	 : (  0, 180),
	'PArmIK_R'	 : (  0, 180),
	'PBrow_L'	 : (  0, 180),
	'PBrow_R'	 : (  0, 180),
	'PBrows'	 : (  0, 180),
	'PCheek_L'	 : (  0, 180),
	'PCheek_R'	 : (  0, 180),
	'PFace'	 : (  0, 180),
	'PJaw'	 : (  0, 180),
	'PLegIK_L'	 : (  0, 180),
	'PLegIK_R'	 : (  0, 180),
	'PLoLid_L'	 : (  0, 180),
	'PLoLid_R'	 : (  0, 180),
	'PLoLip'	 : (  0, 180),
	'PLoLip_L'	 : (  0, 180),
	'PLoLip_R'	 : (  0, 180),
	'PMouth'	 : (  0, 180),
	'PMouth_L'	 : (  0, 180),
	'PMouth_R'	 : (  0, 180),
	'PNose'	 : (  0, 180),
	'PTounge'	 : (  0, 180),
	'PUpLid_L'	 : (  0, 180),
	'PUpLid_R'	 : (  0, 180),
	'PUpLip'	 : (  0, 180),
	'PUpLip_L'	 : (  0, 180),
	'PUpLip_R'	 : (  0, 180),
	'Pelvis'	 : (  0,   0),
	'Root'	 : (  0,   0),
	'Spine1'	 : (  0,   0),
	'Spine2'	 : (  0,   0),
	'Spine3'	 : (  0,   0),
	'Stomach'	 : (180, 180),
	'Toe-1-1_L'	 : (  5, 139),
	'Toe-1-1_R'	 : ( -5, -139),
	'Toe-1-2_L'	 : (  5, 139),
	'Toe-1-2_R'	 : ( -5, -139),
	'Toe-2-1_L'	 : (  8, 103),
	'Toe-2-1_R'	 : ( -8, -103),
	'Toe-2-2_L'	 : (  4, -29),
	'Toe-2-2_R'	 : ( -4,  29),
	'Toe-2-3_L'	 : (  4, -29),
	'Toe-2-3_R'	 : ( -4,  29),
	'Toe-3-1_L'	 : (-19, 159),
	'Toe-3-1_R'	 : ( 19, -159),
	'Toe-3-2_L'	 : ( 25, 175),
	'Toe-3-2_R'	 : (-25, -175),
	'Toe-3-3_L'	 : ( 25, 175),
	'Toe-3-3_R'	 : (-25, -175),
	'Toe-4-1_L'	 : (-29, -162),
	'Toe-4-1_R'	 : ( 29, 162),
	'Toe-4-2_L'	 : ( 30, 172),
	'Toe-4-2_R'	 : (-30, -172),
	'Toe-4-3_L'	 : ( 30, 172),
	'Toe-4-3_R'	 : (-30, -172),
	'Toe-5-1_L'	 : (-32, 160),
	'Toe-5-1_R'	 : ( 32, -160),
	'Toe-5-2_L'	 : ( 36, -171),
	'Toe-5-2_R'	 : (-36, 171),
	'Toe-5-3_L'	 : ( 36, -171),
	'Toe-5-3_R'	 : (-36, 171),
	'ToeIK_L'	 : (  5, -164),
	'ToeIK_R'	 : ( -5, 164),
	'Toe_L'	 : (  5, -164),
	'Toe_R'	 : ( -5, 164),
	'Torso'	 : (  0, 180),
	'ToungeBase'	 : (  0,   0),
	'ToungeTip'	 : (  0,   0),
	'UpArmTwist_L'	 : (  0,  97),
	'UpArmTwist_R'	 : (  0, -97),
	'UpArm_L'	 : (  0,  97),
	'UpArmIK_L'	 : (  0,  97),
	'UpArm_R'	 : (  0, -97),
	'UpArmIK_R'	 : (  0, -97),
	'UpLegTwist_L'	 : ( 19, -177),
	'UpLegTwist_R'	 : (-19, 177),
	'UpLeg_L'	 : ( 19, -177),
	'UpLegIK_L'	 : ( 19, -177),
	'UpLeg_R'	 : (-19, 177),
	'UpLegIK_R'	 : (-19, 177),
	'UpLid_L'	 : ( -2, -16),
	'UpLid_R'	 : (  2,  16),
}

#
#	Definition of constraints
#
#	( Bone, type, influence, target, driver, arg1, arg2 )
#
#	The driver will be a bone that drives the influence, but presently is a flag that can turn the
#	constraint off.
#

Bone = 0
Obj = 1
constraints = [
	("Stomach", "LIMITROT", 1.0, "None", None, 5, (0, 0, 0, 0, 0, 0)),
	("Stomach", "STRETCHTO", 1.0, "Hips", None, "", 0),

	("LoLegIK_L" , "IKSOLVER", 1.0, "Ankle_L", None, 2,  Bone),
	("LoLeg_L" , "COPYROT", 1.0, "LoLegIK_L", "PLegIK_L", 7, 0),
	("Foot_L" , "IKSOLVER", 1.0, "FootIK_L", "PLegIK_L", 1, Bone),
	#("Foot_L" , "COPYROT", 1.0, "FootIK_L", "PLegIK_L", 0x12, 0),
	("Toe_L" , "COPYROT", 1.0, "ToeIK_L", "PLegIK_L", 7, 0),
	("UpLegIK_L" , "IKSOLVER", 1.0, "KneeIK_L", None, 1, Bone),
	("UpLeg_L" , "COPYROT", 1.0, "UpLegIK_L", "PLegIK_L", 7, 0),
	("LegCtrl_L" , "LIMITDIST", 1.0, "Hip_L", None, "", 0),
	("KneeIK_L" , "LIMITDIST", 1.0, "Hip_L", None, "", 0),
	("UpLegTwist_L", "IKSOLVER", 1.0, "LoLeg_L", None, 1, Bone),

	("LoLegIK_R" , "IKSOLVER", 1.0, "Ankle_R", None, 2, Bone),
	("LoLeg_R" , "COPYROT", 1.0, "LoLegIK_R", "PLegIK_R", 7, 0),
	("Foot_R" , "IKSOLVER", 1.0, "FootIK_R", "PLegIK_R", 1, Bone),
	#("Foot_R" , "COPYROT", 1.0, "FootIK_R", "PLegIK_R", 0x12, 0),
	("Toe_R" , "COPYROT", 1.0, "ToeIK_R", "PLegIK_R", 7, 0),
	("UpLegIK_R" , "IKSOLVER", 1.0, "KneeIK_R", None, 1, Bone),
	("UpLeg_R" , "COPYROT", 1.0, "UpLegIK_R", "PLegIK_R", 7, 0),
	("LegCtrl_R" , "LIMITDIST", 1.0, "Hip_R", None, "", 0),
	("KneeIK_R" , "LIMITDIST", 1.0, "Hip_R", None, "", 0),
	("UpLegTwist_R", "IKSOLVER", 1.0, "LoLeg_R", None, 1, Bone),

	("LoArmIK_L" , "IKSOLVER", 1.0, "HandIK_L", None, 2, Bone),
	("LoArm_L" , "COPYROT", 1.0, "LoArmIK_L", "PArmIK_L", 7, 0),
	#("LoArm_L", "LIMITROT", 1.0, "None", None, 7, (-30, 180, -90, 90, -30, 30)), 
	("UpArmIK_L" , "IKSOLVER", 1.0, "ElbowIK_L", None, 1, Bone),
	("UpArm_L" , "COPYROT", 1.0, "UpArmIK_L", "PArmIK_L", 7, 0),
	("Hand_L" , "COPYROT", 1.0, "HandIK_L", "PArmIK_L", 7, 0),
	("HandIK_L" , "LIMITDIST", 1.0, "Clavicle_L", None, "", 0),
	("ElbowIK_L" , "LIMITDIST", 1.0, "Clavicle_L", None, "", 0),

	("LoArmIK_R" , "IKSOLVER", 1.0, "HandIK_R", None, 2, Bone),
	("LoArm_R" , "COPYROT", 1.0, "LoArmIK_R", "PArmIK_R", 7, 0),
	#("LoArm_R", "LIMITROT", 1.0, "None", None, 7, (-30, 180, -90, 90, -30, 30)), 
	("UpArmIK_R" , "IKSOLVER", 1.0, "ElbowIK_R", None, 1, Bone),
	("UpArm_R" , "COPYROT", 1.0, "UpArmIK_R", "PArmIK_R", 7, 0),
	("Hand_R" , "COPYROT", 1.0, "HandIK_R", "PArmIK_R", 7, 0),
	("HandIK_R" , "LIMITDIST", 1.0, "Clavicle_R", None, "", 0),
	("ElbowIK_R" , "LIMITDIST", 1.0, "Clavicle_R", None, "", 0),

	("UpArmTwist_L", "IKSOLVER", 1.0, "LoArm_L", None, 1, Bone),
	("LoArmTwist_L", "IKSOLVER", 1.0, "Hand_L", None, 1, Bone),
	("UpArmTwist_R", "IKSOLVER", 1.0, "LoArm_R", None, 1, Bone),
	("LoArmTwist_R", "IKSOLVER", 1.0, "Hand_R", None, 1, Bone),
	
	("Eye_R" , "IKSOLVER", 1.0, "Gaze_R", "Gaze-switch", 1, Bone),
	("Eye_L" , "IKSOLVER", 1.0, "Gaze_L", "Gaze-switch", 1, Bone),

	("Finger-1-3_R" , "IKSOLVER", 1.0, "Finger-1-IK_R", "FingerIK_L", 3, Bone),
	("Finger-2-3_R" , "IKSOLVER", 1.0, "Finger-2-IK_R", "FingerIK_L", 3, Bone),
	("Finger-3-3_R" , "IKSOLVER", 1.0, "Finger-3-IK_R", "FingerIK_L", 3, Bone),
	("Finger-4-3_R" , "IKSOLVER", 1.0, "Finger-4-IK_R", "FingerIK_L", 3, Bone),
	("Finger-5-3_R" , "IKSOLVER", 1.0, "Finger-5-IK_R", "FingerIK_L", 3, Bone),

	("Finger-1-3_L" , "IKSOLVER", 1.0, "Finger-1-IK_L", "FingerIK_L", 3, Bone),
	("Finger-2-3_L" , "IKSOLVER", 1.0, "Finger-2-IK_L", "FingerIK_L", 3, Bone),
	("Finger-3-3_L" , "IKSOLVER", 1.0, "Finger-3-IK_L", "FingerIK_L", 3, Bone),
	("Finger-4-3_L" , "IKSOLVER", 1.0, "Finger-4-IK_L", "FingerIK_L", 3, Bone),
	("Finger-5-3_L" , "IKSOLVER", 1.0, "Finger-5-IK_L", "FingerIK_L", 3, Bone),	

	("Finger-1-1_R" , "IKSOLVER", 1.0, "Finger-1-Pole_R", "FingerIK_L", 1, Bone),
	("Finger-2-1_R" , "IKSOLVER", 1.0, "Finger-2-Pole_R", "FingerIK_L", 1, Bone),
	("Finger-3-1_R" , "IKSOLVER", 1.0, "Finger-3-Pole_R", "FingerIK_L", 1, Bone),
	("Finger-4-1_R" , "IKSOLVER", 1.0, "Finger-4-Pole_R", "FingerIK_L", 1, Bone),
	("Finger-5-1_R" , "IKSOLVER", 1.0, "Finger-5-Pole_R", "FingerIK_L", 1, Bone),

	("Finger-1-1_L" , "IKSOLVER", 1.0, "Finger-1-Pole_L", "FingerIK_L", 1, Bone),
	("Finger-2-1_L" , "IKSOLVER", 1.0, "Finger-2-Pole_L", "FingerIK_L", 1, Bone),
	("Finger-3-1_L" , "IKSOLVER", 1.0, "Finger-3-Pole_L", "FingerIK_L", 1, Bone),
	("Finger-4-1_L" , "IKSOLVER", 1.0, "Finger-4-Pole_L", "FingerIK_L", 1, Bone),
	("Finger-5-1_L" , "IKSOLVER", 1.0, "Finger-5-Pole_L", "FingerIK_L", 1, Bone),


	("PArmIK_L", "LIMITLOC", 1.0, "None", None, 0x3f, (0,1,0,0,0,0)), 
	("PArmIK_R", "LIMITLOC", 1.0, "None", None, 0x3f, (0,1,0,0,0,0)), 
	("PLegIK_L", "LIMITLOC", 1.0, "None", None, 0x3f, (0,1,0,0,0,0)), 
	("PLegIK_R", "LIMITLOC", 1.0, "None", None, 0x3f, (0,1,0,0,0,0)), 
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
	for (j, v) in vertLocations:
		locations[j] = obj.verts[v].co
	for (j, h, t, k) in otherLocations:
		hloc = locations[h]
		tloc = locations[t]
		vec = vsub(tloc, hloc)
		vec2 = vmul(vec, k)
		loc = vadd(tloc, vec2)
		locations[j] = loc
	for (j, l, r, a) in midLocations:
		left = vmul(locations[l], 1-a)
		right = vmul(locations[r], a)
		locations[j] = vadd(left, right)
		

#
#	getOffs(offs):
#

def getOffs(offs):
	if offs == 0:
		return [0,0,0]
	else:
		return offs

#
#	writeJoints(obj, fp)
#

def writeJoints(obj, fp):
	global locations
	setupLocations(obj)
	fp.write("\njoints\n  j origin -2.0 10.0 0.0 ;\n")
	for (key,val) in locations.items():
		fp.write("  j %s %g %g %g ;\n" % (key, val[0], val[1], val[2]))
	fp.write("end joints\n")
#
#	writeBones(obj, fp)
#

def writeBones(obj, fp):
	for (bone, par, hjoint, hoffs, tjoint, toffs, flags, layers, dispOb, ikFlags) in armature:
		fp.write("\n\tbone %s %s %x %x\n" % (bone, par, flags, layers))
		if hoffs:
			x = getOffs(hoffs)
			fp.write("\t\thead joint %s + %g %g %g ;\n" % (hjoint, x[0], x[1], x[2]))
		else:
			fp.write("\t\thead joint %s ;\n" % (hjoint))
		if toffs:
			x = getOffs(toffs)
			fp.write("\t\ttail joint %s + %g %g %g ;\n" % (tjoint, x[0], x[1], x[2]))
		else:
			fp.write("\t\ttail joint %s ;\n" % (tjoint))
		fp.write("\t\troll %g %g ;\n" % boneRoll[bone])
		fp.write("\tend bone\n")

#
#	writePose24(obj, fp):
#

def writePose24(obj, fp):
	for (bone, par, hjoint, hoffs, tjoint, toffs, flags, layers, dispOb, ikFlags) in armature:
		fp.write("\tposebone %s %x \n" % (bone, ikFlags))
		smash = None
		if dispOb:
			fp.write("\t\tdisplayObject _object['%s'] ;\n" % dispOb)

		for (bone1, type, infl, target, driver, arg1, arg2) in constraints:
			if bone == bone1:
				fp.write("\t\tconstraint %s Const %g \n" % (type, infl))
				if driver:
					fp.write("\t\t\tdriver %s 0.5 ;\n" % driver)
	
				if type == 'IKSOLVER':
					if arg2 == Bone:
						fp.write(
"\t\t\tCHAINLEN	int %d ; \n" % arg1 +
"\t\t\tTARGET	obj HumanRig ; \n" +
"\t\t\tBONE	str %s ; \n" % target)
					else:
						fp.write(
"\t\t\tCHAINLEN	int %d ; \n" % arg1 +
"\t\t\tTARGET	obj %s ; \n" % target)
						smash = "influence=%4.2f" % (infl)

				elif type == 'COPYROT':
					fp.write(
"\t\t\tTARGET	obj HumanRig ;\n" +
"\t\t\tBONE	str %s ; \n" % target +
"\t\t\tCOPY	hex %x ;\n" %  arg1)

				elif type == 'COPYLOC':
					fp.write(
"\t\t\tTARGET	obj HumanRig ;\n" +
"\t\t\tBONE	str %s ;\n" % target)

				elif type == 'STRETCHTO':
					fp.write(
"\t\t\tTARGET	obj HumanRig ;\n" +
"\t\t\tBONE	str %s ;\n" % target +
"\t\t\tPLANE	hex 2 ;\n")

				elif type == 'LIMITDIST':
					fp.write(
"\t\t\tTARGET	obj HumanRig ;\n" +
"\t\t\tBONE	str %s ;\n" % target)

				elif type == 'LIMITROT':
					(xmin, xmax, ymin, ymax, zmin, zmax) = arg2
					fp.write(
"\t\t\tLIMIT	hex %x ;\n" % arg1 +
"\t\t\tOWNERSPACE       hex 1 ;\n" +
"\t\t\tXMIN       float %g ; \n" % xmin +
"\t\t\tXMAX       float %g ; \n" % xmax +
"\t\t\tYMIN       float %g ; \n" % ymin +
"\t\t\tYMAX       float %g ; \n" % ymax +
"\t\t\tZMIN       float %g ; \n" % zmin +
"\t\t\tZMAX       float %g ; \n" % zmax)

				elif type == 'LIMITLOC':
					(xmin, xmax, ymin, ymax, zmin, zmax) = arg2
					fp.write(
"\t\t\tLIMIT	hex %x ;\n" % arg1 +
"\t\t\tOWNERSPACE       hex 1 ;\n" +
"\t\t\tXMIN       float %g ; \n" % xmin +
"\t\t\tXMAX       float %g ; \n" % xmax +
"\t\t\tYMIN       float %g ; \n" % ymin +
"\t\t\tYMAX       float %g ; \n" % ymax +
"\t\t\tZMIN       float %g ; \n" % zmin +
"\t\t\tZMAX       float %g ; \n" % zmax)

				else:
					raise NameError("Unknown type "+type)

				fp.write("\t\tend constraint\n")
				if smash:
					fp.write("\t\tsmash %s ;\n" % smash)
		fp.write("\tend posebone\n")

#
#	writePose25(obj, fp):
#

ConstraintTypeTable = {
	'COPYLOC' : 'COPY_LOCATION',
	'COPYROT' : 'COPY_ROTATION',
	'COPYSCALE' : 'COPY_SCALE',
	'LIMITDIST' : 'LIMIT_DISTANCE',
	'LIMITLOC' : 'LIMIT_LOCATION',
	'LIMITROT' : 'LIMIT_ROTATION',
	'LIMITSCALE' : 'LIMIT_SCALE',
	'TRANSFORM' : 'TRANSFORM',
	'CLAMPTO' : 'CLAMP_TO',
	'DAMPED_TRACK' : 'DAMPED_TRACK',
	'IKSOLVER' : 'IK',
	'LOCKED_TRACK' : 'LOCKED_TRACK',
	'SPLINE_IK' : 'SPLINE_IK',
	'STRETCHTO' : 'STRETCH_TO',
	'TRACKTO' : 'TRACK_TO',
	'ACTION' : 'ACTION',
	'CHILDOF' : 'CHILD_OF',
	'FLOOR' : 'FLOOR',
	'FOLLOWPATH' : 'FOLLOW_PATH',
	'SHRINKWRAP' : 'SHRINKWRAP',
}

def writePose25(obj, fp):
	for (bone, par, hjoint, hoffs, tjoint, toffs, flags, layers, dispOb, ikFlags) in armature:
		fp.write("\tposebone %s %x \n" % (bone, ikFlags))
		smash = None
		if dispOb:
			fp.write("\t\tcustom_shape _object['%s'] ;\n" % dispOb)

		for (bone1, type, infl, target, driver, arg1, arg2) in constraints:
			if bone == bone1:
				fp.write("\t\tconstraint %s Const %g \n" % (ConstraintTypeTable[type], infl))
				if driver:
					fp.write("\t\t\tdriver %s 0.5 ;\n" % driver)
	
				if type == 'IKSOLVER':
					if arg2 == Bone:
						fp.write(
"\t\t\tchain_length	int %d ; \n" % arg1 +
"\t\t\ttarget		obj HumanRig ; \n" +
"\t\t\tsubtarget	str %s ; \n" % target)
					else:
						fp.write(
"\t\t\tchain_length	int %d ; \n" % arg1 +
"\t\t\ttarget		obj %s ; \n" % target)
						smash = "influence=%4.2f" % (infl)

				elif type == 'COPYROT':
					fp.write(
"\t\t\ttarget		obj HumanRig ;\n" +
"\t\t\tsubtarget	str %s ; \n" % target +
"\t\t\tCOPY		hex %x ;\n" %  arg1)

				elif type == 'COPYLOC':
					fp.write(
"\t\t\ttarget		obj HumanRig ;\n" +
"\t\t\tsubtarget	str %s ;\n" % target)

				elif type == 'STRETCHTO':
					fp.write(
"\t\t\ttarget		obj HumanRig ;\n" +
"\t\t\tsubtarget	str %s ;\n" % target +
"\t\t\tplane		hex 2 ;\n")

				elif type == 'LIMITDIST':
					fp.write(
"\t\t\ttarget		obj HumanRig ;\n" +
"\t\t\tsubtarget	str %s ;\n" % target)

				elif type == 'LIMITROT':
					(xmin, xmax, ymin, ymax, zmin, zmax) = arg2
					fp.write(
"\t\t\tLIMIT	hex %x ;\n" % arg1 +
"\t\t\towner_space	str LOCAL ;\n" +
"\t\t\tminimum_x       float %g ; \n" % xmin +
"\t\t\tmaximum_x       float %g ; \n" % xmax +
"\t\t\tminimum_y       float %g ; \n" % ymin +
"\t\t\tmaximum_y       float %g ; \n" % ymax +
"\t\t\tminimum_z       float %g ; \n" % zmin +
"\t\t\tmaximum_z       float %g ; \n" % zmax)
				elif type == 'LIMITLOC':
					(xmin, xmax, ymin, ymax, zmin, zmax) = arg2
					fp.write(
"\t\t\tLIMIT	hex %x ;\n" % arg1 +
"\t\t\towner_space     str LOCAL ;\n" +
"\t\t\tminimum_x       float %g ; \n" % xmin +
"\t\t\tmaximum_x       float %g ; \n" % xmax +
"\t\t\tminimum_y       float %g ; \n" % ymin +
"\t\t\tmaximum_y       float %g ; \n" % ymax +
"\t\t\tminimum_z       float %g ; \n" % zmin +
"\t\t\tmaximum_z       float %g ; \n" % zmax)

				else:
					raise NameError("Unknown type "+type)

				fp.write("\t\tend constraint\n")
				if smash:
					fp.write("\t\tsmash %s ;\n" % smash)
		fp.write("\tend posebone\n")

#
#	colladaBones
#	Extra bones used by collada export
#

colladaBones = [
	("Chin", "Jaw", "jaw-tip", 0, "jaw-tip", [0,0,0.3], 0, 0, None, 0),
	("ToungeParent", "Head-inv", "mouth", 0, "tounge-root", 0, 0, 0, None, 0),
	("Head_L", "Head", "head-end", 0, "r-eye", 0, 0, 0, None, 0),
	("Head_R", "Head", "head-end", 0, "l-eye", 0, 0, 0, None, 0),
	("EyeEnd_L", "Eye_L", "r-eye", [0,0,0.5], "r-eye", [0,0,0.75], 0, 0, None, 0),
	("EyeEnd_R", "Eye_R", "l-eye", [0,0,0.5], "l-eye", [0,0,0.75], 0, 0, None, 0),
	("Spine1_L", "Spine1", "neck", 0, "r-clavicle", 0, 0, 0, None, 0),
	("Spine1_R", "Spine1", "neck", 0, "l-clavicle", 0, 0, 0, None, 0),
]
	
#
#	setupBones(obj):
#	Used by Collada and other exporters
#

def setupBones(obj):
	global boneHead, boneTail, locations
	setupLocations(obj)
	locations['origin'] = (-2.0, 10.0, 0.0)
	boneHead = {}
	boneTail = {}
	for (bone, par, hjoint, hoffs, tjoint, toffs, flags, layers, dispOb, ikFlags) in armature+colladaBones:
		if hoffs:
			x = getOffs(hoffs)
			boneHead[bone] = aljabr.vadd(locations[hjoint], x)
		else:
			boneHead[bone] = locations[hjoint]
		if toffs:
			x = getOffs(toffs)
			boneTail[bone] = aljabr.vadd(locations[tjoint], x)
		else:
			boneTail[bone] = locations[tjoint]

#
#	newSetupJoints (obj, joints, headTails):
#	Used by gobo
#
def newSetupJoints (obj, joints, headTails):
	global boneHead, boneTail, locations
	locations = {}
	for (key, typ, data) in joints:
		if typ == 'j':
			loc = calcJointPos(obj, data)
			locations[key] = loc
			locations[data] = loc
		elif typ == 'v':
			v = int(data)
			locations[key] = obj.verts[v].co
		elif typ == 'x':
			locations[key] = [float(data[0]), float(data[2]), -float(data[1])]

	for (key, typ, data) in joints:
		if typ == 'j':
			pass
		elif typ == 'b':
			locations[key] = locations[data]
		elif typ == 'v':
			pass
		elif typ == 'x':
			pass
		elif typ == 'l':
			((k1, joint1), (k2, joint2)) = data
			locations[key] = vadd(vmul(locations[joint1], k1), vmul(locations[joint2], k2))
		elif typ == 'o':
			(joint, offs) = data
			locations[key] = vadd(locations[joint], offs)
		else:
			raise NameError("Unknown %s" % typ)

	boneHead = {}
	boneTail = {}
	for (bone, head, tail) in headTails:
		boneHead[bone] = locations[head]
		boneTail[bone] = locations[tail]
	return 


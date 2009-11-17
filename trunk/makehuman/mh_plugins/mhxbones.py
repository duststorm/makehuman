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
'''
boneOptions = dict ({\
	Armature.CONNECTED : 0x001, \
	Armature.HINGE : 0x002, \
	Armature.NO_DEFORM : 0x004, \
	Armature.MULTIPLY : 0x008, \
	Armature.HIDDEN_EDIT : 0x010, \
	Armature.ROOT_SELECTED : 0x020, \
	Armature.BONE_SELECTED : 0x040, \
	Armature.TIP_SELECTED : 0x080, \
	Armature.LOCKED_EDIT : 0x100 \
})
'''
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
	#("Chest", "Spine1", "neck", 0, "chest-front", 0, F_CON, L_DEFORM, None, 0),
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

	("Gaze", "Root", "mid-eyes", [0,0,5.25], "mid-eyes", [0,0,4.25], F_NODEF, L_HEAD, None, 0),
	("Gaze_R", "Gaze", "l-eye", [0,0,5], "l-eye", [0,0,4.5], F_NODEF, L_HEAD, None, 0),
	("Gaze_L", "Gaze", "r-eye", [0,0,5], "r-eye", [0,0,4.5], F_NODEF, L_HEAD, None, 0),

	("Clavicle_L", "Spine1", "r-clavicle", 0, "r-shoulder", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle05", 0),
	("UpArm_L", "Clavicle_L", "r-shoulder", 0, "r-elbow", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle03", 0),
	("LoArm_L", "UpArm_L", "r-elbow", 0, "r-hand", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle03", 0),
	("Hand_L", "LoArm_L", "r-hand", 0, "r-finger-3-1", 0, F_CON, L_FK+L_DEFORM+L_ARMFK+L_HANDFK, "MHCircle05", 0),

	("UpArmTwist_L", "Clavicle_L", "r-shoulder", 0, "r-elbow", 0, F_CON, L_DEFORM, None, 0),
	("LoArmTwist_L", "UpArm_L", "r-elbow", 0, "r-hand", 0, F_CON, L_DEFORM, None, 0),

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

	("Clavicle_R", "Spine1", "l-clavicle", 0, "l-shoulder", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle05", 0),
	("UpArm_R", "Clavicle_R", "l-shoulder", 0, "l-elbow", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle03", 0),
	("LoArm_R", "UpArm_R", "l-elbow", 0, "l-hand", 0, F_CON, L_FK+L_DEFORM+L_ARMFK, "MHCircle03", 0),
	("Hand_R", "LoArm_R", "l-hand", 0, "l-finger-3-1", 0, F_CON, L_FK+L_DEFORM+L_ARMFK+L_HANDFK, "MHCircle05", 0),
	("UpArmTwist_R", "Clavicle_R", "l-shoulder", 0, "l-elbow", 0, F_CON, L_DEFORM, None, 0),
	("LoArmTwist_R", "UpArm_R", "l-elbow", 0, "l-hand", 0, F_CON, L_DEFORM, None, 0),

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
	("FootIK_L", "LegCtrl_L", "r-toe-3-1", 0, "r-ankle", 0, F_NODEF, L_LEGIK, "MHCircle03", 0),
	("ToeIK_L", "LegCtrl_L",  "r-toe-3-1", 0,  "r-toe-end", 0, F_NODEF, L_LEGIK, "MHCircle05", 0),
	("Ankle_L", "FootIK_L", "r-ankle", 0, "r-ankle", [0,0,-1], F_NODEF, L_HELP, None, 0),
	("KneeIK_L", "Hip_L", "r-knee-target", 0, "r-knee-target", [0,0.5,0.5], F_NODEF, L_LEGIK, "MHBall", 0),

	("LegCtrl_R", "Root", "l-ankle", [0,-1,0], "l-ankle", [0,-1,-2], F_NODEF, L_LEGIK, None, 0),
	("FootIK_R", "LegCtrl_R", "l-toe-3-1", 0, "l-ankle", 0, F_NODEF, L_LEGIK, "MHCircle03", 0),
	("ToeIK_R", "LegCtrl_R",  "l-toe-3-1", 0,  "l-toe-end", 0, F_NODEF, L_LEGIK, "MHCircle05", 0),
	("Ankle_R", "FootIK_R", "l-ankle", 0, "l-ankle", [0,0,-1], F_NODEF, L_HELP, None, 0),
	("KneeIK_R", "Hip_R", "l-knee-target", 0, "l-knee-target", [0,0.5,0.5], F_NODEF, L_LEGIK, "MHBall", 0),
	("HandIK_L", "Root", "r-hand", 0, "r-finger-3-1", 0, F_NODEF, L_ARMIK+L_HANDIK, "MHCircle05", 0),
	("ElbowIK_L", "Clavicle_L", "r-elbow-target", 0, "r-elbow-target", [0,0,-0.5], F_NODEF, L_ARMIK, "MHBall", 0),

	("HandIK_R", "Root", "l-hand", 0, "l-finger-3-1", 0, F_NODEF, L_ARMIK+L_HANDIK, "MHCircle05", 0),
	("ElbowIK_R", "Clavicle_R", "l-elbow-target", 0, "l-elbow-target", [0,0,-0.5], F_NODEF, L_ARMIK, "MHBall", 0),

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

	# Osipa-like control panel

	("Panel", "None", "origin", [-0.25,-0.25,0], "origin", [-0.25,-0.25,1], F_NODEF, L_PANEL, "Panel", 0),
	("PSync", "Panel", "origin", [1.5,1,0], "origin", [1.5,1,1], F_NODEF, L_PANEL, None, 0),
	("PLips", "Panel", "origin", [3.0,0,0], "origin", [3,0,1], F_NODEF, L_PANEL, None, 0),
	("PTounge", "Panel", "origin", [4.5,0,0], "origin", [4.5,0,1], F_NODEF, L_PANEL, None, 0),
	("PMouthEmotion", "Panel", "origin", [4.0,1.5,0], "origin", [4,1.5,1], F_NODEF, L_PANEL, None, 0),
	("PBrows", "Panel", "origin", [0,4,0], "origin", [0,4,1], F_NODEF, L_PANEL, None, 0),
	("PBrowEmotion", "Panel", "origin", [1.5,4,0], "origin", [1.5,4,1], F_NODEF, L_PANEL, None, 0),
	("PEyeLids", "Panel", "origin", [4,4,0], "origin", [4,4,1], F_NODEF, L_PANEL, None, 0),
	("PEyes", "Panel", "origin", [6.5,4,0], "origin", [6.5,4,1], F_NODEF, L_PANEL, None, 0),
]


'''
	# IK/FK switch bones. Do not work properly
	("ArmIK-switch", "Root", "head-end", [0,1,0], "head-end", [0,1,-1], F_NODEF, L_ROOT),
	("LegIK-switch", "Root", "head-end", [0,1.5,0], "head-end", [0,1.5,-1], F_NODEF, L_ROOT),
	("FingerIK-switch", "Root", "head-end", [0,2,0], "head-end", [0,2,-1], F_NODEF, L_ROOT),
	("Gaze-switch", "Root", "head-end", [0,2.5,0], "head-end", [0,2.5,-1], F_NODEF, L_ROOT),
'''




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
	("LoLeg_L" , "IKSOLVER", 1.0, "Ankle_L", "LegIK-switch", 2,  0),
	("Foot_L" , "IKSOLVER", 1.0, "FootIK_L", "LegIK-switch", 1, Bone),
	("Toe_L" , "COPYROT", 1.0, "ToeIK_L", "LegIK-switch", "", 0),
	("UpLeg_L" , "IKSOLVER", 1.0, "KneeIK_L", "LegIK-switch", 1, Bone),
	("LegCtrl_L" , "LIMITDIST", 1.0, "Hip_L", "LegIK-switch", "", 0),
	("KneeIK_L" , "LIMITDIST", 1.0, "Hip_L", "LegIK-switch", "", 0),
	("UpLegTwist_L", "IKSOLVER", 1.0, "LoLeg_L", None, 1, Bone),

	("LoLeg_R" , "IKSOLVER", 1.0, "Ankle_R", "LegIK-switch", 2, Bone),
	("Foot_R" , "IKSOLVER", 1.0, "FootIK_R", "LegIK-switch", 1, Bone),
	("Toe_R" , "COPYROT", 1.0, "ToeIK_R", "LegIK-switch", "", 0),
	("UpLeg_R" , "IKSOLVER", 1.0, "KneeIK_R", "LegIK-switch", 1, Bone),
	("LegCtrl_R" , "LIMITDIST", 1.0, "Hip_R", "LegIK-switch", "", 0),
	("KneeIK_R" , "LIMITDIST", 1.0, "Hip_R", "LegIK-switch", "", 0),
	("UpLegTwist_R", "IKSOLVER", 1.0, "LoLeg_R", None, 1, Bone),

	("LoArm_L" , "IKSOLVER", 1.0, "HandIK_L", "ArmIK-switch", 2, Bone),
	("LoArm_L", "LIMITROT", 1.0, "None", None, 7, (-30, 180, -90, 90, -30, 30)), 
	("UpArm_L" , "IKSOLVER", 1.0, "ElbowIK_L", "ArmIK-switch", 1, Bone),
	("Hand_L" , "COPYROT", 1.0, "HandIK_L", "ArmIK-switch", "", 0),
	("HandIK_L" , "LIMITDIST", 1.0, "Clavicle_L", "ArmIK-switch", "", 0),
	("ElbowIK_L" , "LIMITDIST", 1.0, "Clavicle_L", "ArmIK-switch", "", 0),

	("LoArm_R" , "IKSOLVER", 1.0, "HandIK_R", "ArmIK-switch", 2, Bone),
	("LoArm_R", "LIMITROT", 1.0, "None", None, 7, (-30, 180, -90, 90, -30, 30)), 
	("UpArm_R" , "IKSOLVER", 1.0, "ElbowIK_R", "ArmIK-switch", 1, Bone),
	("Hand_R" , "COPYROT", 1.0, "HandIK_R", "ArmIK-switch", "", 0),
	("HandIK_R" , "LIMITDIST", 1.0, "Clavicle_R", "ArmIK-switch", "", 0),
	("ElbowIK_R" , "LIMITDIST", 1.0, "Clavicle_R", "ArmIK-switch", "", 0),

	("UpArmTwist_L", "IKSOLVER", 1.0, "LoArm_L", None, 1, Bone),
	("LoArmTwist_L", "IKSOLVER", 1.0, "Hand_L", None, 1, Bone),
	("UpArmTwist_R", "IKSOLVER", 1.0, "LoArm_R", None, 1, Bone),
	("LoArmTwist_R", "IKSOLVER", 1.0, "Hand_R", None, 1, Bone),
	
	#("Eye_R" , "IKSOLVER", 1.0, "Gaze_R", "Gaze-switch", 1, Bone),
	#("Eye_L" , "IKSOLVER", 1.0, "Gaze_L", "Gaze-switch", 1, Bone),

	("Eye_L" , "IKSOLVER", 1.0, "EmptyEye_L", None, 1, Obj),
	("UpLid_L" , "IKSOLVER", 1.0, "EmptyUpLid_L", None, 1, Obj),
	("LoLid_L" , "IKSOLVER", 1.0, "EmptyLoLid_L", None, 1, Obj),
	("Eye_R" , "IKSOLVER", 1.0, "EmptyEye_R", None, 1, Obj),
	("UpLid_R" , "IKSOLVER", 1.0, "EmptyUpLid_R", None, 1, Obj),
	("LoLid_R" , "IKSOLVER", 1.0, "EmptyLoLid_R", None, 1, Obj),

	("Finger-1-3_R" , "IKSOLVER", 1.0, "Finger-1-IK_R", "FingerIK-switch", 3, Bone),
	("Finger-2-3_R" , "IKSOLVER", 1.0, "Finger-2-IK_R", "FingerIK-switch", 3, Bone),
	("Finger-3-3_R" , "IKSOLVER", 1.0, "Finger-3-IK_R", "FingerIK-switch", 3, Bone),
	("Finger-4-3_R" , "IKSOLVER", 1.0, "Finger-4-IK_R", "FingerIK-switch", 3, Bone),
	("Finger-5-3_R" , "IKSOLVER", 1.0, "Finger-5-IK_R", "FingerIK-switch", 3, Bone),

	("Finger-1-3_L" , "IKSOLVER", 1.0, "Finger-1-IK_L", "FingerIK-switch", 3, Bone),
	("Finger-2-3_L" , "IKSOLVER", 1.0, "Finger-2-IK_L", "FingerIK-switch", 3, Bone),
	("Finger-3-3_L" , "IKSOLVER", 1.0, "Finger-3-IK_L", "FingerIK-switch", 3, Bone),
	("Finger-4-3_L" , "IKSOLVER", 1.0, "Finger-4-IK_L", "FingerIK-switch", 3, Bone),
	("Finger-5-3_L" , "IKSOLVER", 1.0, "Finger-5-IK_L", "FingerIK-switch", 3, Bone),	

	("Finger-1-1_R" , "IKSOLVER", 1.0, "Finger-1-Pole_R", "FingerIK-switch", 1, Bone),
	("Finger-2-1_R" , "IKSOLVER", 1.0, "Finger-2-Pole_R", "FingerIK-switch", 1, Bone),
	("Finger-3-1_R" , "IKSOLVER", 1.0, "Finger-3-Pole_R", "FingerIK-switch", 1, Bone),
	("Finger-4-1_R" , "IKSOLVER", 1.0, "Finger-4-Pole_R", "FingerIK-switch", 1, Bone),
	("Finger-5-1_R" , "IKSOLVER", 1.0, "Finger-5-Pole_R", "FingerIK-switch", 1, Bone),

	("Finger-1-1_L" , "IKSOLVER", 1.0, "Finger-1-Pole_L", "FingerIK-switch", 1, Bone),
	("Finger-2-1_L" , "IKSOLVER", 1.0, "Finger-2-Pole_L", "FingerIK-switch", 1, Bone),
	("Finger-3-1_L" , "IKSOLVER", 1.0, "Finger-3-Pole_L", "FingerIK-switch", 1, Bone),
	("Finger-4-1_L" , "IKSOLVER", 1.0, "Finger-4-Pole_L", "FingerIK-switch", 1, Bone),
	("Finger-5-1_L" , "IKSOLVER", 1.0, "Finger-5-Pole_L", "FingerIK-switch", 1, Bone),

	# Osipa-like panel
	("PSync" , "LIMITLOC", 1.0, "None", None, 0x3f, (-1, 1, 0, 0, -1, 1)),
	("PLips" , "LIMITLOC", 1.0, "None", None, 0x3f, (0, 1, 0, 0, -1, 0)),
	("PTounge" , "LIMITLOC", 1.0, "None", None, 0x3f, (0, 1, 0, 0, -1, 0)),
	("PMouthEmotion" , "LIMITLOC", 1.0, "None", None, 0x3f, (-1, 1, 0, 0, -1, 0)),
	("PBrows" , "LIMITLOC", 1.0, "None", None, 0x3f, (0, 0, 0, 0, -1, 1)),
	("PBrowEmotion" , "LIMITLOC", 1.0, "None", None, 0x3f, (-1, 1, 0, 0, -1, 0)),
	("PEyeLids" , "LIMITLOC", 1.0, "None", None, 0x3f, (-1, 1, 0, 0, -1, 1)),
	("PEyes" , "LIMITLOC", 1.0, "None", None, 0x3f, (-1, 1, 0, 0, -1, 1)),

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
		fp.write("  j %s %f %f %f ;\n" % (key, val[0], val[1], val[2]))
	fp.write("end joints\n")
#
#	writeBones(obj, fp)
#

def writeBones(obj, fp):
	for (bone, par, hjoint, hoffs, tjoint, toffs, flags, layers, dispOb, ikFlags) in armature:
		fp.write("\n\tbone %s %s %x %x\n" % (bone, par, flags, layers))
		if hoffs:
			x = getOffs(hoffs)
			fp.write("\t\thead joint %s + %f %f %f ;\n" % (hjoint, x[0], x[1], x[2]))
		else:
			fp.write("\t\thead joint %s ;\n" % (hjoint))
		if toffs:
			x = getOffs(toffs)
			fp.write("\t\ttail joint %s + %f %f %f ;\n" % (tjoint, x[0], x[1], x[2]))
		else:
			fp.write("\t\ttail joint %s ;\n" % (tjoint))
		fp.write("\tend bone\n")

#
#	writePose(obj, fp):
#

def writePose(obj, fp):
	for (bone, par, hjoint, hoffs, tjoint, toffs, flags, layers, dispOb, ikFlags) in armature:
		fp.write("\tposebone %s %x \n" % (bone, ikFlags))
		smash = None
		if dispOb:
			fp.write("\t\tdisplayObject _object['%s'] ;\n" % dispOb)

		for (bone1, type, infl, target, driver, arg1, arg2) in constraints:
			if bone == bone1:
				fp.write("\t\tconstraint %s Const %f \n" % (type, infl))
				if driver:
					fp.write("\t\t\tdriver %s ;\n" % driver)
	
				if type == 'IKSOLVER':
					if arg2 == Bone:
						fp.write(\
"\t\t\tCHAINLEN	int %d ; \n\
\t\t\tTARGET	obj HumanRig ; \n\
\t\t\tBONE	str %s ; \n" % (arg1, target))
					else:
						fp.write(\
"\t\t\tCHAINLEN	int %d ; \n\
\t\t\tTARGET	obj %s ; \n" % (arg1, target))
						smash = "influence=%4.2f" % (infl)

				elif type == 'COPYROT':
					fp.write(\
"\t\t\tTARGET	obj HumanRig ;\n\
\t\t\tBONE	str %s ;\n" % (target))

				elif type == 'COPYLOC':
					fp.write(\
"\t\t\tTARGET	obj HumanRig ;\n\
\t\t\tBONE	str %s ;\n" % (target))

				elif type == 'STRETCHTO':
					fp.write(\
"\t\t\tTARGET	obj HumanRig ;\n\
\t\t\tBONE	str %s ;\n\
\t\t\tPLANE	hex 2 ;\n" % (target))

				elif type == 'LIMITDIST':
					fp.write(\
"\t\t\tTARGET	obj HumanRig ;\n\
\t\t\tBONE	str %s ;\n" % (target))

				elif type == 'LIMITROT':
					(xmin, xmax, ymin, ymax, zmin, zmax) = arg2
					fp.write(\
"\t\t\tLIMIT	hex %x ;\n\
\t\t\tOWNERSPACE       hex 1 ;\n\
\t\t\tXMIN       float %f ; \n\
\t\t\tXMAX       float %f ; \n\
\t\t\tYMIN       float %f ; \n\
\t\t\tYMAX       float %f ; \n\
\t\t\tZMIN       float %f ; \n\
\t\t\tZMAX       float %f ; \n" % (arg1, xmin, xmax, ymin, ymax, zmin, zmax))
				elif type == 'LIMITLOC':
					(xmin, xmax, ymin, ymax, zmin, zmax) = arg2
					fp.write(\
"\t\t\tLIMIT	hex %x ;\n\
\t\t\tOWNERSPACE       hex 1 ;\n\
\t\t\tXMIN       float %f ; \n\
\t\t\tXMAX       float %f ; \n\
\t\t\tYMIN       float %f ; \n\
\t\t\tYMAX       float %f ; \n\
\t\t\tZMIN       float %f ; \n\
\t\t\tZMAX       float %f ; \n" % (arg1, xmin, xmax, ymin, ymax, zmin, zmax))

				elif type == 'ACTION':
					(key, bmin, bmax) = arg2
					fp.write(\
"\t\t\tTARGETSPACE	list 1 hex 0 ; \n\
\t\t\tACTION	act %s ; \n\
\t\t\tTARGET	obj HumanRig ; \n\
\t\t\tBONE	str %s ; \n\
\t\t\tKEYON	hex %d ; \n\
\t\t\tMIN	float %f ; \n\
\t\t\tMAX	float %f ; \n\
\t\t\tSTART	int 1 ; \n\
\t\t\tEND	int 21 ; \n" % (arg1, target, key, bmin, bmax))

				else:
					raise NameError("Unknown type "+type)

				fp.write("\t\tend constraint\n")
				if smash:
					fp.write("\t\tsmash %s ;\n" % smash)
		fp.write("\tend posebone\n")

#
#	writeEmpty(fp, empty, loc, offs, parentBone, extra)
#

def writeEmpty(fp, empty, loc, offs, parent, extra):
	vec = locations[loc]
	if offs:
		vec = vadd(vec, offs)
	fp.write(\
"\nempty ; \n\
object %s Empty \n\
  layers 0 1 ;\n\
  matrix \n\
    row 1.000000 0.000000 0.000000 0.000000 ;\n\
    row 0.000000 1.000000 0.000000 0.000000 ;\n\
    row 0.000000 0.000000 1.000000 0.000000 ;\n\
    row %f %f %f 1.000000 ;\n\
  end matrix\n\
  %s ;\n"  % (empty, vec[0], vec[1], vec[2], parent) )
	if extra:
		fp.write("  %s ;\n" % extra)
	fp.write("end object\n")

#
#	writePyDriver(fp, icu, empty, driverChannel, driverBone, factor1, channel1, factor2, channel2)
#

def writePyDriver(fp, icu, empty, driverChannel, driverBone, factor1, channel1, factor2, channel2):
	bone = 'ob("HumanRig").getPose().bones["%s"]' % driverBone
	expr1 = '%3.1f*%s.%s' % (factor1, bone, channel1)
	if factor2 == 0:
		expr2 = ''
	elif factor2 < 0:
		expr2 = '-%3.1f*%s.%s' % (-factor2, bone, channel2)
	else:
		expr2 = '+%3.1f*%s.%s' % (factor2, bone, channel2)

	fp.write(\
"  icu %s 0 2 \n\
    driver 2 ; \n\
    driverObject _object['%s'] ; \n\
    driverChannel %d ; \n\
    driverExpression '%s%s' ; \n\
    extend 0 ; \n\
    interpolation 2 ; \n\
  end icu \n" % (icu, empty, driverChannel, expr1, expr2) )

	

def writeEmpties(fp):
	fp.write("\nipo Object IpoEye_L\n")
	writePyDriver(fp, "RotY", "EmptyEye_L", 1, "PEyes", 3.0, "loc.x", 0, "loc.z")
	writePyDriver(fp, "RotX", "EmptyEye_L", 1, "PEyes", 2.0, "loc.z", 0, "loc.x")
	fp.write("end ipo\n")

	fp.write("\nipo Object IpoUpLid_L\n")
	writePyDriver(fp, "RotX", "EmptyUpLid_L", 1, "PEyes", 2.0, "loc.z", 0, "loc.x")
	fp.write("end ipo\n")

	fp.write("\nipo Object IpoLoLid_L\n")
	writePyDriver(fp, "RotX", "EmptyLoLid_L", 1, "PEyes", 2.0, "loc.z", 0, "loc.x")
	fp.write("end ipo\n")

	fp.write("\nipo Object IpoEye_R\n")
	writePyDriver(fp, "RotY", "EmptyEye_R", 1, "PEyes", 3.0, "loc.x", 0, "loc.z")
	writePyDriver(fp, "RotX", "EmptyEye_R", 1, "PEyes", 2.0, "loc.z", 0, "loc.x")
	fp.write("end ipo\n")

	fp.write("\nipo Object IpoUpLid_R\n")
	writePyDriver(fp, "RotX", "EmptyUpLid_R", 1, "PEyes", 2.0, "loc.z", 0, "loc.x")
	fp.write("end ipo\n")

	fp.write("\nipo Object IpoLoLid_R\n")
	writePyDriver(fp, "RotX", "EmptyLoLid_R", 1, "PEyes", 2.0, "loc.z", 0, "loc.z")
	fp.write("end ipo\n")

	writeEmpty(fp, "EmptyEyeBase_L", "r-eye", 0, "parent HumanRig 7 Head", "ipo IpoEye_L")
	writeEmpty(fp, "EmptyEye_L", "r-eye", [0,0,1], "parent EmptyEyeBase_L 0 None", None)
	writeEmpty(fp, "EmptyUpLidBase_L", "r-eye", 0, "parent HumanRig 7 Head", "ipo IpoUpLid_L")
	writeEmpty(fp, "EmptyUpLid_L", "r-upLid", 0, "parent EmptyUpLidBase_L 0 None", None)
	writeEmpty(fp, "EmptyLoLidBase_L", "r-eye", 0, "parent HumanRig 7 Head", "ipo IpoLoLid_L")
	writeEmpty(fp, "EmptyLoLid_L", "r-loLid", 0, "parent EmptyLoLidBase_L 0 None", None)

	writeEmpty(fp, "EmptyEyeBase_R", "l-eye", 0, "parent HumanRig 7 Head", "ipo IpoEye_R")
	writeEmpty(fp, "EmptyEye_R", "l-eye", [0,0,1], "parent EmptyEyeBase_R 0 None", None)
	writeEmpty(fp, "EmptyUpLidBase_R", "l-eye", 0, "parent HumanRig 7 Head", "ipo IpoUpLid_R")
	writeEmpty(fp, "EmptyUpLid_R", "l-upLid", 0, "parent EmptyUpLidBase_R 0 None", None)
	writeEmpty(fp, "EmptyLoLidBase_R", "l-eye", 0, "parent HumanRig 7 Head", "ipo IpoLoLid_R")
	writeEmpty(fp, "EmptyLoLid_R", "l-loLid", 0, "parent EmptyLoLidBase_R 0 None", None)




#!BPY
""" 
Name: 'MH LiPMouth'
Blender: 249
Group: 'Animation'
TUltip: 'MakEuman LiPMouth'
"""

__author__= ['Thomas Larsson']
__url__ = ("www.makEuman.org")
__version__= '0.3'
__bpydoc__= '''\
LiPMouth in Blender for the MH facial keys
'''
""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://www.makehuman.org/node/319)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

MHX (MakEuman eXchange format) exporter for Blender.

TODO
"""

import Blender
from Blender import *
from Blender.Mathutils import *
import os

overallScale = 0.2

#
#	Visemes
#

Visemes = ({\
	'rest' : [('PMouth', (0,0)), ('PUpLip', (0,-0.1)), ('PLoLip', (0,0.1)), ('PJaw', (0,0.05)), ('PTongue', (0,0.0))], \
	'etc' : [('PMouth', (0,0)), ('PUpLip', (0,-0.1)), ('PLoLip', (0,0.1)), ('PJaw', (0,0.15)), ('PTongue', (0,0.0))], \
	'MBP' : [('PMouth', (-0.3,0)), ('PUpLip', (0,1)), ('PLoLip', (0,0)), ('PJaw', (0,0.1)), ('PTongue', (0,0.0))], \
	'OO' : [('PMouth', (-1.5,0)), ('PUpLip', (0,0)), ('PLoLip', (0,0)), ('PJaw', (0,0.2)), ('PTongue', (0,0.0))], \
	'O' : [('PMouth', (-1.1,0)), ('PUpLip', (0,0)), ('PLoLip', (0,0)), ('PJaw', (0,0.5)), ('PTongue', (0,0.0))], \
	'R' : [('PMouth', (-0.9,0)), ('PUpLip', (0,-0.2)), ('PLoLip', (0,0.2)), ('PJaw', (0,0.2)), ('PTongue', (0,0.0))], \
	'FV' : [('PMouth', (0,0)), ('PUpLip', (0,0)), ('PLoLip', (0,-0.8)), ('PJaw', (0,0.1)), ('PTongue', (0,0.0))], \
	'S' : [('PMouth', (0,0)), ('PUpLip', (0,-0.2)), ('PLoLip', (0,0.2)), ('PJaw', (0,0.05)), ('PTongue', (0,0.0))], \
	'SH' : [('PMouth', (-0.6,0)), ('PUpLip', (0,-0.5)), ('PLoLip', (0,0.5)), ('PJaw', (0,0)), ('PTongue', (0,0.0))], \
	'EE' : [('PMouth', (0.3,0)), ('PUpLip', (0,-0.3)), ('PLoLip', (0,0.3)), ('PJaw', (0,0.025)), ('PTongue', (0,0.0))], \
	'AH' : [('PMouth', (-0.1,0)), ('PUpLip', (0,-0.4)), ('PLoLip', (0,0)), ('PJaw', (0,0.35)), ('PTongue', (0,0.0))], \
	'EH' : [('PMouth', (0.1,0)), ('PUpLip', (0,-0.2)), ('PLoLip', (0,0.2)), ('PJaw', (0,0.2)), ('PTongue', (0,0.0))], \
	'TH' : [('PMouth', (0,0)), ('PUpLip', (0,-0.5)), ('PLoLip', (0,0.5)), ('PJaw', (-0.2,0.1)), ('PTongue', (0,-0.6))], \
	'L' : [('PMouth', (0,0)), ('PUpLip', (0,-0.2)), ('PLoLip', (0,0.2)), ('PJaw', (0.2,0.2)), ('PTongue', (0,-0.8))], \
	'G' : [('PMouth', (0,0)), ('PUpLip', (0,-0.1)), ('PLoLip', (0,0.1)), ('PJaw', (-0.3,0.1)), ('PTongue', (0,-0.6))], \

	'blink' : [('PUpLid_L', (0,1.0)), ('PLoLid_L', (0,-0.5)), ('PUpLid_R', (0,1.0)), ('PLoLid_R', (0,-0.5))], \
	'unblink' : [('PUpLid_L', (0,0)), ('PLoLid_L', (0,0)), ('PUpLid_R', (0,0)), ('PLoLid_R', (0,0))], \

})

MohoVisemes = dict({\
	'rest' : 'rest', \
	'etc' : 'etc', \
	'AI' : 'AH', \
	'O' : 'O', \
	'U' : 'OO', \
	'WQ' : 'AH', \
	'L' : 'L', \
	'E' : 'EH', \
	'MBP' : 'MBP', \
	'FV' : 'FV', \
})

MagpieVisemes = dict({\
	"CONS" : "t,d,k,g,T,D,s,z,S,Z,h,n,N,j,r,tS", \
	"AI" : "i,&,V,aU,I,0,@,aI", \
	"E" : "eI,3,e", \
	"O" : "O,@U,oI", \
	"UW" : "U,u,w", \
	"MBP" : "m,b,p", \
	"L" : "l", \
	"FV" : "f,v", \
	"Sh" : "dZ", \
})

def setViseme(vis):
	amtOb = Object.Get('Human')
	amtOb.sel = True
	pose = amtOb.getPose()
	pbones = pose.bones
	for (b, (x, z)) in 	Visemes[vis]:
		loc = Vector(float(x),0,float(z))
		pbones[b].loc = loc*overallScale
	pose.update()
	Window.PoseMode(0)
	Window.PoseMode(1)

	meshOb = Object.Get('HumanMesh')
	meshOb.sel = True
	Window.EditMode(1)
	Window.EditMode(0)
	amtOb.sel = True

	Draw.Redraw(-1)
	return

#
#	Load file
#

startFrame = 1

def loadMoho(file):
	loadFile(file, 'Moho')

def loadMagpie(file):
	loadFile(file, 'Magpie')

def loadFile(file, format):
	global toggleNewAction, startFrame
	(path, fileName) = os.path.split(file)
	(name, ext) = os.path.splitext(fileName)
	fp = open(file, "r")
	for ob in Object.GetSelected():
		if (ob.type == 'Armature'):
			if toggleNewAction:
				act = Armature.NLA.NewAction(name)
			else:
				try:
					act = ob.getAction()			
				except:
					act = Armature.NLA.NewAction(name)
			act.setActive(ob)

			if format == 'Moho':
				readMoho(fp, ob, startFrame-1)
			elif format == 'Magpie':
				readMagpie(fp, ob, startFrame-1)
			Draw.Redraw(-1)
			fp.close()
			act.setActive(ob)
			Draw.PupMenu("Action %s loaded" % name)
			return
	fp.close()
	Draw.PupMenu("No armature selected")
	return

#
#	Load Moho files in .dat format
#

def readMoho(fp, ob, offs):
	pose = ob.getPose()
	lineNo = 0
	for line in fp: 
		lineSplit= line.split()
		lineNo += 1
		if len(lineSplit) < 2:
			pass
		else:
			vis = MohoVisemes[lineSplit[1]]
			readMohoPose(int(lineSplit[0])+offs, vis, ob, pose.bones)
	pose.update()

def readMohoPose(frame, vis, ob, pbones):
	for (b, (x, z)) in Visemes[vis]:
		loc = Vector(float(x),0,float(z))
		pbones[b].loc = loc*overallScale
		pbones[b].insertKey(ob, frame, [Object.Pose.LOC], False)

#
#	Load Magpie files in .mag format
#

def readMagpie(fp, ob, offs):
	pose = ob.getPose()
	lineNo = 0
	for line in fp: 
		lineSplit= line.split()
		lineNo += 1
		if len(lineSplit) < 3:
			pass
		elif lineSplit[2] == 'X':
			vis = MoagpieVisemes[lineSplit[3]]
			readMagpiePose(int(lineSplit[0])+offs, vis, ob, pose.bones)
	pose.update()

def readMagpiePose(frame, vis, ob, pbones):
	for (b, (x, z)) in Visemes[vis]:
		loc = Vector(float(x),0,float(z))
		pbones[b].loc = loc*overallScale
		pbones[b].insertKey(ob, frame, [Object.Pose.LOC], False)

#
#	dampening
#

maxSlope = 0.1

def dampenIcu(icu):
	global maxSlope
	maxScaledSlope = maxSlope*overallScale
	first = True
	for (n,bz) in enumerate(icu.bezierPoints):
		x1 = bz.pt[0]
		y1 = bz.pt[1]
		if first:
			first = False
		else:
			slope = (y1-y0)/(x1-x0)
			if slope > maxScaledSlope:
				print (x0,y0), (x1, y1), " to "
				x2 = (x0+x1)/2
				y2 = (y0+y1)/2
				y0 += (slope-maxScaledSlope)*(x2-x0)
				y1 -= (slope-maxScaledSlope)*(x1-x2)
				icu.bezierPoints[n].pt = [x1,y1]
				icu.bezierPoints[n-1].pt = [x0,y0]
				print "   ", (x0,y0), (x1, y1)
		x0 = x1
		y0 = y1
	icu.recalc()
	

def dampenIpo(ipo):
	dampenIcu(ipo[Ipo.PO_LOCX])
	dampenIcu(ipo[Ipo.PO_LOCZ])

def dampenAction():
	for ob in Object.GetSelected():
		if (ob.type == 'Armature'):
			act = ob.getAction()
			ipos = act.getAllChannelIpos()
			dampenIpo(ipos['PMouth'])
			dampenIpo(ipos['PUpLip'])
			dampenIpo(ipos['PLoLip'])
			dampenIpo(ipos['PJaw'])
			dampenIpo(ipos['PTongue'])
			Draw.PupMenu("Action %s dampened with max slope %f" % (act.name, maxSlope))
	return

#
#	User interface
#

def event(evt, val):   
	if not val:  # val = 0: it's a key/mbutton release
		if evt in [Draw.LEFTMOUSE, Draw.MIDDLEMOUSE, Draw.RIGHTMOUSE]:
			Draw.Redraw(-1)
		return
	if evt == Draw.ESCKEY:
		Draw.Exit()               
		return
	else: 
		return
	Draw.Redraw(-1)

toggleNewAction = 1

def button_event(evt): 
	global toggleNewAction
	if evt == 1:
		setViseme('rest')
	elif evt == 2:
		setViseme('etc')
	elif evt == 3:
		setViseme('MBP')
	elif evt == 4:
		setViseme('OO')
	elif evt == 5:
		setViseme('O')
	elif evt == 6:
		setViseme('R')
	elif evt == 7:
		setViseme('FV')
	elif evt == 8:
		setViseme('S')
	elif evt == 9:
		setViseme('SH')
	elif evt == 10:
		setViseme('EE')
	elif evt == 11:
		setViseme('AH')
	elif evt == 12:
		setViseme('EH')
	elif evt == 13:
		setViseme('TH')
	elif evt == 14:
		setViseme('L')
	elif evt == 15:
		setViseme('G')

	elif evt == 41:
		setViseme('blink')
	elif evt == 42:
		setViseme('unblink')

	elif evt == 21:
		Window.FileSelector (loadMoho, 'OPEN DAT FILE')
	elif evt == 22:
		Window.FileSelector (loadMagpie, 'OPEN MAG FILE')
	elif evt == 23:
		toggleNewAction = 1 - toggleNewAction
	elif evt == 31:
		dampenAction()
	elif evt == 40:
		Draw.Exit()
		return
	Draw.Redraw(-1)

def numEvent(evt, val):
	global maxSlope, startFrame
	if evt == 24:
		startFrame = val
	elif evt == 32:
		maxSlope = val
	Draw.Redraw(-1)

def gui():
	global maxSlope, toggleNewAction
	BGL.glClearColor(1,1,0.5,1)
	BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
	BGL.glColor3f(0,0,0)

	BGL.glRasterPos2i(10,1510)
	Draw.Text("MHX LiPMouth for Blender", "large")
	Draw.PushButton('rest', 1, 10, 430, 70, 20)
	Draw.PushButton('etc', 2, 10, 400, 70, 20)
	Draw.PushButton('MBP', 3, 10, 370, 70, 20)
	Draw.PushButton('OO', 4, 10, 340, 70, 20)
	Draw.PushButton('O', 5, 10, 310, 70, 20)
	Draw.PushButton('R', 6, 10, 280, 70, 20)
	Draw.PushButton('FV', 7, 10, 250, 70, 20)
	Draw.PushButton('S', 8, 10, 220, 70, 20)
	Draw.PushButton('SH', 9, 10, 190, 70, 20)
	Draw.PushButton('EE', 10, 10, 160, 70, 20)
	Draw.PushButton('AH', 11, 10, 130, 70, 20)
	Draw.PushButton('EH', 12, 10, 100, 70, 20)
	Draw.PushButton('TH', 13, 10, 70, 70, 20)
	Draw.PushButton('L' , 14, 10, 40, 70, 20)
	Draw.PushButton('G', 15, 10, 10, 70, 20)

	Draw.PushButton('Blink', 41, 110, 430, 70, 20)
	Draw.PushButton('Unblink', 42, 110, 400, 70, 20)

	Draw.PushButton('Moho', 21, 110, 250, 70, 20)
	Draw.PushButton('Magpie', 22, 110, 220, 70, 20)
	Draw.Toggle("New action", 23, 110, 190, 90, 20, toggleNewAction)
	bstartFrame = Draw.Create(startFrame)
	bstartFrame = Draw.Number('Start frame: ', 24, 110,160, 150, 20, bstartFrame.val, 0,1000, 'Max slope for dampening', numEvent )

	Draw.PushButton('Damping', 31, 110, 100, 70, 20)
	bmaxSlope = Draw.Create(maxSlope)
	bmaxSlope = Draw.Number('Max slope: ', 32, 110, 70, 150, 20, bmaxSlope.val, 0,10, 'Max slope for dampening', numEvent )

	Draw.PushButton('Exit', 40, 110, 10, 70, 20)
	
Draw.Register(gui, event, button_event) 
	
	
	

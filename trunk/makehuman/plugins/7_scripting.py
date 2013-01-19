#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Joel Palmius

**Copyright(c):**      MakeHuman Team 2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

# We need this for gui controls
import gui3d
import mh
import humanmodifier
import gui
import log
import os
from cStringIO import StringIO
from core import G
import glmodule
from PyQt4 import QtGui

class ScriptingView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Scripting')

        self.directory = os.getcwd()
        self.filename =  None

        box = self.addLeftWidget(gui.GroupBox('Script'))

        self.scriptText = self.addTopWidget(gui.DocumentEdit())
        self.scriptText.setText('');

        self.scriptText.setLineWrapMode(QtGui.QTextEdit.NoWrap)

        self.loadButton = box.addWidget(gui.Button('Load ...'), 0, 0)
        self.saveButton = box.addWidget(gui.Button('Save ...'), 0, 1)

        @self.loadButton.mhEvent
        def onClicked(event):
            filename = mh.getOpenFileName(self.directory, 'Python scripts (*.py);;All files (*.*)')
            if(os.path.exists(filename)):
                contents = open(filename, 'r').read()
                self.scriptText.setText(contents)
                dlg = gui.Dialog()
                dlg.prompt("Load script","File was loaded in an acceptable manner","OK")
                self.filename = filename
                self.directory = os.path.split(filename)[0]
            else:
                dlg = gui.Dialog()
                dlg.prompt("Load script","File " + filename + " does not seem to exist","OK")

        @self.saveButton.mhEvent
        def onClicked(event):
            filename = mh.getSaveFileName(self.filename or self.directory, 'Python scripts (*.py);;All files (*.*)')
            with open(filename, "w") as f:
                f.write(self.scriptText.toPlainText())
            dlg = gui.Dialog()
            dlg.prompt("Save script","File was written in an acceptable manner","OK")
            self.filename = filename
            self.directory = os.path.split(filename)[0]

        box2 = self.addLeftWidget(gui.GroupBox('Examples'))

        self.insertLabel = box2.addWidget(gui.TextView('Append example to script'))
        self.listView = box2.addWidget(gui.ListView())
        self.listView.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)

        testlist = [ 
            'applyTarget()', 
            'incrementingFilename()',
            'loadModel()',
            'saveModel()',
            'screenShot()',
            'setAge()',
            'printDetailStack()',
            'setWeight()'
        ]

        self.listView.setData(testlist)

        self.insertButton = box2.addWidget(gui.Button('Append'))

        @self.insertButton.mhEvent
        def onClicked(event):
            item = self.listView.getSelectedItem()

            if(item == 'applyTarget()'):
                text = "# applyTarget(<target file name>, <power (from 0.0 to 1.0)>)\n"
                text = text + "#\n"
                text = text + "# This will apply the target on the model. If the target was already applied, the power will be updated\n"
                text = text + "# Note that targets are relative to the data/targets directory, and should not include the .target\n"
                text = text + "# extension, so a valid target name would be, for example, \"breast/breast-dist-max\"\n\n"
                text = text + "MHScript.applyTarget('aTargetName',1.0)\n\n"
                self.scriptText.addText(text)

            if(item == 'loadModel()'):
                text = "# loadModel(<model name>,[path])\n"
                text = text + "#\n"
                text = text + "# This will load a human model from an MHM file. The <model name> part should be a string without spaces\n"
                text = text + "# and without the .MHM extension. The [path] part defaults to the user's makehuman/models directory.\n\n"
                text = text + "MHScript.loadModel('myTestModel')\n\n"
                self.scriptText.addText(text)

            if(item == 'incrementingFilename()'):
                text = "# incrementingFilename(<file name base>, [file extension], [pad length])\n"
                text = text + "#\n"
                text = text + "# This will return a file name containing a numerical component which increases by one for each call.\n"
                text = text + "# The default file extension is \".png\". The default pad length is 4. For example, the following lines:\n";
                text = text + "#\n"
                text = text + "# print incrementingFilename(\"test\",\".target\",3) + \"\\n\"\n"
                text = text + "# print incrementingFilename(\"test\",\".target\",3) + \"\\n\"\n"
                text = text + "#\n"
                text = text + "# Will print:\n"
                text = text + "#\n"
                text = text + "# test001.target\n"
                text = text + "# test002.target\n"
                text = text + "#\n"
                text = text + "# The counter is reset each time the script is executed\n\n"
                text = text + "filename = MHScript.incrementingFilename('test')\n\n"
                self.scriptText.addText(text)

            if(item == 'printDetailStack()'):
                text = "# printDetailStack()\n"
                text = text + "#\n"
                text = text + "# This will print a list of all applied targets (and their weights) to standard output.\n\n"
                text = text + "MHScript.printDetailStack()\n\n"
                self.scriptText.addText(text)

            if(item == 'saveModel()'):
                text = "# saveModel(<model name>,[path])\n"
                text = text + "#\n"
                text = text + "# This will save the human model to an MHM file. The <model name> part should be a string without spaces\n"
                text = text + "# and without the .MHM extension. The [path] part defaults to the user's makehuman/models directory.\n"
                text = text + "# Note that this will not save any thumbnail.\n\n"
                text = text + "MHScript.saveModel('myTestModel')\n\n"
                self.scriptText.addText(text)

            if(item == 'screenShot()'):
                text = "# screenShot(<png file name>)\n"
                text = text + "#\n"
                text = text + "# This will save a png file of how the model currently looks.\n\n"
                text = text + "MHScript.screenShot('screenshot.png')\n\n"
                self.scriptText.addText(text)

            if(item == 'setAge()'):
                text = "# setAge(age)\n"
                text = text + "#\n"
                text = text + "# Sets the age of the model. The age parameter is a float between 0 and 1, where 0 is 12 years old and 1 is 70.\n\n"
                text = text + "MHScript.setAge(0.5)\n\n"
                self.scriptText.addText(text)

            if(item == 'setWeight()'):
                text = "# setWeight(weight)\n"
                text = text + "#\n"
                text = text + "# Sets the weight of the model. The weight parameter is a float between 0 and 1, where 0 is starved and\n"
                text = text + "# 1 is severely overweight\n\n"
                text = text + "MHScript.setWeight(0.5)\n\n"
                self.scriptText.addText(text)

        # human = gui3d.app.selectedHuman
        # human.applyAllTargets()
        
    def onShow(self, event):
        gui3d.app.statusPersist('This is a rough scripting module')

    def onHide(self, event):
        gui3d.app.statusPersist('')

class ScriptingExecuteTab(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Execute')

        box = self.addLeftWidget(gui.GroupBox('Execute'))

        self.execButton = box.addWidget(gui.Button('Execute'))

        @self.execButton.mhEvent
        def onClicked(event):
            width = G.windowWidth;
            height = G.windowHeight;
            print "width=" + str(width) + " height=" + str(height) + "\n";

            global MHScript
            global scriptingView

            MHScript = Scripting()
            executeScript(str(scriptingView.scriptText.toPlainText()))

class Scripting():
    def __init__(self):
        self.human = gui3d.app.selectedHuman
        self.fileIncrement = 0;
        self.modelPath = mh.getPath('models')
        if(not os.path.exists(self.modelPath)):
            os.makedirs(self.modelPath)

    def applyTarget(self,targetName,power):
        log.message("SCRIPT: applyTarget(" + targetName + ", " + str(power) + ")")
        self.human.setDetail("data/targets/" + targetName + ".target",power)
        self.human.applyAllTargets()
        glmodule.draw()

    def saveModel(self,name,path = mh.getPath('models')):
        log.message("SCRIPT: saveModel(" + name + "," + path + ")")
        filename = os.path.join(path,name + ".mhm")
        self.human.save(filename,name)

    def loadModel(self,name,path = mh.getPath('models')):
        log.message("SCRIPT: loadModel(" + name + "," + path + ")")
        filename = os.path.join(path,name + ".mhm")
        self.human.load(filename, True, gui3d.app.progress)

    def screenShot(self,fileName):
        log.message("SCRIPT: screenShot(" + fileName + ")")
        width = G.windowWidth;
        height = G.windowHeight;
        width = width - 3;
        height = height - 3;
        mh.grabScreen(1,1,width,height,fileName)

    def incrementingFilename(self,basename,suffix=".png",width=4):
        fn = basename;
        i = width - 1;
        self.fileIncrement += 1
        while(i > 0):       
            power = 10**i;
            if(self.fileIncrement < power):
                fn = fn + "0";
            i -= 1
        fn = fn + str(self.fileIncrement) + suffix
        return fn        

    def printDetailStack(self):
        log.message("SCRIPT: printDetailStack()")
        for target in self.human.targetsDetailStack.keys():
		print str(self.human.targetsDetailStack[target]) + "\t" + target

    def setAge(self,age):
        log.message("SCRIPT: setAge(" + str(age) + ")")
        self.human.setAge(age)
        humanmodifier.MacroModifier('macrodetails', None, 'Age', 0.0, 1.0).setValue(gui3d.app.selectedHuman, age)
        self.human.applyAllTargets()
        glmodule.draw()

    def setWeight(self,weight):
        log.message("SCRIPT: setWeight(" + str(weight) + ")")
        self.human.setWeight(weight)
        humanmodifier.MacroModifier('macrodetails', 'universal', 'Weight', 0.0, 1.0).setValue(gui3d.app.selectedHuman, weight)
        self.human.applyAllTargets()
        glmodule.draw()

MHScript = None

def executeScript(scriptSource):
    print scriptSource
    try:
        exec(scriptSource)
        dlg = gui.Dialog()
        dlg.prompt("Good job!","The script was executed without problems.","OK")
    except Exception as e:
        log.error(e, exc_info = True)
        dlg = gui.Dialog()
        dlg.prompt("Crappy script","The script produced an exception: " + format(str(e)),"OK")

scriptingView = None

def load(app):

    global scriptingView

    category = app.getCategory('Scripting')
    scriptingView = ScriptingView(category)
    executeView = ScriptingExecuteTab(category)
    taskview = category.addTask(scriptingView)
    taskview1 = category.addTask(executeView)

def unload(app):
    pass



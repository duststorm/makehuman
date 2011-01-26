#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

from gui3d import TextObject
from datetime import datetime
from threading import Thread
from time import sleep

class ClockThread(Thread):

    def __init__(self, clockText):
    
        Thread.__init__(self)
        self.clockText = clockText
    
    def run(self):

        while 1:
            sleep(1)
            self.clockText.setText(datetime.now().strftime("%H:%M:%S"))
            self.clockText.app.redraw()

print 'clock imported'

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements

clockThread = None

def load(app):
    clockText = TextObject(app, position=[740, 10, 9.2])
    clockText.setText(datetime.now().strftime("%H:%M:%S"))
    clockThread = ClockThread(clockText)
    clockThread.start()

    print 'clock loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):
    print 'clock unloaded'



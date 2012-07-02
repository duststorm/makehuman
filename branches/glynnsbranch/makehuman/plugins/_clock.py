#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

from gui3d import TextObject
from datetime import datetime
from threading import Thread
from time import sleep
from mh import callAsync

class ClockThread(Thread):

    def __init__(self, method):
    
        Thread.__init__(self)
        self.method = method
        self.running = True
    
    def run(self):

        while self.running:
            sleep(1)
            callAsync(self.method)

print 'clock imported'

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements

clockThread = None

def load(app):
    
    clockText = TextObject(app, position=[740, 10, 9.2])
    clockText.setText(datetime.now().strftime("%H:%M:%S"))
    
    def updateClock():
        clockText.setText(datetime.now().strftime("%H:%M:%S"))
        clockText.app.redraw()
          
    global clockThread
    clockThread = ClockThread(updateClock)
    clockThread.start()

    print 'clock loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):
    
    global clockThread
    clockThread.running = False
    clockThread.join()
        
    print 'clock unloaded'



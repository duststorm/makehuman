#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, mh, os, module3d
import qtgui as gui

class FontRadioButton(gui.RadioButton):

    def __init__(self, group, font):
    
        super(FontRadioButton, self).__init__(group, font.capitalize(), gui3d.app.settings.get('font', 'arial') == font, style=gui3d.RadioButtonStyle._replace(fontFamily=font))
        self.font = font
        
    def onClicked(self, event):
    
        gui3d.app.settings['font'] = self.font
        gui3d.app.prompt('Info', 'You need to restart for your font changes to be applied.', 'OK', helpId='fontHelp')
        
class LanguageRadioButton(gui.RadioButton):

    def __init__(self, group, language):
    
        super(LanguageRadioButton, self).__init__(group, language.capitalize(), gui3d.app.settings.get('language', 'english') == language)
        self.language = language
        
    def onClicked(self, event):
    
        gui3d.app.settings['language'] = self.language
        gui3d.app.setLanguage(self.language)
        gui3d.app.prompt('Info', 'You need to restart for your language changes to be applied.', 'OK', helpId='languageHelp')  

class SettingsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Settings')

        self.shaderGroup = []
        shaderBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Shader')))
        self.shaderNo = shaderBox.addWidget(gui.RadioButton(self.shaderGroup, "No shader", True))
        self.shaderPhong = shaderBox.addWidget(gui.RadioButton(self.shaderGroup, "Phong shader"))
        self.shaderToon = shaderBox.addWidget(gui.RadioButton(self.shaderGroup, "Toon shader"))
        #self.shaderSkin = shaderBox.addWidget(gui.RadioButton(self.shaderGroup, "Skin shader"))
        
        sliderBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Slider behavior')))
        self.realtimeUpdates = sliderBox.addWidget(gui.CheckBox("Update real-time",
            gui3d.app.settings.get('realtimeUpdates', True)))
        self.realtimeNormalUpdates = sliderBox.addWidget(gui.CheckBox("Update normals",
            gui3d.app.settings.get('realtimeNormalUpdates', True)))
            
        mouseBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Mouse behavior')))
        self.normal = mouseBox.addWidget(gui.Slider(gui3d.app.settings.get('lowspeed', 1), 1, 10,
            "Normal: %d"))
        self.shift = mouseBox.addWidget(gui.Slider(gui3d.app.settings.get('highspeed', 5), 1, 10,
            "Shift: %d"))
            
        modes = [] 
               
        unitBox = self.unitsBox = self.addWidget(mh.addWidget(mh.Frame.LeftTop, gui.GroupBox('Units')))
        metric = unitBox.addWidget(gui.RadioButton(modes, 'Metric', gui3d.app.settings.get('units', 'metric') == 'metric'))
        imperial = unitBox.addWidget(gui.RadioButton(modes, 'Imperial', gui3d.app.settings.get('units', 'metric') == 'imperial'))
        
        fonts = []
        
        fontsBox = self.fontsBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Font')))
        
        fontFiles = [os.path.basename(filename).replace('.fnt', '') for filename in os.listdir('data/fonts') if filename.split(os.extsep)[-1] == "fnt"]
        for font in fontFiles:
            fontsBox.addWidget(FontRadioButton(fonts, font))
        
        languages = []
        
        languageBox = self.languageBox = self.addWidget(mh.addWidget(mh.Frame.RightTop, gui.GroupBox('Language')))
        languageBox.addWidget(LanguageRadioButton(languages, 'english'))
        
        languageFiles = [os.path.basename(filename).replace('.ini', '') for filename in os.listdir('data/languages') if filename.split(os.extsep)[-1] == "ini"]
        for language in languageFiles:
            languageBox.addWidget(LanguageRadioButton(languages, language))
        
        @self.shaderNo.mhEvent
        def onClicked(event):
            human = gui3d.app.selectedHuman
            human.mesh.setShader(0)
            
        @self.shaderPhong.mhEvent
        def onClicked(event):
            self.setShader("data/shaders/glsl/phong_vertex_shader.txt", "data/shaders/glsl/phong_fragment_shader.txt")
                
        @self.shaderToon.mhEvent
        def onClicked(event):
            self.setShader("data/shaders/glsl/toon_vertex_shader.txt", "data/shaders/glsl/toon_fragment_shader.txt")
            
        #@self.shaderSkin.mhEvent
        #def onClicked(event):
            #self.setShader("data/shaders/glsl/skin_vertex_shader.txt", "data/shaders/glsl/skin_fragment_shader.txt")
            #gui3d.app.selectedHuman.mesh.setShaderParameter("gradientMap", module3d.getTexture("data/textures/color_temperature.png").textureId)
            #gui3d.app.selectedHuman.mesh.setShaderParameter("ambientOcclusionMap", module3d.getTexture("data/textures/female_young.tif").textureId)
                
        @self.realtimeUpdates.mhEvent
        def onClicked(event):
            gui3d.app.settings['realtimeUpdates'] = self.realtimeUpdates.selected
            
        @self.realtimeNormalUpdates.mhEvent
        def onClicked(event):
            gui3d.app.settings['realtimeNormalUpdates'] = self.realtimeNormalUpdates.selected
            
        @self.normal.mhEvent
        def onChange(value):
            gui3d.app.settings['lowspeed'] = value
            
        @self.shift.mhEvent
        def onChange(value):
            gui3d.app.settings['highspeed'] = value
            
        @metric.mhEvent
        def onClicked(event):
            gui3d.app.settings['units'] = 'metric'
            
        @imperial.mhEvent
        def onClicked(event):
            gui3d.app.settings['units'] = 'imperial'
                
    def setShader(self, vertex, fragment):
            human = gui3d.app.selectedHuman
            try:
                human.vertex_shader = mh.createVertexShader(open(vertex).read())
                human.fragment_shader = mh.createFragmentShader(open(fragment).read())
                human.shader_program = mh.createShader(human.vertex_shader, human.fragment_shader)
                human.mesh.setShader(human.shader_program)
            except Exception, e:
                print "No shader support: " + str(e)
    
    def onShow(self, event):
    
        gui3d.TaskView.onShow(self, event)
        self.shaderNo.setFocus()
    
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()
        
    def onResized(self, event):
        
        self.fontsBox.setPosition([event.width - 150, self.fontsBox.getPosition()[1], 9.0])
        self.languageBox.setPosition([event.width - 150, self.languageBox.getPosition()[1], 9.0])

def load(app):
    category = app.getCategory('Settings')
    taskview = category.addView(SettingsTaskView(category))
    print 'Settings imported'

def unload(app):
    pass



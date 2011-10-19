#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, mh, os

class LanguageRadioButton(gui3d.RadioButton):

    def __init__(self, parent, group, language):
    
        gui3d.RadioButton.__init__(self, parent, group, language.capitalize(), parent.app.settings.get('language', 'english') == language)
        self.language = language
        
    def onClicked(self, event):
    
        gui3d.RadioButton.onClicked(self, event)
        self.app.settings['language'] = self.language
        self.app.setLanguage(self.language)
        self.app.prompt('Info', 'You need to restart for your language changes to be applied.', 'OK', helpId='languageHelp')  

class SettingsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Settings')

        self.shaderGroup = []
        y = 80
        shaderBox = gui3d.GroupBox(self, [10, y, 9.0], 'Shader');y+=25
        self.shaderNo = gui3d.RadioButton(shaderBox, self.shaderGroup, "No shader", True);y+=24
        self.shaderPhong = gui3d.RadioButton(shaderBox, self.shaderGroup, "Phong shader");y+=24
        self.shaderToon = gui3d.RadioButton(shaderBox, self.shaderGroup, "Toon shader");y+=24
        self.shaderSkin = gui3d.RadioButton(shaderBox, self.shaderGroup, "Skin shader");y+=24
        y+=16
        
        sliderBox = gui3d.GroupBox(self, [10, y, 9.0], 'Slider behavior');y+=25
        self.realtimeUpdates = gui3d.CheckBox(sliderBox, "Update real-time",
            self.app.settings.get('realtimeUpdates', True));y+=24
        self.realtimeNormalUpdates = gui3d.CheckBox(sliderBox, "Update normals",
            self.app.settings.get('realtimeNormalUpdates', True));y+=24
        y+=16
            
        mouseBox = gui3d.GroupBox(self, [10, y, 9.0], 'Mouse behavior');y+=25
        self.normal = gui3d.Slider(mouseBox,
            self.app.settings.get('lowspeed', 1), 1, 10,
            "Normal: %d");y+=36
        self.shift = gui3d.Slider(mouseBox,
            self.app.settings.get('highspeed', 5), 1, 10,
            "Shift: %d");y+=36
        y+=16
            
        modes = [] 
               
        unitBox = self.unitsBox = gui3d.GroupBox(self, [10, y, 9.0], 'Units');y += 25
        metric = gui3d.RadioButton(unitBox, modes, 'Metric', self.app.settings.get('units', 'metric') == 'metric');y += 24
        imperial = gui3d.RadioButton(unitBox, modes, 'Imperial', self.app.settings.get('units', 'metric') == 'imperial');y += 24
        y+=16
        
        fonts = []
        
        y = 80
        unitBox = self.unitsBox = gui3d.GroupBox(self, [650, y, 9.0], 'Font');y += 25
        arial = gui3d.RadioButton(unitBox, fonts, 'Arial', self.app.settings.get('font', 'arial') == 'arial', style=gui3d.RadioButtonStyle._replace(fontFamily='arial'));y += 24
        courier = gui3d.RadioButton(unitBox, fonts, 'Courier', self.app.settings.get('font', 'arial') == 'courier', style=gui3d.RadioButtonStyle._replace(fontFamily='courier'));y += 24
        ubuntu = gui3d.RadioButton(unitBox, fonts, 'Ubuntu', self.app.settings.get('font', 'arial') == 'ubuntu', style=gui3d.RadioButtonStyle._replace(fontFamily='ubuntu'));y += 24
        verdana = gui3d.RadioButton(unitBox, fonts, 'Verdana', self.app.settings.get('font', 'arial') == 'verdana', style=gui3d.RadioButtonStyle._replace(fontFamily='verdana'));y += 24
        y+=16
        
        languages = []
        
        languageBox = self.languageBox = gui3d.GroupBox(self, [650, y, 9.0], 'Language');y += 25
        LanguageRadioButton(languageBox, languages, 'english');y += 24
        
        languageFiles = [os.path.basename(filename).replace('.ini', '') for filename in os.listdir('data/languages') if filename.split(os.extsep)[-1] == "ini"]
        for language in languageFiles:
            LanguageRadioButton(languageBox, languages, language);y += 24
        
        @self.shaderNo.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderNo, event)
            human = self.app.selectedHuman
            human.mesh.setShader(0)
            
        @self.shaderPhong.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderPhong, event)
            self.setShader("data/shaders/glsl/phong_vertex_shader.txt", "data/shaders/glsl/phong_fragment_shader.txt")
                
        @self.shaderToon.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderToon, event)
            self.setShader("data/shaders/glsl/toon_vertex_shader.txt", "data/shaders/glsl/toon_fragment_shader.txt")
            
        @self.shaderSkin.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderSkin, event)
            self.setShader("data/shaders/glsl/skin_vertex_shader.txt", "data/shaders/glsl/skin_fragment_shader.txt")
            self.app.selectedHuman.mesh.setShaderParameter("gradientMap", mh.loadTexture("data/textures/color_temperature.png", 0))
            self.app.selectedHuman.mesh.setShaderParameter("ambientOcclusionMap", mh.loadTexture("data/textures/female_young.tif", 0))
                
        @self.realtimeUpdates.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.realtimeUpdates, event)
            self.app.settings['realtimeUpdates'] = self.realtimeUpdates.selected
            
        @self.realtimeNormalUpdates.event
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.realtimeNormalUpdates, event)
            self.app.settings['realtimeNormalUpdates'] = self.realtimeNormalUpdates.selected
            
        @self.normal.event
        def onChange(value):
            self.app.settings['lowspeed'] = value
            
        @self.shift.event
        def onChange(value):
            self.app.settings['highspeed'] = value
            
        @metric.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(metric, event)
            self.app.settings['units'] = 'metric'
            
        @imperial.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(imperial, event)
            self.app.settings['units'] = 'imperial'
            
        @arial.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(arial, event)
            self.app.settings['font'] = 'arial'
            self.app.prompt('Info', 'You need to restart for your font changes to be applied.',
                'OK', helpId='fontHelp')
            
        @courier.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(courier, event)
            self.app.settings['font'] = 'courier'
            self.app.prompt('Info', 'You need to restart for your font changes to be applied.',
                'OK', helpId='fontHelp')
            
        @ubuntu.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(ubuntu, event)
            self.app.settings['font'] = 'ubuntu'
            self.app.prompt('Info', 'You need to restart for your font changes to be applied.',
                'OK', helpId='fontHelp')
            
        @verdana.event
        def onClicked(event):
            gui3d.RadioButton.onClicked(verdana, event)
            self.app.settings['font'] = 'verdana'
            self.app.prompt('Info', 'You need to restart for your font changes to be applied.',
                'OK', helpId='fontHelp')
                
    def setShader(self, vertex, fragment):
            human = self.app.selectedHuman
            try:
                human.vertex_shader = mh.createVertexShader(open(vertex).read())
                human.fragment_shader = mh.createFragmentShader(open(fragment).read())
                human.shader_program = mh.createShader(human.vertex_shader, human.fragment_shader)
                human.mesh.setShader(human.shader_program)
            except Exception, e:
                print "No shader support: " + str(e)
                
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        self.app.saveSettings()

def load(app):
    category = app.getCategory('Settings')
    taskview = SettingsTaskView(category)
    print 'Settings imported'

def unload(app):
    pass



#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, mh, os, module3d

class FontRadioButton(gui3d.RadioButton):

    def __init__(self, group, font):
    
        gui3d.RadioButton.__init__(self, group, font.capitalize(), gui3d.app.settings.get('font', 'arial') == font, style=gui3d.RadioButtonStyle._replace(fontFamily=font))
        self.font = font
        
    def onClicked(self, event):
    
        gui3d.RadioButton.onClicked(self, event)
        gui3d.app.settings['font'] = self.font
        gui3d.app.prompt('Info', 'You need to restart for your font changes to be applied.', 'OK', helpId='fontHelp')
        
class LanguageRadioButton(gui3d.RadioButton):

    def __init__(self, group, language):
    
        gui3d.RadioButton.__init__(self, group, language.capitalize(), gui3d.app.settings.get('language', 'english') == language)
        self.language = language
        
    def onClicked(self, event):
    
        gui3d.RadioButton.onClicked(self, event)
        gui3d.app.settings['language'] = self.language
        gui3d.app.setLanguage(self.language)
        gui3d.app.prompt('Info', 'You need to restart for your language changes to be applied.', 'OK', helpId='languageHelp')  

class SettingsTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Settings')

        self.shaderGroup = []
        y = 80
        shaderBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Shader'));y+=25
        self.shaderNo = shaderBox.addView(gui3d.RadioButton(self.shaderGroup, "No shader", True));y+=24
        self.shaderPhong = shaderBox.addView(gui3d.RadioButton(self.shaderGroup, "Phong shader"));y+=24
        self.shaderToon = shaderBox.addView(gui3d.RadioButton(self.shaderGroup, "Toon shader"));y+=24
        #self.shaderSkin = shaderBox.addView(gui3d.RadioButton(self.shaderGroup, "Skin shader"));y+=24
        y+=16
        
        sliderBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Slider behavior'));y+=25
        self.realtimeUpdates = sliderBox.addView(gui3d.CheckBox("Update real-time",
            gui3d.app.settings.get('realtimeUpdates', True)));y+=24
        self.realtimeNormalUpdates = sliderBox.addView(gui3d.CheckBox("Update normals",
            gui3d.app.settings.get('realtimeNormalUpdates', True)));y+=24
        y+=16
            
        mouseBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Mouse behavior'));y+=25
        self.normal = mouseBox.addView(gui3d.Slider(gui3d.app.settings.get('lowspeed', 1), 1, 10,
            "Normal: %d"));y+=36
        self.shift = mouseBox.addView(gui3d.Slider(gui3d.app.settings.get('highspeed', 5), 1, 10,
            "Shift: %d"));y+=36
        y+=16
            
        modes = [] 
               
        unitBox = self.unitsBox = self.addView(gui3d.GroupBox([10, y, 9.0], 'Units'));y += 25
        metric = unitBox.addView(gui3d.RadioButton(modes, 'Metric', gui3d.app.settings.get('units', 'metric') == 'metric'));y += 24
        imperial = unitBox.addView(gui3d.RadioButton(modes, 'Imperial', gui3d.app.settings.get('units', 'metric') == 'imperial'));y += 24
        y+=16
        
        fonts = []
        
        y = 80
        fontsBox = self.fontsBox = self.addView(gui3d.GroupBox([650, y, 9.0], 'Font'));y += 25
        
        fontFiles = [os.path.basename(filename).replace('.fnt', '') for filename in os.listdir('data/fonts') if filename.split(os.extsep)[-1] == "fnt"]
        for font in fontFiles:
            fontsBox.addView(FontRadioButton(fonts, font));y += 24
        y+=16
        
        languages = []
        
        languageBox = self.languageBox = self.addView(gui3d.GroupBox([650, y, 9.0], 'Language'));y += 25
        languageBox.addView(LanguageRadioButton(languages, 'english'));y += 24
        
        languageFiles = [os.path.basename(filename).replace('.ini', '') for filename in os.listdir('data/languages') if filename.split(os.extsep)[-1] == "ini"]
        for language in languageFiles:
            languageBox.addView(LanguageRadioButton(languages, language));y += 24
        
        @self.shaderNo.mhEvent
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderNo, event)
            human = gui3d.app.selectedHuman
            human.mesh.setShader(0)
            
        @self.shaderPhong.mhEvent
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderPhong, event)
            self.setShader("data/shaders/glsl/phong_vertex_shader.txt", "data/shaders/glsl/phong_fragment_shader.txt")
                
        @self.shaderToon.mhEvent
        def onClicked(event):
            gui3d.RadioButton.onClicked(self.shaderToon, event)
            self.setShader("data/shaders/glsl/toon_vertex_shader.txt", "data/shaders/glsl/toon_fragment_shader.txt")
            
        #@self.shaderSkin.mhEvent
        #def onClicked(event):
            #gui3d.RadioButton.onClicked(self.shaderSkin, event)
            #self.setShader("data/shaders/glsl/skin_vertex_shader.txt", "data/shaders/glsl/skin_fragment_shader.txt")
            #gui3d.app.selectedHuman.mesh.setShaderParameter("gradientMap", module3d.getTexture("data/textures/color_temperature.png").textureId)
            #gui3d.app.selectedHuman.mesh.setShaderParameter("ambientOcclusionMap", module3d.getTexture("data/textures/female_young.tif").textureId)
                
        @self.realtimeUpdates.mhEvent
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.realtimeUpdates, event)
            gui3d.app.settings['realtimeUpdates'] = self.realtimeUpdates.selected
            
        @self.realtimeNormalUpdates.mhEvent
        def onClicked(event):
            gui3d.ToggleButton.onClicked(self.realtimeNormalUpdates, event)
            gui3d.app.settings['realtimeNormalUpdates'] = self.realtimeNormalUpdates.selected
            
        @self.normal.mhEvent
        def onChange(value):
            gui3d.app.settings['lowspeed'] = value
            
        @self.shift.mhEvent
        def onChange(value):
            gui3d.app.settings['highspeed'] = value
            
        @metric.mhEvent
        def onClicked(event):
            gui3d.RadioButton.onClicked(metric, event)
            gui3d.app.settings['units'] = 'metric'
            
        @imperial.mhEvent
        def onClicked(event):
            gui3d.RadioButton.onClicked(imperial, event)
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



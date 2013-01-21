#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import mh
import gui3d
import gui
import log

class FontRadioButton(gui.RadioButton):

    def __init__(self, group, font):
    
        super(FontRadioButton, self).__init__(group, font.capitalize(), gui3d.app.settings.get('font', 'Ubuntu') == font)
        self.font = font
        
    def onClicked(self, event):
        gui3d.app.settings['font'] = self.font
        gui3d.app.setFont(self.font)

class ThemeRadioButton(gui.RadioButton):

    def __init__(self, group, label, theme):
    
        self.theme = theme
        checked = (gui3d.app.settings.get('guiTheme', 'makehuman') == self.theme)
        super(ThemeRadioButton, self).__init__(group, label, checked)
        
    def onClicked(self, event):
        gui3d.app.settings['guiTheme'] = self.theme
        gui3d.app.setTheme(self.theme)

class PlatformRadioButton(gui.RadioButton):

    def __init__(self, group, looknfeel):
    
        super(PlatformRadioButton, self).__init__(group, looknfeel, gui3d.app.getLookAndFeel().lower() == looknfeel.lower())
        self.looknfeel = looknfeel
        
    def onClicked(self, event):
        gui3d.app.setLookAndFeel(self.looknfeel)
        
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
        shaderBox = self.addLeftWidget(gui.GroupBox('Shader'))
        self.shaderNo = shaderBox.addWidget(gui.RadioButton(self.shaderGroup, "No shader", True))
        self.shaderPhong = shaderBox.addWidget(gui.RadioButton(self.shaderGroup, "Phong shader"))
        self.shaderToon = shaderBox.addWidget(gui.RadioButton(self.shaderGroup, "Toon shader"))
        #self.shaderSkin = shaderBox.addWidget(gui.RadioButton(self.shaderGroup, "Skin shader"))
        
        sliderBox = self.addLeftWidget(gui.GroupBox('Slider behavior'))
        self.realtimeUpdates = sliderBox.addWidget(gui.CheckBox("Update real-time",
            gui3d.app.settings.get('realtimeUpdates', True)))
        self.realtimeNormalUpdates = sliderBox.addWidget(gui.CheckBox("Update normals",
            gui3d.app.settings.get('realtimeNormalUpdates', True)))
        self.cameraAutoZoom = sliderBox.addWidget(gui.CheckBox("Auto-zoom camera",
            gui3d.app.settings.get('cameraAutoZoom', True)))
        self.sliderImages = sliderBox.addWidget(gui.CheckBox("Slider images",
            gui3d.app.settings.get('sliderImages', True)))
            
        mouseBox = self.addLeftWidget(gui.SliderBox('Mouse behavior'))
        self.normal = mouseBox.addWidget(gui.Slider(gui3d.app.settings.get('lowspeed', 1), 1, 10,
            "Normal: %d"))
        self.shift = mouseBox.addWidget(gui.Slider(gui3d.app.settings.get('highspeed', 5), 1, 10,
            "Shift: %d"))
            
        modes = [] 
        unitBox = self.unitsBox = self.addLeftWidget(gui.GroupBox('Units'))
        metric = unitBox.addWidget(gui.RadioButton(modes, 'Metric', gui3d.app.settings.get('units', 'metric') == 'metric'))
        imperial = unitBox.addWidget(gui.RadioButton(modes, 'Imperial', gui3d.app.settings.get('units', 'metric') == 'imperial'))
        
        themes = []
        themesBox = self.themesBox = self.addRightWidget(gui.GroupBox('Theme'))
        self.themeNative = themesBox.addWidget(ThemeRadioButton(themes, "Native look", "default"))
        self.themeMH = themesBox.addWidget(ThemeRadioButton(themes, "MakeHuman", "makehuman"))

        # For debugging themes on multiple platforms
        '''
        platforms = []
        platformsBox = self.platformsBox = self.addRightWidget(gui.GroupBox('Look and feel'))
        for platform in gui3d.app.getLookAndFeelStyles():
            platformsBox.addWidget(PlatformRadioButton(platforms, platform))
        '''

        # We might allow overriding the font from the style, but for now loaded fonts can be used from a style
        '''
        fonts = []
        fontsBox = self.fontsBox = self.addRightWidget(gui.GroupBox('Font'))
        fontsBox.addWidget(FontRadioButton(fonts, "Default"))
        for font in gui3d.app.getCustomFonts():
            fontsBox.addWidget(FontRadioButton(fonts, font))
        '''
        
        languages = []
        languageBox = self.languageBox = self.addRightWidget(gui.GroupBox('Language'))
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

        @self.cameraAutoZoom.mhEvent
        def onClicked(event):
            gui3d.app.settings['cameraAutoZoom'] = self.cameraAutoZoom.selected

        @self.sliderImages.mhEvent
        def onClicked(event):
            gui3d.app.settings['sliderImages'] = self.sliderImages.selected
            gui.Slider.showImages(self.sliderImages.selected)
            mh.refreshLayout()
            
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
                log.message("No shader support: %s", str(e))
    
    def onShow(self, event):
    
        gui3d.TaskView.onShow(self, event)
        self.shaderNo.setFocus()
    
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()

def load(app):
    category = app.getCategory('Settings')
    taskview = category.addTask(SettingsTaskView(category))

def unload(app):
    pass



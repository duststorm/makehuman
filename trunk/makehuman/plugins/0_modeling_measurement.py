import os.path
#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import os
import random
import algos3d
import mh
import humanmodifier
import events3d
import aljabr

class MeasureSlider(humanmodifier.ModifierSlider):
    def __init__(self, parent, y, template, measure, modifier):
        
        humanmodifier.ModifierSlider.__init__(self, parent, [10, y, 9.1], value=0.0, min=-1.0, max=1.0,
            label=template + parent.parent.getMeasure(measure), modifier=modifier)
        self.template = template
        self.measure = measure
        
    def onChanging(self, value):
        humanmodifier.ModifierSlider.onChanging(self, value)
        self.updateLabel()
        
    def onChange(self, value):
        humanmodifier.ModifierSlider.onChange(self, value)
        self.parent.parent.syncSliderLabels()
        
    def updateLabel(self):
        self.label.setText(self.template + self.parent.parent.getMeasure(self.measure))
        
    def update(self):
        humanmodifier.ModifierSlider.update(self)
        self.updateLabel()

class MeasureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Measure')

        self.ruler = Ruler()

        measurements = [
            ('neck', ['neckcirc', 'neckheight']),
            ('upperarm', ['upperarm', 'upperarmlenght']),
            ('lowerarm', ['lowerarmlenght', 'wrist']),
            ('torso', ['frontchest', 'bust', 'underbust', 'waist', 'napetowaist', 'waisttohip', 'shoulder']),
            ('hips', ['hips']),
            ('upperleg', ['upperlegheight', 'thighcirc']),
            ('lowerleg', ['lowerlegheight', 'calf']),
            ('ankle', ['ankle']),
        ]
            
        sliderLabel = {
            'neckcirc':'Neck circum: ',
            'neckheight':'Neck height: ',
            'upperarm':'Upper arm circum: ',
            'upperarmlenght':'Upperarm lenght: ',
            'lowerarmlenght':'Lowerarm lenght: ',
            'wrist':'Wrist circum: ',
            'frontchest':'Front chest dist: ',
            'bust':'Bust circum: ',
            'underbust':'Underbust circum: ',
            'waist':'Waist circum: ',
            'napetowaist':'Nape to waist: ',
            'waisttohip':'Waist to hip: ',
            'shoulder':'Shoulder dist: ',
            'hips':'Hips circum: ',
            'upperlegheight':'Upperleg height: ',
            'thighcirc':'Thigh circ.: ',
            'lowerlegheight':'Lowerleg height: ',
            'calf':'Calf circum: ',
            'ankle':'Ankle circum: '
        }
        
        self.groupBoxes = {}
        self.sliders = []
        
        self.modifiers = {}
        
        measureDataPath = "data/targets/measure/"
        human = self.app.selectedHuman

        for name, subnames in measurements:
            # Create box
            box = gui3d.GroupBox(self, [10, 80, 9.0], name.capitalize(), gui3d.GroupBoxStyle._replace(height=25+36*len(subnames)+6))
            self.groupBoxes[name] = box
            
            # Create sliders
            yy = 80 + 25
            
            for subname in subnames:
                modifier = humanmodifier.Modifier(
                    os.path.join(measureDataPath, "measure-%s-decrease.target" % subname),
                    os.path.join(measureDataPath, "measure-%s-increase.target" % subname))
                self.modifiers[subname] = modifier
                slider = MeasureSlider(box, yy, sliderLabel[subname], subname, modifier)
                self.sliders.append(slider)
                yy += 36
               
        y = 80
        self.statsBox = gui3d.GroupBox(self, [650, y, 9.0], 'Statistics', gui3d.GroupBoxStyle._replace(height=25+22*4+6));y += 25
        self.height = gui3d.TextView(self.statsBox, [658, y, 9.1], 'Height: ');y += 22
        self.chest = gui3d.TextView(self.statsBox, [658, y, 9.1], 'Chest: ');y += 22
        self.waist = gui3d.TextView(self.statsBox, [658, y, 9.1], 'Waist: ');y += 22
        self.hips = gui3d.TextView(self.statsBox, [658, y, 9.1], 'Hips: ');y += 22
        y+=16
        self.braBox = gui3d.GroupBox(self, [650, y, 9.0], 'Brassiere size', gui3d.GroupBoxStyle._replace(height=25+22*4+6));y += 25
        self.eu = gui3d.TextView(self.braBox, [658, y, 9.1], 'EU: ');y += 22
        self.jp = gui3d.TextView(self.braBox, [658, y, 9.1], 'JP: ');y += 22
        self.us = gui3d.TextView(self.braBox, [658, y, 9.1], 'US: ');y += 22
        self.uk = gui3d.TextView(self.braBox, [658, y, 9.1], 'UK: ');y += 22
        y+=16
            
    def getMeasure(self, measure):
        
        human = self.app.selectedHuman
        measure = self.ruler.getMeasure(human, measure, self.app.settings['units'])
        if self.app.settings['units'] == 'metric':
            return '%.1f cm' % measure
        else:
            return '%.1f in' % measure

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        self.groupBoxes['torso'].children[0].setFocus()
        self.syncSliders()
        
    def onResized(self, event):
        
        self.statsBox.setPosition([event[0] - 150, self.braBox.getPosition()[1], 9.0])
        self.braBox.setPosition([event[0] - 150, self.braBox.getPosition()[1], 9.0])
        
    def hideAllSliders(self):
        for group in self.groupBoxes.itervalues():
            group.hide()

    def syncSliders(self):
        
        for slider in self.sliders:
            slider.update()
           
        self.syncStatistics()
        self.syncBraSizes()
            
    def syncSliderLabels(self):
        
        for slider in self.sliders:
            slider.updateLabel()
            
        self.syncStatistics()
        self.syncBraSizes()
    
    def syncStatistics(self):
        
        human = self.app.selectedHuman
        
        height = 10 * max(human.meshData.verts[8223].co[1] - human.meshData.verts[12361].co[1], human.meshData.verts[8223].co[1] - human.meshData.verts[13155].co[1])
        if self.app.settings['units'] == 'metric':
            height = '%.2f cm' % height
        else:
            height = '%.2f in' % (height * 0.393700787)
        
        self.height.setText('Height: %s' % height)
        self.chest.setText('Chest: %s' % self.getMeasure('bust'))
        self.waist.setText('Waist: %s' % self.getMeasure('waist'))
        self.hips.setText('Hips: %s' % self.getMeasure('hips'))
        
    def syncBraSizes(self):
        
        human = self.app.selectedHuman
        
        bust = self.ruler.getMeasure(human, 'bust', 'metric')
        underbust = self.ruler.getMeasure(human, 'underbust', 'metric')
        
        eucups = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        
        mod = int(underbust)%5
        band = underbust - mod if mod < 2.5 else underbust - mod + 5
        cup = max(0, int(round(((bust - underbust - 10) / 2))))
        self.eu.setText('EU: %d%s' % (band, eucups[cup]))
        
        jpcups = ['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        
        mod = int(underbust)%5
        band = underbust - mod if mod < 2.5 else underbust - mod + 5
        cup = max(0, int(round(((bust - underbust - 5) / 2.5))))
        self.jp.setText('JP: %d%s' % (band, jpcups[cup]))
        
        uscups = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
           
        band = underbust * 0.393700787
        band = band + 5 if int(band)%2 else band + 4
        cup = max(0, int(round((bust - underbust - 10) / 2)))
        self.us.setText('US: %d%s' % (band, uscups[cup]))

        ukcups = ['AA', 'A', 'B', 'C', 'D', 'DD', 'E', 'F', 'FF', 'G', 'GG', 'H']
        
        self.uk.setText('UK: %d%s' % (band, ukcups[cup]))
        
    def loadHandler(self, human, values):
        
        modifier = self.modifiers.get(values[1], None)
        if modifier:
            modifier.setValue(human, float(values[2]))
       
    def saveHandler(self, human, file):
        
        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('measure %s %f\n' % (name, value))

def load(app):
    """
    Plugin load function, needed by design.
    """
    category = app.getCategory('Modelling')
    taskview = MeasureTaskView(category)
    
    app.addLoadHandler('measure', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)
    
    print 'Measurement loaded'

    @taskview.event
    def onMouseDown(event):        
        part = app.scene3d.getSelectedFacesGroup()
        bodyZone = app.selectedHuman.getPartNameForGroupName(part.name)
        print bodyZone
        if bodyZone in app.selectedHuman.bodyZones:            
            if bodyZone == "neck":
                taskview.hideAllSliders()
                taskview.groupBoxes['neck'].show()
            elif (bodyZone == "r-upperarm") or (bodyZone == "l-upperarm"):
                taskview.hideAllSliders()
                taskview.groupBoxes['upperarm'].show()
            elif (bodyZone == "r-lowerarm") or (bodyZone == "l-lowerarm"):
                taskview.hideAllSliders()
                taskview.groupBoxes['lowerarm'].show()
            elif (bodyZone == "torso") or (bodyZone == "pelvis"):
                taskview.hideAllSliders()
                taskview.groupBoxes['torso'].show()              
            elif bodyZone == "hip":
                taskview.hideAllSliders()
                taskview.groupBoxes['hips'].show()   
            elif (bodyZone == "l-upperleg") or (bodyZone == "r-upperleg"):
                taskview.hideAllSliders()
                taskview.groupBoxes['upperleg'].show()   
            elif (bodyZone == "l-lowerleg") or (bodyZone == "r-lowerleg"):
                taskview.hideAllSliders()
                taskview.groupBoxes['lowerleg'].show() 
            elif (bodyZone == "l-foot") or (bodyZone == "r-foot"):
                taskview.hideAllSliders()
                taskview.groupBoxes['ankle'].show() 
            else:
                taskview.hideAllSliders()
                
    taskview.hideAllSliders()
    taskview.groupBoxes['torso'].show()

class Ruler:

    """
  This class contains ...
  """

    def __init__(self):

    # these are tables of vertex indices for each body measurement of interest

        self.Measures = {}
        self.Measures['thighcirc'] = [7066,7205,7204,7192,7179,7176,7166,6886,7172,6813,7173,7101,7033,7032,7041,7232,7076,7062,7063,7229,7066]
        self.Measures['neckcirc'] = [3131,3236,3058,3059,2868,2865,3055,3137,5867,2857,3483,2856,3382,2916,2915,3417,8186,10347,10786,
                                    10785,10373,10818,10288,10817,9674,10611,10809,10806,10674,10675,10515,10614]
        self.Measures['neckheight'] = [8184,8185,8186,8187,7463]
        self.Measures['upperarm']=[10701,10700,10699,10678,10337,10334,10333,10330,10280,10331,10702,10708,9671,10709,10329,10328]
        self.Measures['wrist']=[9894,9895,9607,9606,9806,10512,10557,9807,9808,9809,9810,10565,9653,9682,9681,9832,10507]
        self.Measures['frontchest']=[2961,10764]
        self.Measures['bust']=[6908,3559,3537,3556,3567,3557,4178,3558,4193,3561,3566,3565,3718,3563,2644,4185,2554,4169,2553,3574,2634,2653,3466,3392,
                2942,3387,4146,4433,2613,10997,9994,10078,10368,10364,10303,10380,10957,10976,10218,11055,10060,11054,10044,10966,10229,10115,
                10227,10226,10231,10036,10234,10051,10235,10225,10236,10255,10233]
        self.Measures['napetowaist']=[7463,7472]
        self.Measures['waisttohip']=[4681,6575]
        self.Measures['shoulder'] = [10819,10816,10021,10821,10822,10693,10697]
        self.Measures['underbust'] = [7245,3583,6580,3582,3705,3581,3411,3401,3467,4145,2612,10998,10080,10302,10366,10356,10352,10362,10361,10350,10260,10349,7259]
        self.Measures['waist'] = [6853,4682,3529,2950,3702,3594,3405,5689,3587,4466,6898,9968,10086,9970,10359,10197,10198,10130,10771,10263,6855]
        self.Measures['upperlegheight'] = [6755,7026]
        self.Measures['lowerlegheight'] = [6866,13338]
        self.Measures['calf'] = [7141,7142,7137,6994,6989,6988,6995,6997,6774,6775,6999,6803,6974,6972,6971,7002,7140,7139]
        self.Measures['ankle'] = [6938,6937,6944,6943,6948,6784,6935,6766,6767,6954,6799,6955,6958,6949,6952,6941]
        self.Measures['upperarmlenght'] = [9945,10696]
        self.Measures['lowerarmlenght'] = [9696,9945]
        self.Measures['hips'] = [7298,2936,3527,2939,2940,3816,3817,3821,4487,3822,3823,3913,3915,4506,5688,4505,4504,4503,6858,6862,6861,6860,
                                            6785,6859,7094,7096,7188,7189,6878,7190,7194,7195,7294,7295,7247,7300]

    def getMeasure(self, human, measurementname, mode):
        measure = 0
        vindex1 = self.Measures[measurementname][0]
        for vindex2 in self.Measures[measurementname]:
            measure += aljabr.vdist(human.meshData.verts[vindex1].co, human.meshData.verts[vindex2].co)
            vindex1 = vindex2
            
        if mode == 'metric':
            return 10.0 * measure
        else:
            return 10.0 * measure * 0.393700787







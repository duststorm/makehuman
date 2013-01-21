import gui
from export import Exporter

class ExporterMHX(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Blender exchange (mhx)"
        self.filter = "Blender Exchange (*.mhx)"

    def build(self, options):
        #self.version24 = options.addWidget(gui.CheckBox("Version 2.4", False))
        #self.version25 = options.addWidget(gui.CheckBox("Version 2.5", True))
        self.mhxSeparateFolder = options.addWidget(gui.CheckBox("Separate folder", False))
        self.mhxFeetOnGround = options.addWidget(gui.CheckBox("Feet on ground", True))
        self.mhxExpressionUnits = options.addWidget(gui.CheckBox("Expressions", False))
        #self.mhxFaceShapes = options.addWidget(gui.CheckBox("Face shapes", True))
        self.mhxBodyShapes = options.addWidget(gui.CheckBox("Body shapes", True))
        self.mhxCustomShapes = options.addWidget(gui.CheckBox("Custom shapes", False))
        #self.mhxFacePanel = options.addWidget(gui.CheckBox("Face panel", True))
        self.mhxClothes = options.addWidget(gui.CheckBox("Clothes", True))
        self.mhxMasks = options.addWidget(gui.CheckBox("Clothes masks", False))
        self.mhxHidden = options.addWidget(gui.CheckBox("Keep hidden faces", True))
        self.mhxClothesRig = options.addWidget(gui.CheckBox("Clothes rig", True))
        self.mhxCage = options.addWidget(gui.CheckBox("Cage", False))
        self.mhxAdvancedSpine = options.addWidget(gui.CheckBox("Advanced spine", False))
        self.mhxMaleRig = options.addWidget(gui.CheckBox("Male rig", False))
        #self.mhxSkirtRig = options.addWidget(gui.CheckBox("Skirt rig", False))

        rigs = []
        self.mhxMhx = options.addWidget(gui.RadioButton(rigs, "Use mhx rig", True))
        self.rigifyMhx = options.addWidget(gui.RadioButton(rigs, "Use rigify rig", False))
        addedRigs = self.addRigs(options, rigs)
        self.mhxRigs = [(self.mhxMhx, "mhx"), (self.rigifyMhx, "rigify")] + addedRigs

    def export(self, human, filename):
        import mh2mhx
        #mhxversion = []
        #if self.version24.selected: mhxversion.append('24')
        #if self.version25.selected: mhxversion.append('25')

        for (button, rig) in self.mhxRigs:
            if button.selected:
                break

        options = {
            'mhxversion': ["25"],  #mhxversion,
            'usemasks':        self.mhxMasks.selected,
            'hidden':          self.mhxHidden.selected,
            #'expressions':     False,    #self.mhxExpressions.selected,
            'expressionunits': self.mhxExpressionUnits.selected,
            #'faceshapes':      self.mhxFaceShapes.selected,
            'bodyshapes':      self.mhxBodyShapes.selected,
            'customshapes':    self.mhxCustomShapes.selected,
            #'facepanel':       self.mhxFacePanel.selected,
            'clothes':         self.mhxClothes.selected,
            'cage':            self.mhxCage.selected,
            'separatefolder':  self.mhxSeparateFolder.selected,
            'feetonground':    self.mhxFeetOnGround.selected,
            'advancedspine':   self.mhxAdvancedSpine.selected,
            'malerig':         self.mhxMaleRig.selected,
            'skirtrig':        False, #self.mhxSkirtRig.selected,
            'clothesrig':      self.mhxClothesRig.selected,
            'mhxrig':          rig,
        }

        mh2mhx.exportMhx(human, filename("mhx"), options)

def load(app):
    app.addExporter(ExporterMHX())

def unload(app):
    pass

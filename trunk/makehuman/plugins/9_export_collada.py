import gui
from export import Exporter

class ExporterCollada(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Collada (dae)"
        self.filter = "Collada (*.dae)"

    def build(self, options):
        # Collada options
        self.colladaRot90X = options.addWidget(gui.CheckBox("Rotate 90 X", False))
        self.colladaRot90Z = options.addWidget(gui.CheckBox("Rotate 90 Z", False))
        self.colladaEyebrows = options.addWidget(gui.CheckBox("Eyebrows", True))
        self.colladaLashes = options.addWidget(gui.CheckBox("Eyelashes", True))
        self.colladaHelpers = options.addWidget(gui.CheckBox("Helper geometry", False))
        self.colladaHidden = options.addWidget(gui.CheckBox("Keep hidden faces", True))
        # self.colladaSeparateFolder = options.addWidget(gui.CheckBox("Separate folder", False))
        # self.colladaPngTexture = options.addWidget(gui.CheckBox("PNG texture", selected=True))

        self.daeScales = self.addScales(options)
        self.daeRigs = self.addRigs(options)

    def export(self, human, filename):
        import mh2collada

        for (button, rig) in self.daeRigs:
            if button.selected:
                break                

        options = {
            "daerig": rig,
            "rotate90X": self.colladaRot90X.selected,
            "rotate90Z": self.colladaRot90Z.selected,
            "eyebrows":  self.colladaEyebrows.selected,
            "lashes":    self.colladaLashes.selected,
            "helpers":   self.colladaHelpers.selected,
            "hidden":    self.colladaHidden.selected,
            "scale":     self.getScale(self.daeScales),
        }

        mh2collada.exportCollada(human, filename("dae"), options)

def load(app):
    app.addExporter(ExporterCollada())

def unload(app):
    pass

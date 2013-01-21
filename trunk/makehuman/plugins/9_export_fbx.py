import gui
from export import Exporter

class ExporterFBX(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Filmbox (fbx)"
        self.filter = "Filmbox (*.fbx)"

    def build(self, options):
        self.fbxEyebrows = options.addWidget(gui.CheckBox("Eyebrows", True))
        self.fbxLashes   = options.addWidget(gui.CheckBox("Eyelashes", True))
        self.fbxHelpers  = options.addWidget(gui.CheckBox("Helper geometry", False))
        self.fbxHidden   = options.addWidget(gui.CheckBox("Keep hidden faces", True))
        self.fbxSkeleton = options.addWidget(gui.CheckBox("Skeleton", True))
        self.fbxSmooth   = options.addWidget(gui.CheckBox("Subdivide", False))
        self.fbxScales   = self.addScales(options)
        self.fbxRigs     = self.addRigs(options)

    def export(self, human, filename):
        import mh2fbx

        for (button, rig) in self.fbxRigs:
            if button.selected:
                break

        options = {
            "fbxrig":    rig,
            "helpers":   self.fbxHelpers.selected,
            "hidden":    self.fbxHidden.selected,
            "eyebrows":  self.fbxEyebrows.selected,
            "lashes":    self.fbxLashes.selected,
            "scale":     self.getScale(self.fbxScales),
            "subdivide": self.fbxSmooth.selected
        }

        mh2fbx.exportFbx(human, filename("fbx"), options)

def load(app):
    app.addExporter(ExporterFBX())

def unload(app):
    pass

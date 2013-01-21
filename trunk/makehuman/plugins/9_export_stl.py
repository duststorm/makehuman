import gui
from export import Exporter

class ExporterSTL(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Stereolithography (stl)"
        self.filter = "Stereolithography (*.stl)"

    def build(self, options):
        stlOptions = []
        self.stlAscii = options.addWidget(gui.RadioButton(stlOptions,  "Ascii", selected=True))
        self.stlBinary = options.addWidget(gui.RadioButton(stlOptions, "Binary"))
        self.stlSmooth = options.addWidget(gui.CheckBox("Subdivide", False))

    def export(self, human, filename):
        import mh2stl

        mesh = human.getSubdivisionMesh() if self.stlSmooth.selected else human.meshData

        if self.stlAscii.selected:
            mh2stl.exportStlAscii(mesh, filename("stl"))
        else:
            mh2stl.exportStlBinary(mesh, filename("stl"))

def load(app):
    app.addExporter(ExporterSTL())

def unload(app):
    pass

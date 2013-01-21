import gui
from export import Exporter

class ExporterSkel(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.group = "rig"
        self.name = "Skeleton (skel)"
        self.filter = "Skeleton (*.skel)"

    def build(self, options):
        self.exportSmooth = options.addWidget(gui.CheckBox("Subdivide", False))

    def export(self, human, filename):
        import mh2skel
        mesh = human.getSubdivisionMesh() if self.exportSmooth.selected else human.meshData
        mh2skel.exportSkel(mesh, filename("skel"))

def load(app):
    app.addExporter(ExporterSkel())

def unload(app):
    pass

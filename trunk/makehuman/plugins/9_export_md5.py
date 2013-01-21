import gui
from export import Exporter

class ExporterMD5(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "MD5"
        self.filter = "MD5 (*.md5)"

    def export(self, human, filename):
        import mh2md5
        mh2md5.exportMd5(human.meshData, filename("md5mesh"))

def load(app):
    app.addExporter(ExporterMD5())

def unload(app):
    pass

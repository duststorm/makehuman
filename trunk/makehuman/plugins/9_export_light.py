import gui
from export import Exporter

class ExporterLight(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.group = "map"
        self.name = "Lightmap"
        self.filter = "PNG (*.png)"

    def build(self, options):
        self.lightmapDisplay = options.addWidget(gui.CheckBox("Display on human", False))

    def export(self, human, filename):
        import projection

        dstImg = projection.mapLighting()
        filepath = filename("png")
        dstImg.save(filepath)

        if self.lightmapDisplay:
            import log
            human.setTexture(filepath)
            log.message("Enabling shadeless rendering on body")
            human.mesh.setShadeless(True)

def load(app):
    app.addExporter(ExporterLight())

def unload(app):
    pass

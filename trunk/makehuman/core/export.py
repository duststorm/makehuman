import os
import gui
import log

class Exporter(object):
    def __init__(self):
        self.group = "mesh"

    def build(self, options):
        pass

    def export(self, human, filename):
        raise NotImplementedError()

    _scales = {
        "decimeter": 1.0,
        "meter": 0.1,
        "inch": 0.254,
        "centimeter": 10.0
        }

    def addScales(self, options):
        check = True
        buttons = []
        scales = []
        for name in ["decimeter", "meter", "inch", "centimeter"]:
            button = options.addWidget(gui.RadioButton(scales, name, check))
            check = False
            buttons.append((button,name))
        return buttons

    def getScale(self, buttons):
        for (button, name) in buttons:
            if button.selected and name in self._scales:
                return (self._scales[name], name)
        return (1, "decimeter")
        
    def addRigs(self, options, rigs = None):
        path = "data/rigs"
        if not os.path.exists(path):
            log.message("Did not find directory %s", path)
            return []

        check = rigs is None
        buttons = []
        rigs = rigs if rigs is not None else []
        for fname in os.listdir(path):
            (name, ext) = os.path.splitext(fname)
            if ext == ".rig":
                button = options.addWidget(gui.RadioButton(rigs, "Use %s rig" % name, check))
                check = False
                buttons.append((button, name))
        return buttons

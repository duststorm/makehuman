import PIL.Image as img
import numpy as np

_modes = {
    'L': 1,
    'LA': 2,
    'RGB': 3,
    'RGBA': 4
    }
         
def load(path):
    image = img.open(path)
    if image.mode not in ("L", "RGB", "RGBA"):
        image = image.convert("RGBA")
    w, h = image.size
    d = _modes[image.mode]
    pixels = image.tostring("raw", image.mode)
    data = np.fromstring(pixels, dtype=np.uint8).reshape((h,w,d))
    return data

def save(path, data):
    h, w, d = data.shape
    mode = [None,'L','LA','RGB','RGBA'][d]
    image = img.fromstring(mode, (w, h), data.tostring())
    image.save(path)

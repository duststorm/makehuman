from core import G
if G.use_pil:
    import PIL.Image as img
else:
    import image_base as img

class Image(object):
    def __new__(cls, *args, **kwargs):
        self = super(Image, cls).__new__(cls)
        self.surface = None
        return self

    def __init__(self, path = None, width = 0, height = 0, bitsPerPixel = 32):
        if path is not None:
            self.load(path)
        elif width != 0 and height != 0:
            if bitsPerPixel == 32:
                self.surface = img.new("RGBA", (width, height))
            elif bitsPerPixel == 24:
                self.surface = img.new("RGB", (width, height))

    def load(self, path):
        "Loads the specified image from file"
        self.surface = img.open(path)
        if self.surface.mode not in ("L", "RGB", "RGBA"):
            self.surface = self.surface.convert("RGBA");

    def save(self, path):
        if self.surface is None:
            raise RuntimeError("image not initialized")
        self.surface.save(path)

    def resized_(self, width, height):
        if self.surface is None:
            raise RuntimeError("image not initialized")

        if width * height < self.width * self.height:
            filter = img.ANTIALIAS
        else:
            filter = img.BILINEAR

        return self.surface.resize((width, height), filter)

    def resized(self, width, height):
        im = Image()
        im.surface = self.resized_(width, height)
        return im

    def resize(self, width, height):
        self.surface = self.resized_(width, height)

    def blit(self, other, x, y):
        if self.surface is None:
            raise RuntimeError("destination image not initialized")
        if other.surface is None:
            raise RuntimeError("source image not initialized")
        self.surface.paste(other.surface, (x, y))

    def getWidth(self):
        if self.surface is None:
            return 0
        return self.surface.size[0]

    width = property(getWidth, None, None, "The width of the image.")

    def getHeight(self):
        if self.surface is None:
            return 0
        return self.surface.size[1]

    height = property(getHeight, None, None, "The height of the image.")

    def getBitsPerPixel(self):
        if self.surface is None:
            return 0
        return {"RGB": 24, "RGBA": 32}[self.surface.mode]

    bitsPerPixel = property(getBitsPerPixel, None, None, "The bits per pixel of the image.")

    def __getitem__(self, xy):
        if self.surface is None:
            raise RuntimeError("image not initialized")

        if not isinstance(xy, tuple) or len(xy) != 2:
            raise TypeError("tuple of length 2 expected")

        x, y = xy

        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("tuple of 2 ints expected")

        if x < 0 or x >= self.surface.size[0] or y < 0 or y >= self.surface.size[1]:
            raise IndexError("element index out of range")

        pix = self.surface.getpixel(xy)
        if not isinstance(pix, tuple):
            return (pix, pix, pix, 255)
        if len(pix) == 2:
            return (pix[0], pix[0], pix[0], pix[1])
        if len(pix) == 3:
            return pix + (255,)
        return pix

    def __setitem__(self, xy, color):
        if self.surface is None:
            raise RuntimeError("image not initialized")

        if not isinstance(xy, tuple) or len(xy) != 2:
            raise TypeError("tuple of length 2 expected")

        x, y = xy

        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("tuple of 2 ints expected")

        if x < 0 or x >= self.surface.size[0] or y < 0 or y >= self.surface.size[1]:
            raise IndexError("element index out of range")

        if not isinstance(color, tuple):
            raise TypeError("tuple expected")

        self.surface.putpixel(xy, color)

import struct
import numpy as np

def save(path, data):
    h, w, c = data.shape

    rowsize = w * c
    padsize = (rowsize + 3) / 4 * 4

    # BITMAPFILEHEADER structure
    #
    #  0 2      signature: 'B','M'
    #  2 4      file size
    #  6 2      reserved
    #  8 2      reserved
    # 10 4      offset to bitmap data

    file_header = struct.pack(
        '<2cI2hI',
        'B','M',
        14 + 40 + h * padsize,
        0, 0,
        54)

    # BITMAPINFOHEADER structure
    #
    # 0     4       BITMAPINFOHEADER size
    # 4     4       width
    # 8     4       height (+ve => bottom-up, -ve => top-down)
    # 12    2       number of planes (must be 1)
    # 14    2       bits per pixel
    # 16    4       compression
    # 20    4       image size
    # 24    4       X pixels per meter
    # 28    4       Y pixels per meter
    # 32    4       number of palette colors used
    # 36    4       number of important palette colors
    # 40 ... palette

    info_header = struct.pack(
        '<IIIHHIIIIII',
        40,
        w, h,
        1,
        c * 8,
        0,
        w * h,
        2953, 2953,
        0, 0)

    data = data[:,:,::-1]       # RGB->BGR
    data = data[::-1,:,:]       # vertical flip

    if rowsize % 4 != 0:
        data2 = np.zeros((h, padsize), dtype=np.uint8)
        data2[:,:rowsize] = data.reshape((h, rowsize))
        data = data2

    with file(path, 'wb') as f:
        f.write(file_header)
        f.write(info_header)
        f.write(np.ascontiguousarray(data).tostring())

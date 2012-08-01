import sys
from ctypes import *

if sys.platform == 'win32':
    _png = CDLL('bin/win/libpng12-0.dll')
elif sys.platform == 'darwin':
    _png = CDLL('/opt/local/lib/libpng.dylib')
else:
    _png = CDLL('libpng.so')

INFO_gAMA	= 0x0001
INFO_sBIT	= 0x0002
INFO_cHRM	= 0x0004
INFO_PLTE	= 0x0008
INFO_tRNS	= 0x0010
INFO_bKGD	= 0x0020
INFO_hIST	= 0x0040
INFO_pHYs	= 0x0080
INFO_oFFs	= 0x0100
INFO_tIME	= 0x0200
INFO_pCAL	= 0x0400
INFO_sRGB	= 0x0800
INFO_iCCP	= 0x1000
INFO_sPLT	= 0x2000
INFO_sCAL	= 0x4000
INFO_IDAT	= 0x8000

COLOR_MASK_PALETTE	= 1
COLOR_MASK_COLOR	= 2
COLOR_MASK_ALPHA	= 4

COLOR_TYPE_GRAY		= 0
COLOR_TYPE_PALETTE	= COLOR_MASK_COLOR | COLOR_MASK_PALETTE
COLOR_TYPE_RGB		= COLOR_MASK_COLOR
COLOR_TYPE_RGB_ALPHA	= COLOR_MASK_COLOR | COLOR_MASK_ALPHA
COLOR_TYPE_GRAY_ALPHA	= COLOR_MASK_ALPHA
# aliases
COLOR_TYPE_RGBA		= COLOR_TYPE_RGB_ALPHA
COLOR_TYPE_GA		= COLOR_TYPE_GRAY_ALPHA

COMPRESSION_TYPE_BASE	= 0
COMPRESSION_TYPE_DEFAULT = COMPRESSION_TYPE_BASE

FILTER_TYPE_BASE	= 0	# Single row per-byte filtering
INTRAPIXEL_DIFFERENCING = 64	# Used only in MNG datastreams
FILTER_TYPE_DEFAULT	= FILTER_TYPE_BASE

INTERLACE_NONE		= 0	# Non-interlaced image
INTERLACE_ADAM7		= 1	# Adam7 interlacing
INTERLACE_LAST		= 2	# Not a valid value

rw_func = CFUNCTYPE(None, c_void_p, c_void_p, c_size_t)
flush_func = CFUNCTYPE(None, c_void_p)

# png_structp png_create_read_struct(png_const_charp user_png_ver, png_voidp error_ptr, png_error_ptr error_fn, png_error_ptr warn_fn)
create_read_struct = _png.png_create_read_struct
create_read_struct.argtypes = [c_char_p, c_void_p, c_void_p, c_void_p]
create_read_struct.restype = c_void_p

# png_infop png_create_info_struct(png_structp png_ptr)
create_info_struct = _png.png_create_info_struct
create_info_struct.argtypes = [c_void_p]
create_info_struct.restype = c_void_p

# png_uint_32 png_get_valid(png_const_structp png_ptr, png_const_infop info_ptr, png_uint_32 flag)
get_valid = _png.png_get_valid
get_valid.argtypes = [c_void_p, c_void_p, c_uint]
get_valid.restype = c_uint

# png_uint_32 png_get_IHDR(png_structp png_ptr, png_infop info_ptr, png_uint_32 *width, png_uint_32 *height, int *bit_depth, int *color_type, int *interlace_method, int *compression_method, int *filter_method)
get_IHDR = _png.png_get_IHDR
get_IHDR.argtypes = [c_void_p, c_void_p, POINTER(c_uint), POINTER(c_uint), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
get_IHDR.restype = c_uint

# void png_read_info(png_structp png_ptr, png_infop info_ptr)
read_info = _png.png_read_info
read_info.argtypes = [c_void_p, c_void_p]
read_info.restype = None

# void png_set_expand_gray_1_2_4_to_8(png_structp png_ptr)
set_expand_gray_1_2_4_to_8 = _png.png_set_expand_gray_1_2_4_to_8
set_expand_gray_1_2_4_to_8.argtypes = [c_void_p]
set_expand_gray_1_2_4_to_8.restype = None

# void png_set_palette_to_rgb(png_structp png_ptr)
set_palette_to_rgb = _png.png_set_palette_to_rgb
set_palette_to_rgb.argtypes = [c_void_p]
set_palette_to_rgb.restype = None

# void png_set_tRNS_to_alpha(png_structp png_ptr)
set_tRNS_to_alpha = _png.png_set_tRNS_to_alpha
set_tRNS_to_alpha.argtypes = [c_void_p]
set_tRNS_to_alpha.restype = None

# void png_set_filler(png_structp png_ptr, png_uint_32 filler, int flags)
set_filler = _png.png_set_filler
set_filler.argtypes = [c_void_p, c_uint, c_int]
set_filler.restype = None

# void png_set_packing(png_structp png_ptr)
set_packing = _png.png_set_packing
set_packing.argtypes = [c_void_p]
set_packing.restype = None

# void png_set_strip_16(png_structp png_ptr)
set_strip_16 = _png.png_set_strip_16
set_strip_16.argtypes = [c_void_p]
set_strip_16.restype = None

# void png_read_update_info(png_structp png_ptr, png_infop info_ptr)
read_update_info = _png.png_read_update_info
read_update_info.argtypes = [c_void_p, c_void_p]
read_update_info.restype = None

# void png_read_row(png_structp png_ptr, png_bytep row, png_bytep display_row)
read_row = _png.png_read_row
read_row.argtypes = [c_void_p, c_void_p, c_void_p]
read_row.restype = None

# void png_read_end(png_structp png_ptr, png_infop info_ptr)
read_end = _png.png_read_end
read_end.argtypes = [c_void_p, c_void_p]
read_end.restype = None

# void png_destroy_read_struct(png_structpp png_ptr_ptr, png_infopp info_ptr_ptr, png_infopp end_info_ptr_ptr)
destroy_read_struct = _png.png_destroy_read_struct
destroy_read_struct.argtypes = [POINTER(c_void_p), POINTER(c_void_p), POINTER(c_void_p)]
destroy_read_struct.restype = None

# void png_set_read_fn(png_structp png_ptr, png_voidp io_ptr, png_rw_ptr read_data_fn)
set_read_fn = _png.png_set_read_fn
set_read_fn.argtypes = [c_void_p, c_void_p, rw_func]
set_read_fn.restype = None

# png_voidp png_get_io_ptr(png_structp png_ptr)
get_io_ptr = _png.png_get_io_ptr
get_io_ptr.argtypes = [c_void_p]
get_io_ptr.restype = c_void_p

# png_const_charp png_get_header_ver(png_const_structp png_ptr)
get_header_ver = _png.png_get_header_ver
get_header_ver.argtypes = [c_void_p]
get_header_ver.restype = c_char_p

# png_structp png_create_write_struct(png_const_charp user_png_ver, png_voidp error_ptr, png_error_ptr error_fn, png_error_ptr warn_fn)
create_write_struct = _png.png_create_write_struct
create_write_struct.argtypes = [c_char_p, c_void_p, c_void_p, c_void_p]
create_write_struct.restype = c_void_p

# void png_destroy_write_struct(png_structpp png_ptr_ptr, png_infopp info_ptr_ptr)
destroy_write_struct = _png.png_destroy_write_struct
destroy_write_struct.argtypes = [POINTER(c_void_p), POINTER(c_void_p)]
destroy_write_struct.restype = None

# void png_set_IHDR(png_structp png_ptr, png_infop info_ptr, png_uint_32 width, png_uint_32 height, int bit_depth, int color_type, int interlace_method, int compression_method, int filter_method)
set_IHDR = _png.png_set_IHDR
set_IHDR.argtypes = [c_void_p, c_void_p, c_uint, c_uint, c_int, c_int, c_int, c_int, c_int]
set_IHDR.restype = None

# void png_set_rows(png_structp png_ptr, png_infop info_ptr, png_bytepp row_pointers)
set_rows = _png.png_set_rows
set_rows.argtypes = [c_void_p, c_void_p, POINTER(c_void_p)]
set_rows.restype = None

# void png_set_write_fn(png_structp png_ptr, png_voidp io_ptr, png_rw_ptr write_data_fn, png_flush_ptr output_flush_fn)
set_write_fn = _png.png_set_write_fn
set_write_fn.argtypes = [c_void_p, c_void_p, rw_func, flush_func]
set_write_fn.restype = None

# void png_write_png(png_structp png_ptr, png_infop info_ptr, int transforms, png_voidp params)
write_png = _png.png_write_png
write_png.argtypes = [c_void_p, c_void_p, c_int, c_void_p]
write_png.restype = None

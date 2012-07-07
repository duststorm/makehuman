from cProfile import Profile

_prof = None
_sort = -1
_print = False
_accum = None

def run(cmd, globals, locals):
    flush()
    try:
        _prof.runctx(cmd, globals, locals)
    finally:
        show()

def accum(cmd, globals, locals):
    global _accum
    if _accum != cmd:
        flush()
        _accum = cmd
    _prof.runctx(cmd, globals, locals)

def flush():
    if _accum is not None:
        show()
    reset()

def show():
    _prof.print_stats(_sort)

def reset():
    global _prof, _accum
    _prof = Profile()
    _accum = None

def set_sort(sort):
    global _sort
    _sort = sort

def set_print(enable):
    global _print
    _print = enable

reset()
set_sort('cumulative')

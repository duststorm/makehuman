from cProfile import Profile

_sort = 'cumulative'
_accum = {}

def run(cmd, globals, locals):
    prof = Profile()
    try:
        prof.runctx(cmd, globals, locals)
    finally:
        show(prof)

def accum(cmd, globals, locals):
    if cmd not in _accum:
        prof = Profile()
        _accum[cmd] = prof
    else:
        prof = _accum[cmd]
    prof.runctx(cmd, globals, locals)

def flush():
    for cmd in sorted(_accum.keys()):
        show(_accum[cmd])
    _accum.clear()

def show(prof):
    prof.print_stats(_sort)

def set_sort(sort):
    global _sort
    _sort = sort

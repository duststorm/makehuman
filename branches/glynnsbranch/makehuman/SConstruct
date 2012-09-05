import platform
import sys, os

pyver = sys.version_info
if platform.system() == "Windows":
    pyver = '%d%d' % (pyver[0], pyver[1])
else:
    pyver = '%d.%d' % (pyver[0], pyver[1])
   
pydir = os.path.dirname(os.path.normpath(sys.executable))

env = DefaultEnvironment(ENV=os.environ, CCFLAGS = '-O2')
conf = Configure(env)

env.Append(CPPPATH = ['include'])

if not env.GetOption('clean'):
    
    # Append to CPPPATH and LIBPATH if on windows
    if platform.system() == "Windows":
        if 'msvc' in env['TOOLS']:
            env.Append(CPPPATH = [os.path.join(pydir, 'include'), 'd:/sdl/include', 'd:/glew/include', 'c:/sdl/include', 'c:/glew/include'])
            env.Append(LIBPATH = [os.path.join(pydir, 'libs'), 'd:/sdl/lib', 'd:/glew/lib', 'c:/sdl/lib', 'c:/glew/lib'])
        else:
            mingwinc = 'c:/mingw/include'
            mingwlib = 'c:/mingw/lib'
            env.Append(CPPPATH = [os.path.join(pydir, 'include'), mingwinc, mingwinc + '/SDL'])
            env.Append(LIBPATH = [os.path.join(pydir, 'libs'), mingwlib, mingwlib + '/SDL'])
    else:
        env.Append(CPPPATH = ['/usr/include/python' + pyver, '/usr/include/GL', '/usr/include/SDL'])
            
    # Check for libs and headers
    if conf.CheckLib('m'):
        env.Append(LIBS = ['m']);
    if not (conf.CheckLib('python' + pyver, 'Py_Initialize') and conf.CheckHeader('Python.h')):
        print "The Python" + pyver + " development libraries must be installed"
        exit(1)
    if platform.system() != "Windows":
        if not (conf.CheckLib('X11')):
            print "The X11 development libraries must be installed"
            exit(1)
    if not (conf.CheckLib('SDL', 'SDL_Init') and conf.CheckHeader('SDL.h')):
        print "The SDL development libraries must be installed"
        exit(1)
    else:
        if platform.system() == "Windows":
            env.Append(LIBS = ['SDLmain'])
    if not (conf.CheckLib('GLEW') or conf.CheckLib('glew32', 'glewInit')):
        print "The GLEW must be installed"
        exit(1)
        
    # Add additional libs and set flags
    if platform.system() == "Windows":
        env.Append(LIBS = ['opengl32','glu32','shell32','kernel32','user32','shlwapi'])
        if 'msvc' in env['TOOLS']:
            env.Append(CFLAGS='/O2 /GL /D "_UNICODE" /D "UNICODE" /FD /EHsc /MD')
            env.Append(LINKFLAGS='/OPT:REF /OPT:ICF /LTCG /MACHINE:X86 /NODEFAULTLIB:libcmt.lib /SUBSYSTEM:CONSOLE')
        else:
            env.Append(LINKFLAGS='-mconsole')
    else:
        env.Append(LIBS = ['GL','GLU'])
env=conf.Finish()

# Build application
VariantDir('program_build', 'src', duplicate=0)
sources = ["program_build/core.c", "program_build/glmodule.c", "program_build/arraybuffer.c", "program_build/main.c"]
if platform.system() == "Windows":
    sources.append(env.RES('makehuman.rc'))
env.Program("makehuman", sources)

# Build module
VariantDir('module_build', 'src', duplicate=0)
moduleEnv = env.Clone(CPPDEFINES = "MAKEHUMAN_AS_MODULE", SHLIBPREFIX = "")
if platform.system() == "Windows":
    moduleEnv["SHLIBSUFFIX"] = ".pyd"
moduleEnv.LoadableModule("mh", ["module_build/core.c", "module_build/glmodule.c", "module_build/arraybuffer.c", "module_build/main.c"])

# Generate a dist directory with all of the material necessary to ship
# use the dist target
if platform.system() == "Windows" and 'dist' in COMMAND_LINE_TARGETS:
    Execute([Delete("dist")])
    Execute([Delete("output.exe")])
    Execute([
        Mkdir("dist"),
        #Microsoft Visual C++ 2k10 Runtime
        Copy("dist", r"C:\Windows\System32\msvcr100.dll"),   
        #Python
        Copy("dist", r"C:\Windows\System32\Python27.dll"),
        Copy("dist/lib",r"C:\Python27\lib"),
        Copy("dist/DLLs",r"C:\Python27\DLLs"),
        #GLEW
        Copy("dist",r"C:\Glew\bin\glew32.dll"),
        #SDL
	Copy("dist",r"C:\SDL\lib\libjpeg-8.dll"),
	Copy("dist",r"C:\SDL\lib\libpng15-15.dll"),
	Copy("dist",r"C:\SDL\lib\libtiff-5.dll"),
	Copy("dist",r"C:\SDL\lib\libwebp-2.dll"),
	Copy("dist",r"C:\SDL\lib\SDL.dll"),
	Copy("dist",r"C:\SDL\lib\SDL_image.dll"),
	Copy("dist",r"C:\SDL\lib\zlib1.dll"),
        #MakeHuman
        Copy("dist","makehuman.exe"),
        Copy("dist","makehuman.exe.manifest"),
        Copy("dist","main.py"),
        Copy("dist/apps","apps"),
        Copy("dist/core","core"),
#        Copy("dist/docs","docs"),
        Copy("dist/tools","tools"),
        Copy("dist/utils","utils"),
        Copy("dist/shared","shared"),
        Copy("dist/importers","importers"),
        Copy("dist/plugins","plugins"),
        Copy("dist/data","data"),
	Copy("dist","setup.nsi"),
	Copy("dist","license.txt"),
        Copy("dist/lib","pythonmodules/_socket.pyd"),
        Copy("dist/lib","pythonmodules/linalg_module.pyd"),
	Copy("dist","mh_export.config"),
    ])
    Execute(['makensis dist/setup.nsi'])



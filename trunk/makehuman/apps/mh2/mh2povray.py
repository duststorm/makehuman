#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
POV-Ray Export functions.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Chris Bartlett, Thanasis Papoutsidakis

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This module implements functions to export a human model in POV-Ray format. POV-Ray is a 
Raytracing application (a renderer) that is free to download and use. The generated text 
file contains POV-Ray Scene Description Language (SDL), which consists of human-readable 
instructions for building 3D scenes. 

This module supports the export of a simple mesh2 object or the export of arrays of data
with accompanying macros to assemble POV-Ray objects. Both formats include some handy 
variable and texture definitions that are written into a POV-Ray include file. A POV-Ray 
scene file is also written to the output directory containing a range of examples 
illustrating the use of the include file.

The content of the generated files follows naming conventions intended to make it simple
to adjust to be compliant with the standards for the POV-Ray Object Collection. All 
identifiers start with 'MakeHuman\_'. You can easily perform a global change on this
prefix so that you end up with your own unique prefix.

"""

import os
import string
import shutil
import subprocess
import projection
import mh2povray_ini
import random
import mh
import log

def downloadPovRay():
    
    import webbrowser
    webbrowser.open('http://www.povray.org/download/')

# Create an instance of the Hairgenerator class with a global context.

def povrayExport(obj, app, settings):
    """
  This function exports data in a format that can be used to reconstruct the humanoid 
  object in POV-Ray. It supports a range of options that can be specified in the Python 
  script file mh2povray_ini.py, which is reloaded each time this function is run. This 
  enables these options to be changed while the MakeHuman application is still running.
  
  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.

  camera:
      *Camera object*. The camera to render from 
  
  """

    log.message('POV-Ray Export of object: %s', obj.name)

    # Read settings from an ini file. This reload enables the settings to be
    # changed dynamically without forcing the user to restart the MH
    # application for the changes to take effect.
  
    camera = app.modelCamera
    resolution = (app.settings.get('rendering_width', 800), app.settings.get('rendering_height', 600))

    reload(mh2povray_ini)
    
    path = os.path.join(mh.getPath('render'), mh2povray_ini.outputpath)
    
    format = mh2povray_ini.format if settings['source'] == 'ini' else settings['format']
    action = mh2povray_ini.action if settings['source'] == 'ini' else settings['action']
    
    # The ini format option defines whether a simple mesh2 object is to be generated
    # or the more flexible but slower array and macro combo is to be generated.

    if format == 'array':
        povrayExportArray(obj, camera, resolution, path)
    if format == 'mesh2':
        #povrayExportMesh2(obj, camera, resolution, path, settings)
        povrayExportMesh2_TL(obj, camera, resolution, path, settings)

    outputDirectory = os.path.dirname(path)
    #
    log.debug('out folder: %s', outputDirectory)

    # Export the hair model as a set of spline definitions.
    # Load the test hair data and write it out in POV-Ray format.
    # still unsupported
    #povrayLoadHairsFile('data/hairs/test.hair')
    #povrayWriteHairs(outputDirectory, obj)

    # The ini action option defines whether or not to attempt to render the file once it's been written.
    #
    povray_bin = (app.settings.get('povray_bin', ''))
   
    # try for use better binarie 
    if os.path.exists(povray_bin):
        exetype = settings['bintype']
        #
        if exetype == 'win64':
            povray_bin += '/pvengine64.exe'
        #
        elif exetype == 'win32sse2':
            povray_bin += '/pvengine-sse2.exe'
        #
        elif exetype == 'win32':
            povray_bin += '/pvengine.exe'
        #
        elif exetype == 'linux':
            povray_bin += '/povray'
        #
        log.debug('Povray path: %s', povray_bin)
        #TODO: what to do if the path is too long? Is there any graphic option in QT to browse for files?

    #
    if action == 'render':
        #
        if os.path.isfile(povray_bin):
            #
            if mh2povray_ini.renderscenefile == '':
                outputSceneFile = path.replace('.inc', '.pov')
                baseName = os.path.basename(outputSceneFile)
            else:
                baseName = mh2povray_ini.renderscenefile
            #
            cmdLineOpt = ' +I%s' %  baseName
            #
            if os.name == 'nt':
                povray_bin = '"' + povray_bin + '"'
                baseName = '"' + baseName + '"'
                cmdLineOpt = ' /RENDER %s' % baseName
            #
            cmdLineOpt += ' +W%d +H%d +a0.3 +am2' % resolution
        
            #
            pathHandle = subprocess.Popen(cwd=outputDirectory, args = povray_bin + cmdLineOpt, shell=True)
        #
        else:
            app.prompt('POV-Ray not found',
                       'You don\'t seem to have POV-Ray installed or the path is incorrect.',
                       'Download',
                       'Cancel',
                       downloadPovRay 
                       )
            return

def povrayExportArray(obj, camera, resolution, path):
    """
  This function exports data in the form of arrays of data the can be used to 
  reconstruct a humanoid object using some very simple POV-Ray macros. These macros 
  can build this data into a variety of different POV-Ray objects, including a
  mesh2 object that represents the human figure much as it was displayed in MakeHuman. 

  These macros can also generate a union of spheres at the vertices and a union of 
  cylinders that follow the edges of the mesh. A parameter on the mesh2 macro can be 
  used to generate a slightly inflated or deflated mesh. 

  The generated output file always starts with a standard header, is followed by a set 
  of array definitions containing the object data and is ended by a standard set of 
  POV-Ray object definitions. 
  
  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.
  
  camera:
      *Camera object*. The camera to render from. 
  
  path:
      *string*. The file system path to the output files that need to be generated. 
  """

  # Certain files and blocks of SDL are mostly static and can be copied directly
  # from reference files into the generated output directories or files.

    headerFile = 'data/povray/headercontent.inc'
    staticFile = 'data/povray/staticcontent.inc'
    sceneFile = 'data/povray/makehuman.pov'
    groupingsFile = 'data/povray/makehuman_groupings.inc'
    pigmentMap = gui3d.app.selectedHuman.mesh.texture

  # Define some additional file related strings

    outputSceneFile = path.replace('.inc', '.pov')
    baseName = os.path.basename(path)
    nameOnly = string.replace(baseName, '.inc', '')
    underScores = ''.ljust(len(baseName), '-')
    outputDirectory = os.path.dirname(path)

  # Make sure the directory exists

    if not os.path.isdir(outputDirectory):
        try:
            os.makedirs(outputDirectory)
        except:
            log.error('Error creating export directory.')
            return 0

  # Open the output file in Write mode

    try:
        outputFileDescriptor = open(path, 'w')
    except:
        log.error('Error opening file to write data.')
        return 0

  # Write the file name into the top of the comment block that starts the file.

    outputFileDescriptor.write('// %s\n' % baseName)
    outputFileDescriptor.write('// %s\n' % underScores)

  # Copy the header file SDL straight across to the output file

    try:
        headerFileDescriptor = open(headerFile, 'r')
    except:
        log.error('Error opening file to read standard headers.')
        return 0
    headerLines = headerFileDescriptor.read()
    outputFileDescriptor.write(headerLines)
    outputFileDescriptor.write('''

''')
    headerFileDescriptor.close()

  # Declare POV_Ray variables containing the current makehuman camera.

    povrayCameraData(camera, resolution, outputFileDescriptor)
    
    outputFileDescriptor.write('#declare MakeHuman_TranslateX      = %s;\n' % -obj.x)
    outputFileDescriptor.write('#declare MakeHuman_TranslateY      = %s;\n' % obj.y)
    outputFileDescriptor.write('#declare MakeHuman_TranslateZ      = %s;\n\n' % obj.z)
    
    outputFileDescriptor.write('#declare MakeHuman_RotateX         = %s;\n' % obj.rx)
    outputFileDescriptor.write('#declare MakeHuman_RotateY         = %s;\n' % -obj.ry)
    outputFileDescriptor.write('#declare MakeHuman_RotateZ         = %s;\n\n' % obj.rz)

  # Calculate some useful values and add them to the output as POV-Ray variable
  # declarations so they can be readily accessed from a POV-Ray scene file.

    povraySizeData(obj, outputFileDescriptor)

  # Vertices - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_VertexArray = array[%s] {\n  ' % len(obj.verts))
    for v in obj.verts:
        outputFileDescriptor.write('<%s,%s,%s>' % (v.co[0], v.co[1], v.co[2]))
    outputFileDescriptor.write('''
}

''')

  # Normals - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_NormalArray = array[%s] {\n  ' % len(obj.verts))
    for v in obj.verts:
        outputFileDescriptor.write('<%s,%s,%s>' % (v.no[0], v.no[1], v.no[2]))
    outputFileDescriptor.write('''
}

''')

    faces = [f for f in obj.faces if not 'joint-' in f.group.name]

  # UV Vectors - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_UVArray = array[%s] {\n  ' % len(obj.uvValues))
    for uv in obj.uvValues:
        
        outputFileDescriptor.write('<%s,%s>' % (uv[0], uv[1]))

    # outputFileDescriptor.write("\n")

    outputFileDescriptor.write('''
}

''')

  # Faces - Write a POV-Ray array of arrays to the output stream

    outputFileDescriptor.write('#declare MakeHuman_FaceArray = array[%s][3] {\n  ' % (len(faces) * 2))
    for f in faces:
        outputFileDescriptor.write('{%s,%s,%s}' % (f.verts[0].idx, f.verts[1].idx, f.verts[2].idx))
        outputFileDescriptor.write('{%s,%s,%s}' % (f.verts[2].idx, f.verts[3].idx, f.verts[0].idx))
    outputFileDescriptor.write('''
}

''')

  # FaceGroups - Write a POV-Ray array to the output stream and build a list of indices
  # that can be used to cross-reference faces to the Face Groups that they're part of.

    outputFileDescriptor.write('#declare MakeHuman_FaceGroupArray = array[%s] {\n  ' % obj.faceGroupCount)
    fgIndex = 0
    faceGroupIndex = {}
    for fg in obj.faceGroups:
        faceGroupIndex[fg.name] = fgIndex
        outputFileDescriptor.write('  "%s",\n' % fg.name)
        fgIndex += 1
    outputFileDescriptor.write('''}

''')

  # FaceGroupIndex - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_FaceGroupIndexArray = array[%s] {\n  ' % len(faces))
    for f in faces:
        outputFileDescriptor.write('%s,' % faceGroupIndex[f.group.name])
    outputFileDescriptor.write('''
}

''')

  # UV Indices for each face - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_UVIndexArray = array[%s][3] {\n  ' % (len(faces) * 2))
    for f in faces:
        outputFileDescriptor.write('{%s,%s,%s}' % (f.uv[0], f.uv[1], f.uv[2]))
        outputFileDescriptor.write('{%s,%s,%s}' % (f.uv[2], f.uv[3], f.uv[0]))
    outputFileDescriptor.write('''
}

''')

  # Joint Positions - Write a set of POV-Ray variables to the output stream

    faceGroupExtents = {}
    for f in obj.faces:
        if 'joint-' in f.group.name:

      # Compare the components of each vertex to find the min and max values for this faceGroup

            if f.group.name in faceGroupExtents:
                maxX = max([f.verts[0].co[0], f.verts[1].co[0], f.verts[2].co[0], f.verts[3].co[0], faceGroupExtents[f.group.name][3]])
                maxY = max([f.verts[0].co[1], f.verts[1].co[1], f.verts[2].co[1], f.verts[3].co[1], faceGroupExtents[f.group.name][4]])
                maxZ = max([f.verts[0].co[2], f.verts[1].co[2], f.verts[2].co[2], f.verts[3].co[2], faceGroupExtents[f.group.name][5]])
                minX = min([f.verts[0].co[0], f.verts[1].co[0], f.verts[2].co[0], f.verts[3].co[0], faceGroupExtents[f.group.name][0]])
                minY = min([f.verts[0].co[1], f.verts[1].co[1], f.verts[2].co[1], f.verts[3].co[1], faceGroupExtents[f.group.name][1]])
                minZ = min([f.verts[0].co[2], f.verts[1].co[2], f.verts[2].co[2], f.verts[3].co[2], faceGroupExtents[f.group.name][2]])
            else:
                maxX = max([f.verts[0].co[0], f.verts[1].co[0], f.verts[2].co[0], f.verts[3].co[0]])
                maxY = max([f.verts[0].co[1], f.verts[1].co[1], f.verts[2].co[1], f.verts[3].co[1]])
                maxZ = max([f.verts[0].co[2], f.verts[1].co[2], f.verts[2].co[2], f.verts[3].co[2]])
                minX = min([f.verts[0].co[0], f.verts[1].co[0], f.verts[2].co[0], f.verts[3].co[0]])
                minY = min([f.verts[0].co[1], f.verts[1].co[1], f.verts[2].co[1], f.verts[3].co[1]])
                minZ = min([f.verts[0].co[2], f.verts[1].co[2], f.verts[2].co[2], f.verts[3].co[2]])
            faceGroupExtents[f.group.name] = [minX, minY, minZ, maxX, maxY, maxZ]

  # Write out the centre position of each joint

    for fg in obj.faceGroups:
        if 'joint-' in fg.name:
            jointVarName = string.replace(fg.name, '-', '_')
            jointCentreX = (faceGroupExtents[fg.name][0] + faceGroupExtents[fg.name][3]) / 2
            jointCentreY = (faceGroupExtents[fg.name][1] + faceGroupExtents[fg.name][4]) / 2
            jointCentreZ = (faceGroupExtents[fg.name][2] + faceGroupExtents[fg.name][5]) / 2

      # jointCentre  = "<"+jointCentreX+","+jointCentreY+","+jointCentreZ+">"

            outputFileDescriptor.write('#declare MakeHuman_%s=<%s,%s,%s>;\n' % (jointVarName, jointCentreX, jointCentreY, jointCentreZ))
    outputFileDescriptor.write('''

''')

  # Copy macro and texture definitions straight across to the output file.

    try:
        staticContentFileDescriptor = open(staticFile, 'r')
    except:
        log.error('Error opening file to read static content.')
        return 0
    staticContentLines = staticContentFileDescriptor.read()
    outputFileDescriptor.write(staticContentLines)
    outputFileDescriptor.write('\n')
    staticContentFileDescriptor.close()

  # The POV-Ray include file is complete

    outputFileDescriptor.close()
    log.message("POV-Ray '#include' file generated.")

  # Copy a sample scene file across to the output directory

    try:
        sceneFileDescriptor = open(sceneFile, 'r')
    except:
        log.error('Error opening file to read standard scene file.')
        return 0
    try:
        outputSceneFileDescriptor = open(outputSceneFile, 'w')
    except:
        log.error('Error opening file to write standard scene file.')
        return 0
    sceneLines = sceneFileDescriptor.read()
    sceneLines = string.replace(sceneLines, 'xxFileNamexx', nameOnly)
    sceneLines = string.replace(sceneLines, 'xxUnderScoresxx', underScores)
    sceneLines = string.replace(sceneLines, 'xxLowercaseFileNamexx', nameOnly.lower())
    outputSceneFileDescriptor.write(sceneLines)

  # Copy the skin texture file into the output directory

    try:
        shutil.copy(pigmentMap, os.path.join(outputDirectory, "texture.png"))
    except (IOError, os.error), why:
        log.error("Can't copy %s" % str(why))

  # Copy the makehuman_groupings.inc file into the output directory

    try:
        shutil.copy(groupingsFile, outputDirectory)
    except (IOError, os.error), why:
        log.error("Can't copy %s" % str(why))

  # Job done

    outputSceneFileDescriptor.close()
    sceneFileDescriptor.close()
    log.message('Sample POV-Ray scene file generated.')


def povrayExportMesh2(obj, camera, resolution, path, settings):
    """
  This function exports data in the form of a mesh2 humanoid object. The POV-Ray 
  file generated is fairly inflexible, but is highly efficient. 
  
  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.
  
  camera:
      *Camera object*. The camera to render from. 
  
  path:
      *string*. The file system path to the output files that need to be generated. 
  """

  # Certain blocks of SDL are mostly static and can be copied directly from reference
  # files into the output files.

    headerFile = 'data/povray/headercontent_mesh2only.inc'
    staticFile = 'data/povray/staticcontent_mesh2only.inc'
    sceneFile = 'data/povray/makehuman_mesh2only.pov'
    pigmentMap = gui3d.app.selectedHuman.mesh.texture

  # Define some additional file locations

    outputSceneFile = path.replace('.inc', '.pov')
    baseName = os.path.basename(path)
    nameOnly = string.replace(baseName, '.inc', '')
    underScores = ''.ljust(len(baseName), '-')
    outputDirectory = os.path.dirname(path)

  # Make sure the directory exists

    if not os.path.isdir(outputDirectory):
        try:
            os.makedirs(outputDirectory)
        except:
            log.error('Error creating export directory.')
            return 0

  # Open the output file in Write mode

    try:
        outputFileDescriptor = open(path, 'w')
    except:
        log.error('Error opening file to write data.')
        return 0

  # Write the file name into the top of the comment block that starts the file.

    outputFileDescriptor.write('// %s\n' % baseName)
    outputFileDescriptor.write('// %s\n' % underScores)

  # Copy the header file SDL straight across to the output file

    try:
        headerFileDescriptor = open(headerFile, 'r')
    except:
        log.error('Error opening file to read standard headers.')
        return 0
    # povman test for include globals settings for test SSS
    SSS = mh2povray_ini.SSS if settings['SSS'] == False else settings['SSS']
    
    if SSS:
        outputFileDescriptor.write('// include global settings \n' +
                                   'global_settings { \n' +
                                   '    assumed_gamma 1 \n' +
                                   '    subsurface { \n' +
                                   '        samples 50, 50 \n' +
                                   '        radiosity off }\n' +
                                   '    mm_per_unit 25 \n' +
                                   '} \n'
                                   )
        
    headerLines = headerFileDescriptor.read()
    outputFileDescriptor.write(headerLines)
    outputFileDescriptor.write('''

''')
    headerFileDescriptor.close()

  # Declare POV_Ray variables containing the current makehuman camera.

    povrayCameraData(camera, resolution, outputFileDescriptor)
    
    outputFileDescriptor.write('#declare MakeHuman_TranslateX    = %s;\n' % -obj.x    +
                               '#declare MakeHuman_TranslateY    = %s;\n' % obj.y     +
                               '#declare MakeHuman_TranslateZ    = %s;\n\n' % obj.z   +
                               '\n' +
                               '#declare MakeHuman_RotateX       = %s;\n' % obj.rx    +
                               '#declare MakeHuman_RotateY       = %s;\n' % -obj.ry   +
                               '#declare MakeHuman_RotateZ       = %s;\n\n' % obj.rz  
                               )

  # Calculate some useful values and add them to the output as POV-Ray variable
  # declarations so they can be readily accessed from a POV-Ray scene file.

    povraySizeData(obj, outputFileDescriptor)

  # Mesh2 Object - Write the initial part of the mesh2 object declaration
  
    # povman; test for write geometry data to new file 
    # --------------------------------------------------------------------------
    outputFileDescriptor.write('#if (file_exists("makehuman_geometry.inc")) \n' +
                               '\t#include "makehuman_geometry.inc" \n' +
                               '#end \n'
                               )
    #
    fileGeometry = path.replace('.inc','_geometry.inc')
    #
    try:
        outputFileGeometry = open(fileGeometry, 'w')
    except:
        log.error('Error opening file to write data.')
        return 0
    #---------------------------------------------------------------------------
    # end
    
    outputFileGeometry.write('\n// Humanoid mesh2 definition\n' +
                             '#declare MakeHuman_Mesh2Object = mesh2 {\n')

  # Vertices - Write a POV-Ray array to the output stream

    outputFileGeometry.write('  vertex_vectors {\n  ' +
                             '    %s\n  ' % len(obj.verts)
                             )
    for v in obj.verts:
        outputFileGeometry.write('<%s,%s,%s>' % (v.co[0], v.co[1], v.co[2]))
    outputFileGeometry.write('''
  }

''')

  # Normals - Write a POV-Ray array to the output stream

    outputFileGeometry.write('  normal_vectors {\n  ' +
                             '    %s\n  ' % len(obj.verts)
                             )
    for v in obj.verts:
        outputFileGeometry.write('<%s,%s,%s>' % (v.no[0], v.no[1], v.no[2]))
    outputFileGeometry.write('''
  }

''')

  # UV Vectors - Write a POV-Ray array to the output stream

    outputFileGeometry.write('  uv_vectors {\n  ' +
                             '    %s\n  ' % len(obj.uvValues)
                             )
    for uv in obj.uvValues:
        outputFileGeometry.write('<%s,%s>' % (uv[0], uv[1]))
        
    outputFileGeometry.write('''
  }

''')

  # Faces - Write a POV-Ray array of arrays to the output stream
    # basic filter: joints and helpers are not need for render
    # if use SSS, separate eyebrows and eyes
    
    faces = [f for f in obj.faces 
             if not 'joint' in f.group.name 
             and not 'helper' in f.group.name]
    #
    if SSS:
        faces = [f for f in faces 
                 if not 'eye-cornea' in f.group.name  # for fix black eyes
                 and not 'eyebrown' in f.group.name
                 and not 'lash' in f.group.name]
    #
    outputFileGeometry.write('  face_indices {\n  ' +
                             '    %s\n  ' % (len(faces) * 2)
                             )
    for f in faces:
        outputFileGeometry.write('<%s,%s,%s>' % (f.verts[0].idx, f.verts[1].idx, f.verts[2].idx) +
                                 '<%s,%s,%s>' % (f.verts[2].idx, f.verts[3].idx, f.verts[0].idx)
                                )
    outputFileGeometry.write('''
  }

''')

  # UV Indices for each face - Write a POV-Ray array to the output stream

    outputFileGeometry.write('  uv_indices {\n  ' +
                             '    %s\n  ' % (len(faces) * 2)
                             )
    for fa in faces:
        cont = 0
        outputFileGeometry.write('<%s,%s,%s>' % (fa.uv[0], fa.uv[1], fa.uv[2]) +
                                 '<%s,%s,%s>' % (fa.uv[2], fa.uv[3], fa.uv[0]) 
                                 )
    outputFileGeometry.write('''
  }
''')
  
  # Mesh2 Object - Write the end squiggly bracket for the mesh2 object declaration

    outputFileGeometry.write('''
  uv_mapping
''')
    outputFileGeometry.write('''}

''')
    
    # povman
    outputFileGeometry.close()
    log.message("POV-Ray 'geometry' file generated.")
    
    # Copy texture definitions straight across to the output file.

    try:
        staticContentFileDescriptor = open(staticFile, 'r')
    except:
        log.error('Error opening file to read static content.')
        return 0
    staticContentLines = staticContentFileDescriptor.read()
    outputFileDescriptor.write(staticContentLines)
    outputFileDescriptor.write('\n')
    staticContentFileDescriptor.close()

    # The POV-Ray include file is complete

    outputFileDescriptor.close()
    log.message("POV-Ray '#include' file generated.")

    # Copy a sample scene file across to the output directory

    try:
        sceneFileDescriptor = open(sceneFile, 'r')
    except:
        log.error('Error opening file to read standard scene file.')
        return 0
    try:
        outputSceneFileDescriptor = open(outputSceneFile, 'w')
    except:
        log.error('Error opening file to write standard scene file.')
        return 0
    sceneLines = sceneFileDescriptor.read()
    sceneLines = string.replace(sceneLines, 'xxFileNamexx', nameOnly)
    sceneLines = string.replace(sceneLines, 'xxUnderScoresxx', underScores)
    sceneLines = string.replace(sceneLines, 'xxLowercaseFileNamexx', nameOnly.lower())
    outputSceneFileDescriptor.write(sceneLines)

    # Copy the skin texture file into the output directory

    try:
        shutil.copy(pigmentMap, os.path.join(outputDirectory, "texture.png"))
    except (IOError, os.error), why:
        log.error("Can't copy %s" % str(why))

    # Job done

    outputSceneFileDescriptor.close()
    sceneFileDescriptor.close()
    log.message('Sample POV-Ray scene file generated')


def povrayCameraData(camera, resolution, outputFileDescriptor, settings):
    """
  This function outputs standard camera data common to all POV-Ray format exports. 

  Parameters
  ----------
  
  cameraSettings:
      *list of floats*. A list of float values conveying camera and image related 
      information. This includes the position, orientation and field of view of the
      camera along with the screen dimensions from MakeHuman. These values are passed 
      along to POV-Ray as variables so that the default rendered image can mimic the
      image last displayed in MakeHuman. 
  
  outputFileDescriptor:
      *file descriptor*. The file to which the camera settings need to be written. 
  """

    outputFileDescriptor.write('// MakeHuman Camera and Viewport Settings. \n')
    if settings['SSS'] == True:
        outputFileDescriptor.write('#declare MakeHuman_LightX      = %s;\n' % 11)
        outputFileDescriptor.write('#declare MakeHuman_LightY      = %s;\n' % 20)
        outputFileDescriptor.write('#declare MakeHuman_LightZ      = %s;\n' % 20)
    else:
        outputFileDescriptor.write('#declare MakeHuman_LightX      = %s;\n' % camera.eyeX)
        outputFileDescriptor.write('#declare MakeHuman_LightY      = %s;\n' % camera.eyeY)
        outputFileDescriptor.write('#declare MakeHuman_LightZ      = %s;\n' % camera.eyeZ)
    outputFileDescriptor.write('#declare MakeHuman_EyeX        = %s;\n' % camera.eyeX)
    outputFileDescriptor.write('#declare MakeHuman_EyeY        = %s;\n' % camera.eyeY)
    outputFileDescriptor.write('#declare MakeHuman_EyeZ        = %s;\n' % camera.eyeZ)
    outputFileDescriptor.write('#declare MakeHuman_FocusX      = %s;\n' % camera.focusX)
    outputFileDescriptor.write('#declare MakeHuman_FocusY      = %s;\n' % camera.focusY)
    outputFileDescriptor.write('#declare MakeHuman_FocusZ      = %s;\n' % camera.focusZ)
    outputFileDescriptor.write('#declare MakeHuman_ImageHeight = %s;\n' % resolution[1])
    outputFileDescriptor.write('#declare MakeHuman_ImageWidth  = %s;\n' % resolution[0])
    outputFileDescriptor.write('''

''')


def povraySizeData(obj, outputFileDescriptor):
    """
  This function outputs standard object dimension data common to all POV-Ray 
  format exports. 

  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.
  
  outputFileDescriptor:
      *file descriptor*. The file to which the camera settings need to be written. 
  """

    maxX = 0
    maxY = 0
    maxZ = 0
    minX = 0
    minY = 0
    minZ = 0
    for v in obj.verts:
        maxX = max(maxX, v.co[0])
        maxY = max(maxY, v.co[1])
        maxZ = max(maxZ, v.co[2])
        minX = min(minX, v.co[0])
        minY = min(minY, v.co[1])
        minZ = min(minZ, v.co[2])
    outputFileDescriptor.write('// Figure Dimensions. \n')
    outputFileDescriptor.write('#declare MakeHuman_MaxExtent = < %s, %s, %s>;\n' % (maxX, maxY, maxZ))
    outputFileDescriptor.write('#declare MakeHuman_MinExtent = < %s, %s, %s>;\n' % (minX, minY, minZ))
    outputFileDescriptor.write('#declare MakeHuman_Center    = < %s, %s, %s>;\n' % ((maxX + minX) / 2, (maxY + minY) / 2, (maxZ + minZ) / 2))
    outputFileDescriptor.write('#declare MakeHuman_Width     = %s;\n' % (maxX - minX))
    outputFileDescriptor.write('#declare MakeHuman_Height    = %s;\n' % (maxY - minY))
    outputFileDescriptor.write('#declare MakeHuman_Depth     = %s;\n' % (maxZ - minZ))
    outputFileDescriptor.write('''

''')


# Temporary Function: The loading of hairs should be done by the main application.


def povrayLoadHairsFile(path):

    pass
    #hairsClass.loadHairs(path)


def povrayWriteHairs(outputDirectory, mesh):
    """
  This function generates hair for the POV-Ray format export. Each hair is 
  written out as a sphere_sweep. 

  Parameters
  ----------
  
  outputDirectory:
      *directory path*. A string containing the name of the directory into which the
      output file is to be written. 
  
  mesh:
      *mesh object*. The humanoid mesh object to which hair is added. 
  """
    return # This code needs to be updated
    log.message('Writing hair')

    hairsClass.humanVerts = mesh.verts
    hairsClass.adjustGuides()
    hairsClass.generateHairStyle1()
    hairsClass.generateHairStyle2()

  # The output file name should really be picked up from screen field settings.

    hairFileName = '%s/makehuman_hair.inc' % outputDirectory
    hairFile = open(hairFileName, 'w')

  # Need to work out the total number of hairs upfront to know what size
  # array will be needed in POV-Ray. Writing to an array rather than adding
  # the hairs directly to the scene helps reduce the rendering times for
  # test renders, because you can easily render every 10th hair or every
  # 100th hair.

    totalNumberOfHairs = 0
    for hSet in hairsClass.hairStyle:
        totalNumberOfHairs += len(hSet.hairs)
    hairFile.write('#declare MakeHuman_HairArray = array[%i] {\n' % totalNumberOfHairs)

  # MakeHuman hair styles consist of lots of sets of hairs.

    hairCounter = 0
    for hSet in hairsClass.hairStyle:
        if 'clump' in hSet.name:
            hDiameter = hairsClass.hairDiameterClump * random.uniform(0.5, 1)
        else:
            hDiameter = hairsClass.hairDiameterMultiStrand * random.uniform(0.5, 1)

    # Each hair is represented as a separate sphere_sweep in POV-Ray.

        for hair in hSet.hairs:
            hairCounter += 1
            hairFile.write('sphere_sweep{')
            hairFile.write('b_spline ')
            hairFile.write('%i,' % len(hair.controlPoints))
            controlPointCounter = 0

      # Each control point is written out, along with the radius of the
      # hair at that point.

            for cP in hair.controlPoints:
                controlPointCounter += 1
                hairFile.write('<%s,%s,%s>,%s' % (round(cP[0], 4), round(cP[1], 4), round(cP[2], 4), round(hDiameter / 2, 4)))

      # All coordinates except the last need a following comma.

                if controlPointCounter != len(hair.controlPoints):
                    hairFile.write(',')

      # End the sphere_sweep declaration for this hair

            hairFile.write('}')

      # All but the final sphere_sweep (each array element) needs a terminating comma.

            if hairCounter != totalNumberOfHairs:
                hairFile.write(',\n')
            else:
                hairFile.write('\n')

  # End the array declaration.

    hairFile.write('}\n')
    hairFile.write('\n')

  # Pick up the hair color and create a default POV-Ray hair texture.

    hairFile.write('#ifndef (MakeHuman_HairTexture)\n')
    hairFile.write('  #declare MakeHuman_HairTexture = texture {\n')
    hairFile.write('    pigment {rgb <%s,%s,%s>}\n' % (hairsClass.tipColor[0], hairsClass.tipColor[1], hairsClass.tipColor[2]))
    hairFile.write('  }\n')
    hairFile.write('#end\n')
    hairFile.write('\n')

  # Dynamically create a union of the hairs (or a subset of the hairs).
  # By default use every 25th hair, which is usually ok for test renders.

    hairFile.write('#ifndef(MakeHuman_HairStep) #declare MakeHuman_HairStep = 25; #end\n')
    hairFile.write('union{\n')
    hairFile.write('  #local MakeHuman_I = 0;\n')
    hairFile.write('  #while (MakeHuman_I < %i)\n' % totalNumberOfHairs)
    hairFile.write('    object {MakeHuman_HairArray[MakeHuman_I] texture{MakeHuman_HairTexture}}\n')
    hairFile.write('    #local MakeHuman_I = MakeHuman_I + MakeHuman_HairStep;\n')
    hairFile.write('  #end\n')

  # hairFile.write('  translate -z*0.0\n')

    hairFile.write('}')
    hairFile.close()
    log.message('Totals hairs written: %s', totalNumberOfHairs)
    log.message('Number of tufts %s', len(hairsClass.hairStyle))


#--------------------------------------------------------------------------
#   TL: A version of povrayExportMesh2 that handles clothes
#--------------------------------------------------------------------------

import gui3d
import mh2proxy
import object_collection

def povrayExportMesh2_TL(obj, camera, resolution, path, settings):
    """
    This function exports data in the form of a mesh2 humanoid object. The POV-Ray 
    file generated is fairly inflexible, but is highly efficient. 

    Parameters
    ----------

    obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.

    camera:
      *Camera object*. The camera to render from. 

    path:
      *string*. The file system path to the output files that need to be generated. 
    """

    # Certain blocks of SDL are mostly static and can be copied directly from reference
    # files into the output files.
    headerFile = 'data/povray/headercontent_mesh2only.inc'
    staticFile = 'data/povray/staticcontent_mesh2only_fsss.inc' if settings['SSS'] == True else 'data/povray/staticcontent_mesh2only_tl.inc'
    sceneFile = 'data/povray/makehuman_mesh2only_tl.pov'
    pigmentMap = gui3d.app.selectedHuman.mesh.texture

    # Define some additional file locations
    outputSceneFile = path.replace('.inc', '.pov')
    baseName = os.path.basename(path)
    nameOnly = string.replace(baseName, '.inc', '')
    underScores = ''.ljust(len(baseName), '-')
    outputDirectory = os.path.dirname(path)

    # Make sure the directory exists
    if not os.path.isdir(outputDirectory):
        try:
            os.makedirs(outputDirectory)
        except:
            log.error('Error creating export directory.')
            return 0

    # If fake SSS is enabled, render lightmaps there. # TODO: if they aren't already rendered.
    if settings['SSS'] == True:
        # calculate resolution of each cannel, according to settings
        resred = int(settings['SSSA'])
        resgreen = 2**(10-resred/2) 
        resred = 2**(10-resred)
        # blue channel
        lmap = projection.mapLighting()
        log.debug('SSS: Hi-Res lightmap resolution: %s', lmap.width)
        lmap.save(os.path.join(outputDirectory, 'lighthi.png'))
        # green channel
        lmap.resize(resgreen,resgreen)
        log.debug('SSS: Mid-Res lightmap resolution: %s', lmap.width)
        lmap.save(os.path.join(outputDirectory, 'lightmid.png'))
        # red channel
        lmap.resize(resred,resred)
        log.debug('SSS: Low-Res lightmap resolution: %s', lmap.width)
        lmap.save(os.path.join(outputDirectory, 'lightlo.png'))

    # Open the output file in Write mode
    try:
        outputFileDescriptor = open(path, 'w')
    except:
        log.error('Error opening file to write data.')
        return 0

    # Write the file name into the top of the comment block that starts the file.
    outputFileDescriptor.write('// %s\n' % baseName)
    outputFileDescriptor.write('// %s\n' % underScores)

    # Copy the header file SDL straight across to the output file
    try:
        headerFileDescriptor = open(headerFile, 'r')
    except:
        log.error('Error opening file to read standard headers.')
        return 0
    headerLines = headerFileDescriptor.read()
    outputFileDescriptor.write(headerLines)
    outputFileDescriptor.write('''

''')
    headerFileDescriptor.close()

    # Declare POV Ray variables containing the current makehuman camera.
    povrayCameraData(camera, resolution, outputFileDescriptor, settings)
    
    # Declare POV Ray variables containing the current object position and rotation.
    outputFileDescriptor.write('#declare MakeHuman_TranslateX      = %s;\n' % -obj.x)
    outputFileDescriptor.write('#declare MakeHuman_TranslateY      = %s;\n' % obj.y)
    outputFileDescriptor.write('#declare MakeHuman_TranslateZ      = %s;\n\n' % obj.z)
    outputFileDescriptor.write('#declare MakeHuman_RotateX         = %s;\n' % obj.rx)
    outputFileDescriptor.write('#declare MakeHuman_RotateY         = %s;\n' % -obj.ry)
    outputFileDescriptor.write('#declare MakeHuman_RotateZ         = %s;\n\n' % obj.rz)

    # Calculate some useful values and add them to the output as POV-Ray variable
    # declarations so they can be readily accessed from a POV-Ray scene file.

    povraySizeData(obj, outputFileDescriptor)

    stuffs = object_collection.setupObjects("MakeHuman", gui3d.app.selectedHuman, helpers=False, hidden=False, eyebrows=False, lashes=False, subdivide = settings['subdivide'])

    # Mesh2 Object - Write the initial part of the mesh2 object declaration
    for stuff in stuffs:

        outputFileDescriptor.write('// Humanoid mesh2 definition\n')
        outputFileDescriptor.write('#declare %s_Mesh2Object = mesh2 {\n' % stuff.name)

        # Vertices - Write a POV-Ray array to the output stream
        outputFileDescriptor.write('  vertex_vectors {\n  ')
        outputFileDescriptor.write('    %s\n  ' % len(stuff.verts))

        for v in stuff.verts:
            outputFileDescriptor.write('<%s,%s,%s>' % (-v[0],v[1],v[2]))
        outputFileDescriptor.write('''
  }

''')

        # Normals - Write a POV-Ray array to the output stream
        outputFileDescriptor.write('  normal_vectors {\n  ')
        outputFileDescriptor.write('    %s\n  ' % len(stuff.verts))
        for vno in stuff.vnormals:
            outputFileDescriptor.write('<%s,%s,%s>' % (-vno[0],vno[1],vno[2]))

        outputFileDescriptor.write('''
  }

''')
    
        # UV Vectors - Write a POV-Ray array to the output stream
        outputFileDescriptor.write('  uv_vectors {\n  ')
        outputFileDescriptor.write('    %s\n  ' % len(stuff.uvValues))
        for uv in stuff.uvValues:
            outputFileDescriptor.write('<%s,%s>' % tuple(uv))        

        outputFileDescriptor.write('''
  }

''')

        # Faces - Write a POV-Ray array of arrays to the output stream
        nTriangles = 0
        for f in stuff.faces:
            nTriangles += len(f)-2

        outputFileDescriptor.write('  face_indices {\n  ')
        outputFileDescriptor.write('    %s\n  ' % nTriangles)

        for f in stuff.faces:
            verts = []
            for v,vt in f:
                verts.append(v)
            outputFileDescriptor.write('<%s,%s,%s>' % (verts[0], verts[1], verts[2]))
            if len(verts) == 4:
                outputFileDescriptor.write('<%s,%s,%s>' % (verts[2], verts[3], verts[0]))

        outputFileDescriptor.write('''
  }

''')


        # UV Indices for each face - Write a POV-Ray array to the output stream
        outputFileDescriptor.write('  uv_indices {\n  ')
        outputFileDescriptor.write('    %s\n  ' % nTriangles)

        for f in stuff.faces:
            vts = []
            for v,vt in f:
                vts.append(vt)        
            outputFileDescriptor.write('<%s,%s,%s>' % (vts[0], vts[1], vts[2]))
            if len(vts) == 4:
                outputFileDescriptor.write('<%s,%s,%s>' % (vts[2], vts[3], vts[0]))

        outputFileDescriptor.write('''
  }
''')

        # Mesh2 Object - Write the end squiggly bracket for the mesh2 object declaration
        outputFileDescriptor.write('''
      uv_mapping
''')
        outputFileDescriptor.write('''}

''')

    # Copy texture definitions to the output file.
    try:
        staticContentFileDescriptor = open(staticFile, 'r')
    except:
        log.error('Error opening file to read static content.')
        return 0
    staticContentLines = staticContentFileDescriptor.read()
    staticContentLines = string.replace(staticContentLines, '%%skinoil%%', str(settings['skinoil']))    
    staticContentLines = string.replace(staticContentLines, '%%rough%%', str(settings['rough']))    
    staticContentLines = string.replace(staticContentLines, '%%wrinkles%%', str(settings['wrinkles']))    
    outputFileDescriptor.write(staticContentLines)
    outputFileDescriptor.write('\n')
    staticContentFileDescriptor.close()
    
    # Write items' materials 
    writeItemsMaterials(outputFileDescriptor, stuffs)
             
    # The POV-Ray include file is complete
    outputFileDescriptor.close()
    log.message("POV-Ray '#include' file generated.")

    # Copy a sample scene file across to the output directory
    try:
        sceneFileDescriptor = open(sceneFile, 'r')
    except:
        log.error('Error opening file to read standard scene file.')
        return 0
    try:
        outputSceneFileDescriptor = open(outputSceneFile, 'w')
    except:
        log.error('Error opening file to write standard scene file.')
        return 0
    sceneLines = sceneFileDescriptor.read()
    sceneLines = string.replace(sceneLines, 'xxFileNamexx', nameOnly)
    sceneLines = string.replace(sceneLines, 'xxUnderScoresxx', underScores)
    sceneLines = string.replace(sceneLines, 'xxLowercaseFileNamexx', nameOnly.lower())
    outputSceneFileDescriptor.write(sceneLines)
    
    for stuff in stuffs:
        outputSceneFileDescriptor.write(
            "object { \n" +
            "   %s_Mesh2Object \n" % stuff.name +
            "   rotate <0, 0, MakeHuman_RotateZ> \n" +
            "   rotate <0, MakeHuman_RotateY, 0> \n" +
            "   rotate <MakeHuman_RotateX, 0, 0> \n" +
            "   translate <MakeHuman_TranslateX, MakeHuman_TranslateY, MakeHuman_TranslateZ> \n" +
            "   material {%s_Material} \n" % stuff.name +
            "}  \n")

    # Job done, clean up
    outputSceneFileDescriptor.close()
    sceneFileDescriptor.close()

    # Copy the skin texture file into the output directory
    copyFile(pigmentMap, os.path.join(outputDirectory, "texture.png"))

    for stuff in stuffs[1:]:
        if stuff.texture:
            copyFile(stuff.texture, outputDirectory)
        """
        if proxy.normal:
            copyFile(proxy.normal, outputDirectory)
        if proxy.bump:
            copyFile(proxy.bump, outputDirectory)
        if proxy.displacement:
            copyFile(proxy.displacement, outputDirectory)
        if proxy.transparency:
            copyFile(proxy.transparency, outputDirectory)
        """

    log.message('Sample POV-Ray scene file generated')

"""
Item types
(Negative value) - Error code
0   - Nothing
1   - Generic
2   - Hair
"""
def writeItemsMaterials(outputFileDescriptor, stuffs):
    for stuff in stuffs[1:]:
        proxy = stuff.proxy
        if proxy.type == 'Clothes' and proxy.getUuid() == gui3d.app.selectedHuman.hairProxy.getUuid():
            itemtype = 2
        else:
            itemtype = 1
        outputFileDescriptor.write("#ifndef (%s_Material)\n" % stuff.name +
                                   "#declare %s_Texture =\n" % stuff.name +
                                   "    texture {\n")
        texdata = getChannelData(stuff.texture)                        
        if texdata:                
            outputFileDescriptor.write(
                    '        pigment { image_map {%s "%s" interpolate 2} }\n' % (texdata[1], texdata[0]))
        else:
            outputFileDescriptor.write(
                    '        pigment { rgb <1,1,1> }\n')
        bumpdata = getChannelData(proxy.bump)
        if bumpdata:
           outputFileDescriptor.write(
                    '        normal { bump_map {%s "%s" interpolate 2} }\n' % (bumpdata[1], bumpdata[0]))
        else:
            if itemtype == 2:
                outputFileDescriptor.write(
                        '        normal { ripples 0 scale 0.005 }\n')
            else:
                outputFileDescriptor.write(
                        '        normal { wrinkles 0.2 scale 0.0001 }\n')
        if itemtype == 2:
            outputFileDescriptor.write ("        finish {\n" +
                                "            specular 0\n" +
                                "            roughness 0.5\n" +
                                "            phong 0 phong_size 0 \n" +
                                "            ambient 0\n" +
                                "            diffuse 1\n" +
                                "            reflection {0}\n" +
                                "            conserve_energy\n" +
                                "        }\n" +
                                "    }\n\n" +
                                "#declare %s_Material = material {\n" % stuff.name +
                                "    texture {\n" +
                                "        uv_mapping\n" +
                                "        %s_Texture\n" % stuff.name +
                                "    }\n"
                                "    interior {ior 1}\n" +
                                "}\n\n" +
                                "#end\n")
        else:
            outputFileDescriptor.write ("        finish {\n" +
                                "            specular 0.05\n" +
                                "            roughness 0.2\n" +
                                "            phong 0 phong_size 0 \n" +
                                "            ambient 0.1\n" +
                                "            diffuse 0.9\n" +
                                "            reflection {0}\n" +
                                "            conserve_energy\n" +
                                "        }\n" +
                                "    }\n\n" +
                                "#declare %s_Material = material {\n" % stuff.name +
                                "    texture {\n" +
                                "        uv_mapping\n" +
                                "        %s_Texture\n" % stuff.name +
                                "    }\n"
                                "    interior {ior 1.33}\n" +
                                "}\n\n" +
                                "#end\n")


def writeChannel(outputFileDescriptor, var, channel, stuff, data):
    (path, type) = data
    outputFileDescriptor.write(
            "    #declare %s_%s = %s { \n" % (var, stuff.name, channel) +
            '       image_map { %s "%s" interpolate 2} \n' % (type, path) +
            "    } \n" +
            "     \n")            


def getChannelData(value):
    if value:
        (folder, file) = value
        (fname, ext) = os.path.splitext(file)
        ext = ext.lower()
        if ext == ".tif":
            type = "tiff"
        elif ext == ".jpg":
            type = "jpeg"
        else:
            type = ext[1:]
        return file,type
    else:
        return None
                

def copyFile(path, outputDirectory):
    if isinstance(path, tuple):
        (folder, file) = path
        path = os.path.join(folder, file)
    if path:
        path = os.path.realpath(os.path.expanduser(path))
        log.debug("Copy %s to %s" % (path, outputDirectory))
        try:
            shutil.copy(path, outputDirectory)
        except (IOError, os.error), why:
            log.error("Can't copy %s" % str(why))

#--------------------------------------------------------------------------
#   End TL modications
#--------------------------------------------------------------------------


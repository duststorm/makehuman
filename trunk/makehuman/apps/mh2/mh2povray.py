#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
POV-Ray Export functions.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Chris Bartlett

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

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
import mh2povray_ini
import random
import mh

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

    print 'POV-Ray Export of object: ', obj.name

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
        povrayExportMesh2(obj, camera, resolution, path)

    outputDirectory = os.path.dirname(path)

    # Export the hair model as a set of spline definitions.
    # Load the test hair dataand write it out in POV-Ray format.
  
    #still unsupported
    #povrayLoadHairsFile('data/hairs/test.hair')
    #povrayWriteHairs(outputDirectory, obj)

    # The ini action option defines whether or not to attempt to render the file once
    # it's been written.

    if action == 'render':
       
        if not os.path.isfile(mh2povray_ini.povray_path):
            app.prompt('POV-Ray not found', 'You don\'t seem to have POV-Ray installed or the path in mh2povray_ini.py is incorrect.', 'Download', 'Cancel', downloadPovRay)
            return
    
        if mh2povray_ini.renderscenefile == '':
            outputSceneFile = path.replace('.inc', '.pov')
            baseName = os.path.basename(outputSceneFile)
        else:
            baseName = mh2povray_ini.renderscenefile
        cmdLineOpt = ' +I%s' % baseName
        if os.name == 'nt':
            cmdLineOpt = ' /RENDER %s' % baseName
        cmdLineOpt += ' +W%d +H%d' % resolution

        # pathHandle = subprocess.Popen(cwd = outputDirectory, args = mh2povray_ini.povray_path + " /RENDER " + baseName)
    
        #print mh2povray_ini.povray_path + cmdLineOpt

        pathHandle = subprocess.Popen(cwd=outputDirectory, args=mh2povray_ini.povray_path + cmdLineOpt)

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
    pigmentMap = 'data/textures/texture.tif'

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
            print 'Error creating export directory.'
            return 0

  # Open the output file in Write mode

    try:
        outputFileDescriptor = open(path, 'w')
    except:
        print 'Error opening file to write data.'
        return 0

  # Write the file name into the top of the comment block that starts the file.

    outputFileDescriptor.write('// %s\n' % baseName)
    outputFileDescriptor.write('// %s\n' % underScores)

  # Copy the header file SDL straight across to the output file

    try:
        headerFileDescriptor = open(headerFile, 'r')
    except:
        print 'Error opening file to read standard headers.'
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
        print 'Error opening file to read static content.'
        return 0
    staticContentLines = staticContentFileDescriptor.read()
    outputFileDescriptor.write(staticContentLines)
    outputFileDescriptor.write('\n')
    staticContentFileDescriptor.close()

  # The POV-Ray include file is complete

    outputFileDescriptor.close()
    print "POV-Ray '#include' file generated."

  # Copy a sample scene file across to the output directory

    try:
        sceneFileDescriptor = open(sceneFile, 'r')
    except:
        print 'Error opening file to read standard scene file.'
        return 0
    try:
        outputSceneFileDescriptor = open(outputSceneFile, 'w')
    except:
        print 'Error opening file to write standard scene file.'
        return 0
    sceneLines = sceneFileDescriptor.read()
    sceneLines = string.replace(sceneLines, 'xxFileNamexx', nameOnly)
    sceneLines = string.replace(sceneLines, 'xxUnderScoresxx', underScores)
    sceneLines = string.replace(sceneLines, 'xxLowercaseFileNamexx', nameOnly.lower())
    outputSceneFileDescriptor.write(sceneLines)

  # Copy the textures.tif file into the output directory

    try:
        shutil.copy(pigmentMap, outputDirectory)
    except (IOError, os.error), why:
        print "Can't copy %s" % str(why)

  # Copy the makehuman_groupings.inc file into the output directory

    try:
        shutil.copy(groupingsFile, outputDirectory)
    except (IOError, os.error), why:
        print "Can't copy %s" % str(why)

  # Job done

    outputSceneFileDescriptor.close()
    sceneFileDescriptor.close()
    print 'Sample POV-Ray scene file generated.'


def povrayExportMesh2(obj, camera, resolution, path):
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
    pigmentMap = 'data/textures/texture.tif'

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
            print 'Error creating export directory.'
            return 0

  # Open the output file in Write mode

    try:
        outputFileDescriptor = open(path, 'w')
    except:
        print 'Error opening file to write data.'
        return 0

  # Write the file name into the top of the comment block that starts the file.

    outputFileDescriptor.write('// %s\n' % baseName)
    outputFileDescriptor.write('// %s\n' % underScores)

  # Copy the header file SDL straight across to the output file

    try:
        headerFileDescriptor = open(headerFile, 'r')
    except:
        print 'Error opening file to read standard headers.'
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

  # Mesh2 Object - Write the initial part of the mesh2 object declaration

    outputFileDescriptor.write('// Humanoid mesh2 definition\n')
    outputFileDescriptor.write('#declare MakeHuman_Mesh2Object = mesh2 {\n')

  # Vertices - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('  vertex_vectors {\n  ')
    outputFileDescriptor.write('    %s\n  ' % len(obj.verts))
    for v in obj.verts:
        outputFileDescriptor.write('<%s,%s,%s>' % (v.co[0], v.co[1], v.co[2]))
    outputFileDescriptor.write('''
  }

''')

  # Normals - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('  normal_vectors {\n  ')
    outputFileDescriptor.write('    %s\n  ' % len(obj.verts))
    for v in obj.verts:
        outputFileDescriptor.write('<%s,%s,%s>' % (v.no[0], v.no[1], v.no[2]))
    outputFileDescriptor.write('''
  }

''')

    faces = [f for f in obj.faces if not 'joint-' in f.group.name]

  # UV Vectors - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('  uv_vectors {\n  ')
    outputFileDescriptor.write('    %s\n  ' % len(obj.uvValues))
    for uv in obj.uvValues:
        
        outputFileDescriptor.write('<%s,%s>' % (uv[0], uv[1]))
        
    outputFileDescriptor.write('''
  }

''')

  # Faces - Write a POV-Ray array of arrays to the output stream

    outputFileDescriptor.write('  face_indices {\n  ')
    outputFileDescriptor.write('    %s\n  ' % (len(faces) * 2))
    for f in faces:
        outputFileDescriptor.write('<%s,%s,%s>' % (f.verts[0].idx, f.verts[1].idx, f.verts[2].idx))
        outputFileDescriptor.write('<%s,%s,%s>' % (f.verts[2].idx, f.verts[3].idx, f.verts[0].idx))
    outputFileDescriptor.write('''
  }

''')

  # UV Indices for each face - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('  uv_indices {\n  ')
    outputFileDescriptor.write('    %s\n  ' % (len(faces) * 2))
    for f in faces:
        outputFileDescriptor.write('<%s,%s,%s>' % (f.uv[0], f.uv[1], f.uv[2]))
        outputFileDescriptor.write('<%s,%s,%s>' % (f.uv[2], f.uv[3], f.uv[0]))
    outputFileDescriptor.write('''
  }
''')

  # Mesh2 Object - Write the end squiggly bracket for the mesh2 object declaration

    outputFileDescriptor.write('''
  uv_mapping
''')
    outputFileDescriptor.write('''}

''')

  # Copy texture definitions straight across to the output file.

    try:
        staticContentFileDescriptor = open(staticFile, 'r')
    except:
        print 'Error opening file to read static content.'
        return 0
    staticContentLines = staticContentFileDescriptor.read()
    outputFileDescriptor.write(staticContentLines)
    outputFileDescriptor.write('\n')
    staticContentFileDescriptor.close()

  # The POV-Ray include file is complete

    outputFileDescriptor.close()
    print "POV-Ray '#include' file generated."

  # Copy a sample scene file across to the output directory

    try:
        sceneFileDescriptor = open(sceneFile, 'r')
    except:
        print 'Error opening file to read standard scene file.'
        return 0
    try:
        outputSceneFileDescriptor = open(outputSceneFile, 'w')
    except:
        print 'Error opening file to write standard scene file.'
        return 0
    sceneLines = sceneFileDescriptor.read()
    sceneLines = string.replace(sceneLines, 'xxFileNamexx', nameOnly)
    sceneLines = string.replace(sceneLines, 'xxUnderScoresxx', underScores)
    sceneLines = string.replace(sceneLines, 'xxLowercaseFileNamexx', nameOnly.lower())
    outputSceneFileDescriptor.write(sceneLines)

  # Copy the textures.tif file into the output directory

    try:
        shutil.copy(pigmentMap, outputDirectory)
    except (IOError, os.error), why:
        print "Can't copy %s" % str(why)

  # Job done

    outputSceneFileDescriptor.close()
    sceneFileDescriptor.close()
    print 'Sample POV-Ray scene file generated'


def povrayCameraData(camera, resolution, outputFileDescriptor):
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
    print 'Writing hair'

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
    print 'Totals hairs written: ', totalNumberOfHairs
    print 'Number of tufts', len(hairsClass.hairStyle)



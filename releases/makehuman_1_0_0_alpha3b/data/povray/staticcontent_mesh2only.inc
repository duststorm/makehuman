// Create a camera definition based on the MakeHuman camera settings when this 
// file was generated. We need to convert between the OpenGL vertical FOV and 
// the horizontal POV-Ray camera angle. We also need to account for the way 
// OpenGL reports its camera data, translating before rotating, which further 
// moves the camera. The x-axis is also reversed to the standard POV-Ray settings.
#declare MakeHuman_CameraAngle = 2*atan2d((MakeHuman_ImageWidth/MakeHuman_ImageHeight)*tand(MakeHuman_CameraFOV/2),1);
#declare MakeHuman_Camera = camera {
  location 0 look_at -z
  angle MakeHuman_CameraAngle
  translate <MakeHuman_CameraX, -MakeHuman_CameraY, MakeHuman_CameraZ>
  rotate <-MakeHuman_CameraXRot, MakeHuman_CameraYRot, 0>
}

// Create a standard light definition based on MakeHuman settings.
#declare MakeHuman_LightSource = light_source {<10,10,40>, rgb 1
  translate < MakeHuman_CameraX, -MakeHuman_CameraY, MakeHuman_CameraZ>
  rotate <-MakeHuman_CameraXRot,  MakeHuman_CameraYRot, 0>
}

// Assign default values.
// This texture uses the standard pigment map as a uv-mapped pigment and adds a
// little disruption to the surface normals.  
#ifndef (MakeHuman_Texture)
  #declare MakeHuman_Texture = texture {
    pigment {uv_mapping
      image_map {
        tiff "texture.tif"
      }
    }
    normal {agate 0.3 scale 0.002}
    finish {phong 0.25}
  }
#end

                                                                            
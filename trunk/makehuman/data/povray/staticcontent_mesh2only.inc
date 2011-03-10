// Create a camera definition based on the MakeHuman camera settings when this 
// file was generated. We need to convert between the OpenGL vertical FOV and 
// the horizontal POV-Ray camera angle. We also need to account for the way 
// OpenGL reports its camera data, translating before rotating, which further 
// moves the camera. The x-axis is also reversed to the standard POV-Ray settings.
#declare MakeHuman_Camera = camera {
  perspective
  location <MakeHuman_EyeX, MakeHuman_EyeY, MakeHuman_EyeZ>
  look_at <MakeHuman_FocusX, MakeHuman_FocusY, MakeHuman_FocusZ>
  angle 30
}

// Create a standard light definition based on MakeHuman settings.
#declare MakeHuman_LightSource = light_source {<10,10,40>, rgb 1
  translate < MakeHuman_LightX, -MakeHuman_LightY, MakeHuman_LightZ>
  rotate <0, 0, 0>
}

// Assign default values.
// This texture uses the standard pigment map as a uv-mapped pigment and adds a
// little disruption to the surface normals.  
#ifndef (MakeHuman_Texture)
  #declare MakeHuman_Texture = texture {
    pigment {
      image_map {
        tiff "texture.tif"
      }
    }
    normal {agate 0.3 scale 0.002}
    finish {phong 0.25}
  }
#end

                                                                            
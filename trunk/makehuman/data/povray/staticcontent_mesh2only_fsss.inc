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
#declare MakeHuman_LightSource = light_source {
    <MakeHuman_LightX, MakeHuman_LightY, MakeHuman_LightZ>
    color rgb 1
    spotlight
    radius 1000
    falloff 1000
    tightness 1
    point_at < MakeHuman_TranslateX, MakeHuman_TranslateY, MakeHuman_TranslateZ>
}

// Create the skin material.
// This texture implements a fake SubSurface Scattering method
// using premade lightmaps.  
#ifndef (MakeHuman_Material)                            

#declare TEXTURE = 
    texture {
        pigment { image_map {png "lightlo.png" interpolate 2} }
        normal  { wrinkles %%wrinkles%% scale 0.0002 }
        finish { 
            specular 0
            roughness 0.01
            phong 0 phong_size 0
            ambient rgb <3,0,0> // Apply blur to red channel.
            diffuse 0 //2.0
            reflection {0}
            conserve_energy
        }
    }
    texture {
        pigment { image_map {png "lighthi.png" interpolate 2 transmit all 1/3} }
        normal  { wrinkles %%wrinkles%% scale 0.0002 }
        finish { 
            specular 0
            roughness 0.01
            phong 0 phong_size 0
            ambient rgb <0,1.5,1.5>
            diffuse 0 //2.0
            reflection {0}
            conserve_energy
        }
    }
    texture {
        pigment { image_map {png "texture.png" filter all 1} }
        normal  { wrinkles %%wrinkles%% scale 0.0002 }
        finish { 
            specular %%skinoil%%  // Max highlight intensity: 0 -> 1
            roughness %%rough%%  // surface roughness: 0.0005 -> 1
            phong 0 phong_size 0  // Phong specular disabled
            ambient 0
            diffuse 0
            reflection {0}
            conserve_energy
        }
    }


#declare MakeHuman_Material = material {
    texture {
        uv_mapping
        TEXTURE
    }
    interior{ior 1.33}
}

#end

                                                                            
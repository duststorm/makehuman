// xxFileNamexx.pov
// xxUnderScoresxx

// This scene file illustrates the use of an include file generated from the
// MakeHuman application using the POV-Ray mesh2 export functionality.
// It contains a simple example showing how to render the human figure. 
//
// This file is licensed under the terms of the CC-LGPL. 
// This license permits you to use, modify and redistribute the content.
// 
// Typical render time 1 minute (at 800x600 AA 0.3).
// The default object is about 16 POV-Ray units high and is centred at the 
// origin. 
// 

#include "xxLowercaseFileNamexx.inc"
#if (file_exists("makehuman_hair.inc")) #include "makehuman_hair.inc" #end  

camera {MakeHuman_Camera}
light_source {MakeHuman_LightSource}
object {
  MakeHuman_Mesh2Object
  texture {MakeHuman_Texture}
} 

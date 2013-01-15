#ifndef (%%name%%_Material)
#declare %%name%%_Texture =
    texture {
        pigment_pattern { image_map {png "%%name%%_TPOV.png" interpolate 2} }
        texture_map {
            [0 pigment { image_map {%%type%% "%%file%%" interpolate 2}} ]
            [1
            pigment { image_map {%%type%% "%%file%%" interpolate 2}}           
            normal { bump_map {png "%%name%%_TPOV.png" interpolate 2} %%thin%%}
            finish {
                specular %%spec%%
                roughness 0.02
                phong 0 phong_size 0 
                ambient 0
                diffuse 1
                reflection {0}
                conserve_energy
            }
            ]    
        }
    }            

#declare %%name%%_Material = material {
    texture {
        uv_mapping
        %%name%%_Texture
    }
}
#end   

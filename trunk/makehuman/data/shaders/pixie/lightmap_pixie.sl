surface lightmap ( float Ka = 1, Kd = .5, Km = .1;
                         color specularcolor = 1;
                         string texturename = "";
                         string bumptexture = "";
						 string pointcloudname = "";
						 ) {
    Ci = Cs;
    if (texturename != "")
	Ci *= color texture (texturename);
    float amp = 0;
    normal n = 0;


    if( bumptexture != "" ){
        /* STEP 1 - make a copy of the surface normal */
        n = normalize(N);
          
        /* STEP 2 - calculate the displacement */
        amp = float texture(bumptexture);  
          
        /* STEP 3 - assign the displacement to P */
         point P2 = P - n * amp * Km;
          
        /* STEP 4 - recalculate the surface normal */
        N = calculatenormal(P2);    		
        }

        

    normal Nf = faceforward (normalize(N),I);
    Ci = Ci * (Ka*ambient() + Kd*diffuse(Nf));
    //Ci = n;
    Oi = Os;  Ci *= Oi;
	point Pbake = point(s,t,0);
    bake3d(pointcloudname, "BakeCol", Pbake, normal(0), "coordsystem", "current",  "BakeCol", Ci);
}


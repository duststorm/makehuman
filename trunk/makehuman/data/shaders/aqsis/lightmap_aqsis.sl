
surface
lightmap ( float Ka = 1, Kd = .5, Ks = .5, roughness = .1, Km = .5;
		 color specularcolor = 1;
		 string texturename = ""; 
		 string bumptexture = "";
		 )
{
    normal Nf;
    vector V;
    color Ct;
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

  
  Nf = faceforward (normalize(N),I);
  V = -normalize(I);
  Oi = Os;
  Ci = Os * ( Cs * (Ka*ambient() + Kd*diffuse(Nf)) );
  bake (texturename, s, t, Ci); 
}

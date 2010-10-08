


surface
hair (float Ka = 1;
         float Kd = .5;
         float Ks = .5;
         float roughness = .1;
         color rootcolor = (0.2, 0.11, 0.04);  
         color tipcolor = (0.6, 0.41, 0.24);  
	 color specularcolor = 1;)
{
    normal Nf = faceforward (normalize(N),I);    
    Oi = 0.85*(1-pow(v,5));
    Ci = Os * ( Cs * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
    Ci = Ci * mix(rootcolor, tipcolor, v);
}























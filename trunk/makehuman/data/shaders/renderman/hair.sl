surface
hair    (float Ka = 1;
         float Kd = .5;
         float Ks = .5;
         color rootcolor = color (.109, .037, .007);
         color tipcolor = color (.519, .325, .125);
         float roughness = .1;
	     color specularcolor = 1;)
{
    normal Nf = faceforward (normalize(N),I);
    Oi = 1-pow(v,5);
    Ci = Oi * Os * ( mix(rootcolor, tipcolor, v) * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
}

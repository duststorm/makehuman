/* matte.sl - Standard matte surface for RenderMan Interface.
 * (c) Copyright 1988, Pixar.
 *
 * The RenderMan (R) Interface Procedures and RIB Protocol are:
 *     Copyright 1988, 1989, Pixar.  All rights reserved.
 * RenderMan (R) is a registered trademark of Pixar.
 */

surface hair (float Ka = 1;
	       float Kd = 1;
           float Ks = 1;
           color rootcolor = color (.109, .037, .007);
           color tipcolor = color (.519, .325, .125);
           color specularcolor = (color(1) + tipcolor) / 2;
           float roughness = .1;
    )
{    
    normal Nf = faceforward (normalize(N),I);    
    Oi = Os;    
    Ci = Os * ( mix(rootcolor, tipcolor, v) * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
}

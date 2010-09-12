surface hair (float Ka = 1, Kd = .6, Ks = .35, roughness = .15;            
            color rootcolor = (0.2, 0.11, 0.04);        
	     )
{   
    color tipcolor = rootcolor*1.5;
    color specularcolor = (color(1) + tipcolor) / 2;
    vector V = -normalize(I);
    normal Nf = faceforward (normalize(N),I);
    float angle_ramp = max(0,(1-( V.Nf)));
	
    float skin_matte = comp(diffuse(Nf), 0);
    color glancing_highlight = pow(angle_ramp*skin_matte, 2);
 

    Oi = 0.85*(1-pow(v,5));
    Ci = Oi *diffuse(Nf) * mix(rootcolor, tipcolor, v) ;             

    Ci = Ci + (Oi *specularcolor * Ks * specular(Nf, -normalize(I), roughness));    
   

}
























/*

surface
hair    (
         float Ka = 1;
         float Kd = .5; float Ks = .15; float roughness = .1;
         color specularcolor = 1;         
         point volumeCenter = (0.0, 6.9301475, 0.1637125);
         float headX = 0;
         float headY = 0;
         float headZ = 0;
         float dlenght = 0.5;
         float dmin = 0.3;

         
         )
{
    
    //printf("%f, %f, %f\n",xcomp(volumeCenter),ycomp(volumeCenter),zcomp(volumeCenter));
    
    point realPoint1 = transform ("world", "current", point (headX,headY,headZ));

    normal N1 = normalize(normal(P-realPoint1));
    normal Nf = faceforward (normalize(N),I);
    Oi = 0.85*(1-pow(v,5));
    Ci = Oi*Os * Cs * Kd * diffuse(N1)*diffuse(Nf) + Oi *specularcolor * Ks * specular(N1, -normalize(I), roughness) + Oi *specularcolor * Ks * specular(Nf, -normalize(I), roughness);

float dist = distance(P, realPoint1);

Ci = Ci*pow(((dist-dmin)/dlenght),3)*1.5;


    
    //Ci = diffuse(N1);
    //Ci = N1;
}
*/

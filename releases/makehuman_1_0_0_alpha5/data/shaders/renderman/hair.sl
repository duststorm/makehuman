
    //point realPoint = transform ("world", "current", point (P));

surface
hair    (
         float Ka = 1;
         float Kd = .5; float Ks = .15; float roughness = .1;
         color specularcolor = 1;         
         point volumeCenter = (0.0, 6.9301475, 0.1637125);
         float headX = 0;
         float headY = 0;
         float headZ = 0;
         
         )
{
    
    //printf("%f, %f, %f\n",xcomp(volumeCenter),ycomp(volumeCenter),zcomp(volumeCenter));
    point realPoint = transform ("world", "current", point (headX,headY,headZ));
    normal N1 = normalize(normal(P-realPoint));
    normal Nf = faceforward (normalize(N),I);
    Oi = 0.85*(1-pow(v,5));
    Ci = Oi*Os * Cs * Kd * diffuse(N1)*diffuse(Nf) + Oi *specularcolor * Ks * specular(N1, -normalize(I), roughness) + Oi *specularcolor * Ks * specular(Nf, -normalize(I), roughness);
    //Ci = diffuse(N1);
    //Ci = N1;
}

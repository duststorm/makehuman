
surface
lightmap ( float Ka = 1, Kd = 1, roughness = .1;
		 color specularcolor = 1;
         string texturename = "";
		 string outputtexture = ""; 
		 string bumptexture = "";
		 )

{
  normal Nf;
  vector V;
  color Ct;

  if (texturename != "")
       Ct = color texture (texturename);
  else Ct = 1;

  Nf = faceforward (normalize(N),I);
  V = -normalize(I);
  float skin_matte = comp(diffuse(Nf), 0)*20;
  color glancing_highlight = max(0,((1-(( V.Nf)/0.6))*pow(skin_matte,3)))*0.6;
  
  Oi = Os;
  Ci = Os * ( Cs * Ct * (Ka*ambient() + Kd*diffuse(Nf)));
  Ci = Ci +glancing_highlight*.00005;
  bake (outputtexture, s, t, Ci);

}


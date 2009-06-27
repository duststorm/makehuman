
//(c) MakeHuman team 2007 - www.makehuman.org

color screen(color F; color B)
    {
       color W = (1,1,1);
	   color R = W - (W - F)*(W - B);
	   return R;
    }

color powC(color ColToPow; float Factor)
    {
    float R1 = comp(ColToPow, 0);
	float G1 = comp(ColToPow, 1);
	float B1 = comp(ColToPow, 2);	
	
	float R2 = pow(R1,Factor);
	float G2 = pow(G1,Factor);
	float B2 = pow(B1,Factor);
    
    return color(R2, G2, B2);    
    }

surface skin (
            string ssstexture = "";
			string texturename = "";
			string opacitytexture = "";
            string speculartexture = "";
			float Ks = .5;
			float roughness = .1;
			color specularcolor = 1;
			float desaturation = 1;
            float dark = 4;
            ) 
{	
    normal Nf;
    vector V;
    color Ct;
	color Cd;
    float spec;
	
    if (texturename != "")
        Cd = color texture (texturename);
    else Cd = 1;
    
    if (speculartexture != "")
        spec = float texture (speculartexture);    
	else spec = 1;
    
	if (ssstexture != "")	
        Ct = color texture (ssstexture);		
    else Ct = 1;
	
    if (opacitytexture != "")	
        Oi = float texture (opacitytexture) * Os ;	
	
	
	
	Nf = faceforward (normalize(N),I);
    V = -normalize(I);
	float angle_ramp = (max(0,(1-( V.Nf))))/5;
	float  noise3D = float noise(P*100);
	float skin_matte = comp(diffuse(Nf), 0);
	float dark_area = 0.5*pow((1-skin_matte),3);
    //printf("dark area: %f\n",dark_area);

    color glancing_highlight = max(0,((1-(( V.Nf)/0.6))*pow(skin_matte,3)))*0.6;
    
    
    
	Ci = (Cs * Ct) - angle_ramp*noise3D;	

    Ci = screen(Ci,Cd);

    Ci = powC(Ci,dark)*(2/dark);
  
    
    
	//DESATURATE THE HIGHTLIGHTS
	float desaturate_factor = 0.25*desaturation*pow(skin_matte, 3)*noise3D;
    float desaturate_tone = comp(Ci, 0);
    Ci = mix(Ci,desaturate_tone,desaturate_factor); 	
	//Ci = Ci - (color(dark_area*.1,dark_area*.2,dark_area*.15));
    Ci = Ci - dark_area;
    Ci = mix(desaturate_tone,Ci,0.7);   
    Ci = Ci+ specularcolor * Ks*noise3D*specular(Nf,V,roughness)*spec;
    
    
    
	Ci = Ci*Oi;
    
    
    

    
	
	
    	
	
}

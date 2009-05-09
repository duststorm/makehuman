
//(c) MakeHuman team 2007 - www.makehuman.org

color screen (color F; color B) {
       color W = (1,1,1);
	   color R = W - (W - F)*(W - B);
	   return R;
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
            float lum = 1.5;
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
        Oi = float texture (opacitytexture) ;		
    else Oi = 1;
	
	
	Nf = faceforward (normalize(N),I);
    V = -normalize(I);
	float angle_ramp = (max(0,(1-( V.Nf))))/5;
	float  noise3D = float noise(P*100);
	float skin_matte = comp(diffuse(Nf), 0)*20;
	float dark_area = 0.5*pow((1-skin_matte),3);

    color glancing_highlight = max(0,((1-(( V.Nf)/0.6))*pow(skin_matte,3)))*0.6;
    
    
    
	Ci = (Cs * Ct) + specularcolor * Ks*noise3D*specular(Nf,V,roughness)*spec- angle_ramp*noise3D;	
	//Ci = mix(Ci,Cd,0.5);
    Ci = screen(Ci,Cd);
    Ci = Ci*Ci;

	//DESATURATE THE HIGHTLIGHTS
	
	float CiR2 = comp(Ci, 0);
	float CiG2 = comp(Ci, 1);
	float CiB2 = comp(Ci, 2);
	
	float maxVal = max(CiR2,CiG2,CiB2);
    float desaturate_factor = desaturation*pow(skin_matte, 3)*noise3D;
	
	CiR2 = (desaturate_factor*(maxVal - CiR2)) + CiR2;
	CiG2 = (desaturate_factor*(maxVal - CiG2)) + CiG2;
	CiB2 = (desaturate_factor*(maxVal - CiB2)) + CiB2;	
	
	setcomp (Ci, 0, CiR2);
	setcomp (Ci, 1, CiG2);
	setcomp (Ci, 2, CiB2);
	
	
	Ci = Ci - (color(dark_area*.1,dark_area*.2,dark_area*.15));
    Ci = (Ci * ambient());//+glancing_highlight*12;
    //Ci = Ci*Cd;
	Ci = Ci*Oi;
	//printf("%f\n",Oi);
    
	
	
    	
	
}

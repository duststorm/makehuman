
//(c) MakeHuman team 2007 - www.makehuman.org


//color
//wrappeddiffuse( normal N; float wrappedangle )
//{
	//color C = 0;
	//normal Nn;
    //vector Ln;
    //extern point P;
	//Nn = normalize(N);
	//illuminance( P, Nn, PI/2 ) {
		//Ln = normalize(L);
		//C += Cl * (1 - acos(Ln.Nn) / wrappedangle); 	}
	//return C;
//}

//color
//test( normal N )
//{
	//color C = 0;
    //extern point P;
    //normal Nn = normalize(N);
	//illuminance( P, Nn, PI) {		
		//C += Cl; 	}
	//return C;
//}


//color screen(color F; color B)
    //{
       //color W = (1,1,1);
	   //color R = W - (W - F)*(W - B);
	   //return R;
    //}

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
            string mixtexture = "";
			float Ks = .5;
			float roughness = .1;
			color specularcolor = 1;
			float desaturation = 1;            
            ) 
{	
    normal Nf;
    vector V;
    color Csss;
	color Cflat;
    color Cdiff;
    float spec;
    float mixVal;
	
    if (texturename != "")
        Cflat = color texture (texturename);
    else Cflat = 1;
    
    if (mixtexture != "")
        mixVal = float texture (mixtexture);       
	else mixVal = 1;
    
    if (speculartexture != "")
        spec = float texture (speculartexture);       
	else spec = 1;
    
	if (ssstexture != "")	
        Csss = color texture (ssstexture);		
    else Csss = 1;
	
    if (opacitytexture != "")	
        Oi = float texture (opacitytexture) * Os ;	
	
	
	
	Nf = faceforward (normalize(N),I);
    V = -normalize(I);
	float angle_ramp = max(0,(1-( V.Nf)));
	float  noise3D = float noise(P*100);
	float skin_matte = comp(diffuse(Nf), 0);	
    color glancing_highlight = angle_ramp*skin_matte;
    
    Cdiff = (Cflat+ambient())*skin_matte;//-(1-ambient())/2;

    Ci = mix(Cdiff,Csss,mixVal);        
   
    float desaturate_factor = 0.5* min((desaturation*skin_matte+ comp(noise3D*specular(Nf,V,roughness)*spec,0)),1) ;
    color desaturate_tone = color(comp(Ci, 0)*0.6,comp(Ci, 0),comp(Ci, 0));
    color x2 = color((1-comp(Ci, 0))*0.5+1,1,1);
    color x = color(pow((1-angle_ramp),0.5)/10,0,0);
    Ci = mix(Ci,desaturate_tone,desaturate_factor)-x;
    

    Ci = Ci+ specularcolor * Ks*noise3D*specular(Nf,V,roughness)*spec; 
    Ci = Oi*(Ci*Cflat*x2)*Cflat;

   Ci = Ci+Ci/2.5; 
   

    
    
	
	
    	
	
}

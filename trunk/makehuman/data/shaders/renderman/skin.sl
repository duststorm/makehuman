/*
===========================  ===============================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        data\shaders\skin.sl                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni                                            
Copyright(c):                MakeHuman Team 2001-2008                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================
*/ 
surface skin (
            string lighttexture = "";
            string skintexture = "";
			string bumptexture = "";
            string refltexture = "";
            float Ka = 1;
	        float Kd = 1;
            float Ks = 1;
            float Km = 0.1;
            float Kb = 0;
			float bumping = .5;
            float roughness = .1;
            float contrast = 0;
            float desaturation = 0.5;
            color specularcolor = .1;
            ) 
{		
    Ci = 0;
    float skin_sss_light = 0;
    color skin_color = 0;
    color skin_sss = 0;
    float skin_matte = 0;
    float skin_illum = 0;    
    float skin_noise = 0;
    float skin_refl = 1;
    color red_tone = 0;
    color blue_tone = 0;
    color melanin = (0.42,0.38,0.3);
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
    
   
    
    normal Nf = faceforward (normalize(N),I);
    vector V = -normalize(I);    
    skin_matte = comp(diffuse(Nf), 0);
    
    
    
	if (lighttexture != ""){
        skin_sss = color texture (lighttexture);
        skin_sss_light = comp(skin_sss, 2);  
        }
        
    if (skintexture != ""){	
        skin_color = color texture (skintexture);
        }

    if (refltexture != ""){	
        skin_refl = float texture (refltexture);
        }

    skin_illum = mix(skin_sss_light,skin_matte,0.6)*Kd;    

    
    red_tone = (0.2,0.0,0.0)*(1-skin_illum);
    blue_tone = (-0.2,0.0,0.0)*pow(skin_illum,3);
    
    Ci = skin_illum * skin_color;   
    
    
    //DESATURATE THE HIGHTLIGHTS
	float CiR2, CiG2, CiB2;
	CiR2 = comp(Ci, 0);
	CiG2 = comp(Ci, 1);
	CiB2 = comp(Ci, 2);
	
	float maxVal = max(CiR2,CiG2,CiB2);
    float desaturate_factor = desaturation*pow(skin_sss_light, 3);
    //float desaturate_factor = 0.5*comp(specular(Nf,V,0.5),0);

	
	CiR2 = (desaturate_factor*(maxVal - CiR2)) + CiR2;
	CiG2 = (desaturate_factor*(maxVal - CiG2)) + CiG2;
	CiB2 = (desaturate_factor*(maxVal - CiB2)) + CiB2;	
	
	setcomp (Ci, 0, CiR2);
	setcomp (Ci, 1, CiG2);
	setcomp (Ci, 2, CiB2);

    float angle_ramp = (max(0,(1-( V.Nf))))/4;
    Ci = Ka * ambient() + Ci + angle_ramp +red_tone*skin_color+blue_tone*skin_color;

    float dark_area = 0.5*pow((1-skin_illum),3);
    Ci = (Ci*Cs) - dark_area;

        
    Ci = Ci + (specularcolor * Ks*specular(Nf,V,roughness) * skin_refl);
    Ci = Ci + (100*(pow(angle_ramp,4)) * specular(Nf,V,roughness));

    Ci = Ci+(Ci*contrast);
    
    Ci = Ci - (melanin*Kb);

    //Ci = amp;
        
	
	
	
             
}


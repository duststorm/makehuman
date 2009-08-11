surface hair(

    float Ka = 1;
    float Kd = .6;
    float Ks = .9;
    float roughness = .15;
    color rootcolor = color (.109, .037, .007);
    color tipcolor = color (.519, .325, .125);
    color specularcolor = (color(1) + tipcolor) / 2;
    )
{    
	normal FakeN;
	
	
	
	if (u>0.5)
		FakeN = normalize(N+dPdu*du);
	else
		FakeN = normalize(N-dPdu*du);

    Oi = 1-pow(v,5);
	
    Ci = Os * (Ka*ambient() + mix(rootcolor, tipcolor, v) * diffuse(FakeN)+
        specularcolor * Ks*specular(FakeN,-normalize(I),roughness));
    Ci= Ci*Oi;
}


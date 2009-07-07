/*color
diffuseNoCl( normal N )
{
	color C = 0;
	vector Ln;
    extern point P;

	normal Nn = normalize(N);
	illuminance( P, Nn, PI/2 ) {
		Ln = normalize(L);
		C += Ln.Nn; 	}
	return C;
}*/


surface hair(

    float Ka = .01;
    float Kd = .6;
    float Ks = .9;
    float roughness = .15;
    color rootcolor = color (.109, .037, .007);
    color tipcolor = color (.519, .325, .125);
    color specularcolor = (color(1) + tipcolor) / 2;
    )
{    
	vector FakeN;
	
	
	
	if (u>0.5)
		FakeN = normalize(N+dPdu*du);
	else
		FakeN = normalize(N-dPdu*du);
	
    Ci = Os * (Ka*ambient() + mix(rootcolor, tipcolor, v) * diffuse(FakeN)+
        specularcolor * Ks*specular(FakeN,-normalize(I),roughness));
}


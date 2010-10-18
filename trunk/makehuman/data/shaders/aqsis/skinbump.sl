displacement skinbump 
    (	
	    float bumpVal = 0.1; 	
	    string bumpTexture = ""; 
	    float truedisp = 1
	)
{
    normal n = normalize(N); 
	float hump = 1;		
	
	
	if (bumpTexture != "")
	{
	    hump =  float texture (bumpTexture);			
	}
	
	hump = hump* bumpVal;	


	if (truedisp == 1)
	{
	    P += n * hump ;
        N=calculatenormal(P);
	}
	else
	{
        N = calculatenormal(P + (n * hump));
    } 	
	
}


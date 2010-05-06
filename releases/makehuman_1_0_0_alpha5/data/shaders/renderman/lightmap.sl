surface lightmap(string texturename = ""; ) {
    Ci = Cs;
    float Light = comp(Cs,2);
    if (texturename != "")
	Ci = Light * color texture (texturename); 
    
}








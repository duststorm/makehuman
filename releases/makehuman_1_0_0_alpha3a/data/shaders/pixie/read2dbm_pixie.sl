surface read2dbm(string pointcloudname = ""; float bluramt = 0)
   {
       point Pbake = point(s,t,0);
       texture3d(pointcloudname, Pbake, normal(0),"coordsystem", "current", "radiusscale",1+bluramt, "BakeCol", Ci);
		
        Oi = Os;
    }

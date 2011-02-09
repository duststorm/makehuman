import Blender
from Blender import Scene, Curve, Object, Particle
from random import randrange  

def exportAsCurves(file, guides, number):
    DEG_ORDER_U = 3
    # use negative indices
    M = min(len(guides),number)
    for j in xrange(0,M):
      n = randrange(0,len(guides))
      N = len(guides[n])
      for i in xrange(0,N):
        file.write('v %.6f %.6f %.6f\n' % (guides[n][i][0], guides[n][i][1],\
                                           guides[n][i][2]))
      #name = group.name+"_"+guide.name 
      #file.write('g %s\n' % name)
      file.write('cstype bspline\n') # not ideal, hard coded
      file.write('deg %d\n' % DEG_ORDER_U) # not used for curves but most files have it still
    
      curve_ls = [-(i+1) for i in xrange(N)]
      file.write('curv 0.0 1.0 %s\n' % (' '.join( [str(i) for i in curve_ls] ))) # hair  has no U and V values for the curve
    
      # 'parm' keyword
      tot_parm = (DEG_ORDER_U + 1) + N
      tot_parm_div = float(tot_parm-1)
      parm_ls = [(i/tot_parm_div) for i in xrange(tot_parm)]
      
      file.write('parm u %s\n' % ' '.join( [str(i) for i in parm_ls] ))
      file.write('end\n')

scn= Scene.GetCurrent()
obj = scn.objects.active
parts = obj.getParticleSystems()
hairs = parts[0].getLoc()
file = open("C:\Temp\hair.obj", 'w')
exportAsCurves(file,hairs,300)
file.close()
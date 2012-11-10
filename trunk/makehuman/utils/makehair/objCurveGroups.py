import Blender, sys
from Blender import Scene, Curve, Object, Group

def exportAsCurves(file, guides, groups=None):
    DEG_ORDER_U = 2 #formerly 3
    # use negative indices
    for j in xrange(0,len(guides)):
      guide=guides[j]
      N=len(guide)
      for i in xrange(0,N):
        file.write('v %.6f %.6f %.6f\n' % (guide[i][0], guide[i][1],\
                                           guide[i][2]))
      if groups:
        file.write('g %s\n' % groups[j])
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
guides=[]
file = open("C:/temp/temp.obj", 'w')

#Getting groups from blender then unlinking them because I dont know how to get groupnames of an object
grps = Group.Get()
groups=[]

for grp in grps:
    print "we are now in group: ", grp.name
    for obj in grp.objects:
        groups.append(grp.name)
        guide=[]
        mesh = obj.getData()
        try:
          for cp in mesh[0]:
              guide.append([cp[0],cp[1],cp[2]])
          guides.append(guide)
          scn.objects.unlink(obj)
        except:
          pass
Blender.Redraw()
exportAsCurves(file, guides, groups)
"""
#this is supposed to be for ungrouped guides, use at your own risk
#get the rest of non-grouped objects
guides=[]
file = open("C:/temp/temp2.obj", 'w')
for object in scn.objects.selected:
    guide=[]
    mesh = object.getData()
    try:
      for cp in mesh[0]:
          guide.append([cp[0],cp[1],cp[2]])
      guides.append(guide)
      scn.objects.unlink(object)
    except:
      pass
      
exportAsCurves(file, guides)
file.close()
"""

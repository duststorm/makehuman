def convert_target(filename):
    
    # Load obj to get group information
    groups = {}
    group = None
    
    with open('../data/3dobjs/base.obj', 'r') as f:
        for line in f:
            parts = line.split()
            if parts[0] == 'g':
                group = parts[1]
                groups[group] = []
            elif parts[0] == 'f':
                for i in xrange(1,4):
                    part = parts[i]
                    co = part.split('/')
                    groups[group].append(int(co[0]) - 1)
    
    # Keep only unique vertex indices
    for name, group in groups.iteritems():
        groups[name] = list(set(group))
        #print name, len(groups[name])
        
    #print groups
                
    # Load target to analyze
    target = {}
    
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split()
            target[int(parts[0])] = (float(parts[1]), float(parts[2]), float(parts[3]))
            
    #print target
    
    # Group target
    targetGroups = {}
        
    for name, group in groups.iteritems():
        targetGroup = {}
        for index in group:
            if index in target:
                targetGroup[index] = target[index]
        if len(targetGroup):
            targetGroups[name] = targetGroup
    
    #print len(groups)
    #print len(targetGroups)
    #print targetGroups
        
    # Analyze target
    for name, group in targetGroups.iteritems():
        #print name, len(group), len(groups[name])
        #if len(group) == len(groups[name]):
            x = [v[0] for v in group.values()]
            y = [v[1] for v in group.values()]
            z = [v[2] for v in group.values()]
            
            diffx = max(x) - min(x)
            diffy = max(y) - min(y)
            diffz= max(z) - min(z)
            
            #print name, diffx, diffy, diffz, '[%d of %d]' % (len(group), len(groups[name]))
            
            if len(group) == len(groups[name]):
                if diffx < 0.00001 and diffy < 0.00001 and diffz < 0.00001:
                    print name, x[0], y[0], z[0]
                else:
                    print '%s is not compressible because not all vertices are moved by the same distance' % name
            else:
                print '%s is not compressible because not all vertices are used' % name
    
#convert_target('../data/targets/details/ear-trans-down.target')
#convert_target('../data/targets/details/r-hand-trans-up.target')

import sys

if len(sys.argv) < 2:
  print "Usage: convert_target filename"
else:
	print "Converting %s" % (sys.argv[1])
	convert_target(sys.argv[1])
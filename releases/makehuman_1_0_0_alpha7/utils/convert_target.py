from os import stat
import zlib

def convert_target(filename):
    
    print('Compressing %s' % filename)
    
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
    
    compressedTarget = {}
        
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
                    compressedTarget[name] = (x[0], y[0], z[0])
                    print name, x[0], y[0], z[0]
                else:
                    for i in group:
                        compressedTarget[i] = target[i]
                    print '%s is not compressible because not all vertices are moved by the same distance' % name
            else:
                for i in group:
                        compressedTarget[i] = target[i]
                print '%s is not compressible because not all vertices are used' % name
                
    # Write target
    filename2 = filename.replace('.target', '.target2')
    
    target2 = 'version 1.1\n'
    
    for name, distance in compressedTarget.iteritems():
        target2 += "%s %f %f %f\n" % (name, distance[0], distance[1], distance[2])
    
    with open(filename2, 'wb') as f:
        f.write(zlib.compress(target2))
            
    size = float(stat(filename).st_size)
    size2 = float(stat(filename2).st_size)
    print('Original %d Compressed %d' % (size, size2))
    print('Compression ratio %f%%' % ((size - size2) * 100 / size))
    
convert_target('../data/targets/details/ear-trans-down.target') # 24,528 bytes to 24,528 bytes 0% zlib 6077 75.224234%
convert_target('../data/targets/details/r-hand-trans-up.target') # 46,178 bytes to 14,472 bytes 68% zlib 2007 95.653775%

import sys

if len(sys.argv) < 2:
  print "Usage: convert_target filename"
else:
	print "Converting %s" % (sys.argv[1])
	convert_target(sys.argv[1])
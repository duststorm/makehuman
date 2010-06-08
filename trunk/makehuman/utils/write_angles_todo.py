def mcd(a, b):    
    while b:
        a, b = b, a%b
    return a

rotXmin, rotXmax = -80, 80
rotYmin, rotYmax = -140, 40
rotZmin, rotZmax = -120, 90

stepX = mcd(rotXmin, rotXmax)
stepY = mcd(rotYmin, rotYmax)
stepZ = mcd(rotZmin, rotZmax)

filePath = "todo.txt"
print stepX,stepY,stepZ

try:
    fileDescriptor = open(filePath, "w")
except:
    print "Unable to open %s",(filePath)


for rotX in range(rotXmin, rotXmax,stepX):
    for rotY in range(rotYmin, rotYmax,stepY):
        for rotZ in range(rotZmin, rotZmax,stepZ):
            fileDescriptor.write("%d %d %d\n" % (rotX,rotY,rotZ))


fileDescriptor.close()
    

import sys
sys.path.append("../maketarget")
targetPath = "../maketarget/diff.target"
filterPath = "../maketarget/fit_vert.verts"
import matplotlib.pyplot as plt
import maketargetlib
import os
  
maketargetlib.loadTarget(targetPath)
targetData = maketargetlib.analyzeTarget(15340, 1)
filteredVerts = maketargetlib.loadIndexVerts(filterPath)
dataToPlot = []
for i,l in enumerate(targetData[1]):
    if i in filteredVerts:
        dataToPlot.append(l)
plt.plot(dataToPlot)
plt.ylabel('Displacement')
plt.xlabel('Vertices')
plt.ylim(ymax = 0.20)
plt.title(os.path.basename(targetPath))
plt.show()

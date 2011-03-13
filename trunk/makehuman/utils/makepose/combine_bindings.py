import os

print os.listdir(".")
file = open("binding.txt", 'w')

for filename in os.listdir("."):
  pair = os.path.splitext(filename)
  if (pair[1] == ".verts"):
    file.write(os.path.splitext(filename)[0] + "\n")
    ifile = open(filename)
    verts = ifile.readline()
    file.write(verts.strip())
    while (1):
      verts = ifile.readline()
      if not verts: break
      file.write(" "+verts.strip())
    ifile.close()
    file.write("\n")
    
file.close()
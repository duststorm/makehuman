import module3d

class Font:
  def __init__(self, filename):
    f = open(filename, 'r')

    self.charMap = {}

    for data in f.readlines():
      lineData = data.split()
      
      if lineData[0] == "common":
        for paramValue in lineData[1:]:
          paramData = paramValue.split('=')
        
          if paramData[0] == "lineHeight":
            self.lineHeight = int(paramData[1])
          elif paramData[0] == "scaleW":
            self.width = int(paramData[1])
          elif paramData[0] == "scaleH":
            self.height = int(paramData[1])
          
      elif lineData[0] == "page":
        for paramValue in lineData[1:]:
          paramData = paramValue.split('=')
        
          if paramData[0] == "file":
            self.file = "data/fonts/" +paramData[1][1:-1] # Removes the ""
          
      elif lineData[0] == "char":
        charRecord = {}
        for paramValue in lineData[1:]:
          paramData = paramValue.split('=')
          
          if paramData[0] == "id":
            charRecord["id"] = int(paramData[1])
          elif paramData[0] == "x":
            charRecord["x"] = int(paramData[1])
          elif paramData[0] == "y":
            charRecord["y"] = int(paramData[1])
          elif paramData[0] == "width":
            charRecord["width"] = int(paramData[1])
          elif paramData[0] == "height":
            charRecord["height"] = int(paramData[1])
          elif paramData[0] == "xoffset":
            charRecord["xoffset"] = int(paramData[1])
          elif paramData[0] == "yoffset":
            charRecord["yoffset"] = int(paramData[1])
          elif paramData[0] == "xadvance":
            charRecord["xadvance"] = int(paramData[1])
            
        #print(charRecord)
        self.charMap[charRecord["id"]] = charRecord
        
    #print(self.charMap)
    
  def getAbsoluteCoordsForChar(self, char):
    charRecord = self.charMap[ord(char)]
    x1 = float(charRecord["xoffset"])
    y1 = float(charRecord["yoffset"])
    x2 = float(charRecord["xoffset"] + charRecord["width"])
    y2 = float(charRecord["yoffset"] + charRecord["height"])
    advance = float(charRecord["xadvance"])
    return [x1, y1, x2, y2, advance]
    
  def getRelativeSizesForChar(self, char):
    charRecord = self.charMap[ord(char)]
    x1 = float(charRecord["xoffset"]) / float(self.width)
    y1 = float(charRecord["yoffset"]) / float(self.height)
    x2 = float(charRecord["xoffset"] + charRecord["width"]) / float(self.width)
    y2 = float(charRecord["yoffset"] + charRecord["height"]) / float(self.height)
    advance = float(charRecord["xadvance"]) / float(self.width)
    return [x1, y1, x2, y2, advance]
    
  def getTextureCoordinatesForChar(self, char):
    charRecord = self.charMap[ord(char)]
    u1 = float(charRecord["x"]) / float(self.width)
    v1 = 1.0 - float(charRecord["y"]) / float(self.height)
    u2 = float((charRecord["x"] + charRecord["width"])) / float(self.width)
    v2 = 1.0 - float((charRecord["y"] + charRecord["height"])) / float(self.height)
    return [u1, v1, u2, v2]
    
def createMesh(scene, font, text, position):
  # create object
  obj = scene.newObj(text)
  obj.x = position[0]
  obj.y = position[1]
  obj.z = position[2]
  obj.rx = 0.0
  obj.ry = 0.0
  obj.rz = 0.0
  obj.sx = 1.0
  obj.sy = 1.0
  obj.sz = 1.0
  obj.visibility = 1
  obj.shadeless = 1
  obj.pickable = 0
  obj.cameraMode = 1
  obj.text = ""
  obj.uvValues = []
  obj.indexBuffer = []
  
  # create group
  fg = obj.createFaceGroup("text")
  
  index = 0
  xoffset = 0.0
  
  for char in text:
    co = font.getAbsoluteCoordsForChar(char)
    uv = font.getTextureCoordinatesForChar(char)
    
    # create vertices
    v1 = obj.createVertex([xoffset + co[0], co[1], 0.0])
    v2 = obj.createVertex([xoffset + co[2], co[1], 0.0])
    v3 = obj.createVertex([xoffset + co[2], co[3], 0.0])
    v4 = obj.createVertex([xoffset + co[0], co[3], 0.0])
    
    xoffset += co[4]
    
    uv1 = [uv[0], uv[1]]
    uv2 = [uv[2], uv[1]]
    uv3 = [uv[2], uv[3]]
    uv4 = [uv[0], uv[3]]
    
    # create faces
    f1 = fg.createFace(v1, v4, v2, uv = (uv1, uv4, uv2))
    f2 = fg.createFace(v2, v4, v3, uv = (uv2, uv4, uv3))
  
  fullArrayIndex = 0
  groupVerts = {}
  for f in obj.faces:
    for i, v in enumerate(f.verts):
      t = f.uv[i]
      if v.idx not in groupVerts:
        v.indicesInFullVertArray.append(fullArrayIndex)
        groupVerts[v.idx] = {}
        groupVerts[v.idx][t] = fullArrayIndex
        obj.indexBuffer.append(fullArrayIndex)
        fullArrayIndex += 1
      elif t not in groupVerts[v.idx]:
        v.indicesInFullVertArray.append(fullArrayIndex)
        groupVerts[v.idx][t] = fullArrayIndex
        obj.indexBuffer.append(fullArrayIndex)
        fullArrayIndex += 1
      else:
        obj.indexBuffer.append(groupVerts[v.idx][t])
        
  obj.vertexBufferSize = fullArrayIndex;
  obj.texture = font.file
  
  print(obj.texture)
  
  scene.update()
          
#font = Font("../data/fonts/arial.fnt")
#print(font.getAbsoluteCoordsForChar('a'))
#print(font.getRelativeSizesForChar('a'))
#print(font.getTextureCoordinatesForChar('a'))
""" 
Data Structures and Functions for *Half Edges* processing.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni

**Copyright(c):**      MakeHuman Team 2001-2009

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements the data structures and functions to support vertex/face analysis 
using *Half Edges* and is implemented as a plugin that can be used by developers to validate mesh 
data. For general information about this technique see 
http://www.cgafaq.info/wiki/Half_edge_implementation
and for general information about *Half Edge* data structures see
http://www.flipcode.com/archives/The_Half-Edge_Data_Structure.shtml
.

This technique introduces two *Half Edges* for each edge, each with opposing orientations 
aligned along the length of the edge. Thus one half edge 'belongs' to one face and the other
half edge 'belongs' to the other face which shares that edge.
These functions are particularly useful with the type of surface mesh used by MakeHuman where no 
more than two polygons should share an edge.

This module provides high-level functions to developers to support validation of data structures 
and interrogation of the mesh such as support for tracking around the edges of a single face or 
tracking around a hole in the mesh object. 
It also helps to identify all polygonal faces sharing a particular vertex. 

This module implements HEdge class data structures, building a *Half Edges* dictionary that is used 
to resolve the results data. This dictionary is constructed in two passes:

  - In the first pass the constructor is called to create all HEdges objects by 
    processing Faces in the Object3D collection sequentially.  
    It stores each new *Half Edge* in the HEdges dictionary creating unique key-identifier strings 
    to identify *Half Edges* that may not yet have been processed.
  - In the second pass the linkHEdges function loops through the list to resolve 
    those temporary key-identifier strings into direct references so that it can 
    link in the **next** *Half Edge* and the **twin** *Half Edge* by direct reference.

In addition to the HEdge class data structures, this module includes methods and functions that add new 
attributes to the MakeHuman base classes to hold the results of the analysis that they 
perform. These new attributes are all named using a common prefix of: *he_*

New properties added to base classes:

- **Object3D.he_hedges**. A list of HEdges, indexed using the key-identifier (a string of the form 'vn"-"(vn-1)') of the *Half Edge*.
- **Object3D.he_hedgeCalculated**. A flag indicating whether *Half Edges* have been calculated for this object.
- **Vert.he_hedge**. A HEdge reference from the vertex. This is the vertex that forms the starting point of this *Half Edge*.
- **Face.he_hedge**. A list of 3 HEdges (indexed using 0, 1 and 2), referenced from the triangular Face formed by those *Half Edges*.

**Figure 1:**

.. image:: ../images/hedge_struct.jpg
  :alt: HEdges Structure

In Figure 1 the *Half Edge* **HE1** starts at vertex V2 and ends at vertex V3. 
It sits on face F1. There is a twinned *Half Edge* **HE2** that shares the same edge 
and the same vertices, starting at vertex V3 and ending at vertex V2, but it sits 
on face F2. The MakeHuman Hedge object for *Half Edge* HE1 has attributes that 
reference:

- The start vertex (V2).
- The face on which it sits (F1).
- The next Hedge object which shares the same face (V3-V1).
- The twin Hedge object (HE2).
 
All of the other Half Edges contain the same attributes, enabling the data structure to be 'viewed' in a number of ways that support the integrity and coherence of the 3D mesh. 

Require:

- base modules

"""

__docformat__ = 'restructuredtext'


class HEdge:
    """
    This class implements the data structures and the constructor method required 
    to support vertex/face analysis using *Half Edges*.
    This technique makes high-level functions available to developers to support 
    the validation of MakeHuman mesh data structures (during the development cycle).
     
    A *Half Edges* data structure (sometimes abbreviated to HalfedgeDS or HDS for template parameters) 
    stores information related to the edges of a set of polygons (in this case triangles) 
    that fit together to form 3D planar polyhedra. The *Half Edges* functions track through 
    these structures checking the coherency of the data, validating the orientation of 
    normals and checking for invalid conditions, such as more than two faces sharing 
    an edge.
    
    For more detail, see cgafaq_ , or flipcode_.   

    .. _cgafaq: http://www.cgafaq.info/wiki/Half_edge_implementation

    .. _flipcode: http://www.flipcode.com/archives/The_Half-Edge_Data_Structure.shtml

    **Figure 1:**

    .. image:: ../images/hedge_struct.jpg
       :alt: edge structure diagram

    In Figure 1 the *Half Edge* HE1 starts at vertex V2 and ends at vertex V3. It sits on face F1. There is a twinned *Half Edge* HE2 that shares the same edge and the same vertices, starting at vertex V3 and ending at vertex V2, but it sits on face F2. The MakeHuman Hedge object for *Half Edge* HE1 has attributes that reference:
    
    - The start vertex (V2).
    - The face on which it sits (F1).
    - The next Hedge object which shares the same face (V3-V1).
    - The twin Hedge object (HE2).
     
    All of the other Half Edges contain the same attributes, enabling the data structure to be 'viewed' in a number of ways that support the integrity and coherence of the 3D mesh. 

    """
    def __init__(self,heId,heNextId,heTwinId,heVertId,heFaceId):
        """
        This is the constructor method for the HEdge class which is used to set 
        up the data structures on the first of two passes. 
        During this first pass the twin *Half Edge* to the *Half Edge* currently being 
        instantiated (the half of this edge from the adjoining face) cannot be referenced
        directly as it still needs to be found and may be part of a face that hasn't been
        written into this dictionary yet. 
        
        Unique key-identifiers are therefore stored as strings to enable those twin edges 
        to easily be found in a second pass, once all faces have been built into the 
        dictionary.

        Parameters
        ----------

        heId:     
          *string*.  The key-identifier of this *Half Edge*.
        heNextId: 
          *string*.  The key-identifier of the next *Half Edge* on the same face.
        heTwinId: 
          *string*.  The key-identifier of the twin *Half Edge* on an adjoining face.
        heVertId: 
          *integer*. The index of the first vertex of this *Half Edge*.
        heFaceId: 
          *integer*. The index of the face upon which this *Half Edge* sits.

        This method initializes two types of attribute: Key-identifiers and References.

        Key-identifiers
        ---------------
        Key-identifiers are strings that are written into the HEdges dictionary to uniquely 
        identify twin *Half Edges* from faces that may not have been processed by the time this 
        *Half Edge* (the one that is currently being constructed) is instantiated.

        - self.ID: *string*. The key-identifier of this *Half Edge*.
        - self.twinID: *string*. The key-identifier of the twin of this *Half Edge* on an adjoining face.
        - self.nextID: *string*. The key-identifier of the next *Half Edge* on the same face.
        - self.vID: *integer*. The index of the first vertex of this *Half Edge*.
        - self.fID: *integer*. The index of the face upon which this *Half Edge* sits.

        We use these keys as a dictionary to quickly identify adjacent
        elements without needing to loop through and search the list. 
        (this assumes that the mesh is coherent):

        References
        ----------
        This 'dictionary' also has fields to hold direct references to adjacent elements 
        (instead of their key-identifiers). 
        These references are initially empty and are filled in during a second pass by a 
        subsequent call to the Object3D.linkHEdges method providing a quicker mechanism 
        by which to access these elements:

        - *self.twin*: *HEdge*. The twin half edge.
        - *self.next*: *HEdge*. The next half edge.
        - *self.face*: *Face*. The face upon which this half edge sits.
        - *self.vert*: *Vert*. The first vertex of this half edge
        - *self.sub_vert*: *Vert*. The subdivided vertex if the object is subdivided
        
        """
        self.twinID = heTwinId
        self.nextID = heNextId
        self.ID = heId
        self.fID = heFaceId
        self.vID = heVertId
        self.twin = None
        self.next = None
        self.face = None
        self.vert = None
        
    

    def __str__(self):
        """
        This method is the Print method and returns a string listing the index of this half edge.
 
        """
        return self.ID



def addHedge(ob,heId1,heNextId1,heTwinId1,vIndex,fIndex ):
    """
    This function calls the constructor method of the HEdge class to instantiate 
    a single new *Half Edge* instance and populate it with the data that is available 
    on the first of two passes. This: 
    
      - Adds the new *Half Edge* as *he_hedge* attributes on the Vert and Face 
        objects specified 
      - Adds the vertex and face as attributes to this *Half Edge* 
      - Adds a reference onto the Object3D object (of which the current vertex 
        is a part) back to this *Half Edge* using a string as a key (a key-identifier).
        
    Parameters
    ----------

    ob:     
      *Object3D*.  The Object3D object of which this *Half Edge* is a part.
    heId1:     
      *string*.  The key-identifier of this *Half Edge*.
    heNextId1: 
      *string*.  The key-identifier of the next *Half Edge* on the same face.
    heTwinId1: 
      *string*.  The key-identifier of the twin *Half Edge* on an adjoining face.
    vIndex: 
      *integer*. The index of the first vertex of this *Half Edge*.
    fIndex: 
      *integer*. The index of the face upon which this *Half Edge* sits.

    """

    he = HEdge(heId1,heNextId1,heTwinId1,vIndex,fIndex)
    #print vIndex   
    v = ob.verts[vIndex]
    f = ob.faces[fIndex]        
    f.he_hedge = he #New property for base face class
    v.he_hedge = he #New property for base vert class
    he.vert = v
    he.face = f
    ob.he_hedges[heId1] = he


def linkHEdges(ob):
        """
        This function constructs a *linked list* by performing a second 
        pass through the HEdge dictionary to insert cross-references 
        that were not available during the first pass. 
        Without this linked list, we could still retrieve keys from the 
        *Half Edge* dictionary by following a chain of *nextiID* keys 
        using the following instructions, but this would be slow:

        ::

          nextID = he.getNextID()
          heNext = self.hEdges[nextID]

        with the linked list this is done once and the results are recorded, enabling us to **directly** access a twin edge using:

        ::

          he.twin

        Parameters
        ----------
       
        ob:     
          *Object3D*.  The Object3D object of which this *Half Edge* is a part.

        """
        print "linking hedges", len(ob.he_hedges)
        for he in ob.he_hedges.values():            
            try:                
                he.next = ob.he_hedges[he.nextID]           
            except:
                continue

        for he in ob.he_hedges.values():
            try:                
                he.twin = ob.he_hedges[he.twinID]                
            except:
                continue



def calcHedgeData(ob):
        """
        This function loops through each Face object for a given Object3D object and 
        calculates the *Half Edges* data for each edge of that face, 
        calling the *addHedge* function for each new *Half Edge* to add 
        text strings representing the twin and next *Half Edges* into the HEdge dictionary. 
        
        **First Pass** - Builds dictionary of string references to other half edges 
        that may or may not have been processed yet. 

        .. image:: ../images/face.png
           :alt: Hedges Dictionary Strings

        For example, in the image above:

        HEdge["vo-v1"] has as 'next' HEdge["v1-v2"] and as 'twin'
        HEdge["v1-v0"], where 'v0', 'v1' and 'v2' would evaluate to the indices (in the
        set of all vertices) that point to the 3 vertices defining the face being processed. 
        
        **Second Pass** - 
        Once the first pass is complete this function (calcHedgeData) calls the *linkHEdges* 
        function which performs a second pass, using the dictionary created in the first pass
        to add direct references to the 'twin' and 'next' half edges.

        .. image:: ../images/hedge_twin.jpg
           :alt: Twin Half Edge

        .. image:: ../images/hedge_next.jpg
           :alt: Next Half Edge

        Parameters
        ----------
       
        ob:     
          *Object3D*.  The Object3D object of which this *Half Edge* is a part.

        """
        ob.he_hedges = {} #New property added to base obj
        fIndex = 0        
        
        for f in ob.faces:
            
            vIndex0 = str(f.verts[0].idx)
            vIndex1 = str(f.verts[1].idx)
            vIndex2 = str(f.verts[2].idx) 

            heId1 = vIndex0+"-"+vIndex1
            heNextId1 = vIndex1+"-"+vIndex2
            heTwinId1 = vIndex1+"-"+vIndex0

            heId2 = vIndex1+"-"+vIndex2
            heNextId2 = vIndex2+"-"+vIndex0
            heTwinId2 = vIndex2+"-"+vIndex1

            heId3 = vIndex2+"-"+vIndex0
            heNextId3 = vIndex0+"-"+vIndex1
            heTwinId3 = vIndex0+"-"+vIndex2

            vIndex0 = f.verts[0].idx
            vIndex1 = f.verts[1].idx
            vIndex2 = f.verts[2].idx
            
            addHedge(ob,heId1,heNextId1,heTwinId1,vIndex0,fIndex)
            addHedge(ob,heId2,heNextId2,heTwinId2,vIndex1,fIndex)
            addHedge(ob,heId3,heNextId3,heTwinId3,vIndex2,fIndex)
            
            fIndex += 1
            
        linkHEdges(ob)
        ob.he_hedgeCalculated = 1

def edgesSharedByVert(v):
        """
        This function lists the *Half Edges* that share a specified vertex as 
        their starting points.
        When the *Half Edge* data is created, one of the *HEdge* objects that 
        starts at a vertex is registered against each Vert object. 
        This *Half Edge* is used as the starting point to find the other 
        edges that share that vertex. 
        
        If the *Half Edge* has a *twin* whose *next* *HEdge* also starts at 
        the specified vertex.  
        
        If the *Half Edge* retrieved from the vertex doesn't have a twin 
        (ie it's an open edge) then the third edge of the triangle upon which 
        this *Half Edge* sits is checked to try and find the next *Half Edge* 
        in the chain (the one whose endpoint is at the vertex).

        Parameters
        ----------
       
        v:     
          *Vert*.  The vertex to be scanned.

        """

        i = 0
        try:    
            startHEdge = v.he_hedge
        except:
            print v.idx
        edgesShared = [startHEdge]       
        
        try:
            loopHedge = startHEdge.twin.next
            while loopHedge != startHEdge:                
                edgesShared.append(loopHedge)
                if  i == 10:                
                    break
                i += 1
                try:
                    loopHedge = loopHedge.twin.next
                except:
                    break
                       
        except:            
            if startHEdge.next.next.twin:
                loopHedge = startHEdge.next.next.twin
                while loopHedge != startHEdge:                    
                    edgesShared.append(loopHedge)
                    if  i == 2:                
                        break
                    i += 1
                    if loopHedge.next.next.twin:
                        loopHedge = loopHedge.next.next.twin
                    else:
                        break
            else:                
                edgesShared.append(startHEdge.next)                
        return edgesShared


def hedgesSharedByFace(f):
    """
    This function lists the *Half Edges* that delimit a specified face.
    Each face has an associated *HEdge* object that is one of the 3 
    *Half Edges* delimiting it.
    Each *HEdge* object points to the next *HEdge* object on the same 
    face, so we just follow this chain around until we get back to the 
    starting point.  
    
    .. image:: ../images/face.png
       :alt: HEdges shared by a single face

    Parameters
    ----------
   
    f:     
      *Face*.  The face to be scanned.
    """
    
    hEdgesShared = []
    startHEdge = f.he_hedge
    hEdgesShared.append(startHEdge)
    loopHedge = startHEdge.next
    x = 0
    if loopHedge:
        while loopHedge != startHEdge and x < 2:
            hEdgesShared.append(loopHedge)
            loopHedge = loopHedge.next
            x += 1
    else:
        return []
    return hEdgesShared

def facesSharedByVert(v):
    """
    This function lists the faces that share a specified vertex.
    This function calls the *edgesSharedByVert* function to retrieve a 
    list of *Half Edges* that start at that vertex and returns the list
    of faces that each of those *Half Edges* is on.  
    
    .. image:: ../images/vert.png
       :alt: Faces that share the specified vertex

    Parameters
    ----------
   
    v:     
      *Vertex*.  The vertex to be scanned.
    """
    
    hEdges = edgesSharedByVert(v)
    facesShared = []
    for he in hEdges:
        facesShared.append(he.face)

    return facesShared

#def subvertIdxSharedByVert(v):
    
    #hEdges = edgesSharedByVert(v)
    #subvertsIdxs = []
    #for he in hEdges:
        #subvertsIdxs.append(he.subVertID) #TODO: getter

    #return subvertsIdxs

    
def vertsSharedbyVert(v):
    """
    This function lists the set of vertices from all of the faces that 
    share the specified vertex.
    This function calls the *facesSharedByVert* function to retrieve a 
    list of faces that share the specified vertex and returns the list
    of all of the vertices on all of those faces. The list is deduplicated. 
        
    .. image:: ../images/vert_shared.png
       :alt: Vertices from faces that share the specified vertex

    Parameters
    ----------
   
    v:     
      *Vertex*.  The vertex to be scanned.
    """

    vertsShared = []
    facesShared = facesSharedByVert(v)
    for f in facesShared:
        for ve in f.verts:
            if ve != v and ve not in vertsShared:
                vertsShared.append(ve)
    return vertsShared

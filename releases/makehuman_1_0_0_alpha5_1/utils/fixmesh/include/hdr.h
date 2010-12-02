/*
	hdr.h
	Thomas Larsson 2009
	thomas_larsson_01@hotmail.com

	Main include file.
	Defines the geometrical structures
*/

/*
	Includes
*/
#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "vector.h"

#define Epsilon	1e-6
#define Infinity 1e6

//#define WeightThreshold 0.7
#define TargetThreshold 0.05

extern int verbosity;
extern double weightStep;
extern double zoneSize;
extern double detailThreshold;
extern bool stripPrefix;

/*
 	Flags
*/

#define F_MHX			0x01
#define F_ONLYTRIS		0x02
#define F_ALLOCGROUPS	0x04
#define F_TEXTVERTS		0x08
#define F_PRINTGROUPS	0x10

/*
	Typedefs
*/
typedef unsigned char   uchar;
typedef unsigned int uint;
typedef unsigned short  ushort;


#define BUFSIZE		200
#define NAMESIZE	48
#define MaxMaterial	16
#define MaxGroup	400
#define MaxTextVert	6

	
/* 
	Error handling
*/
extern char theError[BUFSIZE];
extern void raiseError();

#define RaiseError0(str)		{ sprintf(theError, str); raiseError(); }
#define RaiseError1(str, a)		{ sprintf(theError, str, a); raiseError(); }
#define RaiseError2(str, a, b)		{ sprintf(theError, str, a, b); raiseError(); }
#define RaiseError3(str, a, b, c)		{ sprintf(theError, str, a, b, c); raiseError(); }

/*
	Basic data types
*/

struct Face;
struct Mesh;

struct Vert {
	int	 m_idx;
	int	 m_nMats;
	int	 m_mats[MaxMaterial];
	int	 m_nTextVerts;
	int	 m_tv[MaxTextVert];
	double m_weights[MaxGroup];
	Vector3	m_co;
	Vector3 m_offset;

	Vert();
	~Vert();

	void dump(FILE *fp);

	void readCo(int idx, char *cp) ;
	bool hasSameMaterial(Face *pFace);
	void addMaterial(int mat);
	void remapMaterials(int nMats, int *map);
	void addGroup(int group, double weight);
	void insertTextVert(int tv);
};

struct TextVert {
	int	 	m_idx;
	double 	m_uv[2];
	int	 	m_v;

	TextVert();
	~TextVert();
	
	void dump(FILE *fp);
	void readUv(int idx, char *cp);
};

struct Face {
	int	 m_idx;
	int	 m_nCorners;
	int	 m_v[4];
	int	 m_tv[4];
	double m_dist[3];

	int	 m_mat;
	int	 m_bestGroup;
	int	 m_groups[MaxGroup];

	Vector3	m_normal;
	Vector3	m_u01;
	Vector3 m_u02;

	Face();
	~Face();

	void dump(FILE *fp);

	void read(int idx, char *buf, int offs, Mesh *mesh);
	void splitQuad(Face *pFace);
	void setMaterial(int mat, Vert *verts);
	void setGroup(int group, Vert *verts);

	void initNormals(Vert *verts);
	double normalDistance(Vector3 v, Vert *verts);
	double closestCorner(Vector3 v, Vert *verts);
	void setupZone(Vert *verts);
	bool inZone(Vector3 vec, Vert *verts);
	bool findWeights(Vector3 vec, double *weights, Vert *verts);

	bool isNeighbor(Face *pFace);
	void addNeighbor(Face *pFace);
	void findCenter(Vert *verts, Vector3 &center);

};

enum GroupType { GT_NONE, GT_VERT, GT_FACE };

struct Mesh {
	char m_name[NAMESIZE];
	Vector3 m_center;
	int	 m_nVerts;
	int	 m_nVertNormals;
	int	 m_nTextVerts;
	int	 m_nFaces;
	Vert	*m_verts;
	TextVert *m_textVerts;
	Face *  m_faces;

	GroupType m_groupType;	
	int  m_nGroups;
	char m_groupNames[MaxGroup][NAMESIZE];
	int	 m_nMaterials;
	char m_matName[MaxMaterial][NAMESIZE];

	int		*m_targVerts;
	double   *m_weights;

	Mesh();
	~Mesh();
	void init(char *name);
	void dump(FILE *fp);

	void findCenter();
	void recenter(Mesh *mesh);

	void readObjFile(const char *name, int flags);
	void readTargetFile(const char *name, double &threshold);
	void writeObjFile(const char *tarName, int flagsTar);
	void writeTargetFile(const char *name, bool detail, double threshold);
	void readVGroupFile(const char *name);
	void writeVGroupFile(const char *name, double threshold);
	
	void printFace(FILE *out, int f, bool doText);

	void initGroups();
	void allocGroups();
	int setGroup(char *name);
	void findGroups(Mesh *mesh, bool doFaces);
	bool partGroup(int g);
	void readGroups(const char *fileName);
	void saveGroups(const char *fileName);
	int groupFromName(char *name);

	void findTextVerts(Mesh *mesh);

	void initMaterials();
	int insertMaterial(const char *name);
	void countMaterials();

	void saveNeighbors(const char *name);
	void readNeighbors(const char *name);



	Face *findBestFaceWeights(Vert *pVert, double *weights,
	                          int *facesInZone, int *reorder,
	                          double *distsInZone, double *weightsInZone);
	void remapMaterials (Mesh *mesh);

	void setupWeights(Mesh *newMesh);
	void saveWeights(FILE *fp);
	void readWeights(const char *fileName);
	void moveWeights(Mesh *oldMesh);	
};

extern void dumpMesh(Mesh *pMesh, char *name);
extern void storeWeights(const char *fileName, Mesh *oldMesh, Mesh *newMesh);
extern FILE *fileOpen(const char *fileName, const char *mode);


/*
	mesh.cc
	Thomas Larsson 2009
	thomas_larsson_01@hotmail.com

	Mesh handling
*/

#include "stdafx.h"
#include "hdr.h"
#include <math.h>

/*
	Vert::Vert()
	Vert::~Vert()
*/

Vert::Vert()
{
	m_nMats = 0;
	m_nTextVerts = 0;
#if DynGroups
	m_weights = 0;
#endif
}

Vert::~Vert()
{
#if DynGroups
	if (m_weights) delete [] m_weights;
#endif
}

bool Vert::hasSameMaterial(Face *pFace)
{
	for (int m = 0; m < m_nMats; m++) {
		if (m_mats[m] == pFace->m_mat)
			return true;
	}
	return false;
}

/*
	TextVert::TextVert()
	TextVert::~TextVert()
*/

TextVert::TextVert()
{
	m_v = -1;
}

TextVert::~TextVert()
{
}

/*
	Face::Face()
	Face::~Face()

	Creator and destructor
*/

Face::Face()
{
	m_nCorners = 0;
	m_mat = -1;
	m_bestGroup = -1;
	memset(m_v, -1, 4*sizeof(int));
	memset(m_tv, -1, 4*sizeof(int));

	m_normal.init(0,0,0);
	m_u01.init(0,0,0);
	m_u02.init(0,0,0);

#if DynGroups
	m_groups = 0;
#endif
}

Face::~Face()
{
#if DynGroups
	if (m_groups) delete [] m_groups;
#endif
}

/*
	Mesh::Mesh()
	Mesh::~Mesh()
	void Mesh::init(char *name)

	Constructor and destructor and initialization
*/

Mesh::Mesh()
{
	m_nVerts = m_nVertNormals = m_nTextVerts = m_nFaces = 0;
	m_verts = 0;
	m_textVerts = 0;
	m_faces = 0;
	m_center.init(0,0,0);

	m_nMaterials = 0;

	m_targVerts = 0;
	m_weights = 0;
}

void Mesh::init(char *name)
{
	strncpy(m_name, name, 20);
	memset(m_groupNames, 0, MaxGroup*NAMESIZE*sizeof(char));
}

Mesh::~Mesh()
{
	if (m_verts) delete [] m_verts; m_verts = 0;
	if (m_textVerts) delete [] m_textVerts;
	if (m_faces) delete [] m_faces;
	if (m_targVerts) delete [] m_targVerts;
	if (m_weights) delete [] m_weights;
}


void Mesh::findCenter()
{
	Vector3 sum;
	sum.init(0,0,0);
	for (int i = 0; i < m_nVerts; i++) 
		sum.add(m_verts[i].m_co.vec);
	m_center.scale(1.0/m_nVerts, sum);
}

void Mesh::recenter(Mesh *mesh)
{
	Vector3 offs;
	offs.subtract(mesh->m_center, m_center);
	for (int i = 0; i < m_nVerts; i++) 
		m_verts[i].m_co.add(offs.vec);
}

/*
	void Face::initNormals(Vert *verts)

	Init the edges u01 = v1-v0, u02 = v2-v0, and the normal
*/
			

void Face::initNormals(Vert *verts)
{
	m_u01.subtract(verts[m_v[1]].m_co, verts[m_v[0]].m_co);
	m_u02.subtract(verts[m_v[2]].m_co, verts[m_v[0]].m_co);
	m_normal.crossProduct(m_u01, m_u02);
	m_normal.normalize();

	double s1 = scalarProduct(m_normal, m_u01);
	double s2 = scalarProduct(m_normal, m_u02);
	if (fabs(s1) > Epsilon || fabs(s2) > Epsilon)
		RaiseError2("initNormals %lf %lf\n", s1, s2);
}

/*
	void Face::findCenter(Vert *verts, Vector3 &center)
*/

void Face::findCenter(Vert *verts, Vector3 &center)
{
	Vector3 x, y;
	x.add(verts[m_v[0]].m_co, verts[m_v[1]].m_co);
	y.add(x, verts[m_v[2]].m_co);
	center.scale(1.0/3, y);
}

/*
	double Face::normalDistance(Vector3 v, Vert *verts)

	Find the distance from vertex v to the plane spanned by the face.
*/

double Face::normalDistance(Vector3 v, Vert *verts)
{
	Vector3 u;
	u.subtract(v, verts[m_v[0]].m_co);
	double x = scalarProduct(u, m_normal);
	return fabs(x);
}

/*
	double Face::closestCorner(Vector3 vec, Vert *verts)

	Find the sum of the distance from vector vec to the closest of the three corners.
*/

double Face::closestCorner(Vector3 vec, Vert *verts)
{
	double dist = 0, minDist = Infinity;
	Vector3 u;
	for (int i = 0; i < 3; i++) {
		u.subtract(vec, verts[m_v[i]].m_co);
		dist = u.length();
		if (dist < minDist)
			minDist = dist;
	}
	return minDist;
}

/*
	void Face::setupZone(Vert *verts)

 	Prepare the definition of the zone of the face.

 	If vert v is in f, with corners v1, v2, v3, the distance d(v,v1) is no
	bigger than d(v2,v1) and d(v3,v1), and similar for d(v,v2) and d(v,v3). 
 	Define the zone of f as the verts v such that d(v,v1) < c*d(v2,v1) and 
 	d(v,v1) < c*d(v3,v1). When we look for the face that v belongs to, it
 	suffices to look at the faces where v is in the zone. This is important,
 	because we use a sort that does not scale.
*/

void Face::setupZone(Vert *verts)
{
	Vector3 u;
	Vector3 v0 = verts[m_v[0]].m_co;
	Vector3 v1 = verts[m_v[1]].m_co;
	Vector3 v2 = verts[m_v[2]].m_co;
	double x, y;

	x = v0.distanceFrom(v1);
	y = v0.distanceFrom(v2);
	if (x < y)
		m_dist[0] = zoneSize*y;
	else
		m_dist[0] = zoneSize*x;

	x = v1.distanceFrom(v0);
	y = v1.distanceFrom(v2);
	if (x < y)
		m_dist[1] = zoneSize*y;
	else
		m_dist[1] = zoneSize*x;

	x = v2.distanceFrom(v0);
	y = v2.distanceFrom(v1);
	if (x < y)
		m_dist[2] = zoneSize*y;
	else
		m_dist[2] = zoneSize*x;
}

/*
	bool Face::inZone(Vector vec, Vert *verts)

 	Returns true if vector vec is in the zone of the face.
*/

bool Face::inZone(Vector3 vec, Vert *verts)
{
	double d0 = -1, d1 = -1, d2 = -1;
	
	d0 = vec.distanceFrom(verts[m_v[0]].m_co);
	if (d0 > m_dist[0]) goto failed;
	
	d1 = vec.distanceFrom(verts[m_v[1]].m_co);
	if (d1 > m_dist[1]) goto failed;
	
	d2 = vec.distanceFrom(verts[m_v[2]].m_co);
	if (d2 > m_dist[2]) goto failed;

#if 0
	vec.dump(stdout, "(", ") in ");
	verts[m_v[0]].m_co.dump(stdout, " (", ") ");
	verts[m_v[1]].m_co.dump(stdout, " (", ") ");
	verts[m_v[2]].m_co.dump(stdout, " (", ")\n");
//	printf("Dist %lf %lf %lf < %lf %lf %lf\n",  d0, d1, d2, m_dist[0], m_dist[1], m_dist[2]);
#endif
	
	return true;
failed:
	return false;
	printf("%lf %lf %lf\n", d0, d1, d2);
}

/*
	static void sort(int n, double *value, int *reorder)

 	Sort the first n integers according to the values in the second element.
 	The array value is destroyed in the process.
 	reorder contains the ordered list.
*/

static void sort(int n, double *value, int *reorder)
{
	double min;
	int i, j, best;
	
//	printf("Sorting..."); fflush(stdout);
	
	for (i = 0; i < n; i++) {
		min = Infinity-1;
		best = -1;
		for (j = 0; j < n; j++) {
			if (value[j] < min) {
				min = value[j];
				best = j;
			}
		}
		if (best < 0) 
			RaiseError0("sort");
		reorder[i] = best;
		value[best] = Infinity;
	}
}
	
/*
	Face *Mesh::findBestFaceWeights(Vert *pVert, double *weights,
	                                int *facesInZone, int *reorder, 
	                                double *distsInZone, double *weightsInZone)

 	Find the best face in material mat (= the face to which pVert belongs), and
 	compute the weights (w1,w2,w3): v = w1*v1 + w2*v2 + w3*v3.
 	The last four arguments are large arrays (of size m_nFaces) that were
 	allocated in the calling function.
*/

#define DebugVert	0
#define Rescue		0

static double smallestAllowedWeight, biggestAllowedWeight;

Face *Mesh::findBestFaceWeights(Vert *pVert, double *weights, 
                                int *facesInZone, int *reorder, 
                                double *distsInZone, double *weightsInZone)
{
	Face *pFace;
	int i, j, n;
	bool test;
	double dev, mindev, w;
	//int ntries = 0;

	int nInZone;

	smallestAllowedWeight = -weightStep;
	biggestAllowedWeight = 1+weightStep;

#if DebugVert	
	if (pVert->m_idx >= DebugVert)
		i = 1;
#endif

//retry:
	// Find all faces with v in the zone.
	nInZone = 0;
	for (i = 0; i < m_nFaces; i++) {
		pFace = &m_faces[i];
		if (pVert->hasSameMaterial(pFace)) {
			if (pFace->inZone(pVert->m_co, m_verts))
				facesInZone[nInZone++] = pFace->m_idx;
		}
	}
	if (nInZone == 0)
		RaiseError3("No vert in zone for vert %d mat %d size %d\n", 
			pVert->m_idx, pVert->m_mats[0], i);

	// For every face in the zone, find the closest corner to v.
#if Rescue
	minDist = Infinity;
	best = -1;
#endif
	for (i = 0; i < nInZone; i++) {
		pFace = &m_faces[facesInZone[i]];
		distsInZone[i] = pFace->normalDistance(pVert->m_co, m_verts);
#if Rescue
		dist = pFace->closestCorner(pVert->m_co, m_verts);
		if (dist < minDist) {
			minDist = dist;
			best = i;
		}
#endif
	}

	// Sort the faces in the zone according to their distance from v.
	sort(nInZone, distsInZone, reorder);

	// We say that v belongs to the first face in the reordered list, such
	// that all three weights are legal, i.e. w > smallestAllowedWeight and
	// w < biggestAllowedWeight.
	for (i = 0; i < nInZone; i++) {
		pFace = &m_faces[facesInZone[reorder[i]]];
		test = pFace->findWeights(pVert->m_co, weights, m_verts);
#if DebugVert
		if (pVert->m_idx == DebugVert) {
			dist = pFace->normalDistance(pVert->m_co, m_verts);
			printf("f %d %d %d %lf v %d\n", pFace->m_idx, i, reorder[i], dist, pVert->m_idx);
			printf(" v %d %d %d w %lf %lf %lf\n",
			       pFace->m_v[0], pFace->m_v[1], pFace->m_v[2], 
			       weights[0], weights[1], weights[2]);
		}
#endif
		if (test)
			return pFace;
		memcpy(&weightsInZone[3*reorder[i]], weights, 3*sizeof(double));
#if Rescue
		if (best < 0)
			RaiseError0("No verts in zone\n");
		pFace = &m_faces[best];
		pFace->findWeights(pVert->m_co, weights, m_verts);
		return pFace;
#endif
	}

#if 0
	// If this did not work, try again with a more liberal definition of legal.
	if (ntries++ < 5) {
		smallestAllowedWeight -= weightStep;
		biggestAllowedWeight += weightStep;
		goto retry;
	}
#endif

	// We should have left before we arrive here.
	printf("\nDid not find a best face for vert %d at ", pVert->m_idx);
	pVert->m_co.dump(stdout, "(", ").\n");
	mindev = Infinity;
	for (n = 0; n < nInZone; n++) {
		i = reorder[n];
		if (verbosity > 1)
			printf("\n%d %d %d:", n, i, facesInZone[i]);
		dev = 0.0;
		for (j = 0; j < 3; j++) {
			w = weightsInZone[3*i+j];
			if (w > 1+dev) 
				dev = w-1;
			else if (w < -dev)
				dev = -w;
			if (verbosity > 1) {
				printf(" %5.2lf: ", w); 
				m_verts[pFace[i].m_v[j]].m_co.dump(stdout, "(", ") ");
			}
		}
		if (dev < mindev)
			mindev = dev;
	}
	printf("Tested %d faces. Rerun with -weight > %7.3lf\n", nInZone, mindev);
	RaiseError0("\nfindBestFace");

	return 0;
}

/*
	bool Face::findWeights(Vector3 v, double *weights, Vert *verts)

	This face, which has corners v1 v2 v3.
	The coordinate of vertex v is x = w1*x1 + w2*x2 + w3*x3.
	Finds the weights (w1, w2, w3).
 	If all wi are between 0 and 1 and w1+w2+w3 = 1, then the vertex
 	is in the face, and return true.
 	But we require only that wi > smallestAllowedWeight and
 	wi < biggestAllowedWeight;
 	
*/

bool Face::findWeights(Vector3 vec, double *weights, Vert *verts)
{
	double A[3*3], b[3];
	Vector3 co;
	int j;
	int nCols = 3;

	for (j = 0; j < 3; j++) {
		co = verts[m_v[j]].m_co;
		Elt(A,0,j) = 1;
		Elt(A,1,j) = scalarProduct(m_u01, co);
		Elt(A,2,j) = scalarProduct(m_u02, co);
		weights[j] = 0;
	}

	b[0] = 1;
	b[1] = scalarProduct(m_u01, vec);
	b[2] = scalarProduct(m_u02, vec);

	gaussSolve(3, (double*)A, b, weights, 0);

	for (j = 0; j < 3; j++) {
		if (weights[j] > biggestAllowedWeight ||
			weights[j] < smallestAllowedWeight) 
			return false;
	}
	return true;
}

/*
	void Mesh::setupWeights(Mesh *newMesh)
*/

void Mesh::setupWeights(Mesh *newMesh)
{
	Vert *pVert;
	Face *pFace;
	int i, v;
	Vector3 weight;

	// Allocate big arrays. Done once here instead of once for each vert,
	// because I ran into problems with bad_alloc after some 6000 verts.
	int *facesInZone = new int[m_nFaces];
	int *reorder = new int[m_nFaces];
	double *distsInZone = new double[m_nFaces];
	double *weightsInZone = new double[3*m_nFaces];

	// For each face, set up normals and zone.
	for (i = 0; i < m_nFaces; i++) {
		m_faces[i].initNormals(m_verts);
		m_faces[i].setupZone(m_verts);
	}

	// For each vertex in the new mesh, find the best face in the old mesh,
	// its corners (= m_targVerts) and the weights for each corner. Store 
	// these data in the new mesh.
	// First we must allocate.
	
	newMesh->m_targVerts = new int[3*m_nVerts*sizeof(int)];
	newMesh->m_weights = new double [3*m_nVerts*sizeof(double)];

	printf("Vert "); fflush(stdout);
	for (v = 0; v < newMesh->m_nVerts; v++) {
		pVert = &newMesh->m_verts[v];
		if (pVert->m_nMats > 0) {
			pFace = findBestFaceWeights(pVert, &newMesh->m_weights[3*v],
		                            facesInZone, reorder, 
		                            distsInZone, weightsInZone);
			memcpy(&newMesh->m_targVerts[3*v], pFace->m_v, 3*sizeof(int));
		}
		else 
			printf("Warning: vertex %d unassigned material\n", v);

		// This takes some time, so notify the user that we are working.
		if (v % 100 == 0) {
			printf("%d ", v); fflush(stdout);
		}
	}
}

/*
	void Mesh::saveWeights(FILE *fp)

 	Save the target verts and the weights. Each line consists of 7 data:

 	v (new mesh), tv1, tv2, tv3 (old mesh), w1, w2, w3.
*/

void Mesh::saveWeights(FILE *fp)
{
	int v, j;
	int *tvs;
	double *wts;
	double maxWeight = -Infinity, minWeight = Infinity;

	fprintf(fp, "MHCONV %d\n", m_nVerts);
	for (v = 0; v < m_nVerts; v++) {
		if (m_verts[v].m_nMats == 0) {
			fprintf(fp, "%6d %6d %6d %6d %9.6f %9.6f %9.6f\n", 
				v, 0, 1, 2, 1.0, 0.0, 0.0);
		}
		else {
			tvs = &m_targVerts[3*v];
			wts = &m_weights[3*v];
			fprintf(fp, "%6d %6d %6d %6d %9.6f %9.6f %9.6f\n", 
				v, tvs[0], tvs[1], tvs[2], wts[0], wts[1], wts[2]);

			for (j = 0; j < 3; j++) {
				if (wts[j] > maxWeight)
					maxWeight = wts[j];
				if (wts[j] < minWeight)
					minWeight = wts[j];
			}
		}
	}

	if (verbosity >= 2)
		printf("\nWeights %lf - %lf\n", minWeight, maxWeight);
}

/*
	void storeWeights(const char *fileName, Mesh *oldMesh, Mesh *newMesh)

 	Save the data that allows us to map new verts to old faces.
*/

void storeWeights(const char *fileName, Mesh *oldMesh, Mesh *newMesh)
{
	if (verbosity > 0)
		printf("Storing weights\n");

	oldMesh->setupWeights(newMesh);
	FILE *fp = fileOpen(fileName, "w");
	newMesh->saveWeights(fp);
	fclose(fp);

	if (verbosity > 0)
		printf("Weights stored\n");
}

/*
	void Mesh::readWeights(const char *fileName)

 	For use in the convert state. Read the target verts and weights from
 	the file prepared in the build stage.
 	The info is stored in m_targVerts and m_weights.
*/

void Mesh::readWeights(const char *fileName)
{
	int v, nVerts;
	int *tvs;
	double *wts;
	char buf[BUFSIZE], hdr[BUFSIZE];
	int line_nr = 0;

	if (verbosity > 0)
		printf("Reading weights\n");

	FILE *fp = fileOpen(fileName, "r");
	fgets(buf, BUFSIZE, fp);
	if (sscanf(buf, "%s %d", hdr, &nVerts) != 2 ||
		strcmp(hdr, "MHCONV") != 0 ||
		nVerts != m_nVerts)
		RaiseError1("File %s is strange\n", fileName);

	m_targVerts = new int[3*m_nVerts*sizeof(int)];
	m_weights = new double [3*m_nVerts*sizeof(double)];

	for (v = 0; v < m_nVerts; v++) {
		line_nr += 1;
		if (!fgets(buf, BUFSIZE, fp))
			RaiseError2("Unexpected EOF in %s at line %d\n", fileName, line_nr);

		tvs = &m_targVerts[3*v];
		wts = &m_weights[3*v];
		if (sscanf(buf, "%d %d %d %d %lf %lf %lf\n", 
			&v, &tvs[0], &tvs[1], &tvs[2], &wts[0], &wts[1], &wts[2]) != 7)
			RaiseError3("Line %d of %s is strange:\n\t%s\n", line_nr, fileName, buf);
	}
	fclose(fp);

	if (verbosity > 0)
		printf("Weights read\n");
}

/*
	void Mesh::moveWeights(Mesh *oldMorph)

 	Move the verts in the new mesh, according to the data in the old morph.

 	vert.m_co is the coordinate of the base mesh. Not touched.
 	vert.m_offset is the offset in the morph.
 	If the old offsets are x1,x2,x3, the new offset is 
 	x = w1*x1 + w2*x2 + w3*x3. 
*/

void Mesh::moveWeights(Mesh *oldMorph)
{
	int i, v;
	int *tvs;
	double *wts;
	Vert	*pVert;
	Vector3 x[3], y;

	if (verbosity > 0)
		printf("Moving weights\n");

	for (v = 0; v < m_nVerts; v++) {
		if (m_verts[v].m_nMats > 0) {
			tvs = &m_targVerts[3*v];
			wts = &m_weights[3*v];
			for (i = 0; i < 3; i++) {
				pVert = &oldMorph->m_verts[tvs[i]];
				x[i].scale(wts[i], pVert->m_offset );
			}
			y.add(x[1], x[2]);
			m_verts[v].m_offset.add(x[0], y);
		}
	}
	
	if (verbosity > 0)
		printf("Weights moved\n");	
}


void Mesh::findTextVerts(Mesh *oldMesh)
{
	int tv, v, j, oldTv;
	int *tvs;
	double *wts, *uv;
	Vert *pVert;
	TextVert *pTextVert;

	m_nTextVerts = m_nVerts;
	if (m_textVerts != 0)
		RaiseError0("Textverts should not be allocated here\n");
	m_textVerts = new TextVert[m_nTextVerts];
	memset(m_textVerts, 0, m_nTextVerts*sizeof(TextVert));
		
	tv = 0;
	for (v = 0; v < m_nVerts; v++) {
		m_verts[v].m_nTextVerts = 1;
		m_verts[v].m_tv[0] = tv;
		m_textVerts[tv].m_v = v;
		uv = m_textVerts[tv].m_uv;
		tvs = &m_targVerts[3*v];
		wts = &m_weights[3*v];

		uv[0] = uv[1] = 0.0;
		for (j = 0; j < 3; j++) {
			pVert = &oldMesh->m_verts[tvs[j]];
			oldTv = pVert->m_tv[0];
			pTextVert = &oldMesh->m_textVerts[oldTv];
			uv[0] += wts[j]*pTextVert->m_uv[0];
			uv[1] += wts[j]*pTextVert->m_uv[1];
		}

		tv += 1;
	}
}



	
		

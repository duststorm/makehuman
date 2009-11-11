/*
	group.cc
	Thomas Larsson 2009
	thomas_larsson_01@hotmail.com

	Group handling
*/

#include "stdafx.h"
#include "hdr.h"
#include <math.h>


/*
	void allocGroups()
*/

void Mesh::allocGroups()
{
	for (int v = 0; v < m_nVerts; v++) {
#if DynGroups
		m_verts[v].m_weights = new double[MaxGroup];
#endif
		memset(m_verts[v].m_weights, 0, MaxGroup*sizeof(double));
	}

	for (int f = 0; f < m_nFaces; f++) {
#if DynGroups
		m_faces[f].m_groups = new int [MaxGroup];
#endif
		memset(m_faces[f].m_groups, 0, MaxGroup*sizeof(int));
	}
}

void Face::setGroup(int group, Vert *verts)
{
	if (group < 0)
		RaiseError0("No group assigned\n");
	m_groups[group] = 1;
	for (int i = 0; i < m_nCorners; i++)
		verts[m_v[i]].addGroup(group, 1.0);
}


/*
	bool Mesh::partGroup(int g)
*/

bool Mesh::partGroup(int g)
{
	return (!stripPrefix || strncmp("part", m_groupNames[g], 4) == 0);
}

/*
	void Mesh::findGroups(Mesh *oldMesh, bool doFaces)
*/

void Mesh::findGroups(Mesh *oldMesh, bool doFaces)
{
	int i, v, g, f, n, best;
	double w, maxWeight;
	int *tvs;
	double *wts;
	bool belongs;
	Vert	*pVert;
	Vector3 y;

	if (verbosity > 0)
		printf("Finding groups\n");

	m_nGroups = oldMesh->m_nGroups;
	memcpy(m_groupNames, oldMesh->m_groupNames, MaxGroup*NAMESIZE*sizeof(char));

	for (v = 0; v < m_nVerts; v++) {
#if DynGroups
		m_verts[v].m_weights = new double[MaxGroup];
#endif
		memset(m_verts[v].m_weights, 0, MaxGroup*sizeof(double));
	}

	for (v = 0; v < m_nVerts; v++) {
		if (m_verts[v].m_nMats > 0) {
			tvs = &m_targVerts[3*v];
			wts = &m_weights[3*v];
			for (g = 0; g < m_nGroups; g++) {	
				w = 0;
				for (i = 0; i < 3; i++) {
					pVert = &oldMesh->m_verts[tvs[i]];
					w += wts[i]*pVert->m_weights[g];
				}
				m_verts[v].m_weights[g] = w;
			}
		}
	}

	if (!doFaces)
		return;

	// 
	for (f = 0; f < m_nFaces; f++) {
		memset(m_faces[f].m_groups, 0, MaxGroup*sizeof(int));
		best = -1; maxWeight = -Infinity;
		belongs = false;
		for (g = 0; g < m_nGroups; g++) {
			w = 0;
			n = m_faces[f].m_nCorners;
			for (i = 0; i < n; i++) {
				v = m_faces[f].m_v[i];
				w += m_verts[v].m_weights[g];
			}
			w /= n;

			if (w > maxWeight && partGroup(g)) {
				maxWeight = w; best = g;
			}
			if (w > detailThreshold) {
				m_faces[f].m_groups[g] = 1;
				if (!belongs && partGroup(g))
					belongs = true;
			}
		}
		m_faces[f].m_bestGroup = best;
		if (!belongs) {
			m_faces[f].m_groups[best] = 1;
		}
	}

	// Set the vertex weights on the corners to 1.0
	for (f = 0; f < m_nFaces; f++) {
		for (g = 0; g < m_nGroups; g++) {
			for (i = 0; i < m_faces[f].m_nCorners; i++) {
				v = m_faces[f].m_v[i];
				wts = m_verts[v].m_weights;
				if (m_faces[f].m_groups[g])
					wts[g] = 1.0;
				else if (wts[g] > detailThreshold)
					wts[g] = 1.0;
				else 
					wts[g] = 0.0;
			}
		}
	}

	// Test

	for (v = 0; v < m_nVerts; v++) {
		belongs = false;
		wts = m_verts[v].m_weights;
		for (g = 0; g < m_nGroups; g++) {
			if (wts[g] > detailThreshold && partGroup(g)) {
				belongs = true;
				break;
			}
		}
		if (!belongs)
			printf("Warning: vertex %d does not belong to a part group\n", v);
	}
			
	if (verbosity > 0)
		printf("Groups found\n");	
}

/*
	void Mesh::saveGroups(const char *fileName)
*/

void Mesh::saveGroups(const char *fileName)
{
	int v, g;
	
	FILE *fp = fileOpen(fileName, "w");

	if (verbosity > 0)
		printf("Saving groups\n");

	fprintf(fp, "MHGROUP %d\n", m_nGroups);
	
	for (g = 1; g < m_nGroups; g++) {
		fprintf(fp, "Group %d %s\n", g, m_groupNames[g]);
		for (v = 0; v < m_nVerts; v++) {
			if (m_verts[v].m_weights[g] >= detailThreshold)
				fprintf(fp, "%d %lf\n", v, m_verts[v].m_weights[g]);
		}
	}
			
	fclose(fp);

	if (verbosity > 0)
		printf("Groups saved\n");
}

/*
	void Mesh::readGroups(const char *fileName)
*/

void Mesh::readGroups(const char *fileName)
{
	int v, g, g1;
	double w;
	int line_nr = 0;
	char buf[BUFSIZE], hdr[BUFSIZE], str[BUFSIZE];
	
	if (verbosity > 0)
		printf("Reading groups\n");

	FILE *fp = fileOpen(fileName, "r");
	fgets(buf, BUFSIZE, fp);
	if (sscanf(buf, "%s %d", hdr, &m_nGroups) != 2 ||
		strcmp(hdr, "MHGROUP") != 0)
		RaiseError1("File %s is strange\n", fileName);

#if DynGroups	
	if (m_verts[0].m_weights != 0) 
		RaiseError0("Bug: weights already allocated\n");

	for (v = 0; v < m_nVerts; v++) 
		m_verts[v].m_weights = new double[m_nGroups];
#endif

	g = 0;
	strcpy(m_groupNames[0], "Unassigned");
	
	while (fgets(buf, BUFSIZE, fp)) {
		line_nr += 1;
		if (sscanf(buf, "%s %d %s", hdr, &g1, str) == 3 &&
			strcmp(hdr, "Group") == 0 &&
		    g1 == g+1) {
			strcpy(m_groupNames[++g], str);
		}
		else if (sscanf(buf, "%d %lf", &v, &w) == 2) 
			m_verts[v].m_weights[g] = w;
		else
			RaiseError2("Strange line %d in %s\n", line_nr, fileName);
	}
	if (++g != m_nGroups)
		RaiseError2("Expected %d groups but got %d\n", m_nGroups, g);
			
	fclose(fp);

	if (verbosity > 0)
		printf("Groups read\n");
}

/*
	int Mesh::groupFromName(char *name)
*/

int Mesh::groupFromName(char *name)
{
	int n, g;
	char *cp;
	for (g = 0; g < m_nGroups; g++) {
		cp = m_groupNames[g];
		n = strlen(cp);
		if (strncmp(cp, name, n) == 0)
			return g;
	}
	RaiseError1("Did not find group %s\n", name);
	return 0;
}

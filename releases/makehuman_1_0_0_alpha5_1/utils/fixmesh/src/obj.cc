/*
	obj.cc
	Thomas Larsson 2009
	thomas_larsson_01@hotmail.com

	IO for files in Wavefront OBJ format
*/

#include "stdafx.h"
#include <math.h>
#include "hdr.h"


/*
	TextVert
*/

void TextVert::readUv(int idx, char *buf)
{
	m_idx = idx;
	if (sscanf(buf, "%lf %lf", &m_uv[0], &m_uv[1]) != 2)
			RaiseError1("TextVert::readUv %s", buf);
}

/*
	Vert
*/

void Vert::readCo(int idx, char *cp) 
{
	double x[3];
	m_idx = idx;
	if (sscanf(cp, "%lf %lf %lf", &x[0], &x[1], &x[2]) != 3) 
		RaiseError0("MVert::readCo");
	m_co.init(x);
}

static int numberOfTokens(char *buf)
{
	int n = 0;
	char *cp = strtok(buf, " \t\r\n");
	while (cp) {
		n += 1;
		cp = strtok(NULL, " \t\r\n");
	}
	return n;
}

void Vert::addGroup(int group, double weight)
{
	m_weights[group] = weight;
}

void Vert::addMaterial(int mat)
{
	for (int i = 0; i < m_nMats; i++) {
		if (m_mats[i] == mat)
			return;
	}
	m_mats[m_nMats++] = mat;
}

void Vert::insertTextVert(int tv)
{
	for (int i = 0; i < m_nTextVerts; i++) {
		if (m_tv[i] == tv)
			return;
	}
	if (m_nTextVerts >= MaxTextVert)
		RaiseError2("Too many texture verts v %d tv %d\n", m_idx, tv);
	m_tv[m_nTextVerts++] = tv;
}
/*
	void Face::read(int idx, char *buf, int offs, Mesh *mesh)
*/

void Face::read(int idx, char *buf, int offs, Mesh *mesh)
{
	int i;
	char *faceStr[4];
	uint v, tv, vn;
	uint nelts;

	m_idx = idx;
	m_nCorners = 0;
	char *cp = strtok(buf, " \t");
	while (cp && m_nCorners < 4) {
		faceStr[m_nCorners++] = cp;
		cp = strtok(NULL, " \t");
	}
	for ( i = 0; i < m_nCorners; i++) {
		cp = faceStr[i];
		while (cp = strchr(cp, '/'), cp)
			*cp = ' ';
		nelts = sscanf(faceStr[i], "%d %d %d", &v, &tv, &vn);
		v -= offs;
		tv -= offs;
		switch (nelts) {
		case 3:
			// Fall thru
		case 2:
			m_tv[i] = tv;
			if (tv == 0)
				vn = 0;
			if (mesh->m_textVerts) {
				mesh->m_textVerts[tv].m_v = v;				
				mesh->m_verts[v].insertTextVert(tv);
			}
			// Fall thru
		case 1:
			m_v[i] = v;
			break;
		default:
			if (i == 3) {
				m_nCorners = 3;
				m_v[i] = m_tv[i] = -1;
			}
			else
				RaiseError1("readFace: bad face %s\n", faceStr[i]);
			break;
		}
	}
}

void Face::splitQuad(Face *pFace)
{
	m_idx = pFace->m_idx+1;

	m_v[0] = pFace->m_v[0];
	m_v[1] = pFace->m_v[2];
	m_v[2] = pFace->m_v[3];
	pFace->m_v[3] = -1;
	
	m_tv[0] = pFace->m_tv[0];
	m_tv[1] = pFace->m_tv[2];
	m_tv[2] = pFace->m_tv[3];
	pFace->m_tv[3] = -1;

	m_nCorners = pFace->m_nCorners = 3;
	m_mat = pFace->m_mat;
}


void Face::setMaterial(int mat, Vert *verts)
{
	if (mat < 0)
		RaiseError0("No material assigned\n");
	m_mat = mat;
	for (int i = 0; i < m_nCorners; i++)
		verts[m_v[i]].addMaterial(mat);
}

/*
	void Mesh::readObjFile(const char *name, int flags)
*/

void Mesh::readObjFile(const char *name, int flags)
{
	uint v, tv, vn, f, n, i;
	double x;
	Face *pFace;
	Vert *pVert;
	uint lineNo;
	int crntMat = 0;
	int crntGroup = 0;
	char line[BUFSIZE+1];
	char fileName[BUFSIZE];
	const char *ext = (flags & F_MHX ? "mhx" : "obj");
	int offs = (flags & F_MHX ? 0 : 1);

	sprintf(fileName, "%s.%s", name, ext);
	if (verbosity > 0)
		printf("Reading %s file %s\n", ext, fileName);
	FILE *fp = fileOpen(fileName, "r");

	m_nGroups = m_nVerts = m_nTextVerts = m_nFaces = 0;
	m_groupType = GT_NONE;

	lineNo = 0;
	while (fgets(line, BUFSIZE, fp)) {
		lineNo += 1;
//		printf("."); fflush(stdout);
		if (line[0] == '#');
		else if (strncmp(line, "v ", 2) == 0) 
			m_nVerts += 1;
		else if (strncmp(line, "g ", 2) == 0) {
			m_nGroups += 1;
			if (m_groupType == GT_VERT)
				RaiseError0("Cannot mix face and vert groups\n");
			m_groupType = GT_FACE;
		}
		else if (strncmp(line, "vertgroup ", 10) == 0) {
			m_nGroups += 1;
			if (m_groupType == GT_FACE)
				RaiseError0("Cannot mix face and vert groups\n");
			m_groupType = GT_VERT;
		}
		else if ((flags & F_TEXTVERTS) && (strncmp(line, "vt ", 3) == 0) )
			m_nTextVerts += 1;
		else if (strncmp(line, "vn ", 3) == 0) 
			m_nVertNormals += 1;
		else if (strncmp(line, "f ", 2) == 0) {
			m_nFaces += 1;
			if (flags & F_ONLYTRIS) {
				n = numberOfTokens(line+2);
				switch (n) {
					case 3: 
						break;
					case 4: 
						m_nFaces += 1; break;
					default:
						RaiseError3("Face with %d corners at line %d of %s\n", n, lineNo, fileName);
				}
			}
		}
	}

	if (verbosity > 0)
		printf("%d verts, %d groups, %d textVerts, %d vertNormals, %d faces\n",
			m_nVerts, m_nGroups, m_nTextVerts, m_nVertNormals, m_nFaces);

	if (m_nVertNormals > 0 && m_nVertNormals != m_nVerts)
		RaiseError2("Wrong number of vert normals %d %d\n", m_nVertNormals, m_nVerts);

	m_verts = new Vert[m_nVerts];
	if (flags & F_TEXTVERTS)
		m_textVerts = new TextVert[m_nTextVerts];
	else
		m_textVerts = 0;
	m_faces = new Face[m_nFaces];
	initMaterials();
	if (flags & F_ALLOCGROUPS)
		allocGroups ();

	v = tv = vn = f = 0;
	m_nGroups = 1;

	rewind(fp);

	lineNo = 0;
	while (fgets(line, BUFSIZE, fp)) {
		lineNo += 1;

		if (line[0] == '#');
		else if (strncmp(line, "vertgroup ", 10) == 0) {
			crntGroup = setGroup(&line[10]);
		}
		else if (strncmp(line, "g ", 2) == 0) {
			crntGroup = setGroup(&line[2]);
		}
		else if (strncmp(line, "v ", 2) == 0) {
			pVert = &m_verts[v];
			pVert->readCo(v, line+2);
			pVert->m_offset.init(0,0,0);
			v += 1;
		}
		else if (strncmp(line, "wv ", 3) == 0) {
			if (sscanf(line+3, "%d %lf", &i, &x) != 2)
				RaiseError3("Strange line %d in %s: %s\n", lineNo, fileName, line);
			m_verts[i].addGroup(crntGroup, x);
		}
		else if ((flags & F_TEXTVERTS) && (strncmp(line, "vt ", 3) == 0) ) {
			m_textVerts[tv].readUv(tv, line+3);
			tv += 1;
		}
		else if (strncmp(line, "f ", 2) == 0) {
			pFace = &m_faces[f];
			pFace->read(f, line+2, offs, this);
			if (m_groupType == GT_FACE) {
				pFace->setGroup(crntGroup, m_verts);
			}
			pFace->setMaterial(crntMat, m_verts);
			if (flags & F_ONLYTRIS) {
				switch (pFace->m_nCorners) {
					case 3: 
						f += 1; 
						break;
					case 4: 
						m_faces[f+1].splitQuad(pFace);
						f += 2;
						break;
					default:
						RaiseError3("Face with %d corners at line %d in %s\n", 
							pFace->m_nCorners, lineNo, fileName);
				}
			}
			else
				f += 1;
		}
		else if (strncmp(line, "usemtl ", 7) == 0) {
			crntMat = insertMaterial(line+7);
		}
	}	

	fclose(fp);

	if (verbosity > 0)
		printf("%s file %s read\n", ext, fileName);
}

/*
	void Mesh::initMaterials()
*/

void Mesh::initMaterials()
{
	m_nMaterials = 1;
	strcpy(m_matName[0], "Unassigned");
}

/*
	int Mesh::setGroup(char *name) 
*/

int Mesh::setGroup(char *name) 
{
	int i;

	strtok(name, "\r\n");
	for (i = 0; i < m_nGroups; i++) {
		if (strcmp(name, m_groupNames[i]) == 0)
			return i;
	}
	if (i == MaxGroup)
		RaiseError2("Too many groups > %d (%s)\nRecompile.", MaxGroup, name);
	strncpy(m_groupNames[m_nGroups], name, NAMESIZE);
	return m_nGroups++;
}

/*
	int Mesh::insertMaterial(const char *name) 
*/

int Mesh::insertMaterial(const char *name) 
{
	int i;

	for (i = 0; i < m_nMaterials; i++) {
		if (strcmp(name, m_matName[i]) == 0)
			return i;
	}
	if (i == MaxMaterial)
		RaiseError1("Too many materials %d\n", i);
	strcpy(m_matName[m_nMaterials++], name);
	return i;
}

/*
	void Mesh::remapMaterials(Mesh *mesh)
*/

void Mesh::remapMaterials(Mesh *mesh)
{
	int i, j, v, f;
	char oldName[MaxMaterial][NAMESIZE];
	int	map[MaxMaterial];

	memcpy(oldName, m_matName, MaxMaterial*NAMESIZE*sizeof(char));
	memset(map, -1, MaxMaterial*sizeof(int));

	for (i = 0; i < mesh->m_nMaterials; i++) {
		for (j = 0; j < m_nMaterials; j++) {
			if (strcmp(oldName[j], mesh->m_matName[i]) == 0) {
				map[j] = i;
				strcpy(m_matName[j], oldName[i]);
				break;
			}
		}
	}

	if (verbosity >= 2) {
		for (i = 0; i < m_nMaterials; i++) {
			printf("%2d %2d %15s %15s\n", i, map[i], mesh->m_matName[i], m_matName[i]);
		}
	}
	
	for (f = 0; f < m_nFaces; f++) {
		m_faces[f].m_mat = map[m_faces[f].m_mat];
	}
	for (v = 0; v < m_nVerts; v++) {
		m_verts[v].remapMaterials(m_nMaterials, map);
	}
}

void Vert::remapMaterials(int nMats, int *map)
{
	int oldMats[MaxMaterial];

	memcpy(oldMats, m_mats, m_nMats*sizeof(int));
	for (int m = 0; m < m_nMats; m++) 
		m_mats[m] = oldMats[map[m]];
}


/*
	void Mesh::readTargetFile(const char *name)
*/

void Mesh::readTargetFile(const char *name, double &threshold)
{
	int v;
	double x[3];
	double d;
	int lineNo;
	char line[BUFSIZE+1];
	char fileName[BUFSIZE];

	sprintf(fileName, "%s", name);
	if (verbosity > 0)
		printf("Reading target file %s\n", fileName);
	FILE *fp = fileOpen(fileName, "r");

	lineNo = 0;
	threshold = Infinity;
	while (fgets(line, BUFSIZE, fp)) {
		lineNo += 1;
		if (sscanf(line, "%d %lf %lf %lf", &v, &x[0], &x[1], &x[2]) != 4)
		    RaiseError2("readTargetFile line %d file %s\n", lineNo, fileName);
		m_verts[v].m_offset.init(x);
		d = m_verts[v].m_offset.length();
		if (d > Epsilon && d < threshold)
			threshold = d;
	}
	fclose(fp);

	if (verbosity > 0)
		printf("Target file %s read\n", fileName);
}

/*
	void Mesh::writeTargetFile(const char *name, bool detail, double threshold)
*/

void Mesh::writeTargetFile(const char *name, bool detail, double threshold)
{
	int v;
	double *offs;
	char fileName[BUFSIZE];

	sprintf(fileName, "%s", name);
	if (verbosity > 0)
		printf("Writing target file %s\n", fileName);
	FILE *fp = fileOpen(fileName, "w");
		
	for (v = 0; v < m_nVerts; v++) {
		if (!detail || m_verts[v].m_offset.length() > threshold) {
			offs = m_verts[v].m_offset.vec;
			fprintf(fp, "%d %lf %lf %lf\n", v, offs[0], offs[1], offs[2]);
		}
	}
		
	fclose(fp);
	if (verbosity > 0)
		printf("Target file %s written\n", fileName);
}

/*
	void Mesh::writeObjFile(const char *tarName, int flagsTar)
*/

void Mesh::writeObjFile(const char *tarName, int flagsTar)
{
	int v, f, g;
	double *uv;
	Vector3 u;
	char file[BUFSIZE];
	bool empty = true;

	sprintf(file, "%s.obj", tarName);
	if (verbosity > 0)
		printf("Writing file %s\n", file);
	FILE *out = fileOpen(file, "w");

	for (v = 0; v < m_nVerts; v++) {
		u.add( m_verts[v].m_co, m_verts[v].m_offset );
		fprintf(out, "v %lf %lf %lf\n", u.vec[0], u.vec[1], u.vec[2]);
	}

	if (flagsTar & F_TEXTVERTS) {
		for (v = 0; v < m_nTextVerts; v++) {
			uv = m_textVerts[v].m_uv;
			fprintf(out, "vt %lf %lf\n", uv[0], uv[1]);
		}
	}

	for (g = 0; g < m_nGroups; g++) {
		if (flagsTar & F_PRINTGROUPS) {
			empty = true;
			for (f = 0; f < m_nFaces; f++) {
				if (m_faces[f].m_bestGroup == g) {
					empty = false;
					break;
				}
			}
			if (!empty)
				fprintf(out, "g part_%s\n", m_groupNames[g]);
		}

		if (m_nGroups == 1) {
			for (f = 0; f < m_nFaces; f++) 
				printFace(out, f, flagsTar & F_TEXTVERTS);
		}
		else {
			for (f = 0; f < m_nFaces; f++) {
				if (m_faces[f].m_bestGroup == g) 
					printFace(out, f, flagsTar & F_TEXTVERTS);
			}
		}
	}
	fclose(out);
	if (verbosity > 0)
		printf("Obj file %s written\n", file);
}

void Mesh::printFace(FILE *out, int f, bool doText)
{
	int *vlist = m_faces[f].m_v;
	int *tlist;

	if (doText) {
		tlist = m_faces[f].m_tv;
		fprintf(out, "f %d/%d %d/%d %d/%d", 
			vlist[0]+1, tlist[0]+1, vlist[1]+1, tlist[1]+1, vlist[2]+1, tlist[2]+1);
		if (vlist[3] < 0)
			fprintf(out, "\n");
		else
			fprintf(out, " %d/%d\n", vlist[3]+1, tlist[3]+1);
	}
	else {
		fprintf(out, "f %d %d %d", vlist[0]+1, vlist[1]+1, vlist[2]+1);
		if (vlist[3] < 0)
			fprintf(out, "\n");
		else
			fprintf(out, " %d\n", vlist[3]+1);
	}
}

/*
	void Mesh::readVGroupFile(const char *name)
*/

void Mesh::readVGroupFile(const char *name)
{
	int v;
	double w;
	int lineNo;
	char line[BUFSIZE+1];
	char fileName[BUFSIZE];

	sprintf(fileName, "%s", name);
	if (verbosity > 0)
		printf("Reading VGroup file %s\n", fileName);
	FILE *fp = fileOpen(fileName, "r");

	m_nGroups = 1;
	memset(m_groupNames, 0, MaxGroup*NAMESIZE*sizeof(char));
	for (v = 0; v < m_nVerts; v++)
		memset(m_verts[v].m_weights, 0, MaxGroup*sizeof(double));

	lineNo = 0;
	while (fgets(line, BUFSIZE, fp)) {
		lineNo += 1;
		if (sscanf(line, "%d %lf", &v, &w) != 2)
		    RaiseError2("readVGroupFile line %d file %s\n", lineNo, fileName);
		m_verts[v].m_weights[0] = w;
	}
	fclose(fp);

	if (verbosity > 0)
		printf("VGroup file %s read\n", fileName);
}

/*
	void Mesh::writeVGroupFile(const char *name, double threshold)
*/

void Mesh::writeVGroupFile(const char *name, double threshold)
{
	int v;
	double w;
	char fileName[BUFSIZE];

	sprintf(fileName, "%s", name);
	if (verbosity > 0)
		printf("Writing VGroup file %s\n", fileName);
	FILE *fp = fileOpen(fileName, "w");
		
	for (v = 0; v < m_nVerts; v++) {
		w = m_verts[v].m_weights[0];
		if (w > threshold) {
			fprintf(fp, "%d %lf\n", v, w);
		}
	}
		
	fclose(fp);
	if (verbosity > 0)
		printf("VGroup file %s written\n", fileName);
}

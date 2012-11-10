/*
	dump.cc
	Thomas Larsson 2009
	thomas_larsson_01@hotmail.com

	Dump content of data structures to file, mainly for debugging.
*/

#include "stdafx.h"
#include "hdr.h"


void Vert::dump(FILE *fp)
{
    fprintf(fp, "v %5d m ", m_idx);
	for (int m = 0; m < m_nMats; m++)
		fprintf(fp, "%3d ", m_mats[m]);
	m_co.dump(fp, "co ", "\n");
}

void TextVert::dump(FILE *fp)
{
    fprintf(fp, "tv %5d: uv %6.3f %6.3f\n",
        m_idx, m_uv[0], m_uv[1]);
}

void Face::dump(FILE *fp)
{
    fprintf(fp, "f %5d: v %5d %5d %5d %5d m %3d n",
        m_idx, m_v[0], m_v[1], m_v[2], m_v[3], m_mat);
    fprintf(fp, "\n");
}

void Mesh::dump(FILE *fp)
{
    int i;

    fprintf(fp, "Verts\n");
    for (i = 0; i < m_nVerts; i++) {
        m_verts[i].dump(fp);
    }
    fprintf(fp, "TextVerts\n");
    for (i = 0; i < m_nTextVerts; i++) {
        m_textVerts[i].dump(fp);
    }
    fprintf(fp, "Faces\n");
    for (i = 0; i < m_nFaces; i++) {
        m_faces[i].dump(fp);
    }
    fprintf(fp, "Materials\n");
    for (i = 0; i < m_nMaterials; i++) 
        fprintf(fp, "Mat %d %s\n", i, m_matName[i]);
	m_center.dump(fp, "\nCenter ", "\n");
}

void dumpMesh(Mesh *pMesh, char *name)
{
	if (verbosity < 2)
		return;
	
	char fileName[BUFSIZE];
	sprintf(fileName, "%sdump.txt", name);
    FILE *fp = fileOpen(fileName, "w");
    pMesh->dump(fp);
    fclose(fp);
}



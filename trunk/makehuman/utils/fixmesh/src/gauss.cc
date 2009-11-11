/*
	gauss.cc
	Thomas Larsson 2009
	thomas_larsson_01@hotmail.com

	Solve matrix equations with Gaussian elimination.
*/

#include "stdafx.h"
#include <math.h>
#include "hdr.h"

#define DUMPGAUSS	0

#if DUMPGAUSS
static void dumpGauss(FILE *fp, int nCols, double* mat, double* rhs)
{
	int i, j;
	
	if (verbosity < 2) return;

	fprintf(fp, "\n\nGauss elimination nCols = %d:", nCols);
	for (i = 0; i < nCols; i++) {
		fprintf(fp, "\n  ");
		for (j = 0; j < nCols; j++) 
			fprintf(fp, "\t%5.3lf", Elt(mat,i,j));
		fprintf(fp, "\t\t%5.3lf", rhs[i]);
		}
	fprintf(fp, "\n");
}
#endif

#define Swap(x, y, tmp)	{ tmp = x; x = y; y = tmp; }

void gaussSolve(int nCols, double *mat, double *rhs, double *soln, double *dflt)
{
	double fMax, fTmp;
	int i, j, k, m, n, iTmp;
	int *swap = new int[nCols];
	double *vec = new double[nCols];

	for (i = 0; i < nCols; i++)
		swap[i] = i;

#if DUMPGAUSS
	FILE *fp = fileOpen("logeqn.txt", "w");
	dumpGauss(fp, nCols, mat, rhs);
#endif

	for (k = 0; k < nCols-1; k++) {
restartLine:
		fMax = fabs(Elt(mat,k,k));
		m = k;
		for (i = k+1; i < nCols; i++) {
			if (fMax < fabs(Elt(mat,i,k))) {
				fMax = fabs(Elt(mat,i,k));
				m = i;
			}
		}

		if (m != k) {
			for (i = k; i < nCols; i++) 
				Swap( Elt(mat,k,i), Elt(mat,m,i), fTmp);
			Swap(rhs[k], rhs[m], fTmp);
		}

		if (fMax <= Epsilon) {
			if (dflt == 0)
				RaiseError0("GaussElim failed\n");

			fMax = 0;
			n = k;
			for (i = k+1; i < nCols; i++) {
				if (fMax < fabs(Elt(mat,k,i))) {
					fMax = fabs(Elt(mat,k,i));
					n = i;
				}
			}

			if (fMax > Epsilon) {
				for (i = 0; i < nCols; i++) 
					Swap( Elt(mat,i,k), Elt(mat,i,n), fTmp );
				Swap(swap[k], swap[n], iTmp);
				Swap(dflt[k], dflt[n], fTmp);
			}
			else {
				Elt(mat,k,k) = 1;
				rhs[k] = dflt[k];
			}

			goto restartLine;
		}

		for (j = k+1; j < nCols; j++) {
			fTmp = - Elt(mat,j,k) / Elt(mat,k,k);
			for (i = k; i < nCols; i++) 
				Elt(mat,j,i) = Elt(mat,j,i) + fTmp*Elt(mat,k,i);
			rhs[j] += fTmp*rhs[k];
		}
	}

	k = nCols-1;
	if (dflt != 0 && fabs(Elt(mat,k,k)) < Epsilon) {
		Elt(mat,k,k) = 1;
		rhs[k] = dflt[k];
	}

	for (k = nCols-1; k >= 0; k--) {
		vec[k] = rhs[k];
		for (i = k+1; i < nCols; i++) 
			vec[k] -= Elt(mat,k,i)*vec[i];
		vec[k] /= Elt(mat,k,k);
	}

	for (k = 0; k < nCols; k++) 
		soln[k] = vec[swap[k]];

#if DUMPGAUSS
	dumpGauss(fp, nCols, mat, soln);
    fclose(fp);
#endif
}









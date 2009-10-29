/*
	vector.h
	Thomas Larsson 2009
	thomas_larsson_01@hotmail.com

	Definition of the Vector3 and Matrix3 classes
*/

struct Vector3 
{
	double	vec[3];

	Vector3();
	virtual ~Vector3();

	Vector3 *copy();

	void init(double x[3]);
	void init(double x, double y, double z);
	void crossProduct(Vector3 x, Vector3 y);
	double length();

	void add(double x[3]);
	void add(Vector3 x, Vector3 y);
	void subtract(Vector3 x, Vector3 y);
	void subtract(Vector3 x);
	void scale(double s, Vector3 x);
	double distanceFrom(Vector3 x);
	void normalize();

	void dump(FILE *fp, const char *before, const char *after);
};

double scalarProduct(Vector3 u, Vector3 v);

class Matrix3 
{
public:
	double	mat[3][3];
public:
	Matrix3();
	virtual ~Matrix3();
};

extern void solveMatrixEquation(Matrix3 A, Vector3 b, Vector3 pU);
extern void gaussSolve(int nCols, double *mat, double *rhs, double *soln, double *dflt);

#define Elt(A,i,j)	A[i*nCols + j]


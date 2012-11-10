/*
	vector.cc
	Thomas Larsson 2009
	thomas_larsson_01@hotmail.com

	Operations on the Vector3 and Matrix3 classes.
*/

#include "stdafx.h"
#include <math.h>
#include "hdr.h"

/*
	Vector3 - 3D vectors

	This code is straightforward
*/


Vector3::Vector3()
{
	memset(vec, 0, 3*sizeof(double));
}

Vector3::~Vector3()
{
}

void Vector3::init(double x, double y, double z)
{
	vec[0] = x;
	vec[1] = y;
	vec[2] = z;
}

void Vector3::init(double x[3])
{
	for (int i = 0; i < 3; i++) 
		vec[i] = x[i];
}

void Vector3::add(double x[3])
{
	for (int i = 0; i < 3; i++) 
		vec[i] += x[i];
}

void Vector3::add(Vector3 x, Vector3 y)
{
	for (int i = 0; i < 3; i++) 
		vec[i] = x.vec[i] + y.vec[i];
}

void Vector3::subtract(Vector3 x, Vector3 y)
{
	for (int i = 0; i < 3; i++) 
		vec[i] = x.vec[i] - y.vec[i];
}

void Vector3::subtract(Vector3 x)
{
	for (int i = 0; i < 3; i++) 
		vec[i] -= x.vec[i];
}

double scalarProduct(Vector3 x, Vector3 y)
{
	double s = 0;
	for (int i = 0; i < 3; i++)
		s += x.vec[i]*y.vec[i];
	return s;
}

double Vector3::length()
{
	double s = 0;
	for (int i = 0; i < 3; i++)
		s += vec[i]*vec[i];
	return sqrt(s);
}

double Vector3::distanceFrom(Vector3 x)
{
	Vector3 u;
	for (int i = 0; i < 3; i++) 
		u.vec[i] = vec[i] - x.vec[i];
	return u.length();
}

void Vector3::scale(double s, Vector3 x)
{
	for (int i = 0; i < 3; i++) 
		vec[i] = s*x.vec[i];
}

void Vector3::normalize()
{
	double s = 0;
	for (int i = 0; i < 3; i++)
		s += vec[i]*vec[i];

	double len = sqrt(s);
	if (len != 0) {
		for (int i = 0; i < 3; i++) 
			vec[i] /= len;
	}				
}

void Vector3::dump(FILE *fp, const char *before, const char *after)
{
	fprintf(fp, " %s", before);
	for (int i=0; i<3; i++)
		fprintf(fp, " %5.3lf", vec[i]);
	fprintf(fp, " %s", after);
}

void Vector3::crossProduct(Vector3 x, Vector3 y)
{
	vec[0] = x.vec[1]*y.vec[2] - x.vec[2]*y.vec[1];
	vec[1] = x.vec[2]*y.vec[0] - x.vec[0]*y.vec[2];
	vec[2] = x.vec[0]*y.vec[1] - x.vec[1]*y.vec[0];
}

/*
	Matrix3 - 3x3 matrices

	This code is straightforward
*/

Matrix3::Matrix3()
{
	memset(mat, 0, 9*sizeof(double));
}

Matrix3::~Matrix3()
{

}

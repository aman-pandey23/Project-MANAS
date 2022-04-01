#include <iostream>
#include <math.h>
#include <stdio.h>
#include "cmath"
using namespace std;

int theta1;
int theta2;
int theta3;

int xw;
int yw;

int xe = 0;
int ye = 0;
int phie = 0;
int l1 = 0;
int l2 = 0;
int l3 = 0;

void polarxy(int link, int angle, float &x, float &y) {
   x = link * cos(angle);
   y = link * sin(angle);
}

float cosCalc(float a, float b, float c){
  float angle = acos((a*a + b*b - c*c)/(2*a*b));
  return angle;
}

int main() {
   cout << "enter xe: ";
   cin >> xe;
   cout << "\nenter ye: ";
   cin >> ye;
   cout << "\nenter phie: ";
   cin >> phie;
   cout << "\nenter l1: ";
   cin >> l1;
   cout << "\nenter l2: ";
   cin >> l2;
   cout << "\nenter l3: ";
   cin >> l3;

   float xo;
   float yo;
   polarxy(l3,phie,xo,yo);
   xw = xe - xo;
   yw = ye - yo;

   float r = sqrt(xw*xw + yw*yw);
   float gamma = cosCalc(r,l1,l2);

   theta2 = M_PI - cosCalc(l1,l2,r);
   theta1 = atan2(yw,xw) - gamma;
   theta3 = phie - theta1 - theta2;

   cout << "\ntheta1 is " << theta1;
   cout << "\ntheta2 is " << theta2;
   cout << "\ntheta3 is " << theta3;
}

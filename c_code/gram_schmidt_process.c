/*
I searched the internet, it's not there, the implementation of gram
schmidt orthogonalization process
implemented in C is not there, I 
mean not there at all, yeah there's an implementation in C++ on Github
I think, and it does a lot of complicated stuff, I got no idea how that works, Here I just translated 
the python script written into C.
I didn't do a very good job, don't know how efficient this is, Just went for it !

Damn ! That's the most number of I's I've ever used in a sentence !!
*/

#include <stdio.h>
#define len(x) sizeof(x)/sizeof(*x)

void arrcpy(int n, float v1[], float v2[]){
    for (int j=0; j<n; j++){
        v1[j] = v2[j] ;
    }
}


float amp(float v[], int n){
    float sum = 0;
    for (int i=0; i<n; i++){
        sum += v[i]*v[i] ;
    }
    return sum ;
}

float dot(float v1[], float v2[], int n){
    float sum = 0 ;
    for (int i=0; i<n; i++){
        float m = v1[i] ;
        float n = v2[i] ;
        sum += m*n ;
    }
    return sum ;
}

float gs_coff(float v1[], float v2[], int n){
    float nm = dot(v1, v2, n) ;
    float dm = amp(v1, n) ;
    float res = nm/dm ;
    return res ;
}

void mult(float num, float vt[], int n, float res[]){
    for (int i=0; i<n; i++){
        res[i] = num * vt[i] ;
    }
}

void proj(int n, float v1[], float v2[], float res[]){
    float m = gs_coff(v1, v2, n) ;
    mult(m , v1, n, res) ;
}

void sub(int n, float v1[], float v2[], float res[]){
    for (int i=0; i<n; i++){
        res[i] = v1[i] - v2[i] ;
    }
}

void printa(int n, float v[]){
    for (int o=0; o<n; o++){
        printf(" %f ", v[o]) ;
    }
    printf("\n") ;
}

void gram_schmidt(int n, float x[][n], float res[][n]){
    for (int i=0; i<n; i++){
        float temp_vec[n] ;
        arrcpy(n, temp_vec, x[i]) ;
        for (int j=0; j<i; j++){
            float proj_vec[n] ;
            proj(n, res[j], x[i], proj_vec) ;
            sub(n, temp_vec, proj_vec, temp_vec) ;
        }
        arrcpy(n, res[i], temp_vec) ;
    }
}

void prnt(int n, float res[][n]){
    for (int y=0; y<n; y++){
        for (int x=0; x<n; x++){
            printf(" %f | ",res[y][x]) ;
        }
    printf("\n") ;
    }
}

int main(){
    float v[][4] = {{4.0, 1.0, 3.0, -1.0}, {2.0, 1.0, -3.0, 4.0}, {1.0, 0.0, -2.0, 7.0}, {6.0, 2.0, 9.0, -5.0}} ; // Test 2 dimensional array 
    int ln = len(v) ;
    float res[4][4] ;
    gram_schmidt(ln, v, res) ;
    prnt(ln, res) ;
    return 0 ;
}
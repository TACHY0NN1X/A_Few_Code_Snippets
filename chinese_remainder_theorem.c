/*
 Translated from the python in this repo
*/

#include <stdio.h>
#include <stdlib.h>
#define len(x) sizeof(x)/sizeof(*x)

typedef struct {
    int gcd ;
    int x ;
    int y ;
} ext ;

ext egcd(int a, int b);

int modinv(int a, int n);

int prod(int a[], int len);

int crt(int a[], int n[], int len);

int main(){
    /* a & n must be arrays and thier
    lengths must be equal. we are trying to find 
    x ≡ a1 | mod(n1) we are trying to find
    x ≡ a2 | mod(n2) "x" such that it satisfies
    x ≡ a3 | mod(n3) the equations */
    
    int a[] = { 3, 1, 6} ;
    int n[] = { 5, 7, 8} ;
    int ln = len(a) ;
    int result = crt(a, n, ln);
    printf("[+] x  : %d \n----------------------\n", result);
    return 0;
    }
    
ext egcd(int a,int b){
    ext val ;
    ext rev ;
    if (a == 0) {
        val.gcd = b ;
        val.x = 0 ;
        val.y = 1 ;
        return val ;
        }
    else {
        int q = b % a ;
        rev = egcd(q, a) ;
        val.gcd = rev.gcd ;
        val.x = rev.y - ((b/a)*rev.x) ;
        val.y = rev.x ;
        return val;
        }
}

int modinv(int a, int n) {
    ext res = egcd(a, n);
    if (res.gcd != 1) {
        printf("[+] Modular Inverse does not exist !") ;
        exit(1);
        }
    else {
        int result ;
        int q ;
        q = res.x ;
        result = q % n ;
        return result ;
        }
}

int prod(int arr[], int len) {
    int result = 1;
    for (int i = 0; i < len; i++){
    result = result * arr[i];
    }
    return result;
}

int crt(int a[], int n[], int len){
    int sum = 0 ;
    int N = prod(n, len) ;
    for (int i = 0; i < len; i++){
        int ai = a[i] ;
        int ni = n[i] ;
        int Ni = N/ni ;
        int xi = modinv(Ni, ni) ;
        sum += ai*Ni*xi ;
        }
    int res = sum % N ;
    return res ;
}
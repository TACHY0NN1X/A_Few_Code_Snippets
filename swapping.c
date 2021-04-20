#include <stdio.h>

/* A simple version of swapping
 * 1 dimensional two arrays of 
 * same length
 * 
 * No Warranty, Use at your own risk
 * I won't be held responsible for any 
 * damage
 */

//Typedefed arrays can also be swapped
void swap(int *a, int *b, int n){
   int tmp; //Only change type of tmp for any other type
   int hlf, nj;
   hlf = n/2;
   int hlf1 = hlf-1;
   int nm1 = n-1;
   
   for (int j=0; j<=hlf; j++){
      tmp      = *(b + j);
      *(b + j) = *(a + j);
      *(a + j) = tmp;
      
      nj = nm1-j;
      tmp       = *(b + nj);
      *(b + nj) = *(a + nj);
      *(a + nj) = tmp;
   }
   
   if (n%2 == 0){
      tmp         = *(b + hlf1);
      *(b + hlf1) = *(a + hlf1);
      *(a + hlf1) = tmp;
   }
   tmp        = *(b + hlf);
   *(b + hlf) = *(a + hlf);
   *(a + hlf) = tmp;
}

int main(){
   
   int a[] = {1,2,3,4,5,6,7,8,9,10,101};
   int b[] = {11,12,13,14,15,16,17,18,19,20,201};
   
   int n=11;
   puts("before swap");
   for (int i=0; i<n; i++){
      printf(" a : %d \t\t b : %d \n", a[i], b[i]);
   }
   
   swap(a,b,n);
   puts("----");
   puts("after swap");
   
   for (int i=0; i<n; i++){
      printf(" a : %d \t b : %d \n", a[i], b[i]);
   }
   
   return 0;
}
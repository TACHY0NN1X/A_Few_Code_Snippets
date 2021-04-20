/**********************************************************
 * Turing patterns [Reaction-diffusion](Gray Scott Model) *
 **********************************************************/

/* The following lines of code generates 49 images
 * in a folder called gen in the current directory,
 * then using a simple python script you can generate
 * a gif.
 * 
 * No Warranty, Use at your own risk
 * I won't be held responsible for any 
 * damage.
 */
 
 /*****************************************
  * Compilation : gcc -o rdfn rdfn.c -lm  *
  *****************************************/

//Standard Includes
#include <stdio.h>
#include <math.h>

//Includes for Image Operation
#define STB_IMAGE_IMPLEMENTATION
#include <stb/stb_image.h>
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include <stb/stb_image_write.h>

//Typedefed structs for simplying stuff
typedef struct {
   uint8_t r,g,b;
} RGB;

typedef struct {
   double a,b;
} chem;

//Dimensions
#define height 256
#define width  256
#define channels 3

chem grid[width*height];
chem next[width*height];

chem init = {1,0};

//Constants
double dA = 1.0;
double dB = 0.5;
double feed = 0.0545;
double k    = 0.062;

double dt = 1.0;

//Helper functions
int idx();
void swap();
double cond();
int coni();
double laplaceA();
double laplaceB();

int main(){
   
   int dimensions = width*height;
   
   puts("Started ...\t\t>");
   //Setting dish
   for (int i=0; i<dimensions; i++){
      grid[i] = init;
   }
   
   puts("Putting Chemical B \t->");
   //Putting Chemicals
   
   int w1,w2,h1,h2;
   w1 = width/2 - 64;
   w2 = width/2 + 64;
   h1 = height/2 - 64;
   h2 = height/2 + 64;
   
   for (int i=w1; i<w2; i++){
      for (int j=h1; j<h2; j++){
         grid[idx(i,j)].b = 1.0;
      }
   }
   
   puts("Computing Image \t-->");
   
   int max_iterations = 4800;
   int iterations = 0;
   float percent = 0.0;
   
   int image = 0;
   char filename[32];
   
   
   while (iterations <= max_iterations){
      
      for (int x=1; x<(width-1); x++){
         for (int y=1; y<(height-1); y++){
            
            double a = grid[idx(x,y)].a;
            double b = grid[idx(x,y)].b;
            double tp = a*b*b;
            
            next[idx(x,y)].a = a + (dA * laplaceA(x,y) - tp + feed*(1.0-a))*dt;
            next[idx(x,y)].b = b + (dB * laplaceB(x,y) + tp - (k+feed)*b) * dt;
            
            next[idx(x,y)].a = cond(next[idx(x,y)].a, 0.0, 1.0);
            next[idx(x,y)].b = cond(next[idx(x,y)].b, 0.0, 1.0);
            
         }
      }
            
      //Multiple file saving  
      if (iterations % 100 == 0){
         
         RGB px;
         RGB frame[dimensions];
         for (int x=0; x<width; x++){
            for (int y=0; y<height; y++){
         
               double a = grid[idx(x,y)].a;
               double b = grid[idx(x,y)].b;
         
               int c = round((a-b)*255);
               c = coni(c,0,255);
         
               px.r = (c - 128) % 256;
               px.g = (c + 255) % 256;
               px.b = (c + 128) % 256;
         
               frame[ idx(x,y) ] = px;
         
            }
         }
         
         snprintf(filename,32,"gen/t_%d.png",image++);
         stbi_write_png(filename,
                  width, height, channels,
                  frame, width*channels);
   
      }
            
      swap(grid, next, dimensions);
      
      percent = (iterations * 100)/max_iterations;
      printf("\r Status : %3.2f image : %d ",percent,image);
      
      iterations++;
   }
   
   puts("Done.");
   
   return 0;
}

int idx(int x, int y){
   return x + y*width;
}

void swap(chem *a, chem *b, int n){
   chem tmp;
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

double cond(double m, double u, double k){
   if (m<u){ return u;}
   else if (m>k){ return k;}
   return m;
}

int coni(int m, int u, int k){
   if (m<u){ return u;}
   else if (m>k){ return k;}
   return m;
}


double laplaceA(int x, int y){
   
   double sum = 0.0;
   //center
   sum += grid[idx(x,y)].a*-1.0;
   
   //diagnals
   sum += grid[idx(x+1,y+1)].a*0.05;
   sum += grid[idx(x+1,y-1)].a*0.05;
   sum += grid[idx(x-1,y-1)].a*0.05;
   sum += grid[idx(x-1,y+1)].a*0.05;
   
   //adjacent
   sum += grid[idx(x,y+1)].a*0.2;
   sum += grid[idx(x,y-1)].a*0.2;
   sum += grid[idx(x-1,y)].a*0.2;
   sum += grid[idx(x+1,y)].a*0.2;
   
   return sum;
}

double laplaceB(int x, int y){
   
   double sum = 0.0;
   //center
   sum += grid[idx(x,y)].b*-1.0;
   
   //diagnal
   sum += grid[idx(x+1,y+1)].b*0.05;
   sum += grid[idx(x+1,y-1)].b*0.05;
   sum += grid[idx(x-1,y-1)].b*0.05;
   sum += grid[idx(x-1,y+1)].b*0.05;
   
   //adjacent
   sum += grid[idx(x,y+1)].b*0.2;
   sum += grid[idx(x,y-1)].b*0.2;
   sum += grid[idx(x-1,y)].b*0.2;
   sum += grid[idx(x+1,y)].b*0.2;
   
   return sum;
}

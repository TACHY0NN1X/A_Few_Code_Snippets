// Magic number 
// i = 0x1fbd1df5 + (i >> 1);
// Inspirations :
// https://en.m.wikipedia.org/wiki/Fast_inverse_square_root
// http://h14s.p5r.org/2012/09/0x5f3759df.html
// Awesome article 
// Loved it !

#include <stdio.h>
#include <stdlib.h>

float Sqrt( float number ){

    float x2, y;
    long i;
    const float threehalfs = 1.5F;
    const float half = 0.5F;

    x2 = half * number;
    y  = number;

    i  = * ( long * ) &y;
    i  = 0x1fbd1df5 + (i >> 1);

    y  = * ( float * ) &i;

    // Newton - Raphson Iteration for a bit more accuracy
    // For higher speed and enough accuracy reduce the number of iterations to 2
    for ( int iter = 0; iter < 5; iter++ ){
        y  = half * ( y + ( number / y ) );
    }

    return y;
}

int main( int argc, char **argv ){

    if ( argc < 2 || 2 < argc ){
        printf( " Usage : %s <float_number> \n", argv[0] );
        printf( " Calculates sqrt of given float \n" );
        exit(1);
    }

    // For command line use
    float number = atof( argv[1] );
    
    // Normal input based
    //float number;
    //scanf("%f",&number);
    printf( " Input : %9.6f \n", number );

    float result = Sqrt( number );
    printf( " %9.6f \n", result );

    return 0;
}
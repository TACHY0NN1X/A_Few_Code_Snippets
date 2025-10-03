/*
 Just translated from a python
 script, if there are issues in this
 please inform me and i'm a NOOB
 please consider that
*/


#include <iostream>
#include <vector>

using namespace std ;

typedef long double ld ;

typedef vector<vector<ld>> vect2d ;

typedef vector<ld> vect1d ;

void print1d(vect1d v){
    for (auto &x : v){
        cout << x << "  " ;
    }cout << endl ;
}

void print2d(vect2d matrix){
    for (auto &row : matrix){
        for (auto &x : row){
            cout << x << "  " ;
        }
        cout << endl ;
    }
}

ld amp(vect1d v){
    ld sum = 0 ;
    for (int i=0; i<v.size(); i++){
        sum += v[i] * v[i] ;
    }
    return sum ;
}

void equate_len(vect1d &v1, vect1d &v2){
    int sub ;
    if (v1.size() > v2.size()){
        sub = v1.size() - v2.size() ;
        for (int i=0; i<sub; i++){
            v2.push_back(0) ;
        }
    }else{
        sub = v2.size() - v1.size() ;
        for (int i=0; i<sub; i++){
            v1.push_back(0) ;
        }
    }
}

ld dot(vect1d v1, vect1d v2){
    if (v1.size() != v2.size()){
        equate_len(v1,v2) ;
    }

    ld sum = 0 ;
    for (int i=0; i<v1.size(); i++){
        sum += v1[i] * v2[i] ;
    }

    return sum ;
}

ld gs_coff(vect1d v1, vect1d v2){
    ld nm = dot(v1,v2) ;
    ld dm = amp(v1) ;

    ld result = nm / dm ;

    return result ;
}

vect1d mult(ld num, vect1d v){
    vect1d result ;
    for (auto & element : v){
        result.push_back(element * num) ;
    }
    return result ;
}

vect1d proj(vect1d v1, vect1d v2){
    ld m = gs_coff(v1,v2) ;
    vect1d result = mult(m, v1) ;
    return result ;
}

vect1d sub(vect1d v1, vect1d v2){
    if (v1.size() != v2.size()){
        equate_len(v1,v2) ;
    }

    //vect1d res ;
    for (int i=0; i<v1.size();i++){
        v1[i] = (v1[i] - v2[i]) ;
    }
    return v1 ;
}

vect2d gram_schmidt(vect2d X){

    vect2d U ;
    for (auto &x : X){
        vect1d temp_vec = x ;
        for (auto &inu : U){
            vect1d proj_vec = proj(inu, x) ;
            temp_vec = sub(temp_vec, proj_vec);
        }
        U.push_back(temp_vec) ;
    }

    return U ;
}

int main(){
    vect2d mat {{4.0, 1.0, 3.0, -1.0}, 
                {2.0, 1.0, -3.0, 4.0}, 
                {1.0, 0.0, -2.0, 7.0}, 
                {6.0, 2.0, 9.0, -5.0}};

    //print2d(mat) ;

    vect2d result = gram_schmidt(mat) ;
    print2d(result) ;
    
    
    return 0 ;
}
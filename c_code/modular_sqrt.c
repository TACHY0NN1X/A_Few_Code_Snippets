/*
 Translated into C from 
 https://rosettacode.org/wiki/Tonelli-Shanks_algorithm#Python
*/

#include <stdio.h>
#include <stdlib.h>
#define ll long long

typedef struct {
    ll rt1 ;
    ll rt2 ;
} roots ;

ll modpow(ll base, ll exp, ll mod){
    ll res = 1 ;
    while (exp > 0){
        if (exp % 2 == 1){
            res = (res*base) % mod ;
        }
        exp = exp >> 1 ;
        base = (base*base) % mod ;
    }
    return res ;
}

ll legendre(ll a, ll p){
    ll m = (p - 1)/2 ;
    ll res = modpow(a, m, p) ;
    return res ;
}

roots tonelli(ll n, ll p){
    roots result ;
    ll cmp = legendre(n, p) ;
    if (cmp != 1){
        printf(" Not a square (mod p) , square root doesn't exist \n") ;
        exit(1) ;
    }
    ll q = p - 1 ;
    ll s = 0 ;
    while (q % 2 == 0){
        q /= 2 ;
        s += 1 ;
    }
    if (s == 1){
        ll mi = (p + 1)/4 ;
        ll res = modpow(n, mi, p) ;
        result.rt1 = res ;
        result.rt2 = p - res ;
        return result ;
    }
    int z = 2 ;
    for (; z < p ; z++){
        if ((p - 1) == legendre(z, p)){
            break ;
        }
    }
    ll c = modpow(z, p, q) ;
    ll r = modpow(n, ((q + 1)/2), p) ;
    ll t = modpow(n, q, p) ;
    ll m = s ;
    ll t2 = 0 ;
    while ((t - 1) % p != 0){
        t2 = (t * t) % p ;
        int i = 1 ;
        for (; i<m; i++){
            if ((t2 - 1) % p == 0){
                break ;
            }
            t2 = (t2 * t2) % p ;
        }
        ll b = modpow(c, 1 << (m - i - 1), p) ;
        r = (r * b) % p ;
        c = (b * b) % p ;
        t = (t * c) % p ;
        m = i ;
        }
    result.rt1 = r ;
    result.rt2 = (p - r) ;
    return result ;
}

void usage(char *program){
    printf(" Usage : %s [n] [p] \n", program) ;
    printf(" Where [n] and [p] are \n"
           " x^2 ≡ n (mod p) , this \n"
           " returns (x) that satisfies \n"
           " the above equation \n") ;
}

int main(int argc, char **argv){
    if ((argc < 3) || (argc > 3)){
        usage(argv[0]) ;
        return 0 ;
    }
    ll n = atoll(argv[1]) ;
    ll p = atoll(argv[2]) ;
    roots found = tonelli(n, p) ;
    ll root1 = found.rt1 ;
    ll root2 = found.rt2 ;
    printf(" 1st Root : %lld \n", root1) ;
    printf(" 2nd Root : %lld \n", root2) ;
    return 0 ;
}
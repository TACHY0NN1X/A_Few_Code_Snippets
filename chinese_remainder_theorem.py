# Implemented from this video
# https://youtu.be/Y5RcMWiUyyE
# Awesome video


from math import prod
from ast import literal_eval as le
import sys

def egcd(a,b):
    if a == 0 :
        return b, 0, 1
    else :
        gcd, x, y = egcd( b%a , a )
        nx = y - (b//a)*x
        ny = x
        return ( gcd, nx, ny )
        
def modinv(a,p):
    gcd, x, y = egcd(a,p)
    if gcd != 1 :
        raise Exception('Modular inverse doesn\'t exist !!')
    else:
        return x%p
        
def crt(a,n):
    '''a & n must be arrays (list) and thier
    lengths must be equal. we are trying to find 
    x ≡ a1 | mod(n1) we are trying to find
    x ≡ a2 | mod(n2) "x" such that it satisfies
    x ≡ a3 | mod(n3) the equations '''
    N = prod(n)
    sum = 0
    for i in range(len(a)):
        ai = a[i]
        ni = n[i]
        Ni = N / ni
        xi = modinv(Ni,ni)
        sum += ai*Ni*xi
    res = sum % N
    return res
    
if __name__ == '__main__' :
    a = le(sys.argv[1])
    n = le(sys.argv[2])
    print(crt(a,n))
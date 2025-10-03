"""This is python implementation 
of gram schmidt process without 
numpy library , pure pythonic way"""


def amp(q):
    re = sum([x*x for x in q])
    return re

def dot(a,b):
    res = sum([i*j for (i,j) in zip(a,b)])
    return res

def gs_coff(v1, v2):
    a = dot(v2,v1)
    b = amp(v1)
    rel = a/b
    return rel

def mult(cofficient, v):
    return list(map((lambda x : x * cofficient), v))

def proj(v1, v2):
    return mult(gs_coff(v1, v2) , v1)

def gs(X):
    u = []
    for i in range(len(X)):
        temp_vec = X[i]
        for inu in u :
            proj_vec = proj(inu, X[i])
            temp_vec = list(map(lambda x, y : x - y, temp_vec, proj_vec))
        u.append(temp_vec)
    return u

"""This an example vector array for testing purposes"""

v = [[4,2,5, -1],[2,7, -3,6],[2,0, -2,9],[6,2,9, -5]]

ans = gs(v)

for x in ans:
    print("--"*5)
    print(x)    
print("--"*5)
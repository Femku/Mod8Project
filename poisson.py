import math
def poisson(l1,l2,l3,max):
    p= 1-(math.exp(-l1-l2-l3)*sum(((l1+l2+l3)**x)/math.factorial(x) for x in range(0,max)))
    return p

print(poisson(12,2,58,50))

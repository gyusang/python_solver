from cube import *
def fit(state):
    score = 0
    for i in range(12):
        for j in state[i]:
            if j != i:
                score += 1
    return score

import pylab as pl
def f(n):
    r = []
    for i in range(100):
        r.append(fit(mix(n)))
    return pl.average(r),min(r),max(r)

X = range(120)
Y = pl.array([f(x) for x in X])
pl.plot(X,Y[:,0],'g.')
pl.plot(X,Y[:,1],'r-')
pl.plot(X,Y[:,2],'r-')
print("max : %d, avg : %d"%(max(Y[:,2]),pl.average(Y[-40:][:,0])))
pl.show()

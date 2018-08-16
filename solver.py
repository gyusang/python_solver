from cube import *
def fit(state):
    score = 0
    for i in range(12):
        for j in state[i]:
            if j != i:
                score += 1
    return score

# import pylab as pl
# def f(n):
#     r = []
#     for i in range(100):
#         r.append(fit(mix(n)))
#     return pl.average(r),min(r),max(r)
#
# X = range(120)
# Y = pl.array([f(x) for x in X])
# pl.plot(X,Y[:,0],'g.')
# pl.plot(X,Y[:,1],'r-')
# pl.plot(X,Y[:,2],'r-')
# print("max : %d, avg : %d"%(max(Y[:,2]),pl.average(Y[-40:][:,0])))
# pl.show()

def SA(state, k=0.7, T=5000, N=10000, a=0.05):
    moves = []
    logs = []
    temp = T
    f = fit(state)
    def evaluate(delta):
        if delta<=0 : return True
        elif random()<2**(delta/(k*temp)) : return True
        else: return False
    while f>0 and temp>1:
        b = 0
        next = None
        nextf = None
        for i in range(N):
            c = newint(b)
            next = turn(state,c)
            nextf = fit(next)
            if evaluate(nextf-f):
                state = next
                f = nextf
                b = c
                moves.append(c)
        temp *= 1-a;
        print("temp:%f, fit:%d"%(temp,f))
        logs.append((temp,f))
    return logs, state

if __name__=='__main__':
    rtn = SA(mix(),k=0.7, T=100, N=10000, a=0.005)
    import pylab as pl
    graph = pl.array(rtn[0])
    pl.plot(graph[:,0],graph[:,1],'g.')
    pl.show()

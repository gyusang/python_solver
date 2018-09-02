from cube2 import *
from random import random, randint
def fit(state):
    score = 0
    for i in [0,1,2,3,4]:
        for j in range(item_num[i]):
            if i%2 or j%2: # edge condition
                if state[i][j][0] == (i,j): # correct position
                    if state[i][j][1]:
                        score += 4
                else: # not correct position
                    score += 3
            else: # corner condition
                if state[i][j][0] == (i,j): # correct position not correct rotation
                    if state[i][j][1]:
                        score += 2
                else:
                    score += 1
    return score


def SA(state, k=1.0, T=5000, N=10000, a=0.05):
    moves = []
    logs = []
    temp = T
    f = fit(state)
    def evaluate(delta):
        if delta<=0 : return True
        elif random()<2**(-delta/(k*temp)) : return True
        else: return False
    while f>0 and temp>1:
        b, minimum, maximum = 0,f,f
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
                minimum = min(minimum,f)
                maximum = max(maximum,f)
                moves.append(c)
        temp *= 1-a;
        print("temp:%f, fit:%d"%(temp,f))
        logs.append((temp,f,minimum,maximum))
    return logs, state

def GA(state, K=170, N=100, a = 0.8, b = 0.2, e = 0.1):
    if N<=1 :
        print("N should be bigger than 1")
        return
    genes = []
    for i in range(N):
        turns = [0]
        for j in range(K):
            turns.append(newint(turns[-1]))
        turns.pop(0)
        genes.append(turns)
    def turn_fit(no):
        tmp = deepcopy(state)
        return fit(turn(tmp,no))
    def new_pair():
        m = newint(0,N)
        f = newint(0,N)
        while m==f:
            f = newint(0,N)
        return list(genes[m]),list(genes[f])
    genes.sort(key=turn_fit)
    generation = 0
    try:
        while turn_fit(genes[0]) > 0 :
            pool = []
            while len(pool) <= N*(1-e): #crossover
                pair = new_pair()
                initial_fit = turn_fit(pair[0]),turn_fit(pair[1])
                if random()<a:
                    location = randint(1,N-1)
                    pair = [ pair[0][:location] + pair[1][location:], pair[1][location:] + pair[0][:location]]
                for i in range(2):
                    if turn_fit(pair[i]) <= initial_fit[i]:
                        pool.append(pair[i])
            for x in pool: # mutation
                if random()<b:
                    c = randint(0,K-1)
                    if c==0:
                        x[c] = newint(x[c+1])
                    elif c == K-1:
                        x[c] = newint(x[c-1])
                    else:
                        x[c] = newint(x[c-1],x[c+1])
            for i in range(int(N*e)): # elitism
                pool.append(genes[i])
            genes = pool
            genes.sort(key=turn_fit)
            generation += 1
            print("At generation %d, fit = %d"%(generation,turn_fit(genes[0])))
    except:
        print("Exception Ocurred")
    finally:
        return turn_fit(genes[0]),genes[0]


if __name__=='__main__':
    # rtn = SA(mix(),k=0.07, T=30, N=10000, a=0.005)
    # import pylab as pl
    # graph = pl.array(rtn[0])
    # pl.plot(graph[:,0],graph[:,2],'r.')
    # pl.plot(graph[:,0],graph[:,3],'r.')
    # pl.plot(graph[:,0],graph[:,1],'g.')
    # pl.legend(['min','max','last'])
    # pl.title('SA Results')
    # pl.xlabel('Temperature')
    # pl.ylabel('Fitness')
    # pl.show()

    # import pylab as pl
    # def f(n):
    #     r = []
    #     for i in rangMIe(100):
    #         r.append(fit(mix(n)))
    #     return pl.average(r),min(r),max(r)
    #
    # X = range(120)
    # Y = pl.array([f(x) for x in X])
    # pl.plot(X,Y[:,0],'g.')
    # pl.plot(X,Y[:,1],'r-')
    # pl.plot(X,Y[:,2],'r-')
    # pl.title("섞는 횟수에 따른 fitness")
    # pl.xlabel("섞는 횟수")
    # pl.ylabel("Fitness")
    # pl.legend(["평균","최대","최소"])
    # print("max : %d, avg : %d"%(max(Y[:,2]),pl.average(Y[-40:][:,0])))
    # pl.show()
    print(GA(mix()))

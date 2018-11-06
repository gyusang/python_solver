from cube2 import *
from random import random, randint
from threading import Event
import numpy as np

with open('Corners.npy','rb') as f:
    Corners = np.load(f)
Corners = [tuple(b) for b in Corners]
with open('Edges.npy','rb') as f:
    Edges = np.load(f)
Edges = [tuple(b) for b in Edges]
with open('dist_e.npy','rb') as f:
    dist_edge = np.load(f)
with open('dist_c.npy','rb') as f:
    dist_corner = np.load(f)
with open('dist_e_2.npy','rb') as f:
    dist_edge_2 = np.load(f)
with open('dist_c_2.npy','rb') as f:
    dist_corner_2 = np.load(f)

with open('blockinfo.txt', 'r') as file:
    block_info = json.load(file)
block_info = [[[tuple(k) for k in j] for j in i] for i in block_info]

halt = Event()


def fit0(state):
    score = 0
    for i in range(12):
        for j in range(10):
            if state[i][j] != i:
                score += 1
    return score


def fit1(state):
    score = 0
    for i in [0, 1, 2, 3, 4]:
        for j in range(item_num[i]):
            m = 2 if (i % 2 or j % 2) else 3
            for k in range(m):

                loc = block_info[i][j][k]
                blk = state[i][j]
                if block_info[blk[0][0]][blk[0][1]][(k - blk[1] + m) % m][0] != loc[0]:
                    score += 1
    return score


def fit2(state, setting = (4,3,2,1)):
    score = 0
    for i in [0, 1, 2, 3, 4]:
        for j in range(item_num[i]):
            if i % 2 or j % 2:  # edge condition
                if state[i][j][0] == (i, j):  # correct position
                    if state[i][j][1]:
                        score += setting[0]
                else:  # not correct position
                    score += setting[1]
            else:  # corner condition
                if state[i][j][0] == (i, j):  # correct position not correct rotation
                    if state[i][j][1]:
                        score += setting[2]
                else:
                    score += setting[3]
    return score


def fit3(state):
    score = 0
    for i in [0, 1, 2, 3, 4]:
        for j in range(item_num[i]):
            if i % 2 or j % 2:  # edge condition
                if state[i][j][0] == (i, j):  # correct position
                    if state[i][j][1]:
                        score += 0
                else:  # not correct position
                    score += 2
            else:  # corner condition
                if state[i][j][0] == (i, j):  # correct position not correct rotation
                    if state[i][j][1]:
                        score += 0
                else:
                    score += 1
    return score


def fit4(state):
    score = 0
    for i in [0,1,2,3,4]:
        for j in range(item_num[i]):
            if i % 2 or j % 2:
                score += dist_edge[Edges.index(state[i][j][0]),Edges.index((i,j))]
            else:
                score += dist_corner[Corners.index(state[i][j][0]), Corners.index((i, j))]
    return score


def fit5(state):
    score = 0
    for i in [0, 1, 2, 3, 4]:
        for j in range(item_num[i]):
            if i % 2 or j % 2:
                score += dist_edge_2[Edges.index((i, j)), Edges.index(state[i][j][0]), state[i][j][1] - 0]
            else:
                score += dist_corner_2[Corners.index((i, j)), Corners.index(state[i][j][0]), state[i][j][1] - 0]
    return score


fit = fit1


def SA(state, k=1.0, T=5000, N=10000, a=0.05):
    moves = []
    logs = []
    temp = T
    f = fit(state)

    def evaluate(delta):
        if delta <= 0:
            return True
        elif random() < 2 ** (-delta / (k * temp)):
            return True
        else:
            return False

    while f > 0 and temp > 1:
        b, minimum, maximum = 0, f, f
        next = None
        nextf = None
        for i in range(N):
            c = newint(b)
            next = turn(state, c)
            nextf = fit(next)
            if evaluate(nextf - f):
                state = next
                f = nextf
                b = c
                minimum = min(minimum, f)
                maximum = max(maximum, f)
                moves.append(c)
        temp *= 1 - a;
        print("temp:%f, fit:%d" % (temp, f))
        logs.append((temp, f, minimum, maximum))
    return logs, state


def GA(state, K=170, N=100, a=0.8, b=0.2, e=0.1):
    if N <= 1:
        print("N should be bigger than 1")
        return
    genes = []
    min_fits = []
    max_fits = []
    for i in range(N):
        turns = [0]
        for j in range(K):
            turns.append(newint(turns[-1]))
        turns.pop(0)
        genes.append(turns)

    def turn_fit(no):
        tmp = deepcopy(state)
        return fit(turn(tmp, no))

    def new_pair():
        m = randint(0, N-1)
        f = randint(0, N-1)
        while m == f:
            f = randint(0, N-1)
        return list(genes[m]), list(genes[f])

    genes.sort(key=turn_fit)
    generation = 0
    try:
        while turn_fit(genes[0]) > 0 and not halt.is_set():
            pool = []
            while len(pool) <= N * (1 - e):  # crossover
                pair = new_pair()
                initial_fit = turn_fit(pair[0]), turn_fit(pair[1])
                if random() < a:
                    location = randint(1, N - 1)
                    pair = [pair[0][:location] + pair[1][location:], pair[1][location:] + pair[0][:location]]
                for i in range(2):
                    if turn_fit(pair[i]) <= initial_fit[i]:
                        pool.append(pair[i])
            for x in pool:  # mutation
                if random() < b:
                    c = randint(0, K - 1)
                    if c == 0:
                        x[c] = newint(x[c + 1])
                    elif c == K - 1:
                        x[c] = newint(x[c - 1])
                    else:
                        x[c] = newint(x[c - 1], x[c + 1])
            while len(pool) < N:  # elitism
                pool.append(genes.pop(0))
            genes = pool
            genes.sort(key=turn_fit)
            generation += 1
            min_fits.append(turn_fit(genes[0]))
            max_fits.append(turn_fit(genes[-1]))
            print("At generation %d, among %d genes, fit =( %d, %d)" % (generation, N, min_fits[-1], max_fits[-1]))
    except Exception as e:
        print("Exception Occured: "+str(e))
    finally:
        return turn_fit(genes[0]), genes[0], min_fits, max_fits


sample_mix = []
# print(sample_mix)
with open('sample_mix.txt','r') as f:
    sample_mix = json.load(f)
sample_mix = sample_mix[:1]
sample_2 = [x[:50] for x in sample_mix]
# print(sample_mix)
def eval_fit(func_fit, normed=True):
    if normed:
        r = []
        for smp in sample_mix:
            A = deepcopy(solved)
            for x in smp:
                turn(A, x)
                r.append(func_fit(A))
        norm = max(r)
    else:
        norm = 1
    tries = []
    for sample in sample_2:
        A = deepcopy(solved)
        # turn(A, sample_mix)
        fits = [func_fit(A)/norm]
        for x in sample:
            turn(A, x)
            fits.append(func_fit(A)/norm)
        # pl.plot(range(len(fits)), fits, '-')
        tries.append(sum(fits))
    return pl.average(tries)


def eval_GA(K=100, a=0.8, b=0.2, e=0.1):
    if K <= 1:
        print("K should be bigger than 1")
        return
    genes = []
    min_fits = []
    max_fits = []
    for i in range(K):
        setting = []
        for j in range(4):
            setting.append(random())
        genes.append(tuple(setting))

    def set_fit(setting):
        return eval_fit(lambda x:fit2(x,setting))

    def new_pair():
        m = randint(0, K-1)
        f = randint(0, K-1)
        while m == f:
            f = randint(0, K-1)
        return list(genes[m]), list(genes[f])

    genes.sort(key=set_fit)
    generation = 0
    try:
        while set_fit(genes[0]) > 40 and not halt.is_set():
            pool = []
            while len(pool) <= K * (1 - e):  # crossover
                pair = new_pair()
                initial_fit = set_fit(pair[0]), set_fit(pair[1])
                if random() < a:
                    location = randint(0, 3)
                    pair = [pair[0][:location] + pair[1][location:], pair[1][location:] + pair[0][:location]]
                for i in range(2):
                    if set_fit(pair[i]) <= initial_fit[i]:
                        pool.append(pair[i])
            for x in pool:  # mutation
                if random() < b:
                    c = randint(0, 3)
                    x[c] = random()
            while len(pool) < K:  # elitism
                print('elitet')
                pool.append(genes.pop(0))
            genes = pool
            genes.sort(key=set_fit)
            generation += 1
            min_fits.append(set_fit(genes[0]))
            max_fits.append(set_fit(genes[-1]))
            print("At generation %d, among %d genes, fit =( %.2f, %.2f)" % (generation, K, min_fits[-1], max_fits[-1]))
    except Exception as e:
        print("Exception Occured")
        print(e)
    finally:
        return set_fit(genes[0]), genes[:min(20,K)], min_fits, max_fits


if __name__ == '__main__':
    # NOTE SA algorithm

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

    # NOTE 섞는 횟수에 따른 fitness 변화

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
    # pl.title("섞는 횟수에 따른 fitness")
    # pl.xlabel("섞는 횟수")
    # pl.ylabel("Fitness")
    # pl.legend(["평균","최대","최소"])
    # print("max : %d, avg : %d"%(max(Y[:,2]),pl.average(Y[-40:][:,0])))
    # pl.show()

    # NOTE 섞는 과정에서 fitness 변화

    import pylab as pl


    def f(n):
        global r
        A = deepcopy(solved)
        return fit(turn(A, r[:n]))


    r = mix_seq(100)
    fit = fit4
    X = range(101)
    Y = pl.array([f(x) for x in X])
    pl.plot(X, Y, '-', color='C0')
    fit = fit1
    Y = pl.array([f(x) for x in X])
    pl.plot(X, Y, '-', color='C1')
    fit = fit5
    Y = pl.array([f(x) for x in X])
    pl.plot(X, Y, '-', color='C2')
    pl.legend(['fit4', 'fit1', 'fit5'])
    pl.xlabel('움직임 횟수')
    pl.ylabel('Fitness')
    # import pylab as pl
    print("fit1 : %.2f"%eval_fit(fit1, True))
    print("fit4 : %.2f"%eval_fit(fit4, True))
    print("fit5 : %.2f"%eval_fit(fit5, True))
    pl.show()

    # # print("%.2f"%eval_fit(fit1))
    # # print("%.2f"%eval_fit(lambda x: fit2(x, (4,3,2,1))))
    # # print("%.2f"%eval_fit(lambda x:fit2(x,(0,0,0,1)),normed=False))
    # tries = eval_fit(lambda x:fit2(x,(1,0,0,0)),normed=True)
    # pl.title('섞는 횟수에 따른 Fitness 변화')
    # pl.xlabel('섞는 횟수')
    # pl.subplot(221)
    # pl.title('first')
    # pl.xlabel('섞는 횟수')
    # pl.ylabel('Fitness')
    # tries = eval_fit(lambda x: fit2(x, (1, 0, 0, 0)), normed=True)
    # pl.plot(range(len(tries)),tries,'b.')
    # pl.subplot(222)
    # pl.title('second')
    # pl.xlabel('섞는 횟수')
    # pl.ylabel('Fitness')
    # tries = eval_fit(lambda x: fit2(x, (0, 1, 0, 0)), normed=True)
    # pl.plot(range(len(tries)), tries, 'b.')
    # pl.subplot(223)
    # pl.title('third')
    # pl.xlabel('섞는 횟수')
    # pl.ylabel('Fitness')
    # tries = eval_fit(lambda x: fit2(x, (0, 0, 1, 0)), normed=True)
    # pl.plot(range(len(tries)), tries, 'b.')
    # pl.subplot(224)
    # pl.xlabel('섞는 횟수')
    # pl.ylabel('Fitness')
    # pl.title('fourth')
    # tries = eval_fit(lambda x: fit2(x, (0, 0, 0, 1)), normed=True)
    # pl.plot(range(len(tries)), tries, 'b.')
    # pl.show()
    # # print("%.2f" % eval_fit(lambda x: fit2(x, (0,1,0,0))))
    # # print("%.2f" % eval_fit(lambda x: fit2(x, (0, 0, 1, 0))))
    # # print("%.2f" % eval_fit(lambda x: fit2(x, (0, 0, 0, 1))))
    # print(eval_fit(fit3))
    # pl.title('섞는 과정에서 fitness 변화')
    # pl.xlabel('섞는 과정 진행')
    # pl.ylabel('Fitness')
    # pl.legend(['거리함수 1', '거리함수 2', '거리함수 3'])
    # pl.show()
    # print(eval_GA(20, 0.8, 0.2, 0.1))

    # NOTE GA Algorithm

    # print(GA(mix(),K=110,N=355))

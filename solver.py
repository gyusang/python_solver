from cube2 import *
from random import random, randint
from threading import Event

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
    except:
        print("Exception Occured")
    finally:
        return turn_fit(genes[0]), genes[0], min_fits, max_fits


sample_mix = [mix_seq(80) for i in range(50)]
sample_2 = [mix_seq(50) for i in range(10)]
# print(sample_mix)


def eval_fit(func_fit):
    r = []
    for smp in sample_mix:
        A = deepcopy(solved)
        turn(A, smp)
        r.append(func_fit(A))
    norm = pl.average(r)
    tries = []
    for sample in sample_2:
        A = deepcopy(solved)
        # turn(A, sample_mix)
        fits = [func_fit(A)/norm]
        for x in sample:
            turn(A, x)
            fits.append(func_fit(A)/norm)
        tries.append(sum(fits))
    # pl.plot(range(len(fits)), fits, '-')
    # pl.show()
    return pl.average(tries)


def eval_GA(K=100, a=0.8, b=0.2, e=0.1):
    if K <= 1:
        print("N should be bigger than 1")
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

    # import pylab as pl
    #
    #
    # def f(n):
    #     global r
    #     A = deepcopy(solved)
    #     return fit(turn(A, r[:n]))
    #
    #
    # r = mix_seq(40)
    # fit = fit2
    # for i in range(2):
    #     X = range(41)
    #     Y = pl.array([f(x) for x in X])
    #     pl.plot(X, Y, '-', color='C' + str(i))
    #     fit = fit3
    # pl.legend(['fit2', 'fit3'])
    # pl.title('섞는 과정에서 fitness 변화')
    # pl.xlabel('움직임 횟수')
    # pl.ylabel('Fitness')
    # pl.show()
    import pylab as pl
    # print(eval_fit(fit1))
    # print(eval_fit(fit2))
    # print(eval_fit(fit3))
    # print(eval_GA(20, 0.8, 0.2, 0.1))

    # NOTE GA Algorithm

    # print(GA(mix(),K=110,N=355))

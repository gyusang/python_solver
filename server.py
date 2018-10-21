from threading import Timer
from solver import *

K = 200
N = 100


def timeout():
    global halt
    print("Timer Activated : Halting...")
    halt.set()


while N < 1000:
    t = Timer(10, timeout)
    seq = mix_seq()
    cube = deepcopy(solved)
    turn(cube, seq)
    print("K=%d, N=%d, mix=" % (K, N), seq)
    t.start()
    rtn = GA(cube, K=K, N=N)
    t.cancel()
    halt.clear()
    with open("N" + str(N) + "K" + str(K) + ".txt", "w") as file:
        json.dump([seq, rtn], file)
    N = N + 50
    print("Next test...")
    halt.wait(1)

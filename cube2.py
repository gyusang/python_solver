from random import randint
from copy import copy, deepcopy
import json

with open('perms2.txt', 'r') as file:
    perms = json.load(file)

perms = [[[[tuple(k) for k in j[0]], j[1]]for j in i] for i in perms]

def permute(src, p, reverse=False):
    if not reverse:
        x = p[0]
        block = x[0]
        delta = x[1]
        tmp = deepcopy(src[block[-1][0]][block[-1][1]])
        for i in [4, 3, 2, 1]:
            src[block[i][0]][block[i][1]][0] = src[block[i - 1][0]][block[i - 1][1]][0]
            src[block[i][0]][block[i][1]][1] = (src[block[i - 1][0]][block[i - 1][1]][1] + delta[i]) % 3
        src[block[0][0]][block[0][1]][0] = tmp[0]
        src[block[0][0]][block[0][1]][1] = (tmp[1] + delta[0]) % 3

        x = p[1]
        block = x[0]
        delta = x[1]
        tmp = deepcopy(src[block[-1][0]][block[-1][1]])
        for i in [4, 3, 2, 1]:
            src[block[i][0]][block[i][1]][0] = src[block[i - 1][0]][block[i - 1][1]][0]
            src[block[i][0]][block[i][1]][1] = (src[block[i - 1][0]][block[i - 1][1]][1] + delta[i]) % 2
        src[block[0][0]][block[0][1]][0] = tmp[0]
        src[block[0][0]][block[0][1]][1] = (tmp[1] + delta[0]) % 2
    else:
        x = p[0]
        block = x[0]
        delta = x[1]
        tmp = deepcopy(src[block[-1][0]][block[-1][1]])
        for i in [0, 1, 2, 3]:
            src[block[i - 1][0]][block[i - 1][1]][0] = src[block[i][0]][block[i][1]][0]
            src[block[i - 1][0]][block[i - 1][1]][1] = (src[block[i][0]][block[i][1]][1] - delta[i] + 3) % 3

        src[block[-2][0]][block[-2][1]][0] = tmp[0]
        src[block[-2][0]][block[-2][1]][1] = (tmp[1] - delta[-1] + 3) % 3

        x = p[1]
        block = x[0]
        delta = x[1]
        tmp = deepcopy(src[block[-1][0]][block[-1][1]])
        for i in [0, 1, 2, 3]:
            src[block[i - 1][0]][block[i - 1][1]][0] = src[block[i][0]][block[i][1]][0]
            src[block[i - 1][0]][block[i - 1][1]][1] = (src[block[i][0]][block[i][1]][1] - delta[i] + 2) % 2

        src[block[-2][0]][block[-2][1]][0] = tmp[0]
        src[block[-2][0]][block[-2][1]][1] = (tmp[1] - delta[-1] + 2) % 2


def permute_block(block, perm, reversed=False):
    block = tuple(block)
    for p in perm:
        if p[0].count(block) >= 1:
            i = p[0].index(block)
            if not reversed:
                return p[0][(i+1)%5]
            else:
                return p[0][i-1]


def turn(state, no):
    if not isinstance(no, int):
        for i in no:
            if i > 0:
                permute(state, perms[i - 1])
            elif i < 0:
                permute(state, perms[-i - 1], True)
    else:
        i = no
        if i > 0:
            permute(state, perms[i - 1])
        elif i < 0:
            permute(state, perms[-i - 1], True)
    return state


item_num = [10, 5, 20, 5, 10]
solved = [[[(i, j), 0] for j in range(item_num[i])] for i in range(5)]


def newint(b=0, c=0):
    while True:
        a = randint(-12, 12)
        if a == 0 or a == -b or a == -c:
            continue
        else:
            return a


def mix(n=50):
    turns = [0]
    for i in range(n):
        turns.append(newint(turns[-1]))
    turns.pop(0)
    # print("turns : ", turns)
    A = deepcopy(solved)
    return turn(A, turns)


def mix_seq(n=50):
    turns = [0]
    for i in range(n):
        turns.append(newint(turns[-1]))
    turns.pop(0)
    return turns

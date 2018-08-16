import json
from copy import copy,deepcopy
from random import randint, random


with open('perms.txt','r') as file:
	perms = json.load(file)

cw = tuple(tuple(tuple(j) for j in i) for i in perms[0])
ccw = tuple(tuple(tuple(j) for j in i) for i in perms[1])
del perms

def permute(src,perms):
	return [[src[i[0]][i[1]] for i in j] for j in perms]

def turn(state,no):
	cube = copy(state)
	if not isinstance(no,int):
		for i in no:
			if i>0:
				cube = permute(cube,cw[i-1])
			elif i<0:
				cube = permute(cube,ccw[-i-1])
	else:
		i=no
		if i>0:
			cube = permute(cube,cw[i-1])
		elif i<0:
			cube = permute(cube,ccw[-i-1])
	return cube

solved = tuple(tuple(i for x in range(10)) for i in range(12))

def newint(b=0):
    a = None
    while True:
        a = randint(-12,12)
        if a==0 or a==-b: continue
        else: return a

def mix(n=50):
	turns = [0]
	for i in range(n):
		turns.append(newint(turns[-1]))
	turns.pop(0)
	return turn(solved,turns)

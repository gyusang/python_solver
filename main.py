import json
from copy import copy, deepcopy
with open('perms.txt','r') as file:
	perms = json.load(file)

cw = tuple(tuple(tuple(j) for j in i) for i in perms[0])
ccw = tuple(tuple(tuple(j) for j in i) for i in perms[1])
del perms

def permute(src,perms):
	return [[src[i[0]][i[1]] for i in j] for j in perms]

def turn(state,no):
	cube = copy(state)
	if isinstance(no,tuple) or isinstance(no,list):
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
			cube = permute(cube,ccw[-i+1])
	return cube

solved = [[i for x in range(10)] for i in range(1,13)]

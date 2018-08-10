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

colors = (
	'#%02x%02x%02x' % (255,255,255), #White
	'#%02x%02x%02x' % (210,0,255), #Purple
	'#%02x%02x%02x' % (246,255,0), #DarkYellow
	'#%02x%02x%02x' % (6,0,255), #DarkBlue
	'#%02x%02x%02x' % (255,0,0), #Red
	'#%02x%02x%02x' % (0,255,6), #DarkGreen
	'#%02x%02x%02x' % (107,255,110), #LightGreen
	'#%02x%02x%02x' % (255,127,0), #Orange
	'#%02x%02x%02x' % (0,246,255), #LightBlue
	'#%02x%02x%02x' % (249,228,170), #LightYellow
	'#%02x%02x%02x' % (246,21,138), #Pink
	'#%02x%02x%02x' % (132,132,132), #Grey
)

with open('coords.txt','r') as file:
	coords = json.load(file)

frames = coords[0]
centers = coords[1]
blocks = coords[2]
center_coord = coords[3]
del coords

import tkinter as tk
master = tk.Tk()
w = tk.Canvas(master,width=1200,height=600)
w.pack()
w.create_rectangle(50,25,150,75)
print(centers)
tk.mainloop()

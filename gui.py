from copy import deepcopy
from cube2 import *

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
with open('blockinfo.txt','r') as file:
	block_info = json.load(file)
block_info = [[[tuple(k) for k in j] for j in i] for i in block_info]

frames =  [tuple(tuple(j) for j in i)for i in coords[0]]
centers = [tuple(tuple(j) for j in i)for i in coords[1]]
blocks = [[tuple(tuple(k) for k in j) for j in i]for i in coords[2]]
center_coord = tuple(coords[3])
del coords

import tkinter as tk
master = tk.Tk()
master.title("Megaminx")
w = tk.Canvas(master,width=1200,height=600)
w.pack()
cpoly = [] # Center Polygon
fpoly = [] # Frame Outline Polygon
bfpoly = [[] for i in range(12)] # Block Fill Polygon
bopoly = [[] for i in range(12)] # Block Outline Polygon
for i in range(12):
	cpoly.append(w.create_polygon(centers[i],fill=colors[i]))
	for j in range(10):
		bfpoly[i].append(w.create_polygon(blocks[i][j],fill=colors[i]))

for i in range(12):
	for j in range(10):
		bopoly[i].append(w.create_polygon(blocks[i][j],fill='',outline='black',width=2.0))

for i in range(12):
	fpoly.append(w.create_polygon(frames[i],fill='',outline='black',width=3.0))
	w.create_text(center_coord[i],text=str(i+1))

del frames, centers, blocks

l = [10,5,20,5,10]
def update(cube):
	for i in range(5):
		for j in range(l[i]):
			if i%2 or j%2: m=2
			else: m=3
			for k in range(m):
				loc = block_info[i][j][k]
				blk = cube[i][j]
				c = block_info[blk[0][0]][blk[0][1]][(k-blk[1]+m)%m][0]
				w.itemconfig(bfpoly[loc[0]][loc[1]],fill=colors[c]) # fill = color[c]

state = deepcopy(solved)
def gui_turn(no):
	global state
	state = turn(state, no)
	update(state)

def gui_reset():
	global state, solved
	state = deepcopy(solved)
	update(state)

def gui_mix(n=50):
	state = mix(n)
	update(state)

def btn1(e):
	global center_coord
	for i in range(12):
		if (e.x-center_coord[i][0])**2+(e.y-center_coord[i][1])**2<=2304: # 48**2
			gui_turn(i+1)
			return

def btn2(e):
	global center_coord
	for i in range(12):
		if (e.x-center_coord[i][0])**2+(e.y-center_coord[i][1])**2<=2304: # 48**2
			gui_turn(-i-1)
			return

w.bind("<Button-1>",btn1)
w.bind("<Button-2>",btn2)
# tk.mainloop()

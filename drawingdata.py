from copy import deepcopy
delta = (4, 3, 4, 0, 1, 2, 4, 0, 1, 2, 3, 2)
from numpy import *
radius = 120
ratio = 0.4
R = 2*radius*cos(pi/5)
r = radius*ratio
x = int((5*R+2*radius)*sin(3*pi/5)+20)
y = int((R+radius)*cos(pi/5)+R+radius+20)
p = tan(pi * 3 / 10) / tan(pi * 2 / 5)
edge_ratio = ((1-p)+ratio*(1+p))/2
centerX=(R+radius)*sin(3*pi/5)+10
centerY=R+radius+10
out_coord = [[None for j in range(15)] for i in range(12)]
in_coord = [[None for j in range(5)] for i in range(12)]
center_coord = [None for i in range(12)]

for j in range(5):
    out_coord[0][3*(j+delta[0])%15] = int(centerX-radius*sin(2*j*pi/5)),int(centerY+radius*cos(2*j*pi/5))
    in_coord[0][(j+delta[0])%5] = int(centerX - r *sin(2*j*pi/5)),int(centerY+r*cos(2*j*pi/5))
center_coord[0] = int(centerX),int(centerY)

for i in range(5):
    for j in range(5):
        out_coord[5-i][3 * (5 - j + delta[5 - i]) % 15] = int(centerX-R*sin(2*i*pi/5)-radius*sin(2*(i+j)*pi/5)), int(centerY-R*cos(2*i*pi/5)-radius*cos(2*(i+j)*pi/5))
        in_coord[5-i][(5 - j + delta[5 - i]) % 5] = int(centerX-R*sin(2*i*pi/5)-r*sin(2*(i+j)*pi/5)), int(centerY-R*cos(2*i*pi/5)-r*cos(2*(i+j)*pi/5))
    center_coord[5-i]= int(centerX-R*sin(2*i*pi/5)),int(centerY-R*cos(2*i*pi/5))

centerX += 3*R*sin(3*pi/5)
centerY += -R*cos(2*pi/5)

for j in range(5):
    out_coord[11][3*(5-j+delta[11])%15] = int(centerX-radius*sin(2*j*pi/5)),int(centerY-radius*cos(2*j*pi/5))
    in_coord[11][(5-j+delta[11])%5] = int(centerX - r *sin(2*j*pi/5)),int(centerY-r*cos(2*j*pi/5))
center_coord[11] = int(centerX),int(centerY)

for i in range(5):
    for j in range(5):
        out_coord[6+i][3 * (j + delta[6 + i]) % 15] = int(centerX-R*sin(2*i*pi/5)-radius*sin(2*(i+j)*pi/5)), int(centerY+R*cos(2*i*pi/5)+radius*cos(2*(i+j)*pi/5))
        in_coord[6+i][(j + delta[6 + i]) % 5] = int(centerX-R*sin(2*i*pi/5)-r*sin(2*(i+j)*pi/5)), int(centerY+R*cos(2*i*pi/5)+r*cos(2*(i+j)*pi/5))
    center_coord[6+i]= int(centerX-R*sin(2*i*pi/5)),int(centerY+R*cos(2*i*pi/5))

for i in range(12):
    for j in range(5):
        out_coord[i][3*j+1] = tuple( int(edge_ratio*out_coord[i][3*j][k]+(1-edge_ratio)*out_coord[i][3*(j+1)%15][k]) for k in range(2))
        out_coord[i][3*j+2] = tuple( int((1-edge_ratio)*out_coord[i][3*j][k]+edge_ratio*out_coord[i][3*(j+1)%15][k]) for k in range(2))

frames = [[] for i in range(12)]
centers = deepcopy(in_coord)
blocks = [[[] for j in range(10)] for i in range(12)]

for i in range(12):
    for j in range(5):
        frames[i].append(out_coord[i][3*j])
        for k in (-2,-1): blocks[i][2*j].append(out_coord[i][3*j+k])
        for k in (0,-1): blocks[i][2*j].append(in_coord[i][j+k])
        for k in (-1,0,1): blocks[i][2*j+1].append(out_coord[i][(3*j+k+15)%15])
        blocks[i][2*j+1].append(in_coord[i][j])


coords = (frames,centers,blocks,center_coord)
print("Complete. resolution:",x,y)
import json
with open('coords.txt','w') as file:
    json.dump(coords,file)

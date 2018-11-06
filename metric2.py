from cube2 import *
import numpy as np
Edges = []
Corners = []
for i in [0, 1, 2, 3, 4]:
    for j in range(item_num[i]):
        if i % 2 or j % 2:
            Edges.append((i,j))
        else:
            Corners.append((i,j))
dist_edge = np.array([10]*(30*30*2), dtype='i8').reshape((30,30,2))
dist_corner = np.array([10]*(20*20*3), dtype='i8').reshape((20,20,3))

for i in range(30):
    cur_step = [(Edges[i],0)]
    next_step = []
    for rotations in range(10):
        for block in cur_step:
            k = Edges.index(block[0])
            if dist_edge[i][k][block[1]] > rotations:
                dist_edge[i][k][block[1]] = rotations
            if dist_edge[k][i][block[1]] > rotations: # 양방향 위상 변화 같음
                dist_edge[k][i][block[1]] = rotations
            for j in range(12):
                next = permute_block(block, perms[j], True)
                if next is not None:
                    next_step.append(next)
                next = permute_block(block, perms[j], True, True)
                if next is not None:
                    next_step.append(next)
        next_step = list(set(next_step + cur_step))
        cur_step = list(next_step)

# 0, 1 대칭행렬

for i in range(20):
    cur_step = [(Corners[i],0)]
    next_step = []
    for rotations in range(10):
        for block in cur_step:
            k = Corners.index(block[0])
            if dist_corner[i][k][block[1]] > rotations:
                dist_corner[i][k][block[1]] = rotations
            if dist_corner[k][i][(3-block[1])%3] > rotations:
                dist_corner[k][i][(3 - block[1]) % 3] = rotations
            for j in range(12):
                next = permute_block(block, perms[j], True)
                if next is not None:
                    next_step.append(next)
                next = permute_block(block, perms[j], True, True)
                if next is not None:
                    next_step.append(next)
        next_step = list(set(next_step + cur_step))
        cur_step = list(next_step)
        next_step = []

# 0 대칭행렬, 1의 전치행렬 = 2

np.save('dist_e_2.npy',dist_edge)
np.save('dist_c_2.npy',dist_corner)
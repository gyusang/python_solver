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
dist_edge = np.array([10]*(30*30), dtype='i8').reshape((30,30))
dist_corner = np.array([10]*(20*20), dtype='i8').reshape((20,20))

for i in range(30):
    cur_step = [Edges[i]]
    next_step = []
    for rotations in range(10):
        for block in cur_step:
            k = Edges.index(block)
            if dist_edge[i][k] > rotations or dist_edge[k][i] > rotations:
                dist_edge[i][k] = dist_edge[k][i] = rotations
            for j in range(12):
                next = permute_block(block, perms[j], False)
                if not (next is None):
                    next_step.append(next)
                next = permute_block(block, perms[j], False, True)
                if not (next is None):
                    next_step.append(next)
        next_step = list(set(next_step + cur_step))
        cur_step = list(next_step)
dist_edge = np.matrix(dist_edge)
print(dist_edge)

for i in range(20):
    cur_step = [Corners[i]]
    next_step = []
    for rotations in range(10):
        for block in cur_step:
            k = Corners.index(block)
            if dist_corner[i][k] > rotations or dist_corner[k][i] > rotations:
                dist_corner[i][k] = dist_corner[k][i] = rotations
            for j in range(12):
                next = permute_block(block, perms[j], False)
                if next is not None:
                    next_step.append(next)
                next = permute_block(block, perms[j], False, True)
                if next is not None:
                    next_step.append(next)
        next_step = list(set(next_step + cur_step))
        cur_step = list(next_step)
        next_step = []
dist_corner = np.matrix(dist_corner)
print(dist_corner)


np.save('dist_e.npy',dist_edge)
np.save('dist_c.npy',dist_corner)
np.save('Edges.npy', Edges)
np.save('Corners.npy',Corners)
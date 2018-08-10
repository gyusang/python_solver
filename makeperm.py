def makeperm(cycles, reversed=False):
	id = [[(i,j) for j in range(10)] for i in range(12)]
	for cycle in cycles:
		for i in range(len(cycle)):
			if reversed:
				id[cycle[i-1][0]][cycle[i-1][1]] = cycle[i]
			else:
				id[cycle[i][0]][cycle[i][1]] = cycle[i-1]
	return id

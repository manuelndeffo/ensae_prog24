from grid import Grid
from graph import Graph
from solver import Solver

import time
import matplotlib.pyplot as plt
import random
import copy



# create and print a grid of 2 lines and 3 columns
g = Grid(2, 3)
print(g)

# create  and print a grid from a file
data_path = "../input/"
file_name = data_path + "grid0.in"

print(file_name)

g = Grid.grid_from_file(file_name)
print(g)

# Plot the grid g

g.plot_grid()

# The solution of [[3,5,6],[4,1,2]] with the Naive method

print('****************')

N = Solver(2, 3, [[3, 5, 6], [4, 1, 2]])
print(N)
N_sol = N.get_solution()
print('To solve N we need to apply this different swaps:', N_sol)
print('The numbers of swap to solve with the Naive solution are:', len(N_sol))

print('***************')


# Create the graph for [[3, 5, 6], [4, 1, 2]]

print('*************')

graph_N = N.graph_construct()
bfs_N = graph_N.bfs((3, 5, 6, 4, 1, 2), (1, 2, 3, 4, 5, 6))
print(bfs_N)
print('Numbers of swap needed to solve the bfs algorithm are:', len(bfs_N)-1)

print('*****************')

# Bfs with Graph
print('*****************')

new_bfs_N = N.new_bfs_solution((3, 5, 6, 4, 1, 2), (1, 2, 3, 4, 5, 6))
print('The number of solution with the new bfs algorithm', len(new_bfs_N)-1)

print('*****************')

# The solution of N using the BFS algorithm is 

print('*****************')
N = Solver(2, 3, [[3, 5, 6], [4, 1, 2]])
B_sol = N.bfs_solution()
print('To solve N we need to apply this different swaps:', B_sol)
print('The numbers of swap to solve with the Bfs solution are:', len(B_sol))


print('*****************')

print('******A_euclidian*********')

N = Solver(3, 3, [[1, 2, 4], [3, 6, 5], [7, 8, 9]])
print(N)
N_sol = N.A_Star(N.square_ecludian)
print('To solve N we need to apply this different swaps:', N_sol)
print('The lenght', len(N_sol))
print('***************')

print('*******A_STAR*********')

N = Solver(3, 2, [[1, 3], [5,4], [6,2]])
print(N)
N_sol = N.A_Star(N.square_ecludian)
L=N.extract_solution(N_sol)
print('L', L)

print('To solve N we need to apply this different swaps:', N_sol)
print('The lenght', len(N_sol))

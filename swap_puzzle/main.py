from grid import Grid
from graph import Graph
from solver import Solver

import time
import matplotlib.pyplot as plt
import random
import copy

"""
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

# with the new bfs
print('*****************')

new_bfs_N = graph_N.new_bfs((3, 5, 6, 4, 1, 2), (1, 2, 3, 4, 5, 6))
print('The number of solution with the new bfs algorithm', len(new_bfs_N)-1)

print('*****************')

# The solution of N using the BFS algorithm is 

print('*****************')
N = Solver(2, 3, [[3, 5, 6], [4, 1, 2]])
B_sol = N.bfs_solution()
print('To solve N we need to apply this different swaps:', B_sol)
print('The numbers of swap to solve with the Bfs solution are:', len(B_sol))

print('*****************')

"""
"""
print('*******A_STAR*********')

N = Solver(3, 3, [[1, 2, 4], [3, 6, 5], [7, 8, 9]])
print(N)
N_sol = N.A_Star(N.square_ecludian)
print('To solve N we need to apply this different swaps:', N_sol)
print('The lenght', len(N_sol))
print('***************')
"""
"""
print('*******A_STLAR*********')

N = Solver(3, 2, [[1, 3], [5,4], [6,2]])
print(N)
N_sol = N.bfs_solution()
L=N.extract_solution(N_sol)
print('L', L)
print('To solve N we need to apply this different swaps:', N_sol)
print('The lenght', len(N_sol))
print('***************')
"""
"""
N = Solver(3, 2, [[1, 3], [5,4], [6,2]])
print(N)
N_sol = N.A_Star(N.square_ecludian)
L=N.extract_solution(N_sol)
print('L', L)

print('To solve N we need to apply this different swaps:', N_sol)
print('The lenght', len(N_sol))"""


def generate_random_grid(min_rows, max_rows, min_cols, max_cols):
    num_rows = random.randint(min_rows, max_rows)
    num_cols = random.randint(min_cols, max_cols)
    elements = [i for i in range(1, num_rows * num_cols+1)]
    random.shuffle(elements)  # Shuffle the elements randomly
    grid = [elements[i:i+num_cols] for i in range(0, len(elements), num_cols)]
    return grid

def generate_grids(num_grids):
    grids = []
    for i in range(num_grids):
        grid = generate_random_grid(1,3,1,3)
        grids.append(grid)
    return grids

"""
# Measure execution time for A_star function on each grid
def measure_execution_time_A_star_e(grids):
    execution_times = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),gri
        start_time = time.time()
        N.A_Star(N.square_ecludian)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times

def measure_execution_time_A_star_m(grids):
    execution_times = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),grid)
        # Assuming self and h are already defined somewhere in your code
        start_time = time.time()
        N.A_Star(N.manhattan)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times

def measure_execution_time_A_star_mrc(grids):
    execution_times = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),grid)
        # Assuming self and h are already defined somewhere in your code
        start_time = time.time()
        N.A_Star(N.misplaced_rows_cols)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times

def measure_execution_time_A_star_mt(grids):
    execution_times = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),grid)
        start_time = time.time()
        N.A_Star(N.misplaced_tiles)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    return execution_times

# Generate grids
num_grids = 5
grids = generate_grids(num_grids)

# Measure execution time for A_star function
execution_times_e = measure_execution_time_A_star_e(grids)
execution_times_m = measure_execution_time_A_star_m(grids)
execution_times_mrc = measure_execution_time_A_star_mrc(grids)
execution_times_mt = measure_execution_time_A_star_mt(grids)


# Plotting
plt.figure(figsize=(10, 6))

plt.plot(range(1, num_grids + 1), execution_times_e, marker='o', label='Euclidian',color='b')
plt.plot(range(1, num_grids + 1), execution_times_m, marker='o', label='Manhattan',color='r')
plt.plot(range(1, num_grids + 1), execution_times_mrc, marker='o', label='Misplaced rows_cols',color='green')
plt.plot(range(1, num_grids + 1), execution_times_mt, marker='o', label='Hamming',color='pink')

plt.title('Execution Time of A_star on Heuristic')
plt.xlabel('Grid Number')
plt.ylabel('Execution Time (s)')
plt.xticks(range(1, num_grids + 1))
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
"""
def flatten_grid(matrix):

    """
    Convert a matrix or a list of list into a list.
    
    Parameters: 
    -----------
    matrix: list of list
        the list of list you want to flatten

    Output: 
    -------
    flat_list: list
        The corresponding list
    """

    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list

def count_alg_Naive(grids):
    counts = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),grid)
        L=N.get_solution()
        counts.append(len(L))
    return counts

def count_alg_Nbfs(grids):
    counts = []
    for grid in grids:
        sort_g = []
        g_t = []
        for i in range(0, len(grid)):
            for j in range(0, len(grid[0])):
                sort_g.append(grid[i][j])
                g_t.append(grid[i][j])
        print(g_t)
        N= Solver(len(grid), len(grid[0]), grid)
        L = N.new_bfs_solution(tuple(g_t), tuple(sort_g))
        print(L)
        if L is None:
            L=0
        else:
            counts.append(len(L) - 1)
    return counts
    
def count_A_star_mrc(grids):
    counts = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),grid)
        L=N.A_Star(N.misplaced_rows_cols)
        counts.append(len(L)-1)
    return counts

def count_A_star_m(grids):
    counts = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),grid)
        L=N.A_Star(N.manhattan)
        counts.append(len(L)-1)
    return counts

def count_A_star_mt(grids):
    counts = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),grid)
        L=N.A_Star(N.misplaced_tiles)
        counts.append(len(L)-1)
    return counts

def count_A_star_e(grids):
    counts = []
    for grid in grids:
        N=Solver(len(grid),len(grid[0]),grid)
        L=N.A_Star(N.square_ecludian)
        counts.append(len(L)-1)
    return counts

# Generate grids
num_grids = 5
grids = generate_grids(num_grids)
print(grids)

# Measure execution time for A_star function
count_bfs = count_alg_Nbfs(grids)
print(count_bfs)
count_e = count_A_star_e(grids)
print(count_e)
count_naive = count_alg_Naive(grids)
print(count_naive)

plt.figure(figsize=(10, 6))

plt.plot(range(1, num_grids + 1), count_e, marker='o', label='Euclidian', color='cyan')
plt.plot(range(1, num_grids + 1), count_bfs, marker='o', label='New Bfs', color='green')
plt.plot(range(1, num_grids + 1), count_naive, marker='o', label='Naive', color='purple')

plt.title('Number of solving swaps')
plt.xlabel('Grid Number')
plt.ylabel('Number of Swaps ( Random chosen grid)')
plt.xticks(range(1, num_grids + 1))
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
from grid import Grid
from collections import defaultdict
from collections import deque
import copy
import heapq
import math

class Solver(Grid):
    """
    A solver class, to be implemented.
    """
    def __init__(self, m, n, initial_state=[]):
        super().__init__(m, n, initial_state)
        self.final = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]
  
    def position(self, elt):
        for i, row in enumerate(self.state):
            for j, value in enumerate(row):
                if value == elt:
                    return (i, j)

    def position_order(self, elt):
        for i, row in enumerate(self.final):
            for j, value in enumerate(row):
                if value == elt:
                    return (i, j)
    
    def check_column(self, elt):
        return (self.position(elt)[1] == self.position_order(elt)[1])

    def check_row(self, elt):
        return (self.position(elt)[0] == self.position_order(elt)[0])
    
    def correct_position(self, elt):
        return (self.position(elt) == self.position_order(elt))

    def get_solution(self):
        """
        Solves the grid 

        Returns : 
        the sequence of swaps at the format [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        sol = []
        for i in range(self.n*self.m):
            if self.correct_position(i):
                continue
            else:
                if not self.check_column(i):
                    if self.position(i)[1] < self.position_order(i)[1]:
                        while not self.check_column(i):
                            cell = self.position(i)
                            self.swap(cell, (cell[0], cell[1]+1))
                            sol.append((cell, (cell[0], cell[1]+1)))
                    else:
                        while not self.check_column(i):
                            cell = self.position(i)
                            self.swap(cell, (cell[0], cell[1]-1))
                            sol.append((cell, (cell[0], cell[1]-1)))

                if self.position(i)[0] < self.position_order(i)[0]:
                    while not self.check_row(i):
                        cell = self.position(i)
                        self.swap(cell, (cell[0]+1, cell[1]))
                        sol.append((cell, (cell[0]+1, cell[1])))
                else:
                    while not self.check_row(i):
                        cell = self.position(i)
                        self.swap(cell, (cell[0]-1, cell[1]))
                        sol.append((cell, (cell[0]-1, cell[1])))
        return sol

    def bfs_solution(self):
        """" Returns the solution of the grid using the BFS algorithm
             For example the solution of [[1,2],[4,3]] would be [(3,4)]
        """
        g = self.graph_construct()
        tuple_sol = g.bfs(tuple(flatten_grid(self.state)), tuple(flatten_grid(self.final)))
        sol = []
        for i in range(1, len(tuple_sol)):
            for j in range(self.n*self.m):
                if (tuple_sol[i][j] != tuple_sol[i-1][j]):
                    sol.append((tuple_sol[i][j], tuple_sol[i-1][j]))
                    break
        return sol

    def new_bfs_solution2(self,src,dst):

        """
        A new implementation of BFS specific for the swap puzzle
        Finds a shortest path from src to dst by BFS.  

        Parameters: 
        -----------
        src: NodeType
            The source node.
        dst: NodeType
            The destination node.

        Output: 
        -------
        path: list[NodeType] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """ 
        parent = {src: None}
        visited = set()
        visited.append(src)
        queue = deque()
        queue.append(src)

        while len(queue) > 0:
            v = queue.popleft()
            for i in all_one_swaps(self.tuple_to_grid(v)):
                if tuple(flatten_grid(i)) not in visited:
                    queue.append(tuple(flatten_grid(i)))
                    visited.append(tuple(flatten_grid(i)))
                    parent[tuple(flatten_grid(i))] = v
            if v == dst:
                break

        if (dst not in parent.values()) and parent.get(dst) is None:
            path = None
        else:
            path = []
            end_node = dst
            while end_node is not None:
                path.insert(0, end_node)
                end_node = parent[end_node] 

        return path

    def misplaced_tiles(self, tuple_grid):

        count = 0
        count = sum(1 for x, y in zip(self.final, tuple_grid) if x != y)/2
        return count

    def misplaced_rows_cols(self, tup):

        mat = self.tuple_to_grid(tup)
        count = 0
        for i in range(self.m):
            for j  in range(self.n):
                if self.check_column(mat[i][j]) == False:
                    count += 1
                if self.check_row(mat[i][j]) == False :
                    count += 1

        return count/2

    def manhattan(self, tup):
        
        mat = self.tuple_to_grid(tup)
        d = 0
        pos = ()
        
        for i in range(self.m):
            for j in range(self.n):
                pos = self.position_order(mat[i][j])
                d = d + abs(i-pos[0])+abs(j-pos[1])

        return d/2
    
    def square_ecludian(self, tup):

        mat = self.tuple_to_grid(tup)
        d = 0
        pos = ()
        
        for i in range(self.m):
            for j in range(self.n):
                pos = self.position_order(mat[i][j])
                d = d + (i-pos[0])**2 + (j-pos[1])**2

        return d/2

    def A_Star(self, h):

        start = tuple(flatten_grid(self.state))
        goal = tuple(flatten_grid(self.final))

        openSet = [start]
        heapq.heapify(openSet)

        cameFrom = {}

        gScore = defaultdict(lambda: math.inf)
        gScore[start] = 0

        fScore = defaultdict(lambda: math.inf)
        fScore[start] = h(start)

        while len(openSet) > 0:
          
            current = min(openSet, key=lambda node: fScore[node])
            
            if current == goal:
                return reconstruct_path(cameFrom, current)

            openSet.remove(current)
            
            for neighbor in all_one_swaps_tuple(self.tuple_to_grid(current)):
                
                tentative_gScore = gScore[current] + 1
                
                if tentative_gScore < gScore[neighbor]:
                
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + h(neighbor)
                    
                    if neighbor not in openSet:
                        
                        heapq.heappush(openSet, neighbor)
    
    

def flatten_grid(matrix):

    """
    Convert a matrix or a list of list into a grid.
    
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


def swappable(matrix, cell1, cell2):
    
    m = len(matrix)
    n = len(matrix[0])
    
    if 0 <= cell1[0] <= m-1  and 0 <= cell2[0] <= m-1 :
        if 0 <= cell1[1] <= n-1  and 0 <= cell2[1] <= n-1:
            if (cell1[0] == cell2[0] and abs(cell1[1]-cell2[1]) == 1) or (cell1[1] == cell2[1] and abs(cell1[0]-cell2[0]) == 1):
                return True
    else:
        return False


def all_one_swaps(matrix):
    
    track = set()
    all_perm = []
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            for k in [1, -1]:
                if swappable(matrix, (i, j), (i+k, j)):
                    if ((i, j), (i+k, j)) not in track and ((i+k, j), (i, j)) not in track:
                        track.add(((i, j), (i+k, j)))
                        temp = copy.deepcopy(matrix)
                        temp[i+k][j], temp[i][j] = temp[i][j], temp[i+k][j]
                        all_perm.append(temp)
                        
                if swappable(matrix, (i, j), (i, j+k)):
                    if ((i, j), (i, j+k)) not in track and ((i, j+k),(i, j))not in track:
                        track.add(((i, j), (i, j+k)))
                        temp = copy.deepcopy(matrix)
                        temp[i][j+k], temp[i][j] = temp[i][j], temp[i][j+k]
                        all_perm.append(temp)
                        
    return all_perm
    
def all_one_swaps_tuple(matrix):
    
    track = set()
    all_perm = []
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            for k in [1, -1]:
                if swappable(matrix, (i, j), (i+k, j)):
                    if ((i, j), (i+k, j)) not in track and ((i+k, j), (i, j)) not in track:
                        track.add(((i, j), (i+k, j)))
                        temp = copy.deepcopy(matrix)
                        temp[i+k][j], temp[i][j] = temp[i][j], temp[i+k][j]
                        all_perm.append(tuple(flatten_grid(temp)))
                        
                if swappable(matrix, (i, j), (i, j+k)):
                    if ((i, j), (i, j+k)) not in track and ((i, j+k),(i, j))not in track:
                        track.add(((i, j), (i, j+k)))
                        temp = copy.deepcopy(matrix)
                        temp[i][j+k], temp[i][j] = temp[i][j], temp[i][j+k]
                        all_perm.append(tuple(flatten_grid(temp)))
                        
    return all_perm


def reconstruct_path(cameFrom, current):

    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)     
    return total_path





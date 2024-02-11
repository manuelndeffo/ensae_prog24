from grid import Grid
from graph import Graph


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
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
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
        g = self.graph_construct()
        tuple_sol=g.bfs(tuple(flatten_grid(self.state)),tuple(flatten_grid(self.final)))
        sol=[]
        for i in range(1,len(tuple_sol)):
            a_n=i-1
            print('tes',self.n)
            for j in range(0,self.n):
                if (tuple_sol[i][j] != tuple_sol[a_n][j]):
                    sol.append((tuple_sol[i][j], tuple_sol[i-1][j]))
                    break
        return sol

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




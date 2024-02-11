import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations
from graph import Graph

"""
This is the grid module. It contains the Grid class and its associated methods.
"""
class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    def __str__(self): 
        
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        """
        Checks is the current state of the grid is sorted and returns the answer as a boolean.
        """
        return (self.state==[list(range(i*self.n+1, (i+1)*self.n+1)) for i in range(self.m)])
    
    
    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        
        if (cell1[0]==cell2[0] and abs(cell1[1]-cell2[1])==1) or (cell1[1]==cell2[1] and abs(cell1[0]-cell2[0])==1):
            self.state[cell1[0]][cell1[1]],self.state[cell2[0]][cell2[1]]=self.state[cell2[0]][cell2[1]],self.state[cell1[0]][cell1[1]]
        else:
            raise Exception('This swap is not allowed')
            
                
    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        for cell_pair in cell_pair_list:
            self.swap(cell_pair[0],cell_pair[1])
            

    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid
    
    def plot_grid(self,color=''):
        fig, ax = plt.subplots(figsize=(self.m, self.n))
        ax.set_xlim(0,self.n)
        ax.set_ylim(self.m, 0)
        ax.grid(True)
        ax.set_xticks(np.arange(0,self.n, 1.0))
        ax.set_yticks(np.arange(0, self.m, 1.0))

        # Add text inside each grid
        counter=1
        for j in range(self.m):
            for i in range(self.n):
                ax.text(i+0.5,j+0.5, f'{self.state[j][i]}',ha='center',va='center',color='black')
                counter+=1

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Display the colored grid using imshow
        color_intensity=0
        data=np.zeros((self.m+1,self.n+1))
        if not color:
            color='summer'
        ax.imshow(data,cmap=color)


    # get all the permutations of the flatten grid  

    def flatten_grid_permutations(self):
        return list(permutations(flatten_grid(self.state)))

    #convert a list to a grid(matrix)
    def tuple_to_grid(self,T):
        matrix = np.array(T).reshape(self.m,self.n)
        return matrix.tolist()

    # graph construction

    def graph_construct(self):

        all_state_tuple=self.flatten_grid_permutations()
        g=Graph(all_state_tuple)
        all_edges=[]
        for elt1 in self.flatten_grid_permutations():
            for elt2 in self.flatten_grid_permutations():
                if one_swap(self.tuple_to_grid(elt1),self.tuple_to_grid(elt2))==True:
                    if (elt1,elt2) and (elt2,elt1) not in all_edges:
                        all_edges.append((elt1,elt2))
                        
        for ed in all_edges:
            g.add_edge(ed[0],ed[1])
        return g

# convert the grid(Matrix) into a list

def flatten_grid(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list


# get the index of an element in a grid

def get_index(gd, value):
    for i, element in enumerate(gd):
        if value in element:
            return (i, element.index(value))
    return None

# check if there is only one swap between two grid
# count the number of swaps
# all the elements of the grid should be at the same position except two elements]
# check if there was a swap between the two elements that are not at the same position

def one_swap(gr1, gr2):
    S = 0
    for i, j in zip(flatten_grid(gr1),flatten_grid(gr2)):
        if i != j:
            cell1 = get_index(gr1, i)
            cell2 = get_index(gr1, j)
            S += 1

    if S == 2:
        if (cell1[0] == cell2[0] and abs(cell1[1]-cell2[1]) == 1) or \
           (cell1[1] == cell2[1] and abs(cell1[0]-cell2[0]) == 1):
            return True
        else:
            return False
    else:
        return False


g=Grid(2, 3, [[1,2,3],[4,5,6]])
D=g.graph_construct()
s=D.new_bfs((3,5,6,4,1,2),(1,2,3,4,5,6))
print(len(s))
g.plot_grid()
from grid import Grid
from graph import Graph
from solver import Solver
import numpy as np
import random
import sys
import pygame

class Taquin ():
    def __init__(self, puzzle, wall_list, blocs_list):
        """
       Convert a puzzle into a Taquin object.

       Parameters:
       -----------
       puzzle: np.ndarray
           The initial puzzle.
       wall_list: List[Tuple[Tuple[int, int], Tuple[int, int]]]
           The list of walls in the puzzle.
       blocs_list: List[int]
           The list of blocks in the puzzle.
       """
        self.n = np.shape(puzzle)[0]
        self.m = np.shape(puzzle)[1]
        self.plateau = puzzle
        self.actions = 0
        self.walls = wall_list
        self.blocs = blocs_list

    
    def pos(self, p):
        """
        Give the coordonates of a given int form the matrix in the matrix
        Parameters:
        -----------
        p : int 
        the number we search the coordonates
        
        Output:
        -------
        str
            La représentation sous forme de chaîne de caractères de l'objet Taquin.
        """
        for y in range(self.n):
            for x in range(self.m):
                if self.plateau[y][x] == p:
                    return y,x
        return None

        
    def swap_cells(self, cell1, cell2):
        """
        Swap the values between two cells in the puzzle and increment the number of actions.

        Parameters:
        -----------
        cell1: Tuple[int, int]
            Coordinates of the first cell.
        cell2: Tuple[int, int]
            Coordinates of the second cell.
        """
        self.plateau[cell1[0]][cell1[1]],self.plateau[cell2[0]][cell2[1]]=self.plateau[cell2[0]][cell2[1]],self.plateau[cell1[0]][cell1[1]]
        self.actions += 1
    
    
           
    def get_input_cells(self):
        """
        Prompt the user to enter the numbers of two cells and return their positions.

        Output:
        -------
        Tuple[Tuple[int, int], Tuple[int, int]]
            The positions of the two cells.
        """

        
        cell1_num = int(input("Entrez le numéro de la première cellule : "))
        cell2_num = int(input("Entrez le numéro de la deuxième cellule : "))
        return self.pos(cell1_num), self.pos(cell2_num)
    

                
    def graphicplate(self, screen, win=False):
        """
        Draw the game board on the specified pygame surface, indicating whether the player has won (win=True).

        Parameters:
        -----------
        screen: pygame.Surface
            The surface on which to draw the board.
        win: bool, optional
            Indicates whether the player has won, by default False.
        """
        font = pygame.font.Font(None, 60)
        grey = (112, 114, 110)
        if win:
            color = (10, 128, 10)
        else:
            color = (40, 58, 82)
    
        for y in range(self.n):
            for x in range(self.m):
                if self.plateau[y][x] != 0:
                    rect_x = 16 + x * 184
                    rect_y = 60 + y * 184
                    if self.plateau[y][x] in self.blocs :
                        pygame.draw.rect(screen, (88,41,0), pygame.Rect(rect_x, rect_y, 172, 172), border_radius=20)
                    else :
                        pygame.draw.rect(screen, color, pygame.Rect(rect_x, rect_y, 172, 172), border_radius=20)
    
                    if self.plateau[y][x] < 10:
                        dx = 0
                    else:
                        dx = -16
                    text_x = rect_x + 72 + dx
                    text_y = rect_y + 86
                    screen.blit(font.render(str(self.plateau[y][x]), 1, (255, 255, 255)), (text_x, text_y))
    
        for wall in self.walls:
            if wall[0][0] == wall[1][0]:
                x = max(wall[0][1], wall[1][1])
                y = wall[0][0]
                rect_x = 7 + (x) * 184
                rect_y = 60 + (y) * 184
                pygame.draw.rect(screen, grey, pygame.Rect(rect_x, rect_y, 6, 172), border_radius=20)
    
            if wall[0][1] == wall[1][1]:
                x = wall[1][1]
                y = max(wall[1][0], wall[0][0])
                rect_x = 16 + (y) * 184
                rect_y = 51 + (x) * 184
                pygame.draw.rect(screen, grey, pygame.Rect(rect_x, rect_y, 172, 6), border_radius=20)
    
        actions_text = font.render("Actions: {}".format(self.actions), 1, (255, 255, 255))
        screen.blit(actions_text, (15, 12))
       
        
            
                
    def play(self):
        """
        Initialize and manage the pygame game using the Taquin class.
        """
        pygame.quit()   
        pygame.init()
        
        w = int(200 * (self.m))
        l = int(30 + self.n * 200)
        screen = pygame.display.set_mode((w, l))  
        green = (9, 44, 28)
        marroon = (33, 21, 3)
        marroon_light = (47, 32, 8)
        running = True
        
        selected_cell = None  # Variable to store the selected cell
        
        while running:
            screen.fill(green)
            
            pygame.draw.rect(screen, marroon, pygame.Rect( 5, 5, w-10, l-10))  
    
            if (self.plateau == np.array(np.arange(1, self.n * self.m + 1).reshape(self.n, self.m))).all():
                self.graphicplate(screen, win=True)
            else:
                self.graphicplate(screen)
                
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
    
                    if event.key == pygame.K_l:
                        solt = Solver(self.n, self.m, self.initial_grid)
                        hint = solt.extract_solution(A_Star(solt.square_ecludian))
                        print(len(hint))
                        for step in hint:
                            self.swap_cells(step[1], step[0])
    
                
                    if event.key == pygame.K_s:
                        cell1, cell2 = self.get_input_cells()
                        if abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1]) == 1:
                            if (cell1, cell2) not in self.walls and (cell2, cell1) not in self.walls :
                                 if self.plateau[cell1[0]][cell1[1]] not in self.blocs and self.plateau[cell2[0]][cell2[1]]  not in self.blocs :
                                     self.swap_cells(cell1, cell2)
    
                # Handling mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                    pos = pygame.mouse.get_pos()
                    x = (pos[0] - 16) // 184
                    y = (pos[1] - 60) // 184
                    if 0 <= x < self.m and 0 <= y < self.n:
                        if selected_cell is None:
                            selected_cell = (y, x)  # Store the first clicked cell
                        else:
                            if (abs(selected_cell[0] - y) + abs(selected_cell[1] - x)) == 1:  # Check if adjacent cell clicked
                                cell1, cell2 = selected_cell, (y, x)
                                if (cell1, cell2) not in self.walls and (cell2, cell1) not in self.walls :
                                    if self.plateau[cell1[0]][cell1[1]] not in self.blocs and self.plateau[cell2[0]][cell2[1]]  not in self.blocs :
                                        self.swap_cells(cell1, cell2)
                                selected_cell = None  # Reset selected cell after swapping
    
            pygame.display.flip()
    
        pygame.quit()


def create_blocs(m,n,k):
    """ Create the block in a grid and return the grid for block and blocks
    
    Parameters:
    -----------
    n: int
        Numbers of line of the Grid.
    m: int
        Numbers of columns of the Grid.
    nb_blocs_fixes: int
        Numbers of fix blocks in to include in the puzzle
    
    Output:
    -------
    Tuple (blocks_grid,blocks)

    blocks_grid is a list of list
    blocks is a list of blocks
    """

    if k> n*m or k<0:
        raise ValueError("Impossible to create this block")
    
    full_list = list(range(1, n*m + 1))
    fixed_positions = random.sample(range(1,n*m+1), k)
    remaining_elements = [x for x in full_list if x not in fixed_positions]
    random.shuffle(remaining_elements)
    
    for i in sorted(fixed_positions):
        full_list[i-1]
        remaining_elements.insert(i-1, full_list[i-1])
    
    blocks_grid=[]
    blocks=[]

    for i in range(0, len(remaining_elements),n):
        sublist = remaining_elements[i:i+n]
        blocks_grid.append(sublist)
    
    blocks= sorted(fixed_positions)
    
    return (blocks_grid,blocks)


def create_walls(n, m, nbr_walls):
    """
    Crée une liste de murs à partir des dimensions du puzzle et du nombre de murs souhaité.

    Parameters:
    -----------
    n: int
        Nombre de lignes dans le puzzle.
    m: int
        Nombre de colonnes dans le puzzle.
    nbr_walls: int
        Nombre de murs à inclure dans le puzzle.

    Output:
    -------
    List[Tuple[Tuple[int, int], Tuple[int, int]]]
        La liste des murs créés.
    """
    if nbr_walls > (n-1)*m + n*(m-1):
        raise ValueError("Le nombre de murs demandé est trop grand pour la taille de la matrice.")

    all_coordinates = [(i, j) for i in range(n) for j in range(m)]

    adjacent_coordinates = []
    for i in range(1,n):
        for j in range(1,m-1):
            adjacent_coordinates.append(((i, j), (i, j+1)))
    for i in range(1,n-1):
        for j in range(m):
            adjacent_coordinates.append(((i, j), (i+1, j)))

    selected_coordinates = np.random.choice(len(adjacent_coordinates), nbr_walls, replace=False)

    walls = [adjacent_coordinates[i] for i in selected_coordinates]

    return walls

def set_difficulty(matrix, difficulty) : 
    """
    Change the difficulty of a given matrix chnging its distance from an orden matrix. 

    Parameters:
    -----------
    Matrix : np.aray
        the matrix we want to change to set the difficulty
    
    difficulty : int
        The level of difficulty

    Output:
    -------
    The new matrix with a changed difficulty. 
    """
    n = np.shape(matrix)[0]
    m = np.shape(matrix)[1]
    N = Solver(n,m, matrix)
    N_sol = N.A_Star(N.square_ecludian)
    if difficulty == 0 : 
        M = N_sol[int(np.floor(len(N_sol)*0.6))]
    elif difficulty == 1 : 
        M = N_sol[int(np.floor(len(N_sol)*0.8))]
    elif difficulty == 2 : 
        M = N_sol(len(N_sol)-1)
    else : 
        raise ValueError ("Ce niveau de niveau de difficulté n'existe pas.")
    return np.array(M).reshape(n,m)


"""
MISE EN PLACE DU JEU : 
----------------------
One can choose the size of the matrix then can choose betwenn 3 modes :
   
    - chose the lvl of difficulty
    - chose the nbr of blocs
    - chose the nbr of walls
    
Chose 0 for the mode you don't pick and select the correct number for the mode you want.
"""

n = int(input("Veuillez choisir le nombre ligne de votre matrice : "))
m = int(input("Veuillez choisir le nombre colonne de votre matrice : "))
nb_blocs = int(input("Veuillez choisir le nombre de blocs que vous souhaitez : "))
nb_walls = int(input("Veuillez choisir le nombre de murs que vous souhaitez : "))
difficulty = int(input("Veuillez choisir la difficulté 0 = Easy, 1 = Medium, 2 = Hard : "))



puzzle , blocs = create_blocs(n,m,nb_blocs)
new_puzzle = set_difficulty(puzzle, difficulty)
walls = create_walls(n, m, nb_walls)


        
if __name__ == "__main__":
    T = Taquin(new_puzzle, walls, blocs)
    T.play()
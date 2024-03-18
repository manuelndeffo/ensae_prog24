# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph
import ast
import re


def get_info(file_name):

    info = list()
    pattern = r'\[.*?]|[\w]+'

    with open(file_name, "r") as file:
        for line in file:
            lst = re.findall(pattern, line)
            if lst:
                i = int(lst[0])
                j = int(lst[1])
                if lst[2] != 'None':
                    dist = int(lst[2])
                else:
                    dist = None

                if dist is not None:
                    short_path = ast.literal_eval(lst[3])
                else:
                    short_path = None
            info.append([i, j, dist, short_path])

    return info


class Test_bfs(unittest.TestCase):
    def test1_bfs(self):
        gr = Graph.graph_from_file("input/graph1.in")
        infos = get_info("input/graph1.path.out")

        for elt in infos:
            short_path_b = gr.bfs(elt[0], elt[1])
            print(short_path_b)
            if short_path_b is not None:
                d_bfs = len(short_path_b)-1
            else:
                d_bfs = None                 
            self.assertEqual([d_bfs, short_path_b], elt[2:])
    
    def test1_bfs(self):
        gr = Graph.graph_from_file("input/graph2.in")
        infos = get_info("input/graph2.path.out")

        for elt in infos:
            short_path_b = gr.bfs(elt[0], elt[1])
            print(short_path_b)
            if short_path_b is not None:
                d_bfs = len(short_path_b)-1
            else:
                d_bfs = None                 
            self.assertEqual([d_bfs, short_path_b], elt[2:])
    
if __name__ == '__main__':
    unittest.main()
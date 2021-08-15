# Course: CS261 - Data Structures
# Author: Alexander Shen
# Assignment: 6
# Description: Replicate the data structure of an undirected graph.

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        # Adds a dictionary entry with an empty list.
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        # If we are connecting the same node, don't do anything.
        if u == v:
            return

        # find the edge list for each value, if they do not exist create a vertex.
        first = self.adj_list.get(u)
        second = self.adj_list.get(v)
        if not first:
            self.add_vertex(u)
            first = self.adj_list.get(u)
        if not second:
            self.add_vertex(v)
            second = self.adj_list.get(v)
        
        # Don't do anything if the nodes are already connected.
        for adj_1 in first:
            if adj_1 == v:
                return
            for adj_2 in second:
                if adj_2 == u:
                    return
                if adj_1 == adj_2 and adj_2 != adj_2:
                    return
        
        # If we pass then test, connect the two vertices together.
        first.append(v)
        second.append(u)


    def remove_edge(self, v: str, u: str) -> None:
        # Get the edges of the two points, if one of them doesn't exist then do nothing.
        first = self.adj_list.get(u)
        second = self.adj_list.get(v)
        if not first:
            return
        if not second:
            return

        # If there is a match, then remove it from the list.
        for adj_1 in first:
            if adj_1 == v:
                first.remove(v)
                second.remove(u)
            for adj_2 in second:
                if adj_2 == u:
                    first.remove(v)
                    second.remove(u)
                if adj_1 == adj_2 and adj_2 != adj_2:
                    first.remove(v)
                    second.remove(u)
        

    def remove_vertex(self, v: str) -> None:
        # Get a list of edges from the vertex you want to remove.
        # If it doesn't exist do nothing, else remove all edges from the vertex and then pop it from the dictionary.
        removal = self.adj_list.get(v)
        if removal is None:
            return
        else:
            for item in removal:
                node = self.adj_list.get(item)
                node.remove(v)
            self.adj_list.pop(v)
        

    def get_vertices(self) -> []:
        # Returns a list of keys
        new_list = list(self.adj_list.keys())
        return new_list

    def get_edges(self) -> []:
        # Using the list of keys, iterate through it to print out a tuple of its edges.
        # If there are no vertices, then do nothing.
        new_list = list(self.adj_list.keys())
        if not new_list:
            return []
        index = 0
        final_list = []

        # Print all tuples needed
        for key in new_list:
            edges = self.adj_list.get(key)
            for edge in edges:
                print = True
                for num in range(index + 1):
                    if edge == new_list[num]:
                        print = False 
                if print:
                    final_list.append((key, edge))
            index += 1
        
        return final_list
        

    def is_valid_path(self, path: []) -> bool:
        # If there is no path list, then return True
        # If there is a single vertex, return True if the vertex exists.
        found = False
        index = 1
        if len(path) == 0:
            return True
        if len(path) == 1:
            single = self.adj_list.get(path[0])
            if not single:
                return False
            else:
                return True  
        else:
            # Iterate through the keys and edges
            # return True if the next element in path exists and the number is not repeating.
            for key in path:
                if key == path[len(path) - 1] and index == len(path):
                    return True
                edges = self.adj_list.get(key)
                if not edges:
                    return False
                else:
                    for edge in edges:
                        if path[index] == edge:
                            found = True
                        
                    if not found:
                        return False

                    found = False
                    index += 1

    def dfs_helper(self, cur, end, already):
        # Only work if the current vertex has not been visited.
        if cur not in already:
            # Append the current vertex to the visit list.
            already.append(cur)

            cur_list = self.adj_list.get(cur)
            cur_list.sort()
            # Get a list of adj vertices and sort them.

            # Recursively call similarily to a stack.
            for vertex in cur_list:
                self.dfs_helper(vertex, end, already)
        


    def dfs(self, v_start, v_end=None) -> []:
        # If the starting vertex doesn't exist return an empty list.
        check = self.adj_list.get(v_start)
        if not check:
            return []

        # Initialize a visit list and call the recursive helper for dfs.
        visit = []
        self.dfs_helper(v_start, v_end, visit)
        
        # If there is an end, then pop all elements until the end is reached.
        if v_end is not None:
            if v_end not in visit:
                return visit
            else:
                for num in range(len(visit) - 1, -1, -1):
                    if visit[num] != v_end:
                        visit.pop()
                    else:
                        return visit

        # else, return the regular list.
        else:
            return visit

    def bfs(self, v_start, v_end=None) -> []:
        # Track the visited nodes, the queue in which the BFS will use and the final array.
        visit = []
        queue = []
        final = []

        # Addes values to the end of the queues.
        queue.append(v_start)
        visit.append(v_start)

        # While there is a value in the queue.
        while queue:

            # Pop the value from the front of the queue and append it to the final list.
            value = queue.pop(0)
            final.append(value)

            # Get a list of sorted edges, and return an empty list if it doesn't exists.
            cur_list = self.adj_list.get(value)
            if not cur_list:
                return []
            cur_list.sort()
            
            # Iterate through the edges and if the vertex is not visited, append it to the visit and queue.
            for edges in cur_list:
                if edges not in visit:
                    visit.append(edges)
                    queue.append(edges)

         # If there is an end, then pop all elements until the end is reached.
        if v_end is not None:
            if v_end not in final:
                return final
            else:
                for num in range(len(final) - 1, -1, -1):
                    if final[num] != v_end:
                        final.pop()
                    else:
                        return final
        
        # else, return the regular list.
        else:
            return final


    def count_connected_components(self):
        # Perform a DFS on all vertices that are unvisited and count how many times a new recursive call from the main function.
        count = 0
        visit = []
        vertices = list(self.adj_list.keys())

        for vertex in vertices:
            if vertex not in visit:
                self.dfs_helper(vertex, None, visit)
                count += 1

        return count
      

    def has_cycle_helper(self, curr, last, already):
        # Append the current vertex to visited.
        already.append(curr)
        curr_list = self.adj_list.get(curr)

        # iterate through all edges in the current vertex, if it is not in the visit list then call the recursive function.
        # Keep track of the previous vertex, if the vertex is in visit and it isn't looped to itself, then return True
        for edges in curr_list:
            if edges not in already:
                if self.has_cycle_helper(edges, curr, already):
                    return True
            
            elif last != edges:
                return True
        return False

    def has_cycle(self):
        # Similar to the DFS, initialize a list of visited and get a list of vertices.
        visit = []
        vertices = list(self.adj_list.keys())

        # Call a recursive function on all vertices unvisited.
        for vertex in vertices:
            if vertex not in visit:
                if self.has_cycle_helper(vertex, None, visit):
                    return True
        return False

       

   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ECABDCBE']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
